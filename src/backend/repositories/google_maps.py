import requests


def fetch_map_preview(lat: float, lng: float, api_key: str):
    return requests.get(
        f"https://maps.googleapis.com/maps/api/staticmap?center={lat},{lng}&zoom=13&size=600x300&maptype=roadmap&markers=color:red%7Clabel:C%7C{lat},{lng}&key={api_key}",
    )


def resolve_address(lat: float, lng: float, api_key: str) -> str:
    url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&language=pl&key={api_key}"
    response = requests.get(url)
    return response.json()["results"][0]["formatted_address"]
