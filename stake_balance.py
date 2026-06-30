import requests

TOKEN = "edd0aade282af360a96023fdb4037702918585c2ee236b60c5e5f8f2b03bc2ccf0788b8cff2d3b041561fd5248d60588"

query = """
query UserFull {
  user {
    id
    name
    email
    createdAt
    preferredCurrency
    vipLevel {
      id
      level
      name
      nextLevel {
        name
        requiredXp
      }
    }
    xpTotal
    xpThisWeek
    totalBets
    totalWagered
    activeWallet { amount currency }
    balances {
      available { amount currency }
      vault     { amount currency }
      bonus     { amount currency }
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

r = requests.post(
    "https://stake.com/_api/graphql",
    headers=headers,
    json={"query": query, "operationName": "UserFull", "variables": {}},
    timeout=10,
)

import json
print(json.dumps(r.json(), indent=2))
