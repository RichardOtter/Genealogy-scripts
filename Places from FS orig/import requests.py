import requests

url = "https://api.familysearch.org/platform/places/search"
params = {
    "q": 'name:"Wien"'   # interpret the place name "Wien"
}

headers = {
    "Accept": "application/json",
    "Accept-Language": "de"   # request German-language place names
}

response = requests.get(url, params=params, headers=headers)
response.raise_for_status()

data = response.json()
print(data)