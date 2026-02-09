#!/usr/bin/env python3
import json
import csv
import subprocess
from datetime import datetime, timezone
from typing import Optional

FTL_DB = "/etc/pihole/pihole-FTL.db"
GRAVITY_DB = "/etc/pihole/gravity.db"


BLOCKED_STATUSES = (3,)


def _run_sqlite(db_path: str, sql: str) -> str:
    return subprocess.check_output(
        ["sudo", "sqlite3", db_path, "-cmd", ".timeout 2000", sql],
        text=True
    ).strip()


def q_ftl(sql: str) -> str:
    return _run_sqlite(FTL_DB, sql)


def q_gravity(sql: str) -> str:
    return _run_sqlite(GRAVITY_DB, sql)


def safe_int(x) -> Optional[int]:
    try:
        return int(x)
    except Exception:
        return None


def domains_being_blocked() -> Optional[int]:
    try:
        return safe_int(q_gravity("SELECT COUNT(*) FROM gravity;"))
    except Exception:
        return None


def count_today_total() -> Optional[int]:
    try:
        return safe_int(q_ftl("""
SELECT COUNT(*)
FROM queries
WHERE timestamp >= strftime('%s','now','localtime','start of day');
"""))
    except Exception:
        return None


def count_today_blocked() -> Optional[int]:
    try:
        status_list = ",".join(str(s) for s in BLOCKED_STATUSES)
        return safe_int(q_ftl(f"""
SELECT COUNT(*)
FROM queries
WHERE timestamp >= strftime('%s','now','localtime','start of day')
  AND status IN ({status_list});
"""))
    except Exception:
        return None


def count_distinct_today(col: str) -> Optional[int]:
    try:
        return safe_int(q_ftl(f"""
SELECT COUNT(DISTINCT {col})
FROM queries
WHERE timestamp >= strftime('%s','now','localtime','start of day');
"""))
    except Exception:
        return None


def main():
    ts = datetime.now(timezone.utc).isoformat()

    dns_queries_today = count_today_total()
    ads_blocked_today = count_today_blocked()

    unique_clients = count_distinct_today("client")
    unique_domains = count_distinct_today("domain")

    ads_percentage_today = None
    if dns_queries_today is not None and dns_queries_today > 0 and ads_blocked_today is not None:
        ads_percentage_today = (ads_blocked_today / dns_queries_today) * 100.0

    out = {
        "timestamp": ts,
        "source": "ftl_db(queries_table)+gravity_db",
        "domains_being_blocked": domains_being_blocked(),
        "dns_queries_today": dns_queries_today,
        "ads_blocked_today": ads_blocked_today,
        "ads_percentage_today": ads_percentage_today,
        "unique_domains": unique_domains,
        "unique_clients": unique_clients,
        "blocked_statuses_used": list(BLOCKED_STATUSES),
    }

    with open("dns_stats.json", "w") as f:
        json.dump(out, f, indent=2)

    csv_file = "dns_stats.csv"
    fieldnames = list(out.keys())

    write_header = False
    try:
        with open(csv_file, "r") as _:
            pass
    except FileNotFoundError:
        write_header = True

    with open(csv_file, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        if write_header:
            w.writeheader()
        w.writerow(out)

    print("OK: wrote dns_stats.json and appended dns_stats.csv")


if __name__ == "__main__":
    main()
