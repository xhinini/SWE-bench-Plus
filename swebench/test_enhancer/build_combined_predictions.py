import json
import os
from pathlib import Path
from typing import Dict, List, Set

from swebench.harness.constants import (
    KEY_INSTANCE_ID,
    KEY_MODEL,
    KEY_PREDICTION,
    TESTENHANCER_LOG_DIR,
)
from swebench.harness.utils import get_predictions_from_file, load_swebench_dataset
from swebench.test_enhancer.preds_loader import load_predictions_lenient


def read_latest_llm_test_patch(run_id: str, instance_id: str) -> str | None:
    """Find the latest iteration's new_test_patch.diff for an instance and return its text."""
    base = TESTENHANCER_LOG_DIR / run_id / instance_id
    if not base.exists():
        return None
    # Find numeric iteration subdirectories
    iters: List[int] = []
    for p in base.iterdir():
        if p.is_dir() and p.name.isdigit():
            iters.append(int(p.name))
    if not iters:
        return None
    latest = base / str(max(iters)) / "new_test_patch.diff"
    if latest.exists():
        text = latest.read_text(encoding="utf-8")
        return text if text.strip() else None
    return None


def concat_patches(*patches: str) -> str:
    parts: List[str] = []
    for p in patches:
        if not p:
            continue
        s = p
        if not s.endswith("\n"):
            s += "\n"
        parts.append(s)
    return "".join(parts)


def make_gold_with_llm(
    dataset_name: str,
    split: str,
    selected_ids: Set[str],
    run_id: str,
    out_path: Path,
):
    # Load gold predictions from dataset
    gold_preds = get_predictions_from_file("gold", dataset_name, split)
    gold_map = {p[KEY_INSTANCE_ID]: p for p in gold_preds}

    with out_path.open("w", encoding="utf-8") as f:
        cnt = 0
        for iid in selected_ids:
            if iid not in gold_map:
                continue
            gold_patch = gold_map[iid][KEY_PREDICTION]
            llm_patch = read_latest_llm_test_patch(run_id, iid)
            if not llm_patch:
                continue
            combined = concat_patches(gold_patch, llm_patch)
            rec = {
                KEY_INSTANCE_ID: iid,
                KEY_PREDICTION: combined,
                KEY_MODEL: "gold+llm",
            }
            f.write(json.dumps(rec) + "\n")
            cnt += 1
    print(f"Wrote gold+llm predictions to {out_path}")


def make_model_with_llm(
    dataset_name: str,
    split: str,
    predictions_path: str,
    selected_ids: Set[str],
    run_id: str,
    out_path: Path,
):
    preds = load_predictions_lenient(predictions_path)
    pred_map: Dict[str, Dict] = {p[KEY_INSTANCE_ID]: p for p in preds}

    with out_path.open("w", encoding="utf-8") as f:
        cnt = 0
        for iid in selected_ids:
            if iid not in pred_map:
                continue
            model_patch = pred_map[iid][KEY_PREDICTION]
            if not model_patch:
                continue
            llm_patch = read_latest_llm_test_patch(run_id, iid)
            if not llm_patch:
                continue
            combined = concat_patches(model_patch, llm_patch)
            model_name = pred_map[iid].get(KEY_MODEL, Path(predictions_path).stem)
            rec = {
                KEY_INSTANCE_ID: iid,
                KEY_PREDICTION: combined,
                KEY_MODEL: f"{model_name}+llm",
            }
            f.write(json.dumps(rec) + "\n")
            cnt += 1
    print(f"Wrote model+llm predictions to {out_path}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Build combined predictions with LLM tests")
    parser.add_argument("--dataset_name", default="SWE-bench/SWE-bench", type=str)
    parser.add_argument("--split", default="test", type=str)
    parser.add_argument("--run_id", required=True, type=str, help="Run ID used by test enhancer")
    parser.add_argument(
        "--predictions_paths",
        nargs="+",
        required=True,
        help="One or more model predictions files (.json or .jsonl)",
    )
    parser.add_argument(
        "--out_dir", default=".", type=str, help="Directory to write combined predictions"
    )
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Determine the set of instance_ids to consider from the provided predictions files
    selected_ids: Set[str] = set()
    for path in args.predictions_paths:
        preds = load_predictions_lenient(path)
        for p in preds:
            selected_ids.add(p[KEY_INSTANCE_ID])

    # Build gold_with_llm_tests.jsonl limited to selected_ids
    gold_out = out_dir / "gold_with_llm_tests.jsonl"
    make_gold_with_llm(args.dataset_name, args.split, selected_ids, args.run_id, gold_out)

    # Build one model_with_llm jsonl per predictions file
    for path in args.predictions_paths:
        stem = Path(path).stem
        model_out = out_dir / f"{stem}_with_llm_tests.jsonl"
        make_model_with_llm(args.dataset_name, args.split, path, selected_ids, args.run_id, model_out)


if __name__ == "__main__":
    main()
