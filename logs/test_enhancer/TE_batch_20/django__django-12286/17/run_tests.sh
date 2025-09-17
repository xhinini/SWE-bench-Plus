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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 check_framework.test_translation_llm.TranslationCheckPatchedTests.setUp check_framework.test_translation_llm.TranslationCheckPatchedTests.test_called_once_per_check check_framework.test_translation_llm.TranslationCheckPatchedTests.test_called_with_exact_language_code check_framework.test_translation_llm.TranslationCheckPatchedTests.test_multiple_codes_raise_when_patched check_framework.test_translation_llm.TranslationCheckPatchedTests.test_patched_function_accepts_case_variation check_framework.test_translation_llm.TranslationCheckPatchedTests.test_patched_function_overrides_LANGUAGES_setting check_framework.test_translation_llm.TranslationCheckPatchedTests.test_patched_lookuperror_with_nonstandard_code check_framework.test_translation_llm.TranslationCheckPatchedTests.test_raises_lookuperror_reports_E004 check_framework.test_translation_llm.TranslationCheckPatchedTests.test_returns_value_no_error check_framework.test_translation_llm.TranslationCheckPatchedTests.test_variant_handling_raises_lookuperror_reports_E004 check_framework.test_translation_llm.TranslationCheckPatchedTests.test_variant_handling_returns_no_error
coverage json -o coverage.json
: '>>>>> End Test Output'
