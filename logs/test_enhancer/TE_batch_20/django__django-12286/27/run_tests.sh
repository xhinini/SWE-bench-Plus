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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 check_framework.test_translation_llm.test_consistent_with_patched_trans_real_1 check_framework.test_translation_llm.test_consistent_with_patched_trans_real_10 check_framework.test_translation_llm.test_consistent_with_patched_trans_real_2 check_framework.test_translation_llm.test_consistent_with_patched_trans_real_3 check_framework.test_translation_llm.test_consistent_with_patched_trans_real_4 check_framework.test_translation_llm.test_consistent_with_patched_trans_real_5 check_framework.test_translation_llm.test_consistent_with_patched_trans_real_6 check_framework.test_translation_llm.test_consistent_with_patched_trans_real_7 check_framework.test_translation_llm.test_consistent_with_patched_trans_real_8 check_framework.test_translation_llm.test_consistent_with_patched_trans_real_9
coverage json -o coverage.json
: '>>>>> End Test Output'
