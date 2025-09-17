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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 check_framework.test_translation_llm.TranslationCheckMonkeyPatchTests.test_called_with_exact_language_code check_framework.test_translation_llm.TranslationCheckMonkeyPatchTests.test_case_preserved_when_calling_get_supported check_framework.test_translation_llm.TranslationCheckMonkeyPatchTests.test_error_object_and_message_match check_framework.test_translation_llm.TranslationCheckMonkeyPatchTests.test_multiple_codes_varying_behavior check_framework.test_translation_llm.TranslationCheckMonkeyPatchTests.test_no_error_when_get_supported_returns check_framework.test_translation_llm.TranslationCheckMonkeyPatchTests.test_non_string_language_code_handled_by_get_supported check_framework.test_translation_llm.TranslationCheckMonkeyPatchTests.test_patch_scope_is_the_translation_module check_framework.test_translation_llm.TranslationCheckMonkeyPatchTests.test_patch_with_custom_callable check_framework.test_translation_llm.TranslationCheckMonkeyPatchTests.test_raises_lookuperror_returns_E004 check_framework.test_translation_llm.TranslationCheckMonkeyPatchTests.test_unicode_language_code_accepted
coverage json -o coverage.json
: '>>>>> End Test Output'
