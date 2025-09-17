import re
import os
import time
import math
import yaml
import json
import docker
import jinja2
import platform
import traceback

from typing import Iterable, Set, Dict, List
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from pathlib import Path, PurePosixPath

from swebench.harness.constants import (
    APPLY_PATCH_FAIL,
    APPLY_PATCH_PASS,
    DOCKER_PATCH,
    DOCKER_USER,
    DOCKER_WORKDIR,
    INSTANCE_IMAGE_BUILD_DIR,
    KEY_INSTANCE_ID,
    KEY_MODEL,
    KEY_PREDICTION,
    LOG_REPORT,
    LOG_INSTANCE,
    LOG_TEST_OUTPUT,
    RUN_EVALUATION_LOG_DIR,
    TESTENHANCER_LOG_DIR,
    UTF8,
    MAP_REPO_VERSION_TO_SPECS,
    START_TEST_OUTPUT,
    END_TEST_OUTPUT,
)
from swebench.harness.docker_utils import (
    clean_images,
    cleanup_container,
    copy_to_container,
    exec_run_with_timeout,
    list_images,
    remove_image,
    should_remove,
    write_to_container,
)
from swebench.harness.docker_build import (
    BuildImageError,
    build_container,
    build_env_images,
    close_logger,
    setup_logger,
)
from swebench.harness.utils import (
    EvaluationError,
    load_swebench_dataset,
    get_predictions_from_file,
    run_threadpool,
    str2bool,
    optional_str,
)
from swebench.harness.utils import get_modified_files, extract_minimal_patch
from swebench.harness.grading import get_eval_report
from swebench.harness.run_evaluation import GIT_APPLY_CMDS
from swebench.harness.test_spec.test_spec import extract_test_headers, get_node
from swebench.harness.test_spec.test_spec import make_test_spec, TestSpec
from swebench.harness.test_spec.python import get_test_directives
from swebench.harness.test_spec.create_scripts import make_eval_script_list
from swebench.test_enhancer.path_approx import get_mut_paths, pairwise
from swebench.test_enhancer.path_selection import select_uncovered_paths
from swebench.test_enhancer.llm_invocation import LLMInvocation
from swebench.test_enhancer.util import split_imports_and_code, remove_duplicate_defs
from swebench.test_enhancer.preds_loader import load_predictions_lenient

HEREDOC_DELIMITER = "EOF_114329324913"
ADD_PATCH_CONTENT = True
MAX_LLM_RETRIES = 3
FLAKINESS_RETRIES = 2

def _env_bool(name: str, default: bool = False) -> bool:
    try:
        v = os.environ.get(name)
        if v is None:
            return default
        return str(v).strip().lower() in ("1", "true", "yes", "on")
    except Exception:
        return default

def _env_int(name: str, default: int) -> int:
    try:
        v = os.environ.get(name)
        if v is None:
            return default
        return int(str(v).strip())
    except Exception:
        return default

def sanitize_generated_code(code: str) -> str:
    """Sanitize AI-generated code to avoid trivial syntax errors.
    - Fix invalid octal literals like 0o800 (digits must be 0-7). Replace with 0o644.
    - Strip surrounding code fences if any leaked through.
    """
    txt = code.strip()
    # Remove accidental code fences
    if txt.startswith("```"):
        txt = txt.lstrip("`\n").lstrip("yaml").lstrip("python").lstrip().rstrip("`\n")

    # Replace invalid octal literals: any 0o<digits> containing 8 or 9
    def _fix_octal(m):
        lit = m.group(0)
        digits = lit[2:]
        if any(ch in "89" for ch in digits):
            return "0o644"
        return lit

    txt = re.sub(r"0o[0-9_]+", _fix_octal, txt)
    return txt

def sanitize_for_filename(path: str) -> str:
    """Return a safe filename for logs by replacing path separators with double underscores."""
    return re.sub(r"[\\\\/]", "__", path)

def reset_repo(container, instance, timeout, logger):
    env_name = "testbed"
    repo_directory = f"/{env_name}"
    output, timed_out, total_runtime = exec_run_with_timeout(
        container, f"git -C {repo_directory} reset --hard {instance['base_commit']}", timeout
    )
    if timed_out:
        raise EvaluationError(
            instance['instance_id'],
            f"reset_repo timed out after {timeout} seconds.",
            logger,
        )
    else:
        logger.info(f"Repo reset to {instance['base_commit']}")
        logger.info(output)
    # Also remove untracked files that prior attempts may have created (e.g., reproduce.py)
    output, timed_out, total_runtime = exec_run_with_timeout(
        container, f"git -C {repo_directory} clean -xfd", timeout
    )
    if timed_out:
        raise EvaluationError(
            instance['instance_id'],
            f"git clean timed out after {timeout} seconds.",
            logger,
        )
    else:
        logger.info("git clean -fd completed")
    # Verify HEAD equals base_commit and working tree is clean
    head_rev = container.exec_run(f"git -C {repo_directory} rev-parse HEAD").output.decode(UTF8, errors="ignore").strip()
    status = container.exec_run(f"git -C {repo_directory} status --porcelain").output.decode(UTF8, errors="ignore").strip()
    logger.info(f"HEAD after reset: {head_rev}; status: {'clean' if status == '' else status}")
    if head_rev[:40] != instance['base_commit'][:40] or status != "":
        raise EvaluationError(
            instance['instance_id'],
            f"Repository did not reset cleanly to base commit {instance['base_commit']}. HEAD={head_rev}, status={status}",
            logger,
        )

def patch_coverage(container, instance, timeout, logger):
    coverage_patch = '''
diff --git a/coverage/jsonreport.py b/coverage/jsonreport.py
index 43edc4520..7ca468e32 100644
--- a/coverage/jsonreport.py
+++ b/coverage/jsonreport.py
@@ -102,4 +102,17 @@ def report_one_file(self, coverage_data, analysis):
                 'covered_branches': nums.n_executed_branches,
                 'missing_branches': nums.n_missing_branches,
             })
+            reported_file['executed_branches'] = list(
+                [-1, -2] # _convert_branch_arcs(analysis.executed_branch_arcs())
+            )
+            reported_file['missing_branches'] = list(
+                _convert_branch_arcs(analysis.missing_branch_arcs())
+            )
         return reported_file
+
+
+def _convert_branch_arcs(branch_arcs):
+    """Convert branch arcs to a list of two-element tuples."""
+    for source, targets in branch_arcs.items():
+        for target in targets:
+            yield source, target if target != -1 else 0
    '''

    coverage_apply_patch_command = " && ".join([
        "pushd $(python -c 'from distutils.sysconfig import get_python_lib; print(get_python_lib())')",
        f"git apply -v - <<'{HEREDOC_DELIMITER}'\n{coverage_patch}\n{HEREDOC_DELIMITER}\n"
        "popd",
    ])
    output, timed_out, total_runtime = exec_run_with_timeout(
        container, coverage_apply_patch_command, timeout
    )
    if timed_out:
        raise EvaluationError(
            instance['instance_id'],
            f"patch_coverage timed out after {timeout} seconds.",
            logger,
        )

def run_tests(container, instance, log_dir, timeout, logger, llm_test_file: str | None = None, test_file: str | None = None, specific_labels: list[str] | None = None):
    instance_id = instance['instance_id']
    env_name = "testbed"
    repo_directory = f"/{env_name}"
    specs = MAP_REPO_VERSION_TO_SPECS[instance['repo']][instance['version']]

    # test_files = get_modified_files(instance['test_patch'])
    # reset_tests_command = f"git checkout {instane['base_commit']} {' '.join(test_files)}"
    apply_test_patch_command = (
        f"git apply -v - <<'{HEREDOC_DELIMITER}'\n{instance['test_patch']}\n{HEREDOC_DELIMITER}"
    )
    # Build test directives. If specific_labels are provided, run only those.
    # Else if TE_ONLY_LLM=1 and llm_test_file provided, run only the llm module.
    # Otherwise, run upstream directives plus the llm module.
    te_only_llm = _env_bool("TE_ONLY_LLM", False)
    directives: list[str]
    if specific_labels and len(specific_labels) > 0:
        directives = list(specific_labels)
    else:
        directives = list(get_test_directives(instance))
        if llm_test_file:
            # Normalize to POSIX and convert to Django test label
            _llm = llm_test_file.replace("\\", "/")
            if instance["repo"] == "django/django":
                d = _llm[:-3] if _llm.endswith(".py") else _llm
                d = d[len("tests/"):] if d.startswith("tests/") else d
                d = d.replace("/", ".")
            else:
                # For pytest-style repos, passing the file path is sufficient
                d = _llm
            if te_only_llm:
                directives = [d]
            else:
                directives.append(d)
    test_command = " ".join(
        [
            MAP_REPO_VERSION_TO_SPECS[instance["repo"]][instance["version"]][
                "test_cmd"
            ],
            *directives,
        ]
    )
    try:
        logger.info(f"Test directives: {directives}")
        logger.info(f"Full test command: {test_command}")
    except Exception:
        pass
    eval_commands = [
        "source /opt/miniconda3/bin/activate",
        f"conda activate {env_name}",
        f"cd {repo_directory}",
    ]
    # Inherit repo/version-specific runtime environment exports (e.g., LANG/LC_ALL for Django)
    if "eval_commands" in specs and isinstance(specs["eval_commands"], list):
        eval_commands += specs["eval_commands"]
    # Ensure Python uses UTF-8 for stdio to avoid UnicodeEncodeError on U+2026 and similar
    eval_commands.append("export PYTHONIOENCODING=utf8")
    if ((instance['repo'] == "django/django" and float(instance['version']) < 4.0) or (instance['repo'] == 'scikit-learn/scikit-learn' and float(instance['version']) < 1.0) ):
        coverage_command = "coverage json -o coverage.json"
        coverage_install = "python --version && python -m pip install -U pip\npython -m pip install -U 'coverage==6.2'"
        coverage_apply_patch_command = ""
    elif instance['repo'] == "django/django":
        coverage_command = "coverage json -o coverage.json"
        coverage_install = "python --version\npip install -U coverage"
        coverage_apply_patch_command = ""
    elif instance['repo'] == 'sympy/sympy':
        coverage_command = "coverage json -o coverage.json"
        coverage_install = "python --version\npip install -U coverage\ncoverage --version"
        coverage_apply_patch_command = ""
    # elif instance['repo'] == 'pytest-dev/pytest':
    #     coverage_command = "coverage json -o coverage.json"
    #     coverage_install = "python --version\npip install -U coverage\ncoverage --version"
    #     coverage_apply_patch_command = ""
    elif instance['repo'] == 'sphinx-doc/sphinx':
        coverage_command = ""
        coverage_install = ""
        coverage_apply_patch_command = "sed -i -e 's/ pytest / pytest --cov --cov-branch --cov-report json /g' tox.ini"
    elif instance['repo'] in [ 'psf/requests', 'pytest-dev/pytest', ]:
        coverage_command = ""
        coverage_install = "python -m pip install pytest-cov ."
        coverage_apply_patch_command = ""
    # elif instance['repo'] == 'scikit-learn/scikit-learn' :
    #     coverage_command = ""
    #     coverage_install = "python -m pip install -U pip\npython -m pip install 'pytest-cov>=4.1.0'\npython --version\npytest --version"
    #     coverage_apply_patch_command = ""
    else:
        coverage_command = ""
        coverage_install = ""
        coverage_apply_patch_command = ""
    eval_commands += [
        # reset_tests_command,
        coverage_install,
        # apply_test_patch_command,
        coverage_apply_patch_command,
        f": '{START_TEST_OUTPUT}'",
        test_command,
        coverage_command,
        f": '{END_TEST_OUTPUT}'",
        # "cat -n astropy/io/fits/connect.py",
        # "cat -n astropy/io/fits/tests/test_connect.py",
        # reset_tests_command,
    ]

    test_script = "\n".join(["#!/bin/bash", "set -uxo pipefail"] + eval_commands) + "\n"

    # Normalize to LF and write both locally (for logs) and into container without CRLF
    eval_file = Path(log_dir / "run_tests.sh")
    eval_content = test_script.replace("\r\n", "\n").replace("\r", "\n")
    with open(eval_file, "w", encoding=UTF8, newline="\n") as f:
        f.write(eval_content)
    logger.info(
        f"Testrun script for {instance_id} written to {eval_file}; writing into container..."
    )
    # Write directly inside container to avoid any CRLF issues from host OS
    write_to_container(container, eval_content, PurePosixPath("/run_tests.sh"))

    # Run eval script, write output to logs
    test_output, timed_out, total_runtime = exec_run_with_timeout(
        container, "/bin/bash /run_tests.sh", timeout
    )
    test_output_path = log_dir / LOG_TEST_OUTPUT
    logger.info(f"Test runtime: {total_runtime:_.2f} seconds")
    with open(test_output_path, "w", encoding=UTF8) as f:
        f.write(test_output)
        logger.info(f"Test output for {instance_id} written to {test_output_path}")
        if timed_out:
            f.write(f"\n\nTimeout error: {timeout} seconds exceeded.")
            raise EvaluationError(
                instance_id,
                f"Test timed out after {timeout} seconds.",
                logger,
            )
    return test_output_path

def get_coverage(container, instance, log_dir, timeout, logger):
    instance_id = instance['instance_id']
    cov_output, timed_out, total_runtime = exec_run_with_timeout(
        container, "cat coverage.json", timeout
    )
    cov_output_path = log_dir / "coverage.json"
    with open(cov_output_path, "w", encoding=UTF8) as f:
        f.write(cov_output)
        logger.info(f"Coverage output for {instance_id} written to {cov_output_path}")
        if timed_out:
            f.write(f"\n\nTimeout error: {timeout} seconds exceeded.")
            raise EvaluationError(
                instance_id,
                f"Cat coverage timed out after {timeout} seconds.",
                logger,
            )
    cov_report = json.loads(cov_output)
    return cov_report

import ast
from pathlib import Path
from typing import Dict, Set, Tuple, Union, Iterable

def remove_functions_from_file(source: str, names_to_remove: Iterable[str]) -> str:
    """
    Remove standalone functions and class methods from `source`.
    If a class ends up with no methods, remove the class entirely.

    `names_to_remove` can include:
      - bare function names, e.g., "foo"
      - method names, e.g., "bar" (removes any method named bar in any class)
      - fully qualified methods, e.g., "MyClass.baz" (only that class' method)

    Returns the modified source code as a string.
    """
    to_remove: Set[str] = set(names_to_remove)

    # Split into plain names and fully-qualified Class.method names
    plain_funcs: Set[str] = set()
    class_to_methods: Dict[str, Set[str]] = {}
    for name in to_remove:
        if "." in name:
            cls, meth = name.split(".", 1)
            class_to_methods.setdefault(cls, set()).add(meth)
        else:
            plain_funcs.add(name)

    class Remover(ast.NodeTransformer):
        def visit_Module(self, node: ast.Module):
            new_body = []
            for n in node.body:
                n = self.visit(n)
                if n is None:
                    continue
                # Keep lists flattened if any transformer returns a list (we won't here).
                if isinstance(n, list):
                    new_body.extend(n)
                else:
                    new_body.append(n)
            node.body = new_body
            return node

        def visit_FunctionDef(self, node: ast.FunctionDef):
            # Remove top-level function if name matches plain list
            return None if node.name in plain_funcs else node

        def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
            # Remove top-level async function if name matches plain list
            return None if node.name in plain_funcs else node

        def visit_ClassDef(self, node: ast.ClassDef):
            # Collect original method names
            method_nodes = [n for n in node.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
            original_methods = {n.name for n in method_nodes}

            # Which methods of this class should we remove?
            targeted_by_class = class_to_methods.get(node.name, set())
            # Remove if method name matches either the class-specific list OR the plain method names
            remove_names = (original_methods & targeted_by_class) | (original_methods & plain_funcs)

            # Filter the class body
            new_body = []
            for n in node.body:
                if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    if n.name in remove_names:
                        continue  # drop this method
                new_body.append(n)

            # If the class has no methods left, remove the whole class
            has_any_method_left = any(isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) for n in new_body)
            if not has_any_method_left:
                return None

            node.body = new_body
            return node

    tree = ast.parse(source)
    new_tree = Remover().visit(tree)
    ast.fix_missing_locations(new_tree)

    # Use ast.unparse if available (Python 3.9+). Fallback to astor if needed.
    try:
        new_source = ast.unparse(new_tree)  # type: ignore[attr-defined]
    except AttributeError:
        import astor  # pip install astor
        new_source = astor.to_source(new_tree)

    return new_source

def get_list_of_successful_and_failed_tests(container, dataset_name, split, instance,
                                            test_spec, test_file, test_content, test_output_path):
    instance_id = instance['instance_id']
    repo = instance['repo']
    try:
        test_headers = extract_test_headers(repo, test_file, test_content)
    except Exception:
        # Malformed generated test code; treat as having no headers so this iteration contributes nothing
        test_headers = []
    test_spec.FAIL_TO_PASS.extend(test_headers)
    # print(f"fail -> pass: {test_spec.FAIL_TO_PASS}")
    predictions = get_predictions_from_file('gold', dataset_name, split)
    predictions = {pred[KEY_INSTANCE_ID]: pred for pred in predictions}
    pred = predictions[instance_id]
    report = get_eval_report(
        test_spec=test_spec,
        prediction=pred,
        test_log_path=test_output_path,
        include_tests_status=True,
    )
    # Safely extract tests_status; default to empty on missing keys
    try:
        ts = report.get(instance_id, {}).get('tests_status', {})
        ftp = ts.get('FAIL_TO_PASS', {})
        tests_success = ftp.get('success', []) or []
        tests_failure = ftp.get('failure', []) or []
    except Exception:
        tests_success, tests_failure = [], []
        try:
            print(f"[WARN] tests_status missing for {instance_id}; defaulting to empty.")
        except Exception:
            pass
    new_tests_success = [ test for test in test_headers if test in tests_success ]
    new_tests_failure = [ test for test in test_headers if test in tests_failure ]
    return new_tests_success, new_tests_failure


def get_successful_tests(container, dataset_name, split, instance,
               test_spec, test_file, test_content, test_output_path,
               log_dir, timeout, logger):
    _, new_tests_failure = get_list_of_successful_and_failed_tests(container, dataset_name, split, instance,
               test_spec, test_file, test_content, test_output_path)
    instance_id = instance['instance_id']
    repo = instance['repo']
    to_remove = [ get_node(repo, test_file, test) for test in new_tests_failure ]
    to_remove = [ entry for entry in to_remove if entry is not None ]
    logger.info(f"Remove failed targets: {to_remove}")
    if to_remove is not None and len(to_remove) > 0:
        correct_test_content = remove_functions_from_file(test_content, to_remove)
        logger.info(correct_test_content)
    else:
        correct_test_content = test_content
    return correct_test_content


def get_list_of_successful_and_failed_tests_by_pred(
    container,
    instance,
    test_spec: TestSpec,
    test_file: str,
    test_content: str,
    test_output_path: Path,
    pred: Dict,
):
    """
    Like get_list_of_successful_and_failed_tests, but uses an explicit prediction
    object (e.g., from gold or a model-generated patch) instead of loading from file.
    """
    instance_id = instance['instance_id']
    repo = instance['repo']
    test_headers = extract_test_headers(repo, test_file, test_content)
    test_spec.FAIL_TO_PASS.extend(test_headers)
    report = get_eval_report(
        test_spec=test_spec,
        prediction=pred,
        test_log_path=test_output_path,
        include_tests_status=True,
    )
    # Safely extract tests_status; default to empty on missing keys
    try:
        ts = report.get(instance_id, {}).get('tests_status', {})
        ftp = ts.get('FAIL_TO_PASS', {})
        tests_success = ftp.get('success', []) or []
        tests_failure = ftp.get('failure', []) or []
    except Exception:
        tests_success, tests_failure = [], []
        try:
            print(f"[WARN] tests_status missing for {instance_id}; defaulting to empty.")
        except Exception:
            pass
    new_tests_success = [test for test in test_headers if test in tests_success]
    new_tests_failure = [test for test in test_headers if test in tests_failure]
    return new_tests_success, new_tests_failure


def get_successful_tests_by_pred(
    container,
    instance,
    test_spec: TestSpec,
    test_file: str,
    test_content: str,
    test_output_path: Path,
    log_dir,
    timeout,
    logger,
    pred: Dict,
):
    new_tests_success, new_tests_failure = get_list_of_successful_and_failed_tests_by_pred(
        container, instance, test_spec, test_file, test_content, test_output_path, pred
    )
    instance_id = instance['instance_id']
    repo = instance['repo']
    # Detect 'no tests ran': both lists empty but headers exist
    try:
        _headers = extract_test_headers(repo, test_file, test_content)
        if len(_headers) > 0 and len(new_tests_success) == 0 and len(new_tests_failure) == 0:
            # No signal -> treat as zero passes; drop all
            return ""
    except Exception:
        pass
    to_remove = [get_node(repo, test_file, test) for test in new_tests_failure]
    to_remove = [entry for entry in to_remove if entry is not None]
    logger.info(f"Remove failed targets (keep only PASS): {to_remove}")
    if to_remove is not None and len(to_remove) > 0:
        correct_test_content = remove_functions_from_file(test_content, to_remove)
    else:
        correct_test_content = test_content
    return correct_test_content


def get_failed_tests_by_pred(
    container,
    instance,
    test_spec: TestSpec,
    test_file: str,
    test_content: str,
    test_output_path: Path,
    log_dir,
    timeout,
    logger,
    pred: Dict,
):
    new_tests_success, new_tests_failure = get_list_of_successful_and_failed_tests_by_pred(
        container, instance, test_spec, test_file, test_content, test_output_path, pred
    )
    instance_id = instance['instance_id']
    repo = instance['repo']
    # Detect 'no tests ran': both lists empty but headers exist
    try:
        _headers = extract_test_headers(repo, test_file, test_content)
        if len(_headers) > 0 and len(new_tests_success) == 0 and len(new_tests_failure) == 0:
            # No signal -> treat as zero failures; drop all
            return ""
    except Exception:
        pass
    to_remove = [get_node(repo, test_file, test) for test in new_tests_success]
    to_remove = [entry for entry in to_remove if entry is not None]
    logger.info(f"Remove passed targets (keep only FAIL): {to_remove}")
    if to_remove is not None and len(to_remove) > 0:
        correct_test_content = remove_functions_from_file(test_content, to_remove)
    else:
        correct_test_content = test_content
    return correct_test_content

def get_failed_tests(container, dataset_name, split, instance, 
               test_spec, test_file, test_content, test_output_path,
               log_dir, timeout, logger):
    new_tests_success, _ = get_list_of_successful_and_failed_tests(container, dataset_name, split, instance,
               test_spec, test_file, test_content, test_output_path)
    instance_id = instance['instance_id']
    repo = instance['repo']
    to_remove = [ get_node(repo, test_file, test) for test in new_tests_success ]
    to_remove = [ entry for entry in to_remove if entry is not None ]
    logger.info(f"Remove passed targets: {to_remove}")
    if to_remove is not None and len(to_remove) > 0:
        correct_test_content = remove_functions_from_file(test_content, to_remove)
        # logger.info(correct_test_content)
    else:
        correct_test_content = test_content
    return correct_test_content

def build_prompt(
    src_file,
    src_numbered,
    test_file,
    test_content,
    gold_patch_content,
    selected_paths,
    rem_codeblock,
    log_dir,
    model_patch_content: str | None = None,
    enable_paths_section: bool = False,
):
    test_template = """
Please generate test for `{{method_name}}` to cover the path
{{selected_path_for_method}}
-----------------------------------------------------------
    """
    jenv = jinja2.Environment(loader=jinja2.FileSystemLoader("swebench/test_enhancer/templates/"))
    user_prompt = jenv.get_template("python_base.txt").render(
        source_file=src_file,
        source_numbered="\n".join(src_numbered),
        test_file=test_file,
        test_content=test_content,
        count=10,
        patch_content=gold_patch_content,
        model_patch_content=model_patch_content or "",
        add_model_patch_content=(model_patch_content is not None and len(model_patch_content) > 0),
        add_patch_content=ADD_PATCH_CONTENT,
        add_failed_tests_section=False,
        failed_tests_section=rem_codeblock,
    )
    # When enable_paths_section is True, we add a targeted methods section using selected_paths
    if enable_paths_section:
        test_prompt = []
        for method, paths in selected_paths.items():
            for path in paths:
                lines_in_path = []
                for node in path:
                    if node[0] == node[1]:
                        lines_in_path.append(node[0])
                    else:
                        lines_in_path.extend(list(range(node[0], node[1]+1)))
                path_src = [
                    src_numbered[line]
                    for line in range(len(src_numbered))
                    if line+1 in lines_in_path
                ]
                path_src = "\n".join(path_src)
                _test_prompt = jenv.from_string(test_template).render(method_name=method, selected_path_for_method=path_src)
                test_prompt.append(_test_prompt)
        if len(test_prompt) == 0:
            _test_prompt = "Please generated tests for the whole source file given above"
            test_prompt.append(_test_prompt)
        test_prompt = """

## Methods Under Test
        """ + "\n".join(test_prompt)
        user_prompt = user_prompt + test_prompt

    system_prompt = "You are an expert Python test-driven developer"
    file_output_path = log_dir / f"prompt.txt"
    with open(file_output_path, "w", encoding=UTF8) as f:
        f.write(user_prompt)
    return {"system": system_prompt, "user": user_prompt}


def generate_test_by_prompt_llm(model, prompt, logger, log_dir, iter):

    # Call the actual LLM with retries and schema repair
    llm_invoker = LLMInvocation(model)
    # Allow env to override max attempts and backoff between attempts
    max_attempts = _env_int("TE_MAX_LLM_RETRIES", MAX_LLM_RETRIES)
    backoff_base = float(os.environ.get("TE_LLM_PROMPT_BACKOFF_BASE", "2")) if os.environ.get("TE_LLM_PROMPT_BACKOFF_BASE") else 2.0
    attempt = 0
    last_error = None
    while attempt < max_attempts:
        response_tuple = llm_invoker.call_model(prompt)
        if response_tuple[0] is False:
            last_error = response_tuple[1]
            attempt += 1
            # strengthen the instruction to return YAML only
            prompt = {
                "system": prompt.get("system", "You are an expert Python test-driven developer"),
                "user": prompt["user"]
                    + "\n\nIMPORTANT: Return only a valid YAML object with keys: language, number_of_tests, test_behavior, new_imports_code, test_code. Do not include backticks or any prose."
            }
            # Persist attempt failure detail for visibility
            try:
                (log_dir / f"llm_attempt_{attempt}_error.txt").write_text(str(last_error), encoding=UTF8)
            except Exception:
                pass
            # Exponential backoff before next attempt
            try:
                delay = backoff_base * (2 ** (attempt - 1))
                time.sleep(min(delay, 15))
            except Exception:
                pass
            continue
        response, prompt_token_count, response_token_count = response_tuple

        # Persist raw response
        response_path = log_dir / "response.txt"
        with open(response_path, "w", encoding=UTF8) as f:
            f.write(response)

        # Parse YAML with schema validation
        tests_dict = load_yaml(response, logger)
        if isinstance(tests_dict, dict) and isinstance(tests_dict.get("test_code", ""), str):
            if not isinstance(tests_dict.get("new_imports_code", ""), str):
                tests_dict["new_imports_code"] = str(tests_dict.get("new_imports_code", ""))
            import_code = tests_dict.get("new_imports_code", "")
            test_code = tests_dict.get("test_code", "")
            import_code = import_code if isinstance(import_code, str) else ""
            test_code = test_code if isinstance(test_code, str) else ""
            # Sanitize before proceeding to avoid SyntaxError later in parsing/dedup
            codeblock = sanitize_generated_code((import_code + "\n" + test_code).strip()) + "\n"

            # Validate syntax early; if invalid, request a retry by returning False
            try:
                import ast as _ast
                _ast.parse(codeblock)
            except Exception as e:
                invalid_path = log_dir / "codeblock_invalid.txt"
                try:
                    with open(invalid_path, "w", encoding=UTF8) as f:
                        f.write(codeblock)
                except Exception:
                    pass
                logger.info(f"LLM returned invalid Python (will retry): {e}. Saved to {invalid_path}")
                attempt += 1
                # strengthen instruction for next attempt
                prompt = {
                    "system": prompt.get("system", "You are an expert Python test-driven developer"),
                    "user": prompt["user"]
                        + "\n\nIMPORTANT: Your previous code had Python syntax errors. Return only syntactically valid Python in YAML keys new_imports_code and test_code. Ensure every 'with' block has an indented body."
                }
                try:
                    (log_dir / f"llm_attempt_{attempt}_invalid_python.txt").write_text(str(e), encoding=UTF8)
                except Exception:
                    pass
                try:
                    delay = backoff_base * (2 ** (attempt - 1))
                    time.sleep(min(delay, 15))
                except Exception:
                    pass
                continue

            codeblock_path = log_dir / "codeblock.txt"
            with open(codeblock_path, "w", encoding=UTF8) as f:
                f.write(codeblock)
            return response, codeblock

        # schema invalid -> repair and retry
        attempt += 1
        prompt = {
            "system": prompt.get("system", "You are an expert Python test-driven developer"),
            "user": prompt["user"]
                + "\n\nYour previous response was invalid. Return only YAML with keys: language, number_of_tests, test_behavior, new_imports_code, test_code. No code fences, no extra text."
        }
        try:
            (log_dir / f"llm_attempt_{attempt}_invalid_yaml.txt").write_text("Invalid YAML or missing keys.", encoding=UTF8)
        except Exception:
            pass
        try:
            delay = backoff_base * (2 ** (attempt - 1))
            time.sleep(min(delay, 15))
        except Exception:
            pass

    # Final failure: persist a clear marker so batch runner can surface it
    try:
        (log_dir / "llm_no_response.txt").write_text(
            f"LLM failed after {max_attempts} attempts. Last error: {last_error}\n",
            encoding=UTF8,
        )
    except Exception:
        pass
    logger.info(f"LLM invocation/schema validation failed after {max_attempts} attempts: {last_error}")
    return False

def load_yaml(response_text, logger):
    # Try to extract a fenced YAML block first
    text = response_text.strip()
    m = re.search(r"```yaml\s*([\s\S]*?)```", text, re.IGNORECASE)
    if m:
        response_text = m.group(1)
    else:
        # Fall back to removing a leading ```yaml and trailing ``` if present
        response_text = text.removeprefix("```yaml").removesuffix("```")
    try:
        data = yaml.safe_load(response_text)
    except Exception as e:
        logger.info(
            f"Failed to parse AI prediction: {e}." # Attempting to fix YAML formatting.
        )
        # data = try_fix_yaml(response_text, keys_fix_yaml=keys_fix_yaml)
        # if not data:
        #     logger.info(f"Failed to parse AI prediction after fixing YAML formatting.")
        return {}
    codeblock = data.get('test_code', '')
    if isinstance(codeblock, list):
        codeblock = "\n".join(codeblock)
        data['test_code'] = codeblock
    return data


def write_to_test_file(container, log_dir, test_file, test_content, logger):
    # Only attempt to write to a concrete Python test module; some diffs may list directories
    if not str(test_file).endswith('.py'):
        logger.info(f"Skipping reset for non-file test path: {test_file}")
        return

    new_test_file = Path(log_dir / f"{sanitize_for_filename(test_file)}" )
    new_test_file.parent.mkdir(parents=True, exist_ok=True)
    new_test_file.write_text(test_content, encoding=UTF8)
    logger.info(
        f"Writing to test file {new_test_file}, now applying to container..."
    )
    # Ensure the destination directory exists inside the container under repo root
    env_name = "testbed"
    repo_directory = f"/{env_name}"
    # Normalize to POSIX-style path for container filesystem
    tf_posix = str(test_file).replace("\\", "/")
    abs_dst = PurePosixPath(repo_directory) / PurePosixPath(tf_posix)
    parent_dir = str(abs_dst.parent)
    try:
        exec_run_with_timeout(container, f"mkdir -p {parent_dir}", 30)
    except Exception as e:
        logger.info(f"mkdir -p failed for {parent_dir}: {e}")
    try:
        write_to_container(container, new_test_file.read_text(encoding=UTF8), abs_dst)
    except Exception as e:
        logger.info(f"write_to_container error: {abs_dst}: {e}")

def add_tests_to_test_file(container, log_dir, codeblock, src_file, test_file, test_content, logger):
    # Deprecated: we now write to a dedicated LLM test module; keep for backward-compat if needed
    file_output_path = log_dir / f"new_{sanitize_for_filename(test_file)}"
    file_output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_output_path, "w", encoding=UTF8) as f:
        f.write(codeblock)
        logger.info(f"Generated tests for {src_file} written to {file_output_path}")
    your_module = src_file.split('.py')[0].replace('/','.')
    codeblock = codeblock.replace('your_module', your_module)
    new_test_content = test_content + '\n' + codeblock
    write_to_test_file(container, log_dir, test_file, new_test_content, logger)
    return new_test_content

def compute_llm_test_file(test_file: str) -> str:
    """Given an existing test file path, compute a sibling file for LLM tests.
    Examples:
      tests/test_foo.py -> tests/test_foo_llm.py
      tests/foo_test.py -> tests/foo_test_llm.py
      tests/foo.py      -> tests/test_foo_llm.py
    """
    import os
    # Normalize input path to POSIX separators first
    test_file = str(test_file).replace("\\", "/")
    dirn, base = os.path.split(test_file)
    stem = base[:-3] if base.endswith('.py') else base
    if stem == 'tests':
        # Common Django pattern: tests/test_utils/tests.py -> tests/test_utils/tests_llm.py
        new_stem = 'tests_llm'
    elif stem.startswith('test_'):
        new_stem = stem + '_llm'
    else:
        new_stem = 'test_' + stem + '_llm'
    # Always return a POSIX-style path (container uses Linux)
    return (dirn + "/" if dirn else "") + new_stem + '.py'

def build_test_labels(instance: dict, llm_test_file: str, headers: list[str]) -> list[str]:
    """Build concrete test labels to run only specific tests in the generated module.
    Normalizes Django-style headers like 'test_fn (pkg.mod.Class)' to 'pkg.mod.Class.test_fn'.
    For plain function tests, prefixes with the LLM module path.
    For non-Django repos, returns an empty list (fallback to module-level execution).
    """
    if not headers:
        return []
    _llm = llm_test_file.replace("\\", "/")
    if instance.get("repo") == "django/django":
        d = _llm[:-3] if _llm.endswith(".py") else _llm
        d = d[len("tests/"):] if d.startswith("tests/") else d
        d = d.replace("/", ".")
        labels: list[str] = []
        import re as _re
        for h in headers:
            hs = h.strip()
            # Case 1: 'test_fn (pkg.Class)' -> 'pkg.Class.test_fn'
            m = _re.match(r"^(?P<fn>\w+)\s*\(\s*(?P<cls>[\w\.]+)\s*\)$", hs)
            if m:
                labels.append(f"{m.group('cls')}.{m.group('fn')}")
                continue
            # Case 2: already fully-qualified like 'pkg.Class.test_fn'
            if "." in hs and "(" not in hs and ")" not in hs:
                labels.append(hs)
                continue
            # Case 3: 'Class.test_fn' -> prefix module
            if "." in hs and not ("(" in hs or ")" in hs):
                labels.append(f"{d}.{hs}")
                continue
            # Case 4: 'test_fn' -> module-level function
            labels.append(f"{d}.{hs}")
        # Deduplicate
        return sorted(set(labels))
    # TODO: add pytest-style labels for other repos if needed (e.g., path::Class::test)
    return []

def write_llm_tests(container, log_dir, codeblock, src_file, test_file, logger):
    """Write only the provided codeblock into a dedicated LLM test file and copy to container."""
    llm_test_file = compute_llm_test_file(test_file)
    file_output_path = log_dir / f"llm_{sanitize_for_filename(llm_test_file)}"
    file_output_path.parent.mkdir(parents=True, exist_ok=True)
    your_module = src_file.split('.py')[0].replace('/','.')
    codeblock = codeblock.replace('your_module', your_module)
    with open(file_output_path, "w", encoding=UTF8) as f:
        f.write(codeblock)
        try:
            import re as _re
            test_fn_count = len([m for m in _re.finditer(r"^\s*def\s+test_", codeblock, flags=_re.MULTILINE)])
            logger.info(f"Generated LLM tests for {src_file} written to {file_output_path} (test functions: {test_fn_count})")
        except Exception:
            logger.info(f"Generated LLM tests for {src_file} written to {file_output_path}")
    # Write into container at the new path
    write_to_test_file(container, log_dir, llm_test_file, codeblock, logger)
    # For Django's test runner, ensure the base tests module imports our llm module so it is collected.
    try:
        if instance_repo_is_django(instance=None, repo_hint=None):
            _inject_llm_import(container, llm_test_file, test_file, logger)
    except Exception:
        pass
    return llm_test_file

def instance_repo_is_django(instance, repo_hint: str | None) -> bool:
    try:
        if instance is not None:
            return instance.get("repo") == "django/django"
        if repo_hint is not None:
            return repo_hint == "django/django"
    except Exception:
        pass
    return False

def _inject_llm_import(container, llm_test_file: str, base_test_file: str, logger):
    """Append a safe import of the llm module into the base tests module so Django collects it.
    This only affects the ephemeral container workspace; repo is reset between iterations.
    """
    try:
        # Only operate for files shaped like tests/<pkg>/tests.py and tests/<pkg>/tests_llm.py
        llm_path = llm_test_file.replace("\\", "/")
        base_path = str(base_test_file).replace("\\", "/")
        if not (llm_path.endswith("/tests_llm.py") and base_path.endswith("/tests.py")):
            return
        # Derive module import like: from . import tests_llm as _te_llm
        import os as _os
        _dir, _llm_name = _os.path.split(llm_path)
        mod_name = _llm_name[:-3] if _llm_name.endswith('.py') else _llm_name
        env_name = "testbed"
        repo_directory = f"/{env_name}"
        base_abs = str(PurePosixPath(repo_directory) / PurePosixPath(base_path))
        # Read current content
        cat_cmd = f"bash -lc 'cat {base_abs} || true'"
        res = container.exec_run(cat_cmd)
        out = getattr(res, 'output', b'')
        content = out.decode('utf-8', errors='ignore') if isinstance(out, (bytes, bytearray)) else str(out)
        line = f"\n# SWE-Bench Test Enhancer: import generated tests\ntry:\n    from . import {mod_name} as _te_llm\nexcept Exception:\n    pass\n"
        if line.strip() in content:
            return
        new_content = content + ("\n" if not content.endswith("\n") else "") + line
        write_to_container(container, new_content, PurePosixPath(base_abs))
        logger.info(f"Injected import for {mod_name} into {base_path} to ensure collection.")
    except Exception as e:
        try:
            logger.info(f"Failed to inject llm import into {base_test_file}: {e}")
        except Exception:
            pass

def export_new_test_patch(container, instance, llm_test_file: str, log_dir: Path, timeout: int, logger):
    """Export a unified diff for the new LLM test file only and save as new_test_patch.diff."""
    env_name = "testbed"
    repo_directory = f"/{env_name}"
    # Stage the new file and get a cached diff
    cmds = [
        f"git -C {repo_directory} add {llm_test_file}",
        f"git -C {repo_directory} diff --cached -- {llm_test_file}",
    ]
    cmd = " && ".join(cmds)
    output, timed_out, total_runtime = exec_run_with_timeout(container, cmd, timeout)
    if timed_out:
        raise EvaluationError(instance['instance_id'], f"Exporting new test patch timed out after {timeout} seconds.", logger)
    patch_path = log_dir / "new_test_patch.diff"
    patch_path.write_text(output, encoding=UTF8)
    logger.info(f"Exported new test patch to {patch_path}")

def reset_test_file(container, log_dir, test_file, test_content, logger):
    write_to_test_file(container, log_dir, test_file, test_content, logger)

def generate_tests(model, container, dataset_name, split, instance, test_spec, log_dir, src_file, src, test_file, tests, timeout, logger, pred_gold, pred_model):
    orig_tests = tests
    instance_id = instance['instance_id']
    # Iteration controls
    iter = 0
    maxCYC = 30  # up to 30 attempts per instance
    # Accumulator for accepted tests across iterations
    combined_codeblock = ""
    kept_tests_count = 0
    iter_metrics = []
    model_failed_total = 0
    gold_pass_total = 0
    # Coverage-guided generation controls
    enable_cov_guide = _env_bool("TE_ENABLE_COVERAGE_GUIDE", True)
    coverage_patience = _env_int("TE_COVERAGE_PATIENCE", 2)
    max_accepted = _env_int("TE_MAX_ACCEPTED", 300)
    cur_cov_report = None
    best_cov = 0
    plateau = 0
    path_history = {}

    patch_coverage(container, instance, timeout, logger)

    reset_repo(container, instance, timeout, logger)
    apply_gold_patch(container, instance, log_dir, logger)
    # apply_test_patch(container, instance, log_dir, logger)
    reset_test_file(container, log_dir, test_file, tests, logger)

    # Optional: coverage-guided prompting
    # Baseline coverage (upstream tests only, no LLM) before starting iterations
    if enable_cov_guide:
        try:
            baseline_dir = log_dir / "baseline"
            baseline_dir.mkdir(parents=True, exist_ok=True)
            # Run upstream test directives only (no llm file)
            _timeout = min(timeout, _env_int("TE_TEST_TIMEOUT", timeout))
            run_tests(container, instance, baseline_dir, _timeout, logger, llm_test_file=None, test_file=test_file)
            baseline_cov = get_coverage(container, instance, baseline_dir, timeout, logger)
            cur_cov_report = baseline_cov
            # Establish best_cov from baseline
            files = baseline_cov.get("files", {}) if isinstance(baseline_cov, dict) else {}
            for k, v in files.items():
                try:
                    if str(k).endswith(str(src_file)):
                        best_cov = max(best_cov, len(set(v.get("executed_lines", []) or [])))
                except Exception:
                    continue
            try:
                (baseline_dir / "coverage_baseline.json").write_text(
                    json.dumps(baseline_cov, indent=2), encoding=UTF8
                )
            except Exception:
                pass
        except Exception as e:
            logger.info(f"Baseline coverage failed (continuing without guidance): {e}")

    src_numbered = get_lined_source(src)
    rem_codeblock = None

    while iter < maxCYC:
        logger.info(f"This is iteration: {iter}")
        _log_dir = log_dir / str(iter)
        _log_dir.mkdir(parents=True, exist_ok=True)

        if enable_cov_guide:
            try:
                selected_paths = select_uncovered_paths(cur_cov_report, src_file, src, path_history, logger)
            except Exception:
                selected_paths = None
        else:
            selected_paths = None

        prompt = build_prompt(
            src_file,
            src_numbered,
            test_file,
            tests,
            instance['patch'],
            selected_paths,
            rem_codeblock,
            _log_dir,
            model_patch_content=pred_model.get(KEY_PREDICTION, "") if isinstance(pred_model, dict) else "",
            enable_paths_section=bool(selected_paths),
        )
        llm_generation = generate_test_by_prompt_llm(model, prompt, logger, _log_dir, iter)
        if llm_generation:
            response, codeblock = llm_generation
            # Remove duplicates only against previously accepted LLM tests, not upstream tests.
            # Deduping against upstream tests would strip entire classes that share names.
            codeblock = remove_duplicate_defs(combined_codeblock or "", codeblock)
            # Validate syntax to avoid downstream AST.parse failures
            try:
                import ast as _ast
                _ast.parse(codeblock)
            except Exception as e:
                invalid_path = _log_dir / "codeblock_invalid.py"
                try:
                    with open(invalid_path, "w", encoding=UTF8) as f:
                        f.write(codeblock)
                except Exception:
                    pass
                logger.info(f"Skipping iteration {iter} due to invalid Python in generated tests: {e}. Saved to {invalid_path}")
                iter += 1
                logger.info("-"*60)
                continue
        else:
            break

        # 1) Keep tests that FAIL under the model-generated patch
        reset_repo(container, instance, timeout, logger)
        apply_model_patch(container, instance, pred_model, log_dir, logger)
        apply_test_patch(container, instance, log_dir, logger)
        # Overwrite the dedicated LLM test module with only current codeblock
        llm_test_file = write_llm_tests(container, _log_dir, codeblock, src_file, test_file, logger)
        # Allow per-run timeout override for speed-ups
        _timeout = min(timeout, _env_int("TE_TEST_TIMEOUT", timeout))
        test_output_path = run_tests(container, instance, _log_dir, _timeout, logger, llm_test_file=llm_test_file, test_file=test_file)
        new_codeblock = get_failed_tests_by_pred(
            container, instance, test_spec, llm_test_file, codeblock, test_output_path, log_dir, timeout, logger, pred_model
        )
        # Count tests that fail under model patch
        try:
            model_failed_count = len(extract_test_headers(instance['repo'], llm_test_file, new_codeblock))
        except Exception:
            model_failed_count = 0
        # Build labels for only the failing tests (if any) to narrow later runs
        try:
            failing_headers = extract_test_headers(instance['repo'], llm_test_file, new_codeblock)
        except Exception:
            failing_headers = []
        failing_labels = build_test_labels(instance, llm_test_file, failing_headers)
        try:
            logger.info(f"Model-fail headers: {len(failing_headers)}; labels built: {len(failing_labels)}")
        except Exception:
            pass

        # 2) From those, keep tests that PASS under the gold patch
        reset_repo(container, instance, timeout, logger)
        apply_gold_patch(container, instance, log_dir, logger)
        try:
            apply_test_patch(container, instance, log_dir, logger)
        except EvaluationError as e:
            # Persist a metrics.json so batch can skip in future, and return 0
            try:
                (log_dir / "reason.txt").write_text(
                    f"Patch apply failed for test_patch: {e}\n",
                    encoding=UTF8,
                )
                metrics = {
                    "accepted_total": 0,
                    "skipped_patch_apply_failure": True,
                    "instance_id": instance_id,
                }
                (log_dir / "metrics.json").write_text(
                    json.dumps(metrics, indent=2),
                    encoding=UTF8,
                )
            except Exception:
                pass
            return accepted_total
        llm_test_file = write_llm_tests(container, _log_dir, new_codeblock, src_file, test_file, logger)
        _timeout = min(timeout, _env_int("TE_TEST_TIMEOUT", timeout))
        test_output_path = run_tests(
            container, instance, _log_dir, _timeout, logger,
            llm_test_file=llm_test_file, test_file=test_file,
            specific_labels=failing_labels if failing_labels else None,
        )
        new_codeblock = get_successful_tests_by_pred(
            container, instance, test_spec, llm_test_file, new_codeblock, test_output_path, log_dir, timeout, logger, pred_gold
        )
        llm_test_file = write_llm_tests(container, _log_dir, new_codeblock, src_file, test_file, logger)
        # Count tests that pass under gold from the model-failed set
        try:
            gold_pass_from_failed_count = len(extract_test_headers(instance['repo'], llm_test_file, new_codeblock))
        except Exception:
            gold_pass_from_failed_count = 0
        # Count how many of the model-failed tests did NOT pass gold (pre-flakiness)
        try:
            gold_failed_count = max(0, int(model_failed_count) - int(gold_pass_from_failed_count))
        except Exception:
            gold_failed_count = 0

        # Capture the pre-flakiness accepted block and header count for potential relaxed acceptance
        pre_flaky_codeblock = new_codeblock
        try:
            pre_flaky_headers = extract_test_headers(instance['repo'], llm_test_file, pre_flaky_codeblock)
            pre_flaky_count = len(pre_flaky_headers)
        except Exception:
            pre_flaky_headers = []
            pre_flaky_count = 0

        # 3) Flakiness checks: re-run under model (should fail) and under gold (should pass)
        # Model fail consistency
        flakiness_retries = _env_int("TE_FLAKINESS_RETRIES", FLAKINESS_RETRIES)
        for _ in range(flakiness_retries):
            reset_repo(container, instance, timeout, logger)
            apply_model_patch(container, instance, pred_model, log_dir, logger)
            apply_test_patch(container, instance, log_dir, logger)
            llm_test_file = write_llm_tests(container, _log_dir, new_codeblock, src_file, test_file, logger)
            # Recompute current headers to target only those tests
            try:
                curr_headers = extract_test_headers(instance['repo'], llm_test_file, new_codeblock)
            except Exception:
                curr_headers = []
            curr_labels = build_test_labels(instance, llm_test_file, curr_headers)
            _timeout = min(timeout, _env_int("TE_TEST_TIMEOUT", timeout))
            test_output_path = run_tests(
                container, instance, _log_dir, _timeout, logger,
                llm_test_file=llm_test_file, test_file=test_file,
                specific_labels=curr_labels if curr_labels else None,
            )
            new_codeblock = get_failed_tests_by_pred(
                container, instance, test_spec, llm_test_file, new_codeblock, test_output_path, log_dir, timeout, logger, pred_model
            )

        # Gold pass consistency
        for _ in range(flakiness_retries):
            reset_repo(container, instance, timeout, logger)
            apply_gold_patch(container, instance, log_dir, logger)
            apply_test_patch(container, instance, log_dir, logger)
            llm_test_file = write_llm_tests(container, _log_dir, new_codeblock, src_file, test_file, logger)
            # Recompute current headers again to target only those tests
            try:
                curr_headers = extract_test_headers(instance['repo'], llm_test_file, new_codeblock)
            except Exception:
                curr_headers = []
            curr_labels = build_test_labels(instance, llm_test_file, curr_headers)
            test_output_path = run_tests(
                container, instance, _log_dir, timeout, logger,
                llm_test_file=llm_test_file, test_file=test_file,
                specific_labels=curr_labels if curr_labels else None,
            )
            new_codeblock = get_successful_tests_by_pred(
                container, instance, test_spec, llm_test_file, new_codeblock, test_output_path, log_dir, timeout, logger, pred_gold
            )

        # After gold pass runs, compute combined coverage (upstream + LLM) and decide if we should continue
        if enable_cov_guide:
            try:
                combined_dir = _log_dir / "combined"
                combined_dir.mkdir(parents=True, exist_ok=True)
                # Temporarily disable TE_ONLY_LLM to run upstream + LLM together
                _prev_te_only = os.environ.get("TE_ONLY_LLM")
                os.environ["TE_ONLY_LLM"] = "0"
                try:
                    _timeout = min(timeout, _env_int("TE_TEST_TIMEOUT", timeout))
                    run_tests(
                        container, instance, combined_dir, _timeout, logger,
                        llm_test_file=llm_test_file, test_file=test_file,
                    )
                finally:
                    if _prev_te_only is None:
                        try:
                            del os.environ["TE_ONLY_LLM"]
                        except Exception:
                            pass
                    else:
                        os.environ["TE_ONLY_LLM"] = _prev_te_only
                cov_report = get_coverage(container, instance, combined_dir, timeout, logger)
                try:
                    (combined_dir / "coverage_combined.json").write_text(
                        json.dumps(cov_report, indent=2), encoding=UTF8
                    )
                except Exception:
                    pass
                # Match the src_file key by suffix
                files = cov_report.get("files", {}) if isinstance(cov_report, dict) else {}
                covered = 0
                for k, v in files.items():
                    try:
                        if str(k).endswith(str(src_file)):
                            covered = max(covered, len(set(v.get("executed_lines", []) or [])))
                    except Exception:
                        continue
                if covered > best_cov:
                    best_cov = covered
                    plateau = 0
                else:
                    plateau += 1
                    logger.info(f"Coverage plateau step {plateau}/{coverage_patience}: covered={covered}, best={best_cov}")
                cur_cov_report = cov_report
            except Exception as e:
                logger.info(f"Combined coverage failed (continuing without guidance): {e}")

        # Log post-flakiness header count
        try:
            post_flaky_headers = extract_test_headers(instance['repo'], llm_test_file, new_codeblock)
            logger.info(f"Pre-flakiness headers: {pre_flaky_count}; Post-flakiness headers: {len(post_flaky_headers)}")
        except Exception:
            logger.info(f"Pre-flakiness headers: {pre_flaky_count}; Post-flakiness headers: unknown (extract failed)")

        # Optional relaxed acceptance (now default): if flakiness pruning removed everything but
        # we had some gold-pass headers, accept the pre-flaky block unless TE_STRICT_FLAKINESS=1.
        relaxed_acceptance = False
        if (not new_codeblock or new_codeblock.strip() == "") and pre_flaky_count > 0 and not _env_bool("TE_STRICT_FLAKINESS", False):
            new_codeblock = pre_flaky_codeblock
            relaxed_acceptance = True

        # 4) Integrate accepted tests into the combined file for this instance
        # Count headers in this iteration's accepted block (guard against malformed code)
        try:
            accepted_headers = extract_test_headers(instance['repo'], llm_test_file, new_codeblock)
            new_accepted_count = len(accepted_headers)
        except Exception as e:
            accepted_headers = []
            new_accepted_count = 0
            try:
                (log_dir / f"accepted_headers_parse_error_iter{iter}.txt").write_text(
                    f"Parse error when extracting headers from accepted block: {e}\n\n--- code ---\n{new_codeblock}",
                    encoding=UTF8,
                )
            except Exception:
                pass
        # If nothing survived acceptance but we had pre-flaky gold-pass tests, accept them (unless strict)
        if new_accepted_count == 0 and pre_flaky_count > 0 and not _env_bool("TE_STRICT_FLAKINESS", False):
            new_codeblock = pre_flaky_codeblock
            try:
                accepted_headers = extract_test_headers(instance['repo'], llm_test_file, new_codeblock)
                new_accepted_count = len(accepted_headers)
            except Exception as e:
                accepted_headers = []
                new_accepted_count = 0
                try:
                    (log_dir / f"accepted_headers_fallback_parse_error_iter{iter}.txt").write_text(
                        f"Parse error on fallback accepted block: {e}\n\n--- code ---\n{new_codeblock}",
                        encoding=UTF8,
                    )
                except Exception:
                    pass
            relaxed_acceptance = True
        if new_accepted_count > 0:
            kept_tests_count += new_accepted_count
            # Append to the combined codeblock (de-duplicated against what we already have)
            dedup_block = remove_duplicate_defs(combined_codeblock, new_codeblock)
            if dedup_block.strip():
                combined_codeblock = (combined_codeblock + "\n\n" + dedup_block).strip()
                # Write the cumulative tests file to container for visibility
                llm_test_file = write_llm_tests(container, _log_dir, combined_codeblock, src_file, test_file, logger)
                # Also persist a single aggregated file for the instance for easy consumption
                try:
                    accepted_path = log_dir / "accepted_tests.py"
                    accepted_path.write_text(combined_codeblock, encoding=UTF8)
                except Exception:
                    pass
        # Record iteration metrics and update totals
        iter_metrics.append({
            "iter": iter,
            "model_failed": model_failed_count,
            "gold_pass_from_failed": gold_pass_from_failed_count,
            "gold_failed": gold_failed_count,
            "accepted": new_accepted_count,
            "model_accepted": new_accepted_count,
            "accepted_relaxed": relaxed_acceptance,
        })
        model_failed_total += model_failed_count
        gold_pass_total += gold_pass_from_failed_count
        # Concise on-console progress for this instance (suppress in quiet/batch mode)
        if not _env_bool("TE_QUIET", False):
            try:
                print(
                    f"[{instance_id}] iter={iter} accepted_so_far={kept_tests_count} "
                    f"(iter_acc={new_accepted_count} model_failed={model_failed_count} "
                    f"gold_pass={gold_pass_from_failed_count} gold_failed={gold_failed_count} "
                    f"model_acc={new_accepted_count})"
                )
            except Exception:
                pass

        # Stop early if we've reached max accepted tests
        if kept_tests_count >= max_accepted:
            logger.info(f"Reached max accepted tests ({max_accepted}); stopping iterations.")
            break

        # Stop if coverage hasn't improved for patience steps
        if enable_cov_guide and plateau >= coverage_patience:
            logger.info(f"Coverage plateau reached (patience={coverage_patience}); stopping iterations.")
            break

        # 5) Increment attempt counter
        iter += 1
        logger.info("-"*60)
    # After iterations, if we accepted any tests, export a patch for the final LLM test file
    if kept_tests_count > 0:
        try:
            # If we didn’t write in the last loop body for some reason, compute the llm test path and ensure it’s in the repo
            last_llm_test_file = compute_llm_test_file(test_file)
            export_new_test_patch(container, instance, last_llm_test_file, log_dir, timeout, logger)
        except Exception as e:
            logger.info(f"export_new_test_patch failed (non-fatal): {e}")
    # Write metrics.json summarizing counts
    try:
        metrics = {
            "instance_id": instance_id,
            "model_failed_total": model_failed_total,
            "gold_pass_from_failed_total": gold_pass_total,
            "accepted_total": kept_tests_count,
            "iterations": iter_metrics,
        }
        (log_dir / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding=UTF8)
    except Exception as e:
        logger.info(f"Failed to write metrics.json: {e}")
    return kept_tests_count

def get_lined_source(src, range=None):
    src = src.split('\n')
    if src[-1] == '':
        src = src[:-1]
    lines = []
    i = 1
    for line in src:
        line = str(i) + ' ' + line
        if range is None or (i<=range[1] and i >= range[0]):
            lines.append(line)
        i+=1
    return lines

def apply_patch(container, instance_id, patch_content, log_dir, logger):
    # Persist locally for debugging (normalize CRLF to LF and strip trailing whitespace per line)
    # Write original for debugging
    try:
        (log_dir / "patch.original.txt").write_text(patch_content, encoding=UTF8)
    except Exception:
        pass
    normalized = patch_content.replace("\r\n", "\n").replace("\r", "\n")
    # Strip BOM if present
    if normalized.startswith("\ufeff"):
        normalized = normalized.lstrip("\ufeff")
    # Remove any stray diagnostics that may have been embedded
    lines = [ln.rstrip() for ln in normalized.split("\n")]
    cleaned_lines = []
    for ln in lines:
        # Drop common diagnostics that should not be inside a diff
        if ln.startswith("patching file "):
            continue
        if ln.startswith("Checking patch "):
            continue
        if ln.startswith("error: ") or ln.startswith("warning: "):
            continue
        if ln.startswith("Only in "):
            continue
        # Drop stray markers that confuse GNU patch / git apply
        if ln.strip() == r"\ No newline at end of file":
            continue
        cleaned_lines.append(ln)
    normalized = "\n".join(cleaned_lines)
    # If there are any non-diff lines before the first diff header, strip them
    import re as _re
    m = _re.search(r"^(diff --git |---\s+a/)", normalized, flags=_re.MULTILINE)
    if m and m.start() > 0:
        normalized = normalized[m.start():]
    normalized = "\n".join(line.rstrip() for line in normalized.split("\n"))
    if not normalized.endswith("\n"):
        normalized += "\n"
    # Try to extract a minimal well-formed patch (strips noise and fixes hunks)
    try:
        minimal = extract_minimal_patch(normalized)
        if minimal and minimal.strip():
            normalized = minimal if minimal.endswith("\n") else minimal + "\n"
            try:
                (log_dir / "patch.minimal.diff").write_text(normalized, encoding=UTF8)
            except Exception:
                pass
    except Exception as _e:
        # If extraction fails, fall back to normalized
        logger.info(f"extract_minimal_patch failed (using normalized): {_e}")
    # Save normalized as well
    try:
        (log_dir / "patch.normalized.diff").write_text(normalized, encoding=UTF8)
    except Exception:
        pass
    patch_file = Path(log_dir / "patch.diff")
    with open(patch_file, "w", encoding=UTF8, newline="\n") as _f:
        _f.write(normalized)
    logger.info(
        f"Intermediate patch for {instance_id} written to {patch_file}, now applying to container..."
    )

    # Disable CRLF safety which can break hunks
    container.exec_run(f"git -C {DOCKER_WORKDIR} config core.autocrlf false")
    container.exec_run(f"git -C {DOCKER_WORKDIR} config core.safecrlf false")

    # Copy patch to repo workdir inside container (write bytes directly to enforce LF)
    container_patch = f"{DOCKER_WORKDIR}/.swe_patch.diff"
    try:
        write_to_container(container, normalized, PurePosixPath(container_patch))
    except Exception as e:
        logger.info(f"apply_patch: write_to_container failed for {container_patch}: {e}")
        raise

    # Pre-remove any files that the patch intends to create (--- /dev/null -> +++ b/<path>)
    try:
        import re as _re
        new_files: list[str] = []
        lines = normalized.splitlines()
        for i, line in enumerate(lines):
            if line.startswith("--- /dev/null"):
                # Look ahead for corresponding +++ b/<path>
                for j in range(i + 1, min(i + 6, len(lines))):
                    m = _re.match(r"\+\+\+ b/(.+)", lines[j])
                    if m:
                        new_files.append(m.group(1))
                        break
        if new_files:
            logger.info(f"Pre-removing files to be created by patch: {new_files}")
            for nf in new_files:
                abs_nf = f"{DOCKER_WORKDIR}/{nf}"
                container.exec_run(f"rm -f {abs_nf}")
    except Exception as e:
        logger.info(f"Pre-remove new files step failed (safe to ignore): {e}")

    # Apply via direct exec (no shell builtins)
    applied_patch = False
    robust_apply_cmds = [
        f"git apply --verbose {container_patch}",
        f"git apply --verbose --reject --whitespace=nowarn {container_patch}",
        f"git apply --verbose --reject --ignore-space-change --whitespace=nowarn {container_patch}",
        f"patch --batch --forward --binary -p1 -i {container_patch}",
        f"patch --batch --fuzz=5 --forward --binary -p1 -i {container_patch}",
    ]
    last_output = ""
    for git_apply_cmd in robust_apply_cmds:
        val = container.exec_run(
            git_apply_cmd,
            workdir=DOCKER_WORKDIR,
            user=DOCKER_USER,
        )
        out = val.output.decode(UTF8, errors="ignore")
        last_output = out
        reversed_detected = ("Reversed (or previously applied) patch detected" in out) or ("Skipping patch" in out and "hunk" in out)
        if val.exit_code == 0 or reversed_detected:
            logger.info(f"{APPLY_PATCH_PASS}:\n{out}")
            applied_patch = True
            break
        else:
            logger.info(f"Failed to apply patch to container: {git_apply_cmd}\n{out}")
    if not applied_patch:
        logger.info(f"{APPLY_PATCH_FAIL}:\n{last_output}")
        raise EvaluationError(
            instance_id,
            f"{APPLY_PATCH_FAIL}:\n{last_output}",
            logger,
        )

def apply_gold_patch(container, instance, log_dir, logger):
    patch_content = instance['patch'] # + '\n' + instance['test_patch']
    apply_patch(container, instance['instance_id'], patch_content, log_dir, logger)

def apply_test_patch(container, instance, log_dir, logger):
    patch_content = instance['test_patch']
    apply_patch(container, instance['instance_id'], patch_content, log_dir, logger)

def apply_model_patch(container, instance, prediction, log_dir, logger):
    """Apply a model-generated patch contained in a prediction object (JSONL line)."""
    patch_content = prediction[KEY_PREDICTION]
    apply_patch(container, instance['instance_id'], patch_content, log_dir, logger)


def main(
    instance_id,
    dataset_name,
    split,
    model,
    predictions_path: str,
    rm_image: bool,
    force_rebuild: bool,
    client: docker.DockerClient,
    run_id: str,
    timeout: int | None,
    namespace: str | None,
    rewrite_reports: bool,
    instance_image_tag: str = "latest",
    report_dir: str = ".",
):
    log_dir = TESTENHANCER_LOG_DIR / run_id / instance_id

    # Set up logger
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / LOG_INSTANCE
    logger = setup_logger(instance_id, log_file)

    dataset = load_swebench_dataset(dataset_name, split)
    dataset = [ i for i in dataset if i[KEY_INSTANCE_ID] == instance_id ]
    assert len(dataset) == 1
    instance = dataset[0]
    src_files = re.findall(r'^diff --git a/(.*?) b/', instance['patch'], flags=re.MULTILINE)
    # Only keep Python test files; diffs can also include directories like tests/test_utils
    test_files_all = re.findall(r'^diff --git a/(.*?) b/', instance['test_patch'], flags=re.MULTILINE)
    test_files = [f for f in test_files_all if f.endswith('.py')]

    logger.info(src_files)
    logger.info(test_files)

    # def get_modified_files_from_patch(diff_text: str):
    #     modified_files = []
    #     for header in re.finditer(r"^diff --git a/(.+?) b/\1", diff_text, re.MULTILINE):
    #         file_path = header.group(1)
    #         # Ensure file is not marked as new or deleted
    #         context_start = diff_text.find(header.group(0))
    #         context = diff_text[context_start: context_start + 200]  # look ahead
    #         if "new file mode" not in context and "deleted file mode" not in context:
    #             modified_files.append(file_path)
    #     return modified_files
    # test_files = get_modified_files_from_patch(instance['test_patch'])

    # Ensure Test Enhancer can find logs for this run when injecting generated tests
    if os.environ.get('TE_ID') is None:
        os.environ['TE_ID'] = run_id
    # Default to quiet mode (suppress LLM streaming/logging); users can override by setting TE_QUIET=0
    if os.environ.get('TE_QUIET') is None:
        os.environ['TE_QUIET'] = "1"

    test_spec = make_test_spec(
        instance, namespace=namespace, instance_image_tag=instance_image_tag
    )

    container = None
    # Ensure accepted_total is defined even if we fail early (e.g., during build)
    accepted_total = 0
    try:
        # Reuse or remove pre-existing container depending on TE_REUSE_CONTAINER
        reuse = _env_bool("TE_REUSE_CONTAINER", True)
        container_name = test_spec.get_instance_container_name(run_id)
        existing = []
        try:
            existing = client.containers.list(all=True, filters={"name": f"{container_name}"})
        except Exception:
            existing = []
        if reuse and existing:
            # Pick the first matching container (should be unique by name)
            container = existing[0]
            try:
                container.reload()
            except Exception:
                pass
            status = getattr(container, "status", None)
            if status != "running":
                try:
                    container.start()
                    logger.info(f"Reused existing container for {instance_id}: {container.id}")
                except Exception as e:
                    logger.info(f"Failed to start existing container; will rebuild. Reason: {e}")
                    container = None
        elif not reuse and existing:
            # Clean out any existing container to ensure a fresh start
            for c in existing:
                try:
                    c.stop(timeout=5)
                except Exception:
                    pass
                try:
                    cname = getattr(c, 'name', container_name)
                    c.remove(force=True)
                    logger.info(f"Removed pre-existing container {cname}")
                except Exception as e:
                    logger.info(f"Failed to remove pre-existing container: {e}")

        # If no reusable container, build/create a new one
        if container is None:
            # Retry building/starting the container in case of transient timeouts
            build_retries = _env_int("TE_BUILD_MAX_RETRIES", 2)
            build_backoff = _env_int("TE_BUILD_BACKOFF_BASE", 15)
            last_build_err = None
            for _try in range(max(1, build_retries)):
                try:
                    container = build_container(
                        test_spec, client, run_id, logger, rm_image, force_rebuild
                    )
                    container.start()
                    logger.info(f"Container for {instance_id} started: {container.id}")
                    last_build_err = None
                    break
                except BuildImageError as e:
                    last_build_err = e
                except Exception as e:
                    last_build_err = e
                # Backoff then retry
                try:
                    delay = min(120, build_backoff * (2 ** _try))
                    logger.info(f"Build/start attempt {_try+1} failed; retrying in {delay}s: {last_build_err}")
                except Exception:
                    pass
                time.sleep(delay)
            if last_build_err is not None:
                raise last_build_err

        apply_gold_patch(container, instance, log_dir, logger)
        try:
            apply_test_patch(container, instance, log_dir, logger)
        except EvaluationError as e:
            # Persist a metrics.json so batch can skip in future, and return 0
            try:
                (log_dir / "reason.txt").write_text(
                    f"Patch apply failed for test_patch (pre-iteration): {e}\n",
                    encoding=UTF8,
                )
                metrics = {
                    "accepted_total": 0,
                    "skipped_patch_apply_failure": True,
                    "instance_id": instance_id,
                }
                (log_dir / "metrics.json").write_text(
                    json.dumps(metrics, indent=2),
                    encoding=UTF8,
                )
            except Exception:
                pass
            return accepted_total

        # eval_file = Path(log_dir / "eval.sh")
        # eval_file.write_text(test_spec.eval_script)
        # logger.info(
        #     f"Eval script for {instance_id} written to {eval_file}; copying to container..."
        # )
        # copy_to_container(container, eval_file, PurePosixPath("/eval.sh"))

        def get_file_output(file_path, file_output_path):
            file_output, timed_out, total_runtime = exec_run_with_timeout(
                container, f"cat /testbed/{file_path}", timeout
            )
            with open(file_output_path, "w", encoding=UTF8) as f:
                f.write(file_output)
                logger.info(f"File output for {instance_id} written to {file_output_path}")
                if timed_out:
                    f.write(f"\n\nTimeout error: {timeout} seconds exceeded.")
                    raise EvaluationError(
                        instance_id,
                        f"Cat coverage timed out after {timeout} seconds.",
                        logger,
                    )
            return file_output

        def match_test_file(src_file, test_files):
            src_tail = src_file.split('/')[-1].split('.py')[0]
            if len(test_files) == 1: return test_files[0]
            for test_file in test_files:
                test_tail = test_file.split('/')[-1].split('.py')[0]
                if test_tail == f'test_{src_tail}':
                    return test_file
            for test_file in test_files:
                test_tail = test_file.split('/')[-1].split('.py')[0]
                if src_tail in test_tail:
                    return test_file
            return test_files[0]

        # Load predictions: gold and model-generated for this instance
        preds_gold = get_predictions_from_file('gold', dataset_name, split)
        preds_gold = {pred[KEY_INSTANCE_ID]: pred for pred in preds_gold}
        if instance_id not in preds_gold:
            raise EvaluationError(instance_id, f"Gold prediction not found for {instance_id}", logger)
        pred_gold = preds_gold[instance_id]

        preds_model = load_predictions_lenient(predictions_path)
        preds_model = {pred[KEY_INSTANCE_ID]: pred for pred in preds_model}
        if instance_id not in preds_model:
            raise EvaluationError(instance_id, f"Model prediction not found for {instance_id} in {predictions_path}", logger)
        pred_model = preds_model[instance_id]

        if not test_files:
            logger.info("No .py test files detected in test_patch; skipping instance")
            return accepted_total
        for src_file in src_files:
            test_file = match_test_file(src_file, test_files)
            if test_file is None:
                logger.info(f"No matching test file for {src_file}")
                continue
            logger.info(f"Generating tests for {src_file} -> {test_file}")
            path_history = dict()
            file_output_path = log_dir / f"{sanitize_for_filename(src_file)}"
            src = get_file_output(src_file, file_output_path)
            file_output_path = log_dir / f"{sanitize_for_filename(test_file)}"
            tests = get_file_output(test_file, file_output_path)
            accepted_count = generate_tests(model, container, dataset_name, split, instance, test_spec, log_dir, src_file, src, test_file, tests, timeout, logger, pred_gold, pred_model)
            accepted_total += accepted_count

    except BuildImageError as e:
        # Building the environment image failed (e.g., timeout). Log and return 0 so batch can continue.
        try:
            logger.info(traceback.format_exc())
        except Exception:
            pass
        print(e)
        return accepted_total
    except Exception as e:
        error_msg = (
            f"Error in evaluating model for {instance_id}: {e}\n"
            f"{traceback.format_exc()}\n"
            f"Check ({logger.log_file}) for more information."
        )
        logger.error(error_msg)
        # Re-raise so the batch runner can stop and surface the error
        raise
    finally:
        # Remove instance container + image, close logger
        cleanup_container(client, container, logger)
        if rm_image:
            remove_image(client, test_spec.instance_image_key, logger)
        close_logger(logger)
    return accepted_total



if __name__ == "__main__":
    parser = ArgumentParser(
        description="Path approximation with static analysis",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--dataset_name",
        default="SWE-bench/SWE-bench",
        type=str,
        help="Name of dataset or path to JSON file.",
    )
    parser.add_argument(
        "--split", type=str, default="test", help="Split of the dataset"
    )
    parser.add_argument(
        "--instance_ids",
        nargs="+",
        type=str,
        help="Instance IDs to run (space separated)",
    )

    parser.add_argument(
        "--open_file_limit", type=int, default=4096, help="Open file limit"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=1_800,
        help="Timeout (in seconds) for running tests for each instance",
    )
    parser.add_argument(
        "--force_rebuild",
        action='store_true',
        help="Force rebuild of all images",
    )
    parser.add_argument(
        "--cache_level",
        type=str,
        choices=["none", "base", "env", "instance"],
        help="Cache level - remove images above this level",
        default="env",
    )
    # if clean is true then we remove all images that are above the cache level
    # if clean is false, we only remove images above the cache level if they don't already exist
    parser.add_argument(
        "--clean", action='store_true', help="Clean images above cache level"
    )
    parser.add_argument(
        "--run_id", type=str, required=True, help="Run ID - identifies the run"
    )
    parser.add_argument(
        "--namespace",
        type=optional_str,
        default="swebench",
        help='Namespace for images. (use "none" to use no namespace)',
    )
    parser.add_argument(
        "--instance_image_tag", type=str, default="latest", help="Instance image tag"
    )
    parser.add_argument(
        "--rewrite_reports",
        action='store_true',
        help="Doesn't run new instances, only writes reports for instances with existing test outputs",
    )
    parser.add_argument(
        "--report_dir", type=str, default=".", help="Directory to write reports to"
    )
    parser.add_argument(
        "--instance_id", type=str, required=True, help="Instance ID",
    )
    parser.add_argument(
        "--model", type=str, default="gpt-4o-2024-08-06",
        help="LLM model to generate new tests",
    )
    parser.add_argument(
        "--predictions_path", type=str, required=True,
        help="Path to model-generated predictions JSONL used for dual-patch evaluation",
    )
    args = parser.parse_args()

    # run instances locally
    if platform.system() == "Linux":
        import resource
        resource.setrlimit(resource.RLIMIT_NOFILE, (args.open_file_limit, args.open_file_limit))
    client = docker.from_env()

    main(
        args.instance_id,
        args.dataset_name,
        args.split,
        args.model,
        args.predictions_path,
        False,
        args.force_rebuild,
        client,
        args.run_id,
        args.timeout,
        args.namespace,
        args.rewrite_reports,
        args.instance_image_tag,
        args.report_dir,
    )
