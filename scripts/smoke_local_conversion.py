from __future__ import annotations

import argparse
import json
import mimetypes
from datetime import datetime, timezone
from pathlib import Path

import httpx


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a dev-only local smoke conversion against Gotenberg."
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to a local .doc/.docx sample used for smoke testing.",
    )
    parser.add_argument(
        "--gotenberg-url",
        default="http://localhost:3000",
        help="Base URL of the local Gotenberg instance.",
    )
    parser.add_argument(
        "--output-dir",
        default=(
            "work/roadmap/campaigns/"
            "CAM-2026-03-16-GOTENBERG-CONVERTER-MVP-V1/evidence/output"
        ),
        help="Directory where the generated PDF will be written.",
    )
    parser.add_argument(
        "--evidence-file",
        default=(
            "work/roadmap/campaigns/"
            "CAM-2026-03-16-GOTENBERG-CONVERTER-MVP-V1/evidence/latest-run.json"
        ),
        help="JSON file where run evidence will be captured.",
    )
    parser.add_argument(
        "--timeout-sec",
        type=int,
        default=120,
        help="HTTP timeout in seconds for the Gotenberg request.",
    )
    return parser.parse_args()


def build_output_path(output_dir: Path, input_path: Path) -> Path:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    stem = input_path.stem.replace(" ", "_")
    return output_dir / f"{stem}-{timestamp}.pdf"


def main() -> int:
    args = parse_args()
    input_path = Path(args.input).resolve()
    output_dir = Path(args.output_dir).resolve()
    evidence_path = Path(args.evidence_file).resolve()

    if not input_path.exists():
        raise SystemExit(f"Input file not found: {input_path}")

    output_dir.mkdir(parents=True, exist_ok=True)
    evidence_path.parent.mkdir(parents=True, exist_ok=True)
    output_path = build_output_path(output_dir, input_path)

    mime_type = mimetypes.guess_type(input_path.name)[0] or "application/octet-stream"
    evidence: dict[str, object] = {
        "run_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_filename": input_path.name,
        "source_path": str(input_path),
        "gotenberg_url": args.gotenberg_url.rstrip("/"),
        "output_path": str(output_path),
        "status": "failed",
        "output_size_bytes": None,
        "error": None,
        "manual_review": {
            "status": "pending",
            "caveats": "",
        },
        "notes": (
            "Temporary local proof sample. Replace with a safe anonymized fixture "
            "or documented local sample workflow before stabilizing test/docs flow."
        ),
    }

    try:
        with input_path.open("rb") as input_file, httpx.Client(
            timeout=args.timeout_sec,
            trust_env=False,
        ) as client:
            response = client.post(
                f"{args.gotenberg_url.rstrip('/')}/forms/libreoffice/convert",
                files={"files": (input_path.name, input_file, mime_type)},
            )
            response.raise_for_status()

        output_path.write_bytes(response.content)
        evidence["status"] = "ready"
        evidence["output_size_bytes"] = output_path.stat().st_size
    except Exception as exc:  # pragma: no cover - manual smoke helper
        evidence["error"] = str(exc)

    evidence_path.write_text(json.dumps(evidence, indent=2), encoding="utf-8")
    print(json.dumps(evidence, indent=2))
    return 0 if evidence["status"] == "ready" else 1


if __name__ == "__main__":
    raise SystemExit(main())
