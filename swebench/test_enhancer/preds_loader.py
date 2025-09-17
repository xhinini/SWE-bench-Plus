import json
from pathlib import Path
from typing import Dict, List

from swebench.harness.constants import KEY_INSTANCE_ID, KEY_MODEL, KEY_PREDICTION


def _normalize_rec(raw: dict, fallback_model_name: str) -> dict:
    rec: Dict = dict(raw)
    # Map task_id -> instance_id if needed
    if KEY_INSTANCE_ID not in rec:
        if "task_id" in rec:
            rec[KEY_INSTANCE_ID] = rec.pop("task_id")
        else:
            raise ValueError("Prediction record missing instance_id/task_id")
    # Ensure model_patch key is present (map patch -> model_patch if necessary)
    if KEY_PREDICTION not in rec:
        if "patch" in rec:
            rec[KEY_PREDICTION] = rec.pop("patch")
        else:
            # allow empty but present
            rec[KEY_PREDICTION] = raw.get(KEY_PREDICTION, "")
    # Normalize model name field
    if KEY_MODEL not in rec:
        if "model" in rec:
            rec[KEY_MODEL] = rec["model"]
        else:
            rec[KEY_MODEL] = fallback_model_name
    return rec


essential_keys = [KEY_INSTANCE_ID, KEY_PREDICTION]


def load_predictions_lenient(predictions_path: str) -> List[Dict]:
    """Load predictions from .json or .jsonl and normalize to harness keys.

    - Accepts either `instance_id` or `task_id` and maps to `instance_id`.
    - Accepts either `model_patch` or `patch` and maps to `model_patch`.
    - Adds `model_name_or_path` if missing (from provided filename stem or `model`).
    """
    path = Path(predictions_path)
    stem = path.stem
    if predictions_path.endswith(".json"):
        rows = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(rows, dict):
            rows = list(rows.values())
        if not isinstance(rows, list):
            raise ValueError("Predictions must be a list or a dict mapping instance_id to record")
    elif predictions_path.endswith(".jsonl"):
        rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    else:
        raise ValueError("Predictions path must be .json or .jsonl")

    out: List[Dict] = []
    for raw in rows:
        rec = _normalize_rec(raw, stem)
        # Validate essential keys
        for k in essential_keys:
            if k not in rec:
                raise ValueError(f"Prediction missing required key: {k}")
        out.append(rec)
    return out
