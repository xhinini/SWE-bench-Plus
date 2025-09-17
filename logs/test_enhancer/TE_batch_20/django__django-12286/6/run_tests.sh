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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 check_framework.test_translation_llm.RegressionTranslationChecks.test_regression_lookuperror_subclass_is_caught check_framework.test_translation_llm.RegressionTranslationChecks.test_regression_none_LANGUAGE_CODE_is_handled check_framework.test_translation_llm.RegressionTranslationChecks.test_regression_only_specific_codes_allowed check_framework.test_translation_llm.RegressionTranslationChecks.test_regression_side_effect_based_on_input check_framework.test_translation_llm.RegressionTranslationChecks.test_regression_top_level_called_once_for_non_ascii_tag check_framework.test_translation_llm.RegressionTranslationChecks.test_regression_top_level_called_with_exact_LANGUAGE_CODE check_framework.test_translation_llm.RegressionTranslationChecks.test_regression_top_level_raises_lookuperror_causes_E004 check_framework.test_translation_llm.RegressionTranslationChecks.test_regression_top_level_returns_ok_causes_no_errors check_framework.test_translation_llm.RegressionTranslationChecks.test_regression_top_level_used_with_complex_tag check_framework.test_translation_llm.RegressionTranslationChecks.test_regression_trans_real_and_top_level_differ
coverage json -o coverage.json
: '>>>>> End Test Output'
