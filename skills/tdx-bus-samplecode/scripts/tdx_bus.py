#!/usr/bin/env python3
"""TDX Bus API quick CLI (based on tdxmotc/SampleCode patterns).

- Gets OIDC access token (client_credentials)
- Caches token locally to reduce token endpoint calls
- Calls Bus ETA / RealTime endpoints

Env vars:
- TDX_CLIENT_ID
- TDX_CLIENT_SECRET

Examples:
  python tdx_bus.py eta-city --city NewTaipei --top 5
  python tdx_bus.py a1-city --city Taipei --top 5
  python tdx_bus.py a2-city --city Taichung --top 5

Windows:
  py tdx_bus.py eta-city --city NewTaipei --top 5
"""

from __future__ import annotations

import argparse
import json
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

import requests

TOKEN_URL = "https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token"
API_BASE = "https://tdx.transportdata.tw/api/basic"


def default_cache_path() -> Path:
    # Cross-platform, user-scoped cache.
    home = Path.home()
    if os.name == "nt":
        base = Path(os.environ.get("LOCALAPPDATA", str(home)))
        return base / "tdx" / "token.json"
    return home / ".cache" / "tdx" / "token.json"


@dataclass
class Token:
    access_token: str
    expires_at: float  # epoch seconds


def load_token(path: Path) -> Optional[Token]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return Token(access_token=data["access_token"], expires_at=float(data["expires_at"]))
    except Exception:
        return None


def save_token(path: Path, tok: Token) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps({"access_token": tok.access_token, "expires_at": tok.expires_at}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def get_env(name: str) -> str:
    v = os.environ.get(name)
    if not v:
        raise SystemExit(f"Missing env var: {name}")
    return v


def fetch_token(client_id: str, client_secret: str) -> Token:
    # NOTE: requests will handle gzip automatically; Brotli requires extra packages.
    resp = requests.post(
        TOKEN_URL,
        data={
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
        },
        headers={"content-type": "application/x-www-form-urlencoded", "Accept-Encoding": "gzip"},
        timeout=30,
    )
    resp.raise_for_status()
    j = resp.json()
    access_token = j["access_token"]
    expires_in = int(j.get("expires_in", 86400))

    # Refresh a bit early.
    expires_at = time.time() + max(0, expires_in - 300)
    return Token(access_token=access_token, expires_at=expires_at)


def get_token(cache: Path) -> str:
    tok = load_token(cache)
    if tok and tok.expires_at > time.time():
        return tok.access_token

    client_id = get_env("TDX_CLIENT_ID")
    client_secret = get_env("TDX_CLIENT_SECRET")
    new_tok = fetch_token(client_id, client_secret)
    save_token(cache, new_tok)
    return new_tok.access_token


def call_api(path: str, token: str, params: Dict[str, Any]) -> Any:
    url = f"{API_BASE}{path}"
    resp = requests.get(
        url,
        headers={"authorization": f"Bearer {token}", "Accept-Encoding": "gzip"},
        params=params,
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--cache",
        default=str(default_cache_path()),
        help="Token cache file path (default: user cache dir)",
    )

    sub = ap.add_subparsers(dest="cmd", required=True)

    def add_city_cmd(name: str, api_path_fmt: str) -> None:
        sp = sub.add_parser(name)
        sp.add_argument("--city", required=True, help="City in English (e.g., NewTaipei, Taipei)")
        sp.add_argument("--top", type=int, default=5)
        sp.add_argument("--select", default=None, help="OData $select")
        sp.add_argument("--filter", dest="filter_", default=None, help="OData $filter")
        sp.set_defaults(_api_path_fmt=api_path_fmt)

    add_city_cmd("eta-city", "/v2/Bus/EstimatedTimeOfArrival/City/{city}")
    add_city_cmd("a1-city", "/v2/Bus/RealTimeByFrequency/City/{city}")
    add_city_cmd("a2-city", "/v2/Bus/RealTimeNearStop/City/{city}")

    args = ap.parse_args()
    cache = Path(args.cache)

    token = get_token(cache)

    api_path = args._api_path_fmt.format(city=args.city)
    params: Dict[str, Any] = {"$format": "JSON", "$top": args.top}

    if args.select:
        params["$select"] = args.select
    if args.filter_:
        params["$filter"] = args.filter_

    data = call_api(api_path, token, params)
    print(json.dumps(data, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
