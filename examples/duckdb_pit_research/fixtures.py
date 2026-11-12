"""Deterministic synthetic observations, late revisions and universe changes."""

from datetime import date, datetime, time, timedelta, timezone
import json
from pathlib import Path
import random

SYMBOLS = ["SYN_A", "SYN_B", "SYN_C", "SYN_D"]
SEED = 166


def stamp(day, hour, minute=0):
    return datetime.combine(
        date.fromisoformat(day), time(hour, minute), timezone.utc
    ).isoformat()


def build_fixture():
    days = [
        "2026-01-12",
        "2026-01-13",
        "2026-01-14",
        "2026-01-15",
        "2026-01-16",
        "2026-01-19",
        "2026-01-20",
    ]
    sessions = ["2026-01-08", "2026-01-09", *days[:5]]
    decisions = [
        {
            "decision_id": "D" + str(i),
            "decision_at": stamp(day, 9),
            "fill_at": stamp(day, 9, 30),
            "exit_at": stamp(days[i + 1], 9, 30),
            "split": "train_candidate" if i < 3 else "oos",
        }
        for i, day in enumerate(days[:6])
    ]
    closes = {
        "SYN_A": [10000, 10500, 10800, 10700, 11000, 10900, 11100],
        "SYN_B": [10000, 10100, 9900, 9800, 10200, 10300, 10250],
        "SYN_C": [10000, None, 10100, 10300, 10200, 10400, 10350],
        "SYN_D": [10000, 10200, 10100, 10200, 10400, 10300, 10500],
    }
    features = []
    for symbol in SYMBOLS:
        for day, close in zip(sessions, closes[symbol]):
            features.append(
                {
                    "feature_id": f"{symbol}-{day}-r0",
                    "symbol": symbol,
                    "session": day,
                    "event_at": stamp(day, 16),
                    "revision": 0,
                    "published_at": stamp(day, 16, 5),
                    "available_at": stamp(day, 16, 10),
                    "close_cents": close,
                }
            )
    # Published prices can arrive late; an exactly-at-decision row is eligible.
    next(
        f for f in features if f["symbol"] == "SYN_B" and f["session"] == "2026-01-13"
    )["available_at"] = stamp("2026-01-14", 9, 5)
    next(
        f for f in features if f["symbol"] == "SYN_A" and f["session"] == "2026-01-14"
    )["available_at"] = stamp("2026-01-15", 9)
    for symbol, day, close, available in [
        ("SYN_A", "2026-01-09", 9500, stamp("2026-01-14", 12)),
        ("SYN_B", "2026-01-12", 17000, stamp("2026-01-16", 12)),
        ("SYN_A", "2026-01-14", 13000, stamp("2026-01-19", 10)),
    ]:
        features.append(
            {
                "feature_id": f"{symbol}-{day}-r1",
                "symbol": symbol,
                "session": day,
                "event_at": stamp(day, 16),
                "revision": 1,
                "published_at": stamp(day, 17),
                "available_at": available,
                "close_cents": close,
            }
        )
    memberships = [
        {
            "membership_id": symbol + "-initial",
            "symbol": symbol,
            "effective_at": stamp("2026-01-01", 0),
            "revision": 0,
            "published_at": stamp("2026-01-01", 0),
            "available_at": stamp("2026-01-01", 0),
            "is_member": True,
        }
        for symbol in SYMBOLS[:3]
    ]
    memberships += [
        {
            "membership_id": "B-removal",
            "symbol": "SYN_B",
            "effective_at": stamp("2026-01-15", 0),
            "revision": 0,
            "published_at": stamp("2026-01-14", 18),
            "available_at": stamp("2026-01-14", 22),
            "is_member": False,
        },
        {
            "membership_id": "D-late-addition",
            "symbol": "SYN_D",
            "effective_at": stamp("2026-01-16", 0),
            "revision": 0,
            "published_at": stamp("2026-01-16", 8),
            "available_at": stamp("2026-01-16", 10),
            "is_member": True,
        },
    ]
    rng = random.Random(SEED)
    opens = []
    bases = {
        "SYN_A": [10100, 10300, 10000, 10400, 9900, 10050, 9850],
        "SYN_B": [9800, 9600, 9750, 9900, 9700, 9650, 9800],
        "SYN_C": [10000, 9950, 10100, 10050, 10200, 10100, 10300],
        "SYN_D": [10500, 10300, 10600, 10200, 10400, 10300, 10100],
    }
    for symbol in SYMBOLS:
        for day, value in zip(days, bases[symbol]):
            opens.append(
                {
                    "symbol": symbol,
                    "event_at": stamp(day, 9, 30),
                    "available_at": stamp(day, 9, 31),
                    "open_cents": value + rng.randint(-20, 20),
                }
            )
    return {
        "schema_version": 1,
        "seed": SEED,
        "data_class": "SYNTHETIC_ONLY",
        "symbols": SYMBOLS,
        "evaluation_at": stamp("2026-01-21", 12),
        "decisions": decisions,
        "features": features,
        "memberships": memberships,
        "opens": opens,
    }


if __name__ == "__main__":
    path = Path(__file__).parent / "fixtures/synthetic_v1.json"
    path.parent.mkdir(exist_ok=True)
    if path.exists():
        raise SystemExit(
            "Fixture exists; compare a regenerated object instead of overwriting frozen input"
        )
    path.write_text(
        json.dumps(build_fixture(), indent=2) + "\n", encoding="utf-8", newline="\n"
    )
