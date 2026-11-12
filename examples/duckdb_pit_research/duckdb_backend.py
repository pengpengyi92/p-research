"""Optional DuckDB execution; no pandas, remote scans, extensions or services."""

from datetime import datetime
from pathlib import Path

from .model import ContractError, instant, normalized, validate

SQL = Path(__file__).parent / "sql"
MUTATIONS = (
    "event_time_only",
    "published_only",
    "global_latest_before_asof",
    "future_membership",
    "latest_arrival",
)


def connect(data):
    validate(data)
    try:
        import duckdb
    except ImportError as exc:
        raise RuntimeError(
            "Optional example requires: pip install -r examples/duckdb_pit_research/requirements.txt"
        ) from exc
    con = duckdb.connect(
        ":memory:",
        config={"threads": 1, "memory_limit": "128MB", "enable_external_access": False},
    )
    try:
        con.execute("SET TimeZone='UTC'")
        con.execute(
            "CREATE TABLE decisions(decision_id VARCHAR, decision_at TIMESTAMPTZ, fill_at TIMESTAMPTZ, exit_at TIMESTAMPTZ)"
        )
        con.executemany(
            "INSERT INTO decisions VALUES (?, ?, ?, ?)",
            [
                (
                    d["decision_id"],
                    instant(d["decision_at"]),
                    instant(d["fill_at"]),
                    instant(d["exit_at"]),
                )
                for d in data["decisions"]
            ],
        )
        con.execute(
            "CREATE TABLE memberships(membership_id VARCHAR, symbol VARCHAR, effective_at TIMESTAMPTZ, revision INTEGER, published_at TIMESTAMPTZ, available_at TIMESTAMPTZ, is_member BOOLEAN)"
        )
        con.executemany(
            "INSERT INTO memberships VALUES (?, ?, ?, ?, ?, ?, ?)",
            [
                (
                    m["membership_id"],
                    m["symbol"],
                    instant(m["effective_at"]),
                    m["revision"],
                    instant(m["published_at"]),
                    instant(m["available_at"]),
                    m["is_member"],
                )
                for m in data["memberships"]
            ],
        )
        con.execute(
            "CREATE TABLE features(feature_id VARCHAR, symbol VARCHAR, session DATE, event_at TIMESTAMPTZ, revision INTEGER, published_at TIMESTAMPTZ, available_at TIMESTAMPTZ, close_cents BIGINT)"
        )
        con.executemany(
            "INSERT INTO features VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            [
                (
                    f["feature_id"],
                    f["symbol"],
                    f["session"],
                    instant(f["event_at"]),
                    f["revision"],
                    instant(f["published_at"]),
                    instant(f["available_at"]),
                    f["close_cents"],
                )
                for f in data["features"]
            ],
        )
        con.execute(
            "CREATE TABLE market_opens(symbol VARCHAR, event_at TIMESTAMPTZ, available_at TIMESTAMPTZ, open_cents BIGINT)"
        )
        con.executemany(
            "INSERT INTO market_opens VALUES (?, ?, ?, ?)",
            [
                (
                    m["symbol"],
                    instant(m["event_at"]),
                    instant(m["available_at"]),
                    m["open_cents"],
                )
                for m in data["opens"]
            ],
        )
        con.execute("CREATE TABLE symbols(symbol VARCHAR)")
        con.executemany(
            "INSERT INTO symbols VALUES (?)", [(s,) for s in data["symbols"]]
        )
        return con
    except Exception:
        con.close()
        raise


def records(cursor):
    columns = [c[0] for c in cursor.description]
    return [
        {
            name: (
                normalized(value)
                if name.endswith("_at") and isinstance(value, str)
                else value.isoformat() if isinstance(value, datetime) else value
            )
            for name, value in zip(columns, row)
        }
        for row in cursor.fetchall()
    ]


def snapshots(data, mutation=None):
    if mutation is not None and mutation not in MUTATIONS:
        raise ContractError("unknown diagnostic mutation")
    feature_guard = (
        "f.published_at <= a.decision_at AND f.available_at <= a.decision_at"
    )
    if mutation == "event_time_only":
        feature_guard = "TRUE"
    elif mutation == "published_only":
        feature_guard = "f.published_at <= a.decision_at"
    source = "features"
    if mutation == "global_latest_before_asof":
        source = "(SELECT * FROM features QUALIFY row_number() OVER (PARTITION BY symbol, session ORDER BY revision DESC) = 1)"
    query = (SQL / "snapshots.sql").read_text(encoding="utf-8")
    query = query.replace("__FEATURE_GUARD__", feature_guard).replace(
        "__FEATURE_TABLE__", source
    )
    query = query.replace(
        "__MEMBERSHIP_GUARD__",
        (
            "TRUE"
            if mutation == "future_membership"
            else "m.available_at <= d.decision_at"
        ),
    )
    query = query.replace(
        "__SESSION_ORDER__",
        (
            "available_at DESC NULLS LAST, session DESC"
            if mutation == "latest_arrival"
            else "session DESC NULLS LAST"
        ),
    )
    with connect(data) as con:
        return records(con.execute(query))


def labels(data):
    with connect(data) as con:
        return records(
            con.execute(
                (SQL / "labels.sql").read_text(encoding="utf-8"),
                [instant(data["evaluation_at"])] * 2,
            )
        )
