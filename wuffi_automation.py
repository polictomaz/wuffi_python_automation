import requests
import time
import json
import random

# proxy = {
#     'http':  'socks5://localhost:9050',
#     'https': 'socks5://localhost:9050',
# }

# url = 'https://httpbin.org/get'
# Configuration
num_calls = 5  # Number of times to call the API in a row
delay = 10     # Delay between batches of calls (in seconds)
num_batches = 3  # Total number of batches
# taps = 607  # Number of taps

# Define the API URL
api_url = 'https://wuffitap-01-api.wuffi.io/v1/protected-api/tap'

# Define the range
min_val = 3.123
max_val = 5.789

# Define the custom headers
headers = {
    "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
    "referer": "https://wuffitap.wuffi.io",
    "Access-Control-Request-Header": "authorization,content-type, telegram-user-id",
    "Accept-Encoding": "gzip, deflate, br",
    "sec-fetch-site": "same-site",
    "Accept": "*/*",
    "Connection": "keep-alive",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "Content-Type": "application/json",
    "Origin": "https://wuffitap.wuffi.io",
    "Host": "wuffitap-01-api.wuffi.io",
    "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyRGF0YSI6eyJpZCI6NTkyMywidGVsZWdyYW1faWQiOiIxNDczODk0ODMxIiwidXNlcm5hbWUiOiJzbXJkb21pciIsImZpcnN0X25hbWUiOiJTbXJkb01pciIsImxhc3RfbmFtZSI6IiIsImJhbGFuY2UiOiI0NTEiLCJjcmVhdGVkX2F0IjoiMjAyNC0wNy0xN1QwNjo0NTo1MS4wMTJaIiwidXBkYXRlZF9hdCI6IjIwMjQtMDgtMDFUMTQ6Mjg6NDMuNzU4WiIsImRlbGV0ZWRfYXQiOm51bGx9LCJsb2dpblRpbWUiOjE3MjI1MjI1MjM3NzEsImlhdCI6MTcyMjUyMjUyMywiZXhwIjoxNzIyNjA4OTIzfQ.x7RmQ4RZg9w76Z98PTWaWPiHKNPQRS5XgldISQKZReA",
    "telegram-user-id": "1473894831",
}
def random_float_within_range(min_val, max_val):
    return round(random.uniform(min_val, max_val), 3)


def make_api_call():
    taps = random.randint(140, 180)
    end_time = int(time.time() * 1000) - 2 * 1000
    start_time = int(end_time - (random_float_within_range(min_val, max_val) * 1000))
    json_data = json.dumps({
        "taps": taps,
        "startTime": start_time,
        "endTime": end_time
    })
    print("JSON DATA: ", json_data)
    print("ENERGY SPENT: ", taps * 21)
    print("TIME DIFF: ", end_time - start_time)
    try:
        response = requests.put(api_url, headers=headers, data=json_data)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx and 5xx)

        # Check if response content type is JSON and parse it
        if response.headers.get('Content-Type') == 'application/json':
            print("API call successful:", response.json())
        else:
            print("API call successful with non-JSON")

        print("===========")
        return True

    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 403:
            print("HTTP 403 Forbidden error occurred. Stopping further API calls.")
            print("===========")
            return False
        print(f"HTTP error occurred: {http_err}")
        print("Response content:", response.content)  # Print response content for debugging
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}")
    except Exception as e:
        print("Error making API call:", e)
    
    print("===========")
    return False

def main():
    while True:
        if not make_api_call():
            print("Stopping due to 403 error or other critical issue.")
            break
        # Generate a random delay between 10 and 15 minutes
        delay = random.uniform(180, 250)
        print(f"Waiting for {delay / 60:.2f} minutes before the next request...")
        time.sleep(delay)
if __name__ == "__main__":
    main()