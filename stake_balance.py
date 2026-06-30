import requests, json

TOKEN = "edd0aade282af360a96023fdb4037702918585c2ee236b60c5e5f8f2b03bc2ccf0788b8cff2d3b041561fd5248d60588"

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

def q(query, op="Test"):
    r = requests.post(
        "https://stake.com/_api/graphql",
        headers=headers,
        json={"query": query, "operationName": op, "variables": {}},
        timeout=10,
    )
    return r.json()

# Probe 1: field dasar user yang valid
res = q("""
query Test {
  user {
    id name email createdAt
    rakeback { id level name }
    vip { id level name }
    tier { id level name }
    bets { id }
  }
}
""")
print("=== PROBE 1 (rakeback/vip/tier/bets) ===")
print(json.dumps(res.get("errors", res.get("data")), indent=2))
print()

# Probe 2: statistik wagering
res2 = q("""
query Test {
  user {
    statistic {
      bets wins losses wagered
    }
    wager { amount currency }
    totalWager
    weeklyWager
  }
}
""")
print("=== PROBE 2 (statistic/wager) ===")
print(json.dumps(res2.get("errors", res2.get("data")), indent=2))
