"""Add FamilySearch IDs to auxiliary place notes after an exact name-search match.

Candidates and inserted FSPIDs are stored only in AuxPlaceTable.Orig_Note.
PlaceTable is never changed by this utility.
"""

import argparse
import configparser
import json
import re
import sqlite3
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


DEFAULT_CONFIG = "RM-Python-config.ini"
DEFAULT_API_URL = "https://api.familysearch.org/platform/places"
FSPID_PATTERN = re.compile(r"(?:^|\r?\n)\s*FSPID\s*=\s*\d+", re.IGNORECASE)


def note_has_fspid(note):
    return bool(note) and bool(FSPID_PATTERN.search(note))


def note_is_skipped(note):
    return bool(note) and note.startswith("_SKIP")


def name_for_search(place_name):
    return place_name.lstrip().removeprefix("+").lstrip()


def search_result(data):
    entries = data.get("entries", [])
    if not entries:
        return None, None
    entry = entries[0]
    places = entry.get("content", {}).get("gedcomx", {}).get("places", [])
    return (places[0] if places else None), entry.get("score")


def search_place(place_name, api_url, language, timeout, token):
    query = f'name:"{place_name}"'
    url = f"{api_url.rstrip('/')}/search?{urlencode({'q': query})}"
    headers = {"Accept": "application/json", "Accept-Language": language}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    with urlopen(Request(url, headers=headers), timeout=timeout) as response:
        return search_result(json.load(response))


def prepend_fspid(note, fs_id):
    return f"FSPID={fs_id}\r\n{note or ''}"


def update_aux_status(connection, place_id, fs_id, status, error):
    connection.execute(
        """
        UPDATE AuxPlaceTable
        SET FS_ReturnedID = ?,
            FS_LastUpdated = julianday('now') - 2415018.5,
            FS_Status = ?, FS_Error = ?
        WHERE PlaceID = ?
        """,
        (str(fs_id) if fs_id is not None else None, status, error, place_id),
    )


def main():
    parser = argparse.ArgumentParser(
        description="Add FSPID to AuxPlaceTable notes after an exact FamilySearch match."
    )
    parser.add_argument("config", nargs="?", default=DEFAULT_CONFIG)
    parser.add_argument("--place-id", type=int,
                        help="Process one RootsMagic PlaceID.")
    parser.add_argument("--limit", type=int, default=50,
                        help="Maximum candidates to process (default: 50).")
    parser.add_argument("--all", action="store_true",
                        help="Process all eligible candidates.")
    parser.add_argument("--apply", action="store_true",
                        help="Write FSPID values to AuxPlaceTable.Orig_Note. Default is dry run.")
    args = parser.parse_args()
    if args.limit < 1:
        parser.error("--limit must be at least 1")

    config = configparser.ConfigParser()
    config.read(args.config, encoding="utf-8")
    paths = config["FILE_PATHS"]
    options = config["OPTIONS"] if "OPTIONS" in config else {}
    api_url = options.get("FS_API_URL", DEFAULT_API_URL)
    language = options.get("FS_ACCEPT_LANGUAGE", "en,de")
    timeout = float(options.get("FS_REQUEST_TIMEOUT", "30"))
    token = options.get("FS_API_TOKEN", "").strip()
    delay = float(options.get("FS_REQUEST_DELAY", "0"))

    connection = sqlite3.connect(paths["DB_PATH"])
    try:
        query = """
            SELECT PlaceID, Orig_Name, Orig_Note
            FROM AuxPlaceTable a
            WHERE Orig_PlaceType = 0
            ORDER BY a.PlaceID
        """
        parameters = ()
        if args.place_id is not None:
            query = query.replace(
                "ORDER BY a.PlaceID", "AND a.PlaceID = ? ORDER BY a.PlaceID")
            parameters = (args.place_id,)

        candidates = [
            row for row in connection.execute(query, parameters)
            if not note_is_skipped(row[2]) and not note_has_fspid(row[2])
        ]
        if args.place_id is None and not args.all:
            candidates = candidates[:args.limit]
        if not candidates:
            raise RuntimeError(
                "No eligible AuxPlaceTable notes without FSPID= were found.")

        total_candidates = len(candidates)
        print(f"Looking up {total_candidates} place(s)...", flush=True)
        added = candidate = not_found = errors = 0
        for completed, (place_id, place_name, note) in enumerate(candidates, start=1):
            try:
                place, score = search_place(
                    name_for_search(place_name), api_url, language, timeout, token)
                fs_id = place.get("id") if place else None
                if place is None:
                    update_aux_status(connection, place_id,
                                      None, "not_found", None)
                    not_found += 1
                elif score != 100 or not fs_id:
                    update_aux_status(
                        connection, place_id, fs_id, "candidate",
                        f"FamilySearch search score is {score}; exact score 100 is required.",
                    )
                    candidate += 1
                elif args.apply:
                    connection.execute(
                        "UPDATE AuxPlaceTable SET Orig_Note = ? WHERE PlaceID = ?",
                        (prepend_fspid(note, fs_id), place_id),
                    )
                    update_aux_status(connection, place_id,
                                      fs_id, "fsid_added", None)
                    added += 1
                else:
                    update_aux_status(connection, place_id,
                                      fs_id, "exact_match", None)
                    candidate += 1
            except (HTTPError, URLError, TimeoutError, ValueError, json.JSONDecodeError) as error:
                update_aux_status(connection, place_id, None,
                                  "error", str(error)[:500])
                errors += 1
            if delay:
                time.sleep(delay)
            if completed % 10 == 0 or completed == total_candidates:
                print(
                    f"Completed {completed} of {total_candidates}.", flush=True)
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()

    action = "Added" if args.apply else "Exact matches found"
    print(f"{action}: {added if args.apply else candidate}; "
          f"non-exact candidates: {candidate if args.apply else 0}; "
          f"not found: {not_found}; errors: {errors}")


if __name__ == "__main__":
    main()
