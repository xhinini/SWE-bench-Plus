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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 serializers.models.test_data_llm.get_base_source serializers.models.test_data_llm.test_condition_in_correct_function_context serializers.models.test_data_llm.test_guard_present_near_skip_update_comment serializers.models.test_data_llm.test_guard_stable_across_reloads serializers.models.test_data_llm.test_not_raw_and_after_not_force_insert serializers.models.test_data_llm.test_not_raw_and_in_if_block serializers.models.test_data_llm.test_not_raw_and_line_breaks serializers.models.test_data_llm.test_not_raw_and_not_present_as_comment_only serializers.models.test_data_llm.test_not_raw_and_present_simple serializers.models.test_data_llm.test_not_raw_and_whitespace_robustness serializers.models.test_data_llm.test_single_occurrence_of_guard
coverage json -o coverage.json
: '>>>>> End Test Output'
