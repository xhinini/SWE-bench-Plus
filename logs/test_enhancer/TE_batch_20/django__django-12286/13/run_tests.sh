#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && locale-gen
export LANG=en_US.UTF-8
export LANGUAGE=en_US:en
export LC_ALL=en_US.UTF-8
export PYTHONIOENCODING=utf8
python --version && python -m pip install -U pip
python -m pip install -U 'coverage==6.2'

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 check_framework.test_translation_llm._reload_checks_with_fake_translation check_framework.test_translation_llm._restore_modules check_framework.test_translation_llm.test_consistent_language_supported_exact check_framework.test_translation_llm.test_consistent_language_supported_normalized_case check_framework.test_translation_llm.test_consistent_language_supported_variant_base_present check_framework.test_translation_llm.test_inconsistent_language_empty_languages check_framework.test_translation_llm.test_inconsistent_language_not_supported check_framework.test_translation_llm.test_language_code_uppercase_variant check_framework.test_translation_llm.test_language_supported_but_not_listed_exactly check_framework.test_translation_llm.test_language_with_region_number_supported check_framework.test_translation_llm.test_language_with_script_supported check_framework.test_translation_llm.test_non_string_language_code_results_in_e004
coverage json -o coverage.json
: '>>>>> End Test Output'
