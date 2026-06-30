# Stake Balance Fetcher

Script Python untuk mengambil data saldo akun Stake.com menggunakan API token.

## Cara Pakai

```bash
python stake_balance.py --token YOUR_TOKEN_HERE
```

Atau via environment variable:

```bash
STAKE_TOKEN=your_token_here python stake_balance.py
```

## Options

| Flag | Keterangan |
|------|-----------|
| `--token` / `-t` | API token Stake.com |
| `--verbose` / `-v` | Tampilkan raw response (untuk debug) |
| `--json` | Output dalam format JSON mentah |

## Cara Dapat Token Stake

1. Buka [stake.com](https://stake.com) dan login
2. Buka DevTools browser → tab **Network**
3. Lakukan aksi apa saja (klik halaman, refresh)
4. Cari request ke `api.stake.com` → lihat header `x-access-token`
5. Salin nilainya dan gunakan sebagai `--token`

## Stack

- Python 3.13
- Library: `requests`

## User Preferences

- Bahasa komunikasi: Bahasa Indonesia
