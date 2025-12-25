import os
import json
from pathlib import Path
from typing import Iterable, Dict, Any

BASE = Path(__file__).resolve().parents[2] / "data"


def ensure_parent(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)


def write_jsonl(path: Path, items: Iterable[Dict[str, Any]]):
    ensure_parent(path)
    with path.open("w", encoding="utf-8") as f:
        for item in items:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")


def write_placeholder_zero(path: Path):
    ensure_parent(path)
    with path.open("w", encoding="utf-8") as f:
        f.write("")
