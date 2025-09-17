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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 check_framework.test_translation_llm.TranslationReloadTests._expected_error check_framework.test_translation_llm.TranslationReloadTests._make_fake_modules check_framework.test_translation_llm.TranslationReloadTests._reload_checks_with_fakes check_framework.test_translation_llm.TranslationReloadTests.test_case_insensitive_with_missing_trans_real check_framework.test_translation_llm.TranslationReloadTests.test_complex_variant_with_missing_trans_real check_framework.test_translation_llm.TranslationReloadTests.test_multiple_supported_languages_missing_trans_real check_framework.test_translation_llm.TranslationReloadTests.test_region_variant_with_missing_trans_real check_framework.test_translation_llm.TranslationReloadTests.test_script_tag_with_missing_trans_real check_framework.test_translation_llm.TranslationReloadTests.test_supported_language_with_missing_trans_real check_framework.test_translation_llm.TranslationReloadTests.test_unsupported_language_with_missing_trans_real check_framework.test_translation_llm.TranslationReloadTests.test_unsupported_variant_with_missing_trans_real check_framework.test_translation_llm.TranslationReloadTests.test_with_trans_real_present_supported check_framework.test_translation_llm.TranslationReloadTests.test_with_trans_real_present_unsupported
coverage json -o coverage.json
: '>>>>> End Test Output'
