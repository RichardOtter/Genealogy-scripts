from urllib.request import Request, urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError, URLError
import re
import time
import sqlite3
import json
import configparser
import argparse
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))


DEFAULT_CONFIG = "RM-Python-config.ini"
DEFAULT_API_URL = "https://api.familysearch.org/platform/places"
FSPID_PATTERN = re.compile(r"(?:^|\r?\n)\s*FSPID\s*=\s*(\d+)", re.IGNORECASE)


def rm_coordinate(value):
    if value is None:
        return None
    return int(round(float(value) * 10_000_000))


def fs_id_from_note(note):
    if not note:
        return None
    match = FSPID_PATTERN.search(note)
    return int(match.group(1)) if match else None


def note_is_skipped(note):
    return bool(note) and note.startswith("_SKIP")


def name_for_language(names, language):
    for name in names:
        if name.get("lang") == language:
            return name.get("value")
    for name in names:
        if name.get("lang", "").startswith(language + "-"):
            return name.get("value")
    return None


def place_from_search_response(data):
    for entry in data.get("entries", []):
        places = (entry.get("content", {}).get("gedcomx", {})
                  .get("places", []))
        if places:
            return places[0]

    return None


def fetch_place(place_name, api_url, language, timeout, token):
    query = f'name:"{place_name}"'
    url = f"{api_url.rstrip('/')}/search?{urlencode({'q': query})}"
    headers = {
        "Accept": "application/json",
        "Accept-Language": language,
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = Request(url, headers=headers)
    with urlopen(request, timeout=timeout) as response:
        return place_from_search_response(json.load(response))


def value_from(place, *keys):
    for key in keys:
        if place.get(key) is not None:
            return place[key]
    return None


def display_value(place, key):
    display = place.get("display", {})
    return display.get(key) if isinstance(display, dict) else None


def update_place(connection, place_id, fs_id, place, status, error):
    names = place.get("names", []) if place else []
    connection.execute(
        """
        UPDATE AuxPlaceTable
        SET FS_NameFull_en = ?, FS_NameShort_en = ?,
            FS_NameFull_de = ?, FS_NameShort_de = ?, FS_Abbrev = ?,
            FS_Latitude = ?, FS_Longitude = ?, FS_YearStart = ?,
            FS_YearEnd = ?, FS_PlaceType = ?, FS_PlaceStatus = ?,
            FS_ParentID = ?, FS_ReturnedID = ?,
            FS_LastUpdated = julianday('now') - 2415018.5,
            FS_Status = ?, FS_Error = ?
        WHERE PlaceID = ?
        """,
        (
            name_for_language(names, "en"),
            value_from(place or {}, "shortName", "displayName")
            or display_value(place or {}, "name"),
            name_for_language(names, "de"),
            None,
            value_from(place or {}, "abbreviation", "abbr"),
            rm_coordinate(value_from(place or {}, "latitude", "lat")),
            rm_coordinate(value_from(place or {}, "longitude", "lon", "lng")),
            value_from(place or {}, "startYear", "yearStart"),
            value_from(place or {}, "endYear", "yearEnd"),
            value_from(place or {}, "placeType", "type")
            or display_value(place or {}, "type"),
            value_from(place or {}, "status"),
            value_from(place or {}, "parentId", "parentID"),
            place.get("id") if place else None,
            status,
            error,
            place_id,
        ),
    )


def update_status(connection, place_id, status, error):
    connection.execute(
        """
        UPDATE AuxPlaceTable
        SET FS_LastUpdated = julianday('now') - 2415018.5,
            FS_Status = ?, FS_Error = ?
        WHERE PlaceID = ?
        """,
        (status, error, place_id),
    )


def main():
    parser = argparse.ArgumentParser(
        description="Update FamilySearch columns using FSPID values in place notes."
    )
    parser.add_argument("config", nargs="?", default=DEFAULT_CONFIG)
    parser.add_argument("--place-id", type=int,
                        help="Update one RootsMagic PlaceID.")
    parser.add_argument(
        "--limit", type=int, default=50,
        help="Maximum number of FS-ID rows to update (default: 50)."
    )
    parser.add_argument(
        "--all", action="store_true",
        help="Update every matching FS-ID row."
    )
    args = parser.parse_args()

    if args.limit < 1:
        parser.error("--limit must be at least 1")

    config = configparser.ConfigParser()
    config.read(args.config, encoding="utf-8")
    paths = config["FILE_PATHS"]
    options = config["OPTIONS"] if "OPTIONS" in config else {}
    database_path = paths["DB_PATH"]
    api_url = options.get("FS_API_URL", DEFAULT_API_URL)
    language = options.get("FS_ACCEPT_LANGUAGE", "en,de")
    timeout = float(options.get("FS_REQUEST_TIMEOUT", "30"))
    token = options.get("FS_API_TOKEN", "").strip()
    delay = float(options.get("FS_REQUEST_DELAY", "0"))

    connection = sqlite3.connect(database_path)
    connection.execute("PRAGMA foreign_keys = ON")
    query = """
        SELECT PlaceID, Orig_Name, Orig_Note
        FROM AuxPlaceTable
        ORDER BY PlaceID
    """
    parameters = ()
    if args.place_id is not None:
        query = query.replace("ORDER BY PlaceID",
                              "WHERE PlaceID = ? ORDER BY PlaceID")
        parameters = (args.place_id,)

    candidate_rows = connection.execute(query, parameters).fetchall()
    skipped = sum(
        1 for _, _, note in candidate_rows if note_is_skipped(note)
    )
    rows = [
        (place_id, place_name, fs_id)
        for place_id, place_name, note in candidate_rows
        if not note_is_skipped(note)
        if (fs_id := fs_id_from_note(note)) is not None
    ]
    if args.place_id is None and not args.all:
        rows = rows[:args.limit]
    if not rows:
        raise RuntimeError(
            "No snapshot rows with an FSPID=... value in Orig_Note were found. "
            "Run AuxPlaceTable snapshot.sql first."
        )

    ready = mismatch = not_found = errors = 0
    try:
        for place_id, place_name, fs_id in rows:
            try:
                place = fetch_place(
                    place_name, api_url, language, timeout, token)
                if place is None:
                    update_status(connection, place_id, "not_found", None)
                    not_found += 1
                elif str(place.get("id")) != str(fs_id):
                    returned_id = place.get("id", "<missing>")
                    update_place(
                        connection, place_id, fs_id, place, "id_changed",
                        f"Name search returned FS ID {returned_id}; "
                        f"AuxPlaceTable has {fs_id}.",
                    )
                    mismatch += 1
                else:
                    update_place(connection, place_id,
                                 fs_id, place, "ready", None)
                    ready += 1
            except (HTTPError, URLError, TimeoutError, ValueError, json.JSONDecodeError) as error:
                update_status(connection, place_id, "error", str(error)[:500])
                errors += 1
            if delay:
                time.sleep(delay)
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()

    print(
        f"Ready: {ready}; mismatches: {mismatch}; "
        f"not found: {not_found}; errors: {errors}; skipped: {skipped}"
    )


if __name__ == "__main__":
    main()
