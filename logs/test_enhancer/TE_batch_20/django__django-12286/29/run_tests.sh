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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 check_framework.test_translation_llm.test_consistent_exact_match_with_trans_real_blocked check_framework.test_translation_llm.test_consistent_region_case_insensitive_with_trans_real_blocked check_framework.test_translation_llm.test_consistent_region_uppercase_with_trans_real_blocked check_framework.test_translation_llm.test_consistent_script_variant_with_trans_real_blocked check_framework.test_translation_llm.test_consistent_sign_language_with_trans_real_blocked check_framework.test_translation_llm.test_consistent_three_letter_language_with_trans_real_blocked check_framework.test_translation_llm.test_consistent_variant_with_region_and_variant_with_trans_real_blocked check_framework.test_translation_llm.test_inconsistent_language_settings_with_trans_real_blocked check_framework.test_translation_llm.test_inconsistent_when_language_not_listed_even_with_trans_real_blocked
coverage json -o coverage.json
: '>>>>> End Test Output'
