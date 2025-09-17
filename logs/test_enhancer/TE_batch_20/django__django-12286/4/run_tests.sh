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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 check_framework.test_translation_llm.ReloadedTranslationChecksTests._assert_supported_by_stub check_framework.test_translation_llm.ReloadedTranslationChecksTests._with_stubbed_get_supported check_framework.test_translation_llm.ReloadedTranslationChecksTests.test_fake_code_aa_supported check_framework.test_translation_llm.ReloadedTranslationChecksTests.test_fake_code_bb_supported check_framework.test_translation_llm.ReloadedTranslationChecksTests.test_fake_code_cc_supported check_framework.test_translation_llm.ReloadedTranslationChecksTests.test_fake_code_dd_supported check_framework.test_translation_llm.ReloadedTranslationChecksTests.test_fake_code_ee_supported check_framework.test_translation_llm.ReloadedTranslationChecksTests.test_fake_code_ff_supported check_framework.test_translation_llm.ReloadedTranslationChecksTests.test_fake_code_gg_supported check_framework.test_translation_llm.ReloadedTranslationChecksTests.test_fake_code_xx_supported check_framework.test_translation_llm.ReloadedTranslationChecksTests.test_fake_code_yy_supported check_framework.test_translation_llm.ReloadedTranslationChecksTests.test_fake_code_zz_supported
coverage json -o coverage.json
: '>>>>> End Test Output'
