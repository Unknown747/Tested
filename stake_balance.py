import requests

TOKEN = "edd0aade282af360a96023fdb4037702918585c2ee236b60c5e5f8f2b03bc2ccf0788b8cff2d3b041561fd5248d60588"

query = """
query UserBalance {
  user {
    name
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
    json={"query": query, "operationName": "UserBalance", "variables": {}},
    timeout=10,
)

data = r.json()
user = data["data"]["user"]

print(f"Username : {user['name']}")
print()

has_balance = False
for b in user["balances"]:
    available = float(b["available"]["amount"] or 0)
    vault     = float(b["vault"]["amount"] or 0)
    bonus     = float(b["bonus"]["amount"] or 0)
    currency  = b["available"]["currency"].upper()

    if available or vault or bonus:
        has_balance = True
        print(f"  {currency:<6}  available={available:.8f}  vault={vault:.8f}  bonus={bonus:.8f}")

if not has_balance:
    print("  Semua saldo 0")
