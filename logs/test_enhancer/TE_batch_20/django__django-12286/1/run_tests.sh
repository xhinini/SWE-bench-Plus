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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 check_framework.test_translation_llm.TranslationConsistencyMonkeyPatchTests.test_monkeypatch_lookuperror_en_us check_framework.test_translation_llm.TranslationConsistencyMonkeyPatchTests.test_monkeypatch_success_en_us check_framework.test_translation_llm.TranslationConsistencyMonkeyPatchTests.test_monkeypatch_success_fr check_framework.test_translation_llm.TranslationConsistencyMonkeyPatchTests.test_monkeypatch_success_fr_ca check_framework.test_translation_llm.TranslationConsistencyMonkeyPatchTests.test_monkeypatch_success_zh_hans
coverage json -o coverage.json
: '>>>>> End Test Output'
