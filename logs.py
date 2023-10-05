import requests
import json
import time

def get_all_logs(base_url, query, token):
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    all_logs = []
    page = 0
    per_page = 100  # Max value as per API

    while True:
        url = f"{base_url}/api/v2/logs?page={page}&per_page={per_page}&q={query}"
        print(f"Fetching: {url}")  # Debug
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            print(f"Error: {response.text}")
            break

        if 'X-RateLimit-Remaining' in response.headers and int(response.headers['X-RateLimit-Remaining']) <= 1:
            print('Approaching rate limit. Sleeping...')
            time.sleep(5)  # sleep for 5 seconds or as appropriate

        logs = response.json()
        if not logs:
            break  # Exit loop if no more logs

        all_logs.extend(logs)
        page += 1  # Increment the page number for the next API call
        time.sleep(1)  # Optional: to prevent rate limiting

    return all_logs
token = "YOUR-TOKEN"
base_url = "https://YOUR-DOMAIN.us.auth0.com"
query = "seccft"

all_logs = get_all_logs(base_url, query, token)



# Write to a JSON file
with open("logs.json", "w") as f:
    json.dump(all_logs, f, indent=4)

