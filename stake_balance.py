import requests

TOKEN = "edd0aade282af360a96023fdb4037702918585c2ee236b60c5e5f8f2b03bc2ccf0788b8cff2d3b041561fd5248d60588"

query = """
query UserBalance {
  user {
    name
    balances {
      available {
        amount
        currency
      }
    }
  }
}
"""

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "x-access-token": TOKEN,
    "x-language": "en",
    "Origin": "https://stake.com",
    "Referer": "https://stake.com/",
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
    "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124"',
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": '"Android"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "Accept-Language": "en-US,en;q=0.9",
}

endpoints = [
    "https://stake.com/_api/graphql",
    "https://api.stake.com/api/graphql",
    "https://stake.com/graphql",
    "https://api.stake.com/graphql",
]

payload = {
    "operationName": "UserBalance",
    "variables": {},
    "query": query,
}

for url in endpoints:
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=10)
        print(f"[{r.status_code}] {url}")
        print("  ", r.text[:200])
    except Exception as e:
        print(f"[ERR] {url} -> {e}")
    print()
