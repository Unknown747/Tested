#!/usr/bin/env python3
"""
Stake.com Balance Fetcher
Ambil data saldo akun Stake menggunakan API token / session token.

Usage:
    python stake_balance.py --token YOUR_TOKEN_HERE
    atau set environment variable: STAKE_TOKEN=xxx python stake_balance.py
"""

import os
import sys
import json
import argparse
import requests

# ---------------------------------------------------------------------------
# Konfigurasi
# ---------------------------------------------------------------------------

STAKE_GRAPHQL_URL = "https://api.stake.com/graphql"

HEADERS_BASE = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "x-language": "en",
}

# Query GraphQL untuk ambil semua saldo
BALANCE_QUERY = """
query UserBalances {
  user {
    id
    name
    balances {
      available {
        amount
        currency
      }
      vault {
        amount
        currency
      }
    }
  }
}
"""

# Query alternatif (lebih lengkap, termasuk rakeback & bonus)
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
      available {
        amount
        currency
      }
      vault {
        amount
        currency
      }
      bonus {
        amount
        currency
      }
    }
  }
}
"""


# ---------------------------------------------------------------------------
# Fungsi utama
# ---------------------------------------------------------------------------

def fetch_balance(token: str, verbose: bool = False) -> dict:
    """Kirim request GraphQL ke Stake dan kembalikan data saldo."""

    headers = {
        **HEADERS_BASE,
        "x-access-token": token,
    }

    payload = {
        "query": WALLET_QUERY,
        "operationName": "Balances",
    }

    try:
        response = requests.post(
            STAKE_GRAPHQL_URL,
            headers=headers,
            json=payload,
            timeout=15,
        )
    except requests.exceptions.Timeout:
        raise ConnectionError("Request ke Stake timeout (>15 detik). Coba lagi.")
    except requests.exceptions.ConnectionError:
        raise ConnectionError("Gagal terhubung ke api.stake.com. Cek koneksi internet.")
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Request error: {e}")

    if verbose:
        print("[DEBUG] ⚠️  Mode verbose aktif — response mungkin mengandung data sensitif")
        print(f"[DEBUG] Status Code : {response.status_code}")
        print(f"[DEBUG] Response    : {response.text[:500]}")

    response.raise_for_status()

    try:
        data = response.json()
    except ValueError:
        raise ValueError(f"Response bukan JSON valid. Raw: {response.text[:200]}")

    if "errors" in data:
        raise ValueError(f"GraphQL error: {json.dumps(data['errors'], indent=2)}")

    return data.get("data", {})


def print_balances(data: dict):
    """Tampilkan saldo dengan format yang rapi."""

    user = data.get("user")
    if not user:
        print("❌ Tidak ada data user. Cek token Anda.")
        return

    print("=" * 50)
    print(f"  👤 Username : {user.get('name', 'N/A')}")
    print(f"  🆔 User ID  : {user.get('id', 'N/A')}")
    print("=" * 50)

    # Active wallet
    active = user.get("activeWallet")
    if active:
        print(f"\n  💰 Active Wallet : {active['amount']} {active['currency'].upper()}")

    # Semua saldo per currency
    balances = user.get("balances", [])
    if balances:
        print("\n  📊 Rincian Saldo :")
        print(f"  {'Currency':<12} {'Available':>18} {'Vault':>18} {'Bonus':>18}")
        print("  " + "-" * 68)
        for b in balances:
            currency  = b.get("available", {}).get("currency", "?").upper()
            available = float(b.get("available", {}).get("amount", 0) or 0)
            vault     = float(b.get("vault",     {}).get("amount", 0) or 0)
            bonus     = float(b.get("bonus",     {}).get("amount", 0) or 0)

            # Lewati currency dengan semua nilai 0
            if available == 0 and vault == 0 and bonus == 0:
                continue

            print(f"  {currency:<12} {available:>18.8f} {vault:>18.8f} {bonus:>18.8f}")
    else:
        print("\n  (Tidak ada data saldo)")

    print("=" * 50)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Ambil saldo Stake.com via API token")
    parser.add_argument(
        "--token", "-t",
        default=os.environ.get("STAKE_TOKEN", ""),
        help="API / session token Stake (atau set env STAKE_TOKEN)",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Tampilkan response mentah untuk debugging",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output dalam format JSON mentah",
    )
    args = parser.parse_args()

    if not args.token:
        print("❌ Token tidak ditemukan.")
        print("   Gunakan: python stake_balance.py --token YOUR_TOKEN")
        print("   Atau set environment variable: STAKE_TOKEN=xxx")
        sys.exit(1)

    try:
        data = fetch_balance(args.token, verbose=args.verbose)

        if args.json:
            print(json.dumps(data, indent=2))
        else:
            print_balances(data)

    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error: {e}")
        print("   Kemungkinan token salah atau sudah expired.")
        sys.exit(1)
    except ConnectionError as e:
        print(f"❌ {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"❌ {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
