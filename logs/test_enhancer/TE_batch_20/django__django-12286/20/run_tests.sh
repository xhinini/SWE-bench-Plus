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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 check_framework.test_translation_llm.TranslationCheckRegressionTests._run_with_trans_real_removed check_framework.test_translation_llm.TranslationCheckRegressionTests.test_supported_lang_en check_framework.test_translation_llm.TranslationCheckRegressionTests.test_supported_lang_en_us check_framework.test_translation_llm.TranslationCheckRegressionTests.test_supported_lang_fr_ca check_framework.test_translation_llm.TranslationCheckRegressionTests.test_supported_lang_variant check_framework.test_translation_llm.TranslationCheckRegressionTests.test_supported_lang_zh_hans check_framework.test_translation_llm.TranslationCheckRegressionTests.test_unsupported_lang_bytes check_framework.test_translation_llm.TranslationCheckRegressionTests.test_unsupported_lang_invalid_format check_framework.test_translation_llm.TranslationCheckRegressionTests.test_unsupported_lang_none check_framework.test_translation_llm.TranslationCheckRegressionTests.test_unsupported_lang_xx
coverage json -o coverage.json
: '>>>>> End Test Output'
