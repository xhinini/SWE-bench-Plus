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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 prefetch_related.test_models_llm.UUIDGenericForeignKeyTests.setUp prefetch_related.test_models_llm.UUIDGenericForeignKeyTests.test_content_type_assigned_as_instance prefetch_related.test_models_llm.UUIDGenericForeignKeyTests.test_nonexistent_object_returns_none prefetch_related.test_models_llm.UUIDGenericForeignKeyTests.test_prefetch_related_multiple_comments_mixed_formats prefetch_related.test_models_llm.UUIDGenericForeignKeyTests.test_prefetch_related_on_object_list prefetch_related.test_models_llm.UUIDGenericForeignKeyTests.test_refresh_from_db_and_resolve prefetch_related.test_models_llm.UUIDGenericForeignKeyTests.test_resolve_dashed_uuid_string prefetch_related.test_models_llm.UUIDGenericForeignKeyTests.test_resolve_hex_uuid_string_lower prefetch_related.test_models_llm.UUIDGenericForeignKeyTests.test_resolve_hex_uuid_string_upper prefetch_related.test_models_llm.UUIDGenericForeignKeyTests.test_resolve_uuid_object_assigned_before_save
coverage json -o coverage.json
: '>>>>> End Test Output'
