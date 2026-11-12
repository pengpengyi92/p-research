"""Independent stdlib information-set reference and bounded research accounting."""

from datetime import datetime, timedelta, timezone
import hashlib
import json
import math


class ContractError(ValueError):
    pass


class EquivalenceError(AssertionError):
    pass


def instant(value):
    if not isinstance(value, str):
        raise ContractError("timestamp must be an ISO string")
    try:
        result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ContractError("invalid timestamp") from exc
    if result.tzinfo is None:
        raise ContractError("timezone-aware timestamp required")
    return result.astimezone(timezone.utc)


def normalized(value):
    return instant(value).isoformat()


def canonical_bytes(data):
    return (
        json.dumps(data, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n"
    ).encode("utf-8")


def fingerprint(data):
    return hashlib.sha256(canonical_bytes(data)).hexdigest()


def validate(data):
    expected = {
        "schema_version",
        "seed",
        "data_class",
        "symbols",
        "evaluation_at",
        "decisions",
        "features",
        "memberships",
        "opens",
    }
    if (
        not isinstance(data, dict)
        or set(data) != expected
        or type(data["schema_version"]) is not int
        or data["schema_version"] != 1
        or data["data_class"] != "SYNTHETIC_ONLY"
    ):
        raise ContractError("unsupported fixture schema/data class")
    if type(data["seed"]) is not int or data["seed"] < 0:
        raise ContractError("nonnegative integer seed required")
    symbols = data["symbols"]
    if (
        not isinstance(symbols, list)
        or not symbols
        or any(not isinstance(s, str) or not s.startswith("SYN_") for s in symbols)
        or len(set(symbols)) != len(symbols)
    ):
        raise ContractError("unique synthetic symbols required")
    evaluation = instant(data["evaluation_at"])
    fields = {
        "decisions": {"decision_id", "decision_at", "fill_at", "exit_at", "split"},
        "features": {
            "feature_id",
            "symbol",
            "session",
            "event_at",
            "revision",
            "published_at",
            "available_at",
            "close_cents",
        },
        "memberships": {
            "membership_id",
            "symbol",
            "effective_at",
            "revision",
            "published_at",
            "available_at",
            "is_member",
        },
        "opens": {"symbol", "event_at", "available_at", "open_cents"},
    }
    for table, columns in fields.items():
        if not isinstance(data[table], list) or not data[table]:
            raise ContractError("missing/empty input table: " + table)
        keys, ids = set(), set()
        for row in data[table]:
            if not isinstance(row, dict) or set(row) != columns:
                raise ContractError("missing/unknown fields in " + table)
            if table == "decisions":
                key = row["decision_id"]
                if not isinstance(key, str) or not key:
                    raise ContractError("nonempty decision id required")
                if row["split"] not in {"train_candidate", "oos"}:
                    raise ContractError("unknown split")
                if (
                    not instant(row["decision_at"])
                    < instant(row["fill_at"])
                    < instant(row["exit_at"])
                    <= evaluation
                ):
                    raise ContractError("decision < fill < exit <= evaluation required")
            else:
                if row["symbol"] not in symbols:
                    raise ContractError("unknown symbol")
                event = "effective_at" if table == "memberships" else "event_at"
                instant(row[event])
                if table == "opens":
                    key = (row["symbol"], normalized(row["event_at"]))
                else:
                    if type(row["revision"]) is not int or row["revision"] < 0:
                        raise ContractError("nonnegative integer revision required")
                    key = (
                        row["symbol"],
                        (
                            row["session"]
                            if table == "features"
                            else normalized(row["effective_at"])
                        ),
                        row["revision"],
                    )
                    identity = (
                        row["feature_id"]
                        if table == "features"
                        else row["membership_id"]
                    )
                    if not isinstance(identity, str) or not identity or identity in ids:
                        raise ContractError("duplicate/empty record id")
                    ids.add(identity)
                available = instant(row["available_at"])
                if table != "memberships" and instant(row[event]) > available:
                    raise ContractError("observation available before event")
                if table != "opens":
                    published = instant(row["published_at"])
                    if published > available or (
                        table == "features" and instant(row["event_at"]) > published
                    ):
                        raise ContractError("event/publication/availability order")
                if table == "memberships":
                    if type(row["is_member"]) is not bool:
                        raise ContractError("boolean membership required")
                else:
                    value = (
                        row["close_cents"] if table == "features" else row["open_cents"]
                    )
                    if not (table == "features" and value is None) and (
                        type(value) is not int or not 0 < value <= 10**12
                    ):
                        raise ContractError(
                            "positive integer price cents or explicit missing close required"
                        )
                    if (
                        table == "features"
                        and instant(row["event_at"]).date().isoformat()
                        != row["session"]
                    ):
                        raise ContractError("session/event date mismatch")
            if key in keys:
                raise ContractError("duplicate key in " + table)
            keys.add(key)
    for table, event in [("features", "session"), ("memberships", "effective_at")]:
        groups = {}
        for row in data[table]:
            logical_event = (
                row[event] if table == "features" else normalized(row[event])
            )
            groups.setdefault((row["symbol"], logical_event), []).append(row)
        for rows in groups.values():
            ordered = sorted(rows, key=lambda r: r["revision"])
            arrivals = [instant(r["available_at"]) for r in ordered]
            if arrivals != sorted(arrivals):
                raise ContractError("revision availability must not go backwards")
    ordered_decisions = sorted(
        data["decisions"], key=lambda d: instant(d["decision_at"])
    )
    if len({instant(d["decision_at"]) for d in ordered_decisions}) != len(
        ordered_decisions
    ):
        raise ContractError("duplicate decision timestamp")
    return data


def python_snapshots(data):
    validate(data)
    result = []
    for d in sorted(data["decisions"], key=lambda r: r["decision_id"]):
        cutoff = instant(d["decision_at"])
        for symbol in sorted(data["symbols"]):
            member_rows = [
                m
                for m in data["memberships"]
                if m["symbol"] == symbol
                and instant(m["effective_at"]) <= cutoff
                and instant(m["available_at"]) <= cutoff
            ]
            if not member_rows:
                continue
            member = max(
                member_rows, key=lambda m: (instant(m["effective_at"]), m["revision"])
            )
            if not member["is_member"]:
                continue
            by_session = {}
            for f in data["features"]:
                if (
                    f["symbol"] != symbol
                    or instant(f["event_at"]) > cutoff
                    or instant(f["available_at"]) > cutoff
                ):
                    continue
                previous = by_session.get(f["session"])
                if previous is None or f["revision"] > previous["revision"]:
                    by_session[f["session"]] = f
            history = sorted(
                by_session.values(), key=lambda f: f["session"], reverse=True
            )
            current, previous = (history + [None, None])[:2]
            row = {
                "decision_id": d["decision_id"],
                "symbol": symbol,
                "membership_id": member["membership_id"],
                "decision_at": normalized(d["decision_at"]),
            }
            for prefix, record in [("current", current), ("previous", previous)]:
                row[prefix + "_id"] = record["feature_id"] if record else None
                row[prefix + "_close_cents"] = record["close_cents"] if record else None
                row[prefix + "_available_at"] = (
                    normalized(record["available_at"]) if record else None
                )
            a, b = row["current_close_cents"], row["previous_close_cents"]
            row["status"] = (
                "INSUFFICIENT_HISTORY"
                if previous is None
                else "MISSING_VALUE" if a is None or b is None else "READY"
            )
            row["signal"] = (a - b) / b if row["status"] == "READY" else None
            result.append(row)
    return result


def python_labels(data):
    validate(data)
    prices = {(row["symbol"], instant(row["event_at"])): row for row in data["opens"]}
    result = []
    for d in sorted(data["decisions"], key=lambda row: row["decision_id"]):
        for symbol in sorted(data["symbols"]):
            entry = prices.get((symbol, instant(d["fill_at"])))
            exit_row = prices.get((symbol, instant(d["exit_at"])))
            known = (
                entry is not None
                and exit_row is not None
                and max(
                    instant(entry["available_at"]), instant(exit_row["available_at"])
                )
                <= instant(data["evaluation_at"])
            )
            value = (
                (exit_row["open_cents"] - entry["open_cents"]) / entry["open_cents"]
                if known
                else None
            )
            result.append(
                {
                    "decision_id": d["decision_id"],
                    "symbol": symbol,
                    "forward_return": value,
                }
            )
    return result


def assert_equal(expected, actual, tolerance=1e-12):
    if len(expected) != len(actual):
        raise EquivalenceError("row count differs")
    for index, (a, b) in enumerate(zip(expected, actual)):
        if a.keys() != b.keys():
            raise EquivalenceError("schema differs")
        for key in a:
            left, right = a[key], b[key]
            same = (
                math.isclose(left, right, rel_tol=tolerance, abs_tol=tolerance)
                if isinstance(left, float) and isinstance(right, float)
                else left == right
            )
            if not same:
                raise EquivalenceError(
                    f"row {index} field {key} differs: {left!r} != {right!r}"
                )


def audit_provenance(data, rows):
    decisions = {d["decision_id"]: d for d in data["decisions"]}
    features = {f["feature_id"]: f for f in data["features"]}
    memberships = {m["membership_id"]: m for m in data["memberships"]}
    for row in rows:
        cutoff = instant(decisions[row["decision_id"]]["decision_at"])
        member = memberships[row["membership_id"]]
        if (
            instant(member["available_at"]) > cutoff
            or instant(member["effective_at"]) > cutoff
        ):
            raise ContractError("future membership used")
        for name in ("current_id", "previous_id"):
            if row[name] is not None:
                f = features[row[name]]
                if (
                    not instant(f["event_at"])
                    <= instant(f["published_at"])
                    <= instant(f["available_at"])
                    <= cutoff
                ):
                    raise ContractError("future feature used")


def split_plan(data, embargo_minutes=60):
    if type(embargo_minutes) is not int or embargo_minutes < 0:
        raise ContractError("nonnegative integer embargo required")
    test = [d for d in data["decisions"] if d["split"] == "oos"]
    if not test:
        raise ContractError("OOS decisions required")
    first = min(instant(d["decision_at"]) for d in test)
    train, purged = [], []
    for d in data["decisions"]:
        if d["split"] == "train_candidate":
            target = (
                train
                if instant(d["exit_at"]) + timedelta(minutes=embargo_minutes) < first
                else purged
            )
            target.append(d["decision_id"])
    return {
        "train": sorted(train),
        "purged": sorted(purged),
        "oos": sorted(d["decision_id"] for d in test),
        "embargo_minutes": embargo_minutes,
        "fitted_parameters": False,
    }


def evaluate(data, snapshots, labels, cost_bps_per_side=7.0):
    if not math.isfinite(cost_bps_per_side) or cost_bps_per_side < 0:
        raise ContractError("finite nonnegative cost required")
    label_map = {(r["decision_id"], r["symbol"]): r["forward_return"] for r in labels}
    plan = split_plan(data)
    result = {}
    for policy in ("positive_top1", "equal_weight_ready", "cash"):
        daily, equity, peak = [], 1.0, 1.0
        for d in sorted(data["decisions"], key=lambda r: instant(r["decision_at"])):
            ready = [
                r
                for r in snapshots
                if r["decision_id"] == d["decision_id"] and r["status"] == "READY"
            ]
            if policy == "positive_top1":
                chosen = sorted(
                    [r for r in ready if r["signal"] > 0],
                    key=lambda r: (-r["signal"], r["symbol"]),
                )[:1]
            elif policy == "equal_weight_ready":
                chosen = ready
            else:
                chosen = []
            weights = {r["symbol"]: 1 / len(chosen) for r in chosen}
            missing = any(
                label_map.get((d["decision_id"], symbol)) is None for symbol in weights
            )
            gross = (
                None
                if missing
                else sum(
                    weight * label_map[(d["decision_id"], symbol)]
                    for symbol, weight in weights.items()
                )
            )
            turnover = 2 * sum(abs(w) for w in weights.values())
            costs = turnover * cost_bps_per_side / 10000
            net = None if gross is None else gross - costs
            if net is not None and net <= -1:
                raise ContractError(
                    "nonpositive NAV/bankruptcy modeling is not supported"
                )
            # No equity statistic is returned across an unpriced day.
            equity = None if net is None or equity is None else equity * (1 + net)
            peak = max(peak, equity) if equity is not None else peak
            daily.append(
                {
                    "decision_id": d["decision_id"],
                    "split": (
                        "purged"
                        if d["decision_id"] in plan["purged"]
                        else "oos" if d["decision_id"] in plan["oos"] else "train"
                    ),
                    "weights": weights,
                    "gross_exposure": sum(abs(w) for w in weights.values()),
                    "net_exposure": sum(weights.values()),
                    "round_trip_turnover": turnover,
                    "gross_return": gross,
                    "cost_return": costs,
                    "net_return": net,
                    "status": "MISSING_LABEL" if missing else "PRICED",
                    "diagnostic_equity": equity,
                    "diagnostic_drawdown": (
                        equity / peak - 1 if equity is not None else None
                    ),
                }
            )
        oos = [r for r in daily if r["split"] == "oos"]
        oos_equity = 1.0
        for row in oos:
            oos_equity = (
                None
                if row["net_return"] is None or oos_equity is None
                else oos_equity * (1 + row["net_return"])
            )
        result[policy] = {
            "daily": daily,
            "oos_observations": len(oos),
            "oos_net_return": oos_equity - 1 if oos_equity is not None else None,
            "annualized_sharpe": None,
            "sharpe_status": "NOT_IDENTIFIABLE_TINY_SYNTHETIC_SAMPLE",
        }
    return result
