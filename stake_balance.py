#!/usr/bin/env python3
"""
Stake.com Balance Fetcher
Ambil data saldo akun Stake menggunakan API token.

Usage:
    python stake_balance.py --token YOUR_TOKEN_HERE
    STAKE_TOKEN=xxx python stake_balance.py
"""

import os
import sys
import json
import argparse
import cloudscraper

STAKE_GRAPHQL_URL = "https://stake.com/graphql"

WALLET_QUERY = """
query Balances {
  user {
    id
    name
    activeWallet {
      amount
      currency
    }
    balances {
      available { amount currency }
      vault     { amount currency }
      bonus     { amount currency }
    }
  }
}
"""


def fetch_balance(token: str, verbose: bool = False) -> dict:
    scraper = cloudscraper.create_scraper()

    headers = {
        "Content-Type": "application/json",
        "Accept":        "application/json",
        "x-access-token": token,
        "x-language":    "en",
        "Origin":        "https://stake.com",
        "Referer":       "https://stake.com/",
    }

    payload = {"query": WALLET_QUERY, "operationName": "Balances"}

    resp = scraper.post(STAKE_GRAPHQL_URL, headers=headers, json=payload, timeout=20)

    if verbose:
        print(f"[DEBUG] Status  : {resp.status_code}")
        print(f"[DEBUG] Response: {resp.text[:600]}")

    if resp.status_code == 401:
        raise ValueError("Token tidak valid atau sudah expired (401).")
    if resp.status_code == 403:
        raise ValueError("Akses ditolak (403). Token mungkin salah atau perlu cookie tambahan.")

    resp.raise_for_status()

    try:
        data = resp.json()
    except Exception:
        raise ValueError(f"Response bukan JSON valid:\n{resp.text[:300]}")

    if "errors" in data:
        msgs = [e.get("message", str(e)) for e in data["errors"]]
        raise ValueError("GraphQL error: " + " | ".join(msgs))

    return data.get("data", {})


def print_balances(data: dict):
    user = data.get("user")
    if not user:
        print("❌ Tidak ada data user. Token mungkin tidak valid.")
        return

    print("=" * 52)
    print(f"  👤 Username : {user.get('name', 'N/A')}")
    print(f"  🆔 User ID  : {user.get('id', 'N/A')}")
    print("=" * 52)

    active = user.get("activeWallet")
    if active:
        print(f"\n  💰 Active Wallet : {float(active.get('amount') or 0):.8f} {active['currency'].upper()}")

    balances = user.get("balances", [])
    nonzero = []
    for b in balances:
        currency  = (b.get("available") or {}).get("currency", "?").upper()
        available = float((b.get("available") or {}).get("amount", 0) or 0)
        vault     = float((b.get("vault")     or {}).get("amount", 0) or 0)
        bonus     = float((b.get("bonus")     or {}).get("amount", 0) or 0)
        if available or vault or bonus:
            nonzero.append((currency, available, vault, bonus))

    if nonzero:
        print(f"\n  {'Currency':<10} {'Available':>18} {'Vault':>14} {'Bonus':>14}")
        print("  " + "-" * 58)
        for currency, available, vault, bonus in nonzero:
            print(f"  {currency:<10} {available:>18.8f} {vault:>14.8f} {bonus:>14.8f}")
    else:
        print("\n  (Semua saldo 0)")

    print("=" * 52)


def main():
    parser = argparse.ArgumentParser(description="Ambil saldo Stake.com via API token")
    parser.add_argument("--token", "-t", default=os.environ.get("STAKE_TOKEN", ""),
                        help="API token Stake (atau set env STAKE_TOKEN)")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Tampilkan response mentah")
    parser.add_argument("--json", action="store_true",
                        help="Output JSON mentah")
    args = parser.parse_args()

    if not args.token:
        print("❌ Token tidak ditemukan.")
        print("   Gunakan: python stake_balance.py --token YOUR_TOKEN")
        sys.exit(1)

    try:
        data = fetch_balance(args.token, verbose=args.verbose)
        if args.json:
            print(json.dumps(data, indent=2))
        else:
            print_balances(data)
    except ValueError as e:
        print(f"❌ {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
