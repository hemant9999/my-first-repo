import json
from datetime import UTC, datetime
from pathlib import Path


def write_json_report(report: dict, output_dir: Path, prefix: str) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    path = output_dir / f"{prefix}_{timestamp}.json"
    with path.open("w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2)
    return path
