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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 check_framework.test_translation_llm.CheckLanguageSettingsConsistentMockTests.test_checker_between_different_tags_calls_with_each_tag check_framework.test_translation_llm.CheckLanguageSettingsConsistentMockTests.test_get_supported_language_variant_called_with_exact_tag_en_us check_framework.test_translation_llm.CheckLanguageSettingsConsistentMockTests.test_get_supported_language_variant_called_with_exact_tag_zh_hans check_framework.test_translation_llm.CheckLanguageSettingsConsistentMockTests.test_get_supported_language_variant_preserves_case check_framework.test_translation_llm.CheckLanguageSettingsConsistentMockTests.test_multiple_calls_to_checker_use_mock_each_time check_framework.test_translation_llm.CheckLanguageSettingsConsistentMockTests.test_non_lookuperror_exceptions_propagate
coverage json -o coverage.json
: '>>>>> End Test Output'
