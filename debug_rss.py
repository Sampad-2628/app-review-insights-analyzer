import requests
import json

app_id = 1351630927
country = 'in'
url = f"https://itunes.apple.com/{country}/rss/customerreviews/page=1/id={app_id}/sortby=mostrecent/json"

print(f"Fetching: {url}")
try:
    response = requests.get(url, timeout=10)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        # Print keys of the feed
        print("Feed keys:", data.get('feed', {}).keys())
        entries = data.get('feed', {}).get('entry', [])
        print(f"Number of entries: {len(entries)}")
        if entries:
            print("First entry sample:")
            print(json.dumps(entries[0], indent=2))
    else:
        print("Response text:", response.text[:500])
except Exception as e:
    print(f"Error: {e}")
