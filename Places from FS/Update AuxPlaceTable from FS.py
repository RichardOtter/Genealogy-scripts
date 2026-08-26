from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
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


def rm_coordinate(value):
    if value is None:
        return None
    return int(round(float(value) * 10_000_000))


def name_for_language(names, language):
    for name in names:
        if name.get("lang") == language:
            return name.get("value")
    for name in names:
        if name.get("lang", "").startswith(language + "-"):
            return name.get("value")
    return None


def request_json(url, language, timeout, token):
    headers = {
        "Accept": "application/json",
        "Accept-Language": language,
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = Request(url, headers=headers)
    with urlopen(request, timeout=timeout) as response:
        return json.load(response)


def fetch_place_description(fs_id, api_url, language, timeout, token):
    url = f"{api_url.rstrip('/')}/description/{fs_id}?flag=fsh"
    data = request_json(url, language, timeout, token)
    for place in data.get("places", []):
        if str(place.get("id")) == str(fs_id):
            return place
    return None


def type_id_from_url(type_url):
    return int(type_url.rsplit("/", 1)[-1]) if type_url else None


def cache_type(connection, type_url, api_url, timeout, token):
    type_id = type_id_from_url(type_url)
    if type_id is None:
        return
    exists = connection.execute(
        "SELECT 1 FROM AuxFSPlaceTypeTable WHERE FS_PlaceTypeID = ?",
        (type_id,),
    ).fetchone()
    if exists:
        return
    data = request_json(f"{type_url}?flag=fsh", "en", timeout, token)
    label = next(
        (item.get("@value") for item in data.get("labels", [])
         if item.get("@language") == "en"),
        None,
    )
    if label:
        connection.execute(
            """
            INSERT OR REPLACE INTO AuxFSPlaceTypeTable
                (FS_PlaceTypeID, EnglishName, TypeURL, LastUpdated)
            VALUES (?, ?, ?, julianday('now') - 2415018.5)
            """,
            (type_id, label, type_url),
        )


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
            display_value(place or {}, "fullName")
            or name_for_language(names, "en"),
            value_from(place or {}, "shortName", "displayName")
            or display_value(place or {}, "name"),
            name_for_language(names, "de"),
            None,
            value_from(place or {}, "abbreviation", "abbr"),
            rm_coordinate(value_from(place or {}, "latitude", "lat")),
            rm_coordinate(value_from(place or {}, "longitude", "lon", "lng")),
            value_from(place or {}, "startYear", "yearStart"),
            value_from(place or {}, "endYear", "yearEnd"),
            value_from(place or {}, "type"),
            value_from(place or {}, "status"),
            value_from(place.get("jurisdiction", {}) or {}, "resourceId"),
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
        description="Update FamilySearch columns from FS place-description IDs."
    )
    parser.add_argument("config", nargs="?", default=DEFAULT_CONFIG)
    parser.add_argument("--place-id", type=int,
                        help="Update one RootsMagic PlaceID.")
    parser.add_argument(
        "--limit", type=int, default=50,
        help="Maximum FSPID rows to update (default: 50)."
    )
    parser.add_argument(
        "--all", action="store_true",
        help="Update every eligible FSPID row."
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
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS AuxFSPlaceTypeTable (
            FS_PlaceTypeID INTEGER PRIMARY KEY,
            EnglishName TEXT NOT NULL,
            TypeURL TEXT NOT NULL UNIQUE,
            LastUpdated FLOAT
        )
        """
    )
    query = """
                SELECT PlaceID, FSPID
        FROM AuxPlaceTable
        WHERE Orig_PlaceType = 0
                    AND FSPID IS NOT NULL
                    AND NULLIF(TRIM(Uncertain), '') IS NOT NULL
        ORDER BY PlaceID
    """
    parameters = ()
    if args.place_id is not None:
        query = query.replace("ORDER BY PlaceID",
                              "AND PlaceID = ? ORDER BY PlaceID")
        parameters = (args.place_id,)

    rows = connection.execute(query, parameters).fetchall()
    if args.place_id is None and not args.all:
        rows = rows[:args.limit]
    if not rows:
        raise RuntimeError(
            "No eligible place-type 0 rows with FSPID were found."
        )

    ready = not_found = errors = 0
    try:
        for place_id, fs_id in rows:
            try:
                place = fetch_place_description(
                    fs_id, api_url, language, timeout, token)
                if place is None:
                    update_status(connection, place_id, "not_found", None)
                    not_found += 1
                else:
                    update_place(connection, place_id,
                                 fs_id, place, "ready", None)
                    cache_type(
                        connection, value_from(place, "type"), api_url,
                        timeout, token)
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
        f"Ready: {ready}; not found: {not_found}; errors: {errors}"
    )


if __name__ == "__main__":
    main()
