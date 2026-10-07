#!/usr/bin/env python3
"""Null-test for capstone candidate B: engine-vs-broker divergence → Telegram, in seconds.

Zero changes to the engine. Tails Narviko's log files for the divergence lines the engine
already writes (reconciler drift, ledger/books mismatch, day-P&L divergence, attribution
divergence, any CRITICAL) and posts each NEW one to Telegram, deduplicated. Also pages if the
engine's loopback API stops answering during market hours.

Usage:
    python3 null_test_parity.py --repo ~/Kite_Connect_Claude --dry-run     # print, do not send
    python3 null_test_parity.py --repo ~/Kite_Connect_Claude --once        # one pass (cron */1)
    python3 null_test_parity.py --repo ~/Kite_Connect_Claude               # loop every 30 s

Telegram credentials are read from the repo's .env (NOTIFY_TELEGRAM_BOT_TOKEN,
NOTIFY_TELEGRAM_CHAT_ID) or the environment. Nothing is written except the state file.

If this script is enough — divergence reaches the phone within a minute — then candidate B is
a skill plus a connector, not a product. That is the verdict it exists to produce.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

PATTERNS = [
    re.compile(r"\[RECON drift\]"),
    re.compile(r"\[RECON delta\]"),
    re.compile(r"LEDGER.{0,3}BOOKS MISMATCH"),
    re.compile(r"DAY-PNL DIVERGENCE"),
    re.compile(r"ATTRIBUTION DIVERGENCE"),
    re.compile(r"P&L BOOK DIVERGENCE"),
    re.compile(r"POSITION IS UNPROTECTED"),
    re.compile(r"\bCRITICAL\b"),
]
IGNORE = [
    # Known boot-time noise the owner has already triaged (STATUS 2026-08-28). Extend as needed.
    re.compile(r"DAY GUARD RE-ARMED"),
    re.compile(r"TOKEN WATCHDOG"),
]
IST = dt.timezone(dt.timedelta(hours=5, minutes=30))


def market_open(now: dt.datetime) -> bool:
    t = now.astimezone(IST)
    if t.weekday() >= 5:
        return False
    hm = t.hour * 60 + t.minute
    return 9 * 60 + 10 <= hm <= 15 * 60 + 45


def load_env(repo: Path) -> dict:
    env = dict(os.environ)
    envfile = repo / ".env"
    if envfile.exists():
        for line in envfile.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env.setdefault(k.strip(), v.strip().strip('"').strip("'"))
    return env


def telegram(env: dict, text: str, dry: bool) -> bool:
    if dry:
        print(f"[dry-run] TELEGRAM: {text}")
        return True
    token, chat = env.get("NOTIFY_TELEGRAM_BOT_TOKEN"), env.get("NOTIFY_TELEGRAM_CHAT_ID")
    if not token or not chat:
        print("no NOTIFY_TELEGRAM_BOT_TOKEN / NOTIFY_TELEGRAM_CHAT_ID — cannot page", file=sys.stderr)
        return False
    data = urllib.parse.urlencode({"chat_id": chat, "text": text[:3900]}).encode()
    req = urllib.request.Request(f"https://api.telegram.org/bot{token}/sendMessage", data=data)
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.status == 200
    except (urllib.error.URLError, OSError) as e:
        print(f"telegram send failed: {e}", file=sys.stderr)
        return False


def engine_alive(base: str) -> tuple[bool, str]:
    try:
        with urllib.request.urlopen(f"{base}/api/snapshot", timeout=5) as r:
            return r.status == 200, f"HTTP {r.status}"
    except (urllib.error.URLError, OSError) as e:
        return False, str(e)


def tail_new(path: Path, state: dict) -> list[str]:
    """Return lines appended since last pass; handles rotation by size regression."""
    key = str(path)
    if not path.exists():
        return []
    size = path.stat().st_size
    pos = state.get(key, size)  # first run: start at the end, do not replay history
    if size < pos:
        pos = 0  # rotated
    with path.open("rb") as f:
        f.seek(pos)
        chunk = f.read()
    state[key] = pos + len(chunk)
    return chunk.decode("utf-8", errors="replace").splitlines()


def matches(line: str) -> bool:
    if any(p.search(line) for p in IGNORE):
        return False
    return any(p.search(line) for p in PATTERNS)


def fingerprint(line: str) -> str:
    # Strip timestamps and volatile numbers so the same incident does not re-page every 3 s.
    core = re.sub(r"\d[\d:.,\-T+]*", "#", line)
    return hashlib.sha1(core.encode()).hexdigest()[:16]


def one_pass(repo: Path, base: str, state: dict, env: dict, dry: bool, dedup_s: int) -> int:
    now = dt.datetime.now(dt.timezone.utc)
    ts = now.astimezone(IST).strftime("%H:%M:%S")
    sent = 0
    seen: dict = state.setdefault("seen", {})

    if market_open(now):
        ok, why = engine_alive(base)
        if not ok and not state.get("engine_down"):
            telegram(env, f"🔴 {ts} ENGINE UNREACHABLE at {base}: {why}", dry)
            sent += 1
        if ok and state.get("engine_down"):
            telegram(env, f"🟢 {ts} engine reachable again", dry)
        state["engine_down"] = not ok

    for name in ("logs/errors.log", "logs/trading.log"):
        for line in tail_new(repo / name, state):
            if not matches(line):
                continue
            fp = fingerprint(line)
            last = seen.get(fp, 0)
            if now.timestamp() - last < dedup_s:
                continue
            seen[fp] = now.timestamp()
            if telegram(env, f"⚠ {ts} {name}: {line.strip()[:600]}", dry):
                sent += 1
    # keep the dedup map small
    cutoff = now.timestamp() - 24 * 3600
    for k in [k for k, v in seen.items() if v < cutoff]:
        del seen[k]
    return sent


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", required=True, help="Narviko checkout (reads logs/ and .env)")
    ap.add_argument("--base", default="http://127.0.0.1:8080", help="engine loopback base URL")
    ap.add_argument("--state", default=None, help="state file (default: <repo>/data/null_test_parity.json)")
    ap.add_argument("--interval", type=int, default=30)
    ap.add_argument("--dedup", type=int, default=1800, help="seconds before the same incident re-pages")
    ap.add_argument("--once", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    repo = Path(a.repo).expanduser().resolve()
    state_path = Path(a.state) if a.state else repo / "data" / "null_test_parity.json"
    state = json.loads(state_path.read_text()) if state_path.exists() else {}
    env = load_env(repo)

    def save():
        state_path.parent.mkdir(parents=True, exist_ok=True)
        state_path.write_text(json.dumps(state))

    if a.once:
        n = one_pass(repo, a.base, state, env, a.dry_run, a.dedup)
        save()
        print(f"pass done, {n} page(s)")
        return 0
    print(f"watching {repo} every {a.interval}s; dry_run={a.dry_run}")
    while True:
        try:
            one_pass(repo, a.base, state, env, a.dry_run, a.dedup)
            save()
        except Exception as e:  # never die silently — a dead watcher is the failure mode
            print(f"pass error: {e}", file=sys.stderr)
        time.sleep(a.interval)


if __name__ == "__main__":
    sys.exit(main())
