#include <stdint.h>
#include "sqlite3ext.h"
SQLITE_EXTENSION_INIT1

typedef struct {
    uint32_t codepoint;
    uint32_t offset;
    uint8_t length;
} Mapping;

typedef struct {
    uint32_t codepoint;
    uint8_t combining;
    uint8_t nonspacing;
} Property;

#include "rmnocase_unicode.h"

#define ARRAY_LENGTH(array) (sizeof(array) / sizeof((array)[0]))

typedef struct {
    const unsigned char *text;
    int length;
    int position;
    uint32_t offset;
    uint8_t count;
    uint8_t index;
    uint8_t invalid;
} Cursor;

typedef struct {
    Cursor cursor;
    Cursor start;
    Cursor end;
    Cursor scan;
    int in_segment;
    unsigned int combining;
} KeyIterator;

static const Mapping *find_mapping(uint32_t codepoint)
{
    size_t left = 0, right = ARRAY_LENGTH(mappings);
    while (left < right) {
        size_t mid = left + (right - left) / 2;
        if (mappings[mid].codepoint < codepoint)
            left = mid + 1;
        else
            right = mid;
    }
    return left < ARRAY_LENGTH(mappings) && mappings[left].codepoint == codepoint
        ? &mappings[left] : 0;
}

static const Property *find_property(uint32_t codepoint)
{
    size_t left = 0, right = ARRAY_LENGTH(properties);
    while (left < right) {
        size_t mid = left + (right - left) / 2;
        if (properties[mid].codepoint < codepoint)
            left = mid + 1;
        else
            right = mid;
    }
    return left < ARRAY_LENGTH(properties) && properties[left].codepoint == codepoint
        ? &properties[left] : 0;
}

static int continuation(unsigned char value)
{
    return (value & 0xC0) == 0x80;
}

static uint32_t decode_utf8(Cursor *cursor)
{
    const unsigned char *p = cursor->text + cursor->position;
    int remaining = cursor->length - cursor->position;
    unsigned char first = p[0];
    uint32_t result;
    int count;

    if (first < 0x80) {
        count = 1;
        result = first;
    } else if (first >= 0xC2 && first <= 0xDF && remaining >= 2 &&
               continuation(p[1])) {
        count = 2;
        result = ((uint32_t)(first & 0x1F) << 6) | (p[1] & 0x3F);
    } else if (first >= 0xE0 && first <= 0xEF && remaining >= 3 &&
               continuation(p[1]) && continuation(p[2]) &&
               (first != 0xE0 || p[1] >= 0xA0) &&
               (first != 0xED || p[1] < 0xA0)) {
        count = 3;
        result = ((uint32_t)(first & 0x0F) << 12) |
                 ((uint32_t)(p[1] & 0x3F) << 6) | (p[2] & 0x3F);
    } else if (first >= 0xF0 && first <= 0xF4 && remaining >= 4 &&
               continuation(p[1]) && continuation(p[2]) && continuation(p[3]) &&
               (first != 0xF0 || p[1] >= 0x90) &&
               (first != 0xF4 || p[1] < 0x90)) {
        count = 4;
        result = ((uint32_t)(first & 0x07) << 18) |
                 ((uint32_t)(p[1] & 0x3F) << 12) |
                 ((uint32_t)(p[2] & 0x3F) << 6) | (p[3] & 0x3F);
    } else {
        count = 1;
        cursor->invalid = 1;
        result = 0x110000 + first;
    }
    cursor->position += count;
    return result;
}

static int valid_utf8(const void *text, int length)
{
    Cursor cursor = {0};
    cursor.text = text;
    cursor.length = length;
    while (cursor.position < cursor.length) {
        decode_utf8(&cursor);
        if (cursor.invalid)
            return 0;
    }
    return 1;
}

static int next_token(Cursor *cursor, uint32_t *codepoint)
{
    const Mapping *mapping;
    if (cursor->index < cursor->count) {
        *codepoint = mapping_values[cursor->offset + cursor->index++];
        return 1;
    }
    if (cursor->position == cursor->length)
        return 0;
    *codepoint = decode_utf8(cursor);
    mapping = find_mapping(*codepoint);
    if (mapping) {
        cursor->offset = mapping->offset;
        cursor->count = mapping->length;
        cursor->index = 1;
        *codepoint = mapping_values[mapping->offset];
    } else {
        cursor->count = 0;
        cursor->index = 0;
    }
    return 1;
}

static int same_position(const Cursor *a, const Cursor *b)
{
    return a->position == b->position && a->count == b->count &&
           a->index == b->index;
}

static int next_key(KeyIterator *it, uint32_t *result)
{
    for (;;) {
        uint32_t value;
        const Property *prop;
        Cursor previous;

        if (it->in_segment) {
            while (!same_position(&it->scan, &it->end)) {
                next_token(&it->scan, &value);
                prop = find_property(value);
                if (prop && !prop->nonspacing && prop->combining == it->combining) {
                    *result = value;
                    return 1;
                }
            }
            {
                Cursor search = it->start;
                unsigned int next_combining = 256;
                while (!same_position(&search, &it->end)) {
                    next_token(&search, &value);
                    prop = find_property(value);
                    if (prop && !prop->nonspacing &&
                        prop->combining > it->combining &&
                        prop->combining < next_combining)
                        next_combining = prop->combining;
                }
                if (next_combining < 256) {
                    it->combining = next_combining;
                    it->scan = it->start;
                    continue;
                }
            }
            it->cursor = it->end;
            it->in_segment = 0;
            continue;
        }

        previous = it->cursor;
        if (!next_token(&it->cursor, &value))
            return 0;
        prop = find_property(value);
        if (!prop || prop->combining == 0) {
            if (!prop || !prop->nonspacing) {
                *result = value;
                return 1;
            }
            continue;
        }

        /* Canonical ordering cannot cross a combining-class-zero character,
           including nonspacing marks that will subsequently be removed. */
        it->start = previous;
        it->end = it->cursor;
        for (;;) {
            Cursor before = it->end;
            if (!next_token(&it->end, &value))
                break;
            prop = find_property(value);
            if (!prop || prop->combining == 0) {
                it->end = before;
                break;
            }
        }
        it->scan = it->end;
        it->combining = 0;
        it->in_segment = 1;
    }
}

static int compare(void *context, int a_length, const void *a,
                   int b_length, const void *b)
{
    KeyIterator left = {0}, right = {0};
    uint32_t a_value, b_value;
    int has_a, has_b;
    (void)context;
    if (!valid_utf8(a, a_length) || !valid_utf8(b, b_length))
        sqlite3_log(SQLITE_MISMATCH,
                    "RMNOCASE: invalid UTF-8; sorting invalid bytes after Unicode");
    left.cursor.text = a;
    left.cursor.length = a_length;
    right.cursor.text = b;
    right.cursor.length = b_length;

    for (;;) {
        has_a = next_key(&left, &a_value);
        has_b = next_key(&right, &b_value);
        if (!has_a || !has_b)
            return has_a - has_b;
        if (a_value != b_value)
            return a_value < b_value ? -1 : 1;
    }
}

__declspec(dllexport)
int sqlite3_rmnocase_init(sqlite3 *db, char **error,
                          const sqlite3_api_routines *api)
{
    SQLITE_EXTENSION_INIT2(api);
    if (sqlite3_libversion_number() < 3006023) {
        if (error)
            *error = sqlite3_mprintf("RMNOCASE requires SQLite 3.6.23 or later");
        return SQLITE_ERROR;
    }
    return sqlite3_create_collation(db, "RMNOCASE", SQLITE_UTF8, 0, compare);
}

__declspec(dllexport)
int sqlite3_extension_init(sqlite3 *db, char **error,
                           const sqlite3_api_routines *api)
{
    return sqlite3_rmnocase_init(db, error, api);
}
