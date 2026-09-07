from urllib.request import Request, urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError, URLError
import time
import sqlite3
import json
import configparser
import argparse
import sys
import re
from datetime import datetime
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))


DEFAULT_CONFIG = "RM-Python-config.ini"
DEFAULT_API_URL = "https://api.familysearch.org/platform/places"
TEMPORAL_PATTERN = re.compile(r"^([+-]?\d{1,6})?(?:/([+-]?\d{1,6})?)?$")
BRACKETED_TEXT_PATTERN = re.compile(r"\[[^\]]*\]")


def main():
    parser = argparse.ArgumentParser(
        description="Update FamilySearch columns from FS place-description IDs."
    )
    parser.add_argument("config", nargs="?", default=DEFAULT_CONFIG)
    parser.add_argument("--place-id", type=int,
                        help="Update one RootsMagic PlaceID.")
    parser.add_argument(
        "--limit", type=int, default=50,
        help="Maximum eligible rows to update (default: 50)."
    )
    parser.add_argument(
        "--all", action="store_true",
        help="Update every eligible row."
    )
    parser.add_argument(
        "--skip-ready", action="store_true",
        help="Skip rows whose FS_Status is already ready."
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
    type_table_exists = connection.execute(
        """
        SELECT 1
        FROM sqlite_master
        WHERE type = 'table' AND name = 'AuxFSPlaceTypeTable'
        """
    ).fetchone()
    if type_table_exists is None:
        raise RuntimeError(
            "AuxFSPlaceTypeTable is missing. Run "
            "Initialize AuxPlace tables.sql first."
        )
    query = """
        SELECT PlaceID, Orig_Name, Orig_Normalized, FSPDesID
        FROM AuxPlaceTable
        WHERE Orig_PlaceType = 0
            AND NULLIF(TRIM(Uncertain), '') IS NULL
        ORDER BY PlaceID
    """
    parameters = ()
    if args.skip_ready:
        query = query.replace(
            "ORDER BY PlaceID",
            "AND COALESCE(FS_Status, '') <> 'ready' ORDER BY PlaceID",
        )
    if args.place_id is not None:
        query = query.replace("ORDER BY PlaceID",
                              "AND PlaceID = ? ORDER BY PlaceID")
        parameters = (args.place_id,)

    rows = connection.execute(query, parameters).fetchall()
    if args.place_id is None and not args.all:
        rows = rows[:args.limit]
    if not rows:
        raise RuntimeError(
            "No eligible place-type 0 rows were found."
        )

    configured_report_path = Path(
        paths.get("REPORT_FILE_PATH", "FS lookup report.txt")
    )
    report_timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    report_path = configured_report_path.with_name(
        f"{configured_report_path.stem}-{report_timestamp}"
        f"{configured_report_path.suffix}"
    )
    report_file = report_path.open("w", encoding="utf-8")
    report_file.write(
        "FamilySearch lookup results\n===========================\n\n")
    ready = low_score = not_found = errors = 0
    try:
        total_rows = len(rows)
        print(f"Processing {total_rows} place(s):\n", end="", flush=True)
        for completed, (place_id, original_name, normalized_name,
                        fs_description_id) in enumerate(rows, start=1):
            try:
                comparison_name = preferred_place_name(
                    normalized_name, original_name)
                search_place, score = fetch_name_match(
                    name_for_search(comparison_name),
                    api_url, language, timeout, token)
                found_name = display_value(search_place or {}, "fullName")
                if search_place is None:
                    update_status(connection, place_id, "not_found", None)
                    report_file.write(
                        f"\nPlaceID={place_id}\nOriginal={comparison_name!r}\n"
                        "Found=None; Score=None\n"
                    )
                    not_found += 1
                else:
                    gemeinde_issue = False
                    county_issue = False
                    bracket_format = bool(
                        BRACKETED_TEXT_PATTERN.search(original_name or ""))
                    retry_name = None
                    county_retry_name = None
                    if score != 100:
                        retry_name = truncated_duplicate_level_name(
                            comparison_name)
                        if retry_name:
                            retry_place, retry_score = fetch_name_match(
                                retry_name, api_url, language, timeout, token)
                            if retry_place is not None and retry_score == 100:
                                search_place = retry_place
                                score = retry_score
                                found_name = display_value(
                                    search_place, "fullName")
                                fs_description_id = search_place.get("id")
                                gemeinde_issue = True
                        if score != 100:
                            county_retry_name = name_without_county(
                                comparison_name)
                            if county_retry_name:
                                county_place, county_score = fetch_name_match(
                                    county_retry_name, api_url, language,
                                    timeout, token)
                                if (county_place is not None
                                        and county_score == 100):
                                    search_place = county_place
                                    score = county_score
                                    found_name = display_value(
                                        search_place, "fullName")
                                    fs_description_id = search_place.get("id")
                                    county_issue = True
                    if score != 100:
                        update_status(connection, place_id, "low_score", None)
                        report_file.write(
                            f"\nPlaceID={place_id}\nOriginal={comparison_name!r}"
                            f"\n  Found={found_name!r}; "
                            f"\n  Score={score}; Retry={retry_name!r}; "
                            f"CountyRetry={county_retry_name!r}\n"
                        )
                        low_score += 1
                        if delay:
                            time.sleep(delay)
                        print(".", end="", flush=True)
                        if completed % 10 == 0 or completed == total_rows:
                            print(f" {completed} of {total_rows}", flush=True)
                        continue
                    description_id = fs_description_id
                    if description_id is None:
                        description_id = search_place.get("id")
                    place = fetch_place_description(
                        description_id, api_url, language, timeout, token)
                    if place is None:
                        update_status(connection, place_id, "not_found", None)
                        not_found += 1
                    else:
                        update_place(connection, place_id,
                                     description_id, place, score,
                                     ";".join(filter(None, [
                                         "_BRACKET-TEXT" if bracket_format else None,
                                         "_GEMEINDE-ISSUE" if gemeinde_issue else None,
                                         "_COUNTY" if county_issue else None,
                                     ])),
                                     "ready", None)
                        cache_type(
                            connection, value_from(place, "type"), api_url,
                            timeout, token)
                        ready += 1
            except (HTTPError, URLError, TimeoutError, ValueError, json.JSONDecodeError) as error:
                update_status(connection, place_id, "error", str(error)[:500])
                errors += 1
            if delay:
                time.sleep(delay)
            print(".", end="", flush=True)
            if completed % 10 == 0 or completed == total_rows:
                print(f" {completed} of {total_rows}", flush=True)
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        report_file.close()
        connection.close()

    print(
        f"Ready: {ready}; low score: {low_score}; "
        f"not found: {not_found}; errors: {errors}; "
        f"report: {report_path}"
    )


def rm_coordinate(value):
    if value is None:
        return None
    return int(round(float(value) * 10_000_000))


def temporal_years(place):
    formal = (place.get("temporalDescription", {}) or {}).get("formal")
    if not formal:
        return None, None
    match = TEMPORAL_PATTERN.match(formal)
    if not match:
        return None, None
    start = int(match.group(1)) if match.group(1) else None
    end = int(match.group(2)) if match.group(2) else None
    return start, end


def preferred_place_name(normalized_name, original_name):
    if normalized_name and normalized_name.strip():
        return normalized_name
    return original_name


def name_for_search(place_name):
    cleaned = BRACKETED_TEXT_PATTERN.sub("", place_name or "")
    cleaned = re.sub(r",\s*(?:,\s*)+", ",", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned)
    cleaned = re.sub(r",\s*", ", ", cleaned)
    return cleaned.strip(" ,").lstrip().removeprefix("+").lstrip()


def truncated_duplicate_level_name(place_name):
    cleaned = name_for_search(place_name)
    levels = [level.strip() for level in cleaned.split(",")]
    if len(levels) >= 2 and levels[0].casefold() == levels[1].casefold():
        return ", ".join(levels[1:])
    return None


def name_without_county(place_name):
    cleaned = name_for_search(place_name)
    levels = [level.strip() for level in cleaned.split(",")]
    if levels and re.search(r"\bCounty\b", levels[0], re.IGNORECASE):
        levels[0] = re.sub(r"\bCounty\b", "", levels[0],
                           flags=re.IGNORECASE)
        levels[0] = re.sub(r"\s+", " ", levels[0]).strip(" ,")
        return ", ".join(level for level in levels if level)
    return None


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


def fetch_name_match(place_name, api_url, language, timeout, token):
    query = f'name:"{place_name}"'
    url = f"{api_url.rstrip('/')}/search?{urlencode({'q': query})}"
    data = request_json(url, language, timeout, token)
    entries = data.get("entries", [])
    if not entries:
        return None, None
    places = (entries[0].get("content", {}).get("gedcomx", {})
              .get("places", []))
    return (places[0] if places else None), entries[0].get("score")


def primary_id_from_place(place):
    primary_urls = (place.get("identifiers", {}) or {}).get(
        "http://gedcomx.org/Primary", [])
    if not primary_urls:
        return None
    return primary_urls[0].rstrip("/").rsplit("/", 1)[-1]


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


def update_place(connection, place_id, fs_id, place, score, format_flag,
                 status, error):
    names = place.get("names", []) if place else []
    year_start, year_end = temporal_years(place or {})
    place_status = value_from(place or {}, "status", "placeStatus")
    if place_status is None:
        place_status = display_value(place or {}, "status")
    connection.execute(
        """
        UPDATE AuxPlaceTable
        SET FS_NameFull_en = ?, FS_NameShort_en = ?,
            FS_NameFull_de = ?, FS_NameShort_de = ?, FS_Abbrev = ?,
            FS_Latitude = ?, FS_Longitude = ?, FS_YearStart = ?,
            FS_YearEnd = ?, FS_PlaceType = ?, FS_PlaceStatus = ?,
            FS_ParentID = ?, FSPDesID = ?, FSPID = ?, NonFSPlace = ?,
            FSMatchScore = ?,
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
            year_start,
            year_end,
            value_from(place or {}, "type"),
            place_status,
            value_from(place.get("jurisdiction", {}) or {}, "resourceId"),
            fs_id,
            primary_id_from_place(place) if place else None,
            format_flag,
            int(score),
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


if __name__ == "__main__":
    main()
