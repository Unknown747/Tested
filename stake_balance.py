import requests

TOKEN = "edd0aade282af360a96023fdb4037702918585c2ee236b60c5e5f8f2b03bc2ccf0788b8cff2d3b041561fd5248d60588"

query = """
{ user { name balances { available { amount currency } } } }
"""

r = requests.post(
    "https://stake.com/graphql",
    headers={
        "Content-Type": "application/json",
        "x-access-token": TOKEN,
    },
    json={"query": query},
    timeout=10,
)

print("Status:", r.status_code)
print("Response:", r.text[:500])
