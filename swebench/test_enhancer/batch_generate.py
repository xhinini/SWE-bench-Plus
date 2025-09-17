import argparse
import os
import platform
import json
from pathlib import Path
from typing import Set, List

import docker
from tqdm import tqdm

from swebench.harness.utils import optional_str, get_predictions_from_file
from swebench.test_enhancer.preds_loader import load_predictions_lenient
from swebench.test_enhancer.testgen import main as testgen_main
from swebench.test_enhancer.build_combined_predictions import (
    make_gold_with_llm,
    make_model_with_llm,
)
from swebench.harness.run_evaluation import main as eval_main
from swebench.harness.constants import TESTENHANCER_LOG_DIR, KEY_INSTANCE_ID, KEY_PREDICTION


from concurrent.futures import ThreadPoolExecutor, as_completed


def run_generation_for_predictions(
    dataset_name: str,
    split: str,
    predictions_path: str,
    run_id: str,
    model: str,
    timeout: int,
    namespace: str | None,
    instance_image_tag: str,
    force_rebuild: bool,
    open_file_limit: int,
    max_workers: int,
):
    # Collect instance IDs from predictions file
    preds = load_predictions_lenient(predictions_path)
    instance_ids: List[str] = [p[KEY_INSTANCE_ID] for p in preds]
    pred_map = {p[KEY_INSTANCE_ID]: p for p in preds}

    # Load gold patches once for prescreening
    gold_preds = get_predictions_from_file("gold", dataset_name, split)
    gold_map = {p[KEY_INSTANCE_ID]: p for p in gold_preds}

    def _normalize_patch(p: str) -> str:
        if p is None:
            return ""
        # Normalize line endings, strip trailing whitespace per line, preserve line structure
        lines = p.replace("\r\n", "\n").replace("\r", "\n").split("\n")
        lines = [ln.rstrip() for ln in lines]
        # Drop leading/trailing empty lines
        while lines and lines[0] == "":
            lines.pop(0)
        while lines and lines[-1] == "":
            lines.pop()
        return "\n".join(lines)

    # Ensure test_spec can locate test enhancer logs for patches
    os.environ["TE_ID"] = run_id
    # Silence streaming LLM output during batch runs
    os.environ["TE_QUIET"] = "1"
    # Speed defaults for batch runs
    os.environ.setdefault("TE_ONLY_LLM", "1")              # only run generated module by default
    os.environ.setdefault("TE_FLAKINESS_RETRIES", "0")      # skip flakiness loops by default
    # LLM robustness defaults for batch runs
    os.environ.setdefault("TE_LLM_MAX_RETRIES", "5")         # more resilient by default
    os.environ.setdefault("TE_LLM_BACKOFF_BASE", "2")        # exponential backoff base
    os.environ.setdefault("TE_LLM_REQUEST_TIMEOUT", "45")    # seconds per LLM request (if supported)
    # Docker client/API timeouts (helps avoid Windows named pipe 60s read timeouts)
    os.environ.setdefault("DOCKER_CLIENT_TIMEOUT", "600")
    os.environ.setdefault("COMPOSE_HTTP_TIMEOUT", "600")
    # Hugging Face/Datasets offline to avoid 429s
    os.environ.setdefault("HF_DATASETS_OFFLINE", "1")
    os.environ.setdefault("HF_HUB_OFFLINE", "1")
    # Reduce HF hub chatter
    os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")

    # Docker client
    if platform.system() == "Linux":
        import resource
        resource.setrlimit(resource.RLIMIT_NOFILE, (open_file_limit, open_file_limit))
    client = docker.from_env(timeout=600)

    # Helper to process one instance (fresh docker client per worker for safety)
    def _process_instance(iid: str):
        _metrics = None
        _accepted_total = 0
        _attempts = int(os.environ.get("TE_INSTANCE_RETRIES", "2"))
        # Prescreen: skip if model patch is identical to gold patch
        try:
            model_patch = _normalize_patch(pred_map.get(iid, {}).get(KEY_PREDICTION, ""))
            gold_patch = _normalize_patch(gold_map.get(iid, {}).get(KEY_PREDICTION, ""))
            if model_patch and gold_patch and model_patch == gold_patch:
                inst_dir = TESTENHANCER_LOG_DIR / run_id / iid
                try:
                    inst_dir.mkdir(parents=True, exist_ok=True)
                    (inst_dir / "metrics.json").write_text(
                        json.dumps(
                            {
                                "instance_id": iid,
                                "model_failed_total": 0,
                                "gold_pass_from_failed_total": 0,
                                "accepted_total": 0,
                                "iterations": [],
                                "skipped_identical_patches": True,
                            },
                            indent=2,
                        ),
                        encoding="utf-8",
                    )
                    (inst_dir / "reason.txt").write_text(
                        "Skipped: model patch identical to gold patch after normalization.\n",
                        encoding="utf-8",
                    )
                except Exception:
                    pass
                return (iid, 0, None, None, True, False)
        except Exception:
            pass
        # Cache: if metrics.json already exists for this instance, optionally skip computation
        try:
            inst_dir = TESTENHANCER_LOG_DIR / run_id / iid
            metrics_path = inst_dir / "metrics.json"
            if metrics_path.is_file():
                try:
                    _metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
                    _accepted_total = int(_metrics.get("accepted_total", 0))
                except Exception:
                    _metrics = None
                    _accepted_total = 0
                # If this instance was marked as skipped due to identical patches, always skip
                if isinstance(_metrics, dict) and _metrics.get("skipped_identical_patches"):
                    return (iid, _accepted_total, _metrics, None, False, True)
                # If patch apply failure was recorded for this run, skip as cached to avoid repeated errors
                if isinstance(_metrics, dict) and _metrics.get("skipped_patch_apply_failure"):
                    return (iid, _accepted_total, _metrics, None, False, True)
                # If accepted_total == 0, allow regeneration for a new attempt in this run
                if _accepted_total <= 0:
                    pass  # continue to generation below
                else:
                    return (iid, _accepted_total, _metrics, None, False, True)
        except Exception:
            pass
        # Run generation with retries if LLM produced no response
        last_err = None
        for _try in range(_attempts):
            try:
                local_client = docker.from_env(timeout=600)
                _accepted_total = testgen_main(
                    iid,
                    dataset_name,
                    split,
                    model,
                    predictions_path,
                    False,               # rm_image
                    force_rebuild,
                    local_client,
                    run_id,
                    timeout,
                    namespace,
                    False,               # rewrite_reports
                    instance_image_tag,
                    ".",                # report_dir
                )
                metrics_path = TESTENHANCER_LOG_DIR / run_id / iid / "metrics.json"
                inst_dir = TESTENHANCER_LOG_DIR / run_id / iid
                # Detect any llm_no_response markers from testgen attempts
                had_llm_no_resp = False
                try:
                    for p in inst_dir.rglob("llm_no_response.txt"):
                        had_llm_no_resp = True
                        break
                except Exception:
                    pass
                if had_llm_no_resp and _try + 1 < _attempts:
                    # Clear marker(s) for next attempt and retry
                    try:
                        for p in inst_dir.rglob("llm_no_response.txt"):
                            try:
                                p.unlink(missing_ok=True)  # type: ignore[arg-type]
                            except TypeError:
                                # Python <3.8 fallback
                                try:
                                    p.unlink()
                                except Exception:
                                    pass
                    except Exception:
                        pass
                    print(f"[LLM-RETRY] {iid}: LLM produced no response; retrying instance ({_try+1}/{_attempts-1})...")
                    # Increase LLM-side retries a bit for the next attempt
                    try:
                        cur = int(os.environ.get("TE_LLM_MAX_RETRIES", "5"))
                        os.environ["TE_LLM_MAX_RETRIES"] = str(min(cur + 2, 10))
                    except Exception:
                        pass
                    continue
                # Read metrics on success/no-retry
                if metrics_path.is_file():
                    try:
                        _metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
                    except Exception:
                        _metrics = None
                return (iid, _accepted_total, _metrics, None, False, False)
            except Exception as e:
                last_err = e
                break
        return (iid, 0, None, last_err, False, False)

    # Parallel generation with progress bar
    succeeded: List[str] = []
    total = len(instance_ids)
    with tqdm(total=total, desc=f"{run_id} - Generating tests", unit="inst") as pbar:
        with ThreadPoolExecutor(max_workers=max_workers) as ex:
            futures = {ex.submit(_process_instance, iid): iid for iid in instance_ids}
            for fut in as_completed(futures):
                iid = futures[fut]
                metrics = None
                accepted_total = 0
                skipped_identical = False
                skipped_cached = False
                err = None
                try:
                    iid, accepted_total, metrics, err, skipped_identical, skipped_cached = fut.result()
                except Exception as e:
                    err = e
                if skipped_identical:
                    print(f"[SKIP] {iid}: model patch identical to gold; skipping test generation (strong match).")
                    succeeded.append(iid)
                elif skipped_cached:
                    if metrics is not None:
                        if metrics.get("skipped_patch_apply_failure"):
                            print(f"[SKIP] {iid}: test_patch could not be applied; skipping this instance for run_id={run_id}.")
                        else:
                            print(f"[SKIP] {iid}: metrics.json exists; using cached results (accepted={metrics.get('accepted_total', 0)}).")
                    else:
                        print(f"[SKIP] {iid}: metrics.json exists; using cached results.")
                    succeeded.append(iid)
                elif err is not None:
                    print(f"[ERROR] {iid}: {err}")
                    # Surface error and stop overall run
                    raise err
                else:
                    if metrics is not None:
                        model_failed_total = metrics.get("model_failed_total", 0)
                        gold_pass_total = metrics.get("gold_pass_from_failed_total", 0)
                        print(f"[OK] {iid}: accepted={accepted_total}, model_failed={model_failed_total}, gold_pass_from_failed={gold_pass_total}")
                    else:
                        print(f"[OK] {iid}: accepted_tests={accepted_total}")
                    succeeded.append(iid)
                pbar.update(1)
                # Update progress bar postfix with latest metrics if available
                finished = pbar.n  # number of completed futures so far
                if metrics is not None:
                    pbar.set_postfix_str(
                        f"{finished}/{total} done | acc={accepted_total} mf={metrics.get('model_failed_total',0)} gp={metrics.get('gold_pass_from_failed_total',0)}"
                    )
                else:
                    pbar.set_postfix_str(f"{finished}/{total} done | acc={accepted_total}")
    return set(succeeded)


def run_build_and_eval(
    dataset_name: str,
    split: str,
    predictions_path: str,
    run_id: str,
    selected_ids: Set[str],
    out_dir: Path,
    timeout: int,
    namespace: str | None,
    instance_image_tag: str,
    open_file_limit: int,
    max_workers: int,
):
    out_dir.mkdir(parents=True, exist_ok=True)

    # Build combined predictions
    gold_out = out_dir / "gold_with_llm_tests.jsonl"
    make_gold_with_llm(dataset_name, split, selected_ids, run_id, gold_out)

    stem = Path(predictions_path).stem
    model_out = out_dir / f"{stem}_with_llm_tests.jsonl"
    make_model_with_llm(dataset_name, split, predictions_path, selected_ids, run_id, model_out)

    # Evaluate gold+llm and model+llm
    eval_kwargs = dict(
        dataset_name=dataset_name,
        split=split,
        instance_ids=list(selected_ids),
        force_rebuild=False,
        cache_level="env",
        clean=False,
        open_file_limit=open_file_limit,
        timeout=timeout,
        namespace=namespace,
        rewrite_reports=False,
        modal=False,
        instance_image_tag=instance_image_tag,
        report_dir=".",
        max_workers=max_workers,
    )

    # Gold eval
    eval_main(
        predictions_path=str(gold_out),
        run_id=f"{run_id}_eval_gold",
        **eval_kwargs,
    )
    # Model eval
    eval_main(
        predictions_path=str(model_out),
        run_id=f"{run_id}_eval_model",
        **eval_kwargs,
    )


def main():
    parser = argparse.ArgumentParser(description="Batch generate LLM tests and evaluate gold vs model in one command")
    parser.add_argument("--dataset_name", default="SWE-bench/SWE-bench", type=str)
    parser.add_argument("--split", default="test", type=str)
    parser.add_argument("--predictions_path", required=True, type=str, help="Model predictions file (.jsonl/.json)")
    parser.add_argument("--run_id", required=True, type=str, help="Run ID for test enhancer logs")
    parser.add_argument("--model", default="gpt-5-nano", type=str, help="LLM model for generation")
    parser.add_argument("--timeout", default=1800, type=int)
    parser.add_argument("--namespace", type=optional_str, default="swebench")
    parser.add_argument("--instance_image_tag", default="latest", type=str)
    parser.add_argument("--force_rebuild", action="store_true")
    parser.add_argument("--open_file_limit", default=4096, type=int)
    parser.add_argument("--max_workers", default=4, type=int)
    parser.add_argument("--out_dir", default="combined_preds", type=str)
    args = parser.parse_args()

    selected_ids = run_generation_for_predictions(
        dataset_name=args.dataset_name,
        split=args.split,
        predictions_path=args.predictions_path,
        run_id=args.run_id,
        model=args.model,
        timeout=args.timeout,
        namespace=args.namespace,
        instance_image_tag=args.instance_image_tag,
        force_rebuild=args.force_rebuild,
        open_file_limit=args.open_file_limit,
        max_workers=args.max_workers,
    )

    run_build_and_eval(
        dataset_name=args.dataset_name,
        split=args.split,
        predictions_path=args.predictions_path,
        run_id=args.run_id,
        selected_ids=selected_ids,
        out_dir=Path(args.out_dir),
        timeout=args.timeout,
        namespace=args.namespace,
        instance_image_tag=args.instance_image_tag,
        open_file_limit=args.open_file_limit,
        max_workers=args.max_workers,
    )


if __name__ == "__main__":
    main()
