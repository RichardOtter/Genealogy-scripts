import requests

def get_german_name(place_string):
    url = "https://api.familysearch.org/platform/places/search"
    params = {"q": f'name:"{place_string}"'}
    headers = {
        "Accept": "application/json",
        "Accept-Language": "de"
    }

    r = requests.get(url, params=params, headers=headers)
    r.raise_for_status()
    data = r.json()

    # FamilySearch wraps results inside "places"
    places = data.get("places", [])
    if not places:
        return None

    place = places[0]  # take the top interpretation
    names = place.get("names", [])

    # 1) exact German match
    for n in names:
        if n.get("lang") == "de":
            return n.get("value")

    # 2) any German variant (e.g., de-AT, de-DE)
    for n in names:
        lang = n.get("lang", "")
        if lang.startswith("de"):
            return n.get("value")

    # 3) fallback: first name in list
    if names:
        return names[0].get("value")

    return None


# Example usage
german_name = get_german_name("Vienna")
print("Preferred German name:", german_name)