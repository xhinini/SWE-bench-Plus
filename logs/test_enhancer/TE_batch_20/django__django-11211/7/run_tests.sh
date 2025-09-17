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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 prefetch_related.test_models_llm.GenericForeignKeyDescriptorTests.test_article_id_is_deferred_attribute prefetch_related.test_models_llm.GenericForeignKeyDescriptorTests.test_comment_content_object_is_generic_foreign_key prefetch_related.test_models_llm.GenericForeignKeyDescriptorTests.test_comment_content_object_uuid_is_generic_foreign_key prefetch_related.test_models_llm.GenericForeignKeyDescriptorTests.test_comment_object_pk_is_deferred_attribute prefetch_related.test_models_llm.GenericForeignKeyDescriptorTests.test_comment_object_pk_uuid_is_deferred_attribute prefetch_related.test_models_llm.GenericForeignKeyDescriptorTests.test_taggeditem_content_object_is_generic_foreign_key prefetch_related.test_models_llm.GenericForeignKeyDescriptorTests.test_taggeditem_created_by_fkey_is_deferred_attribute prefetch_related.test_models_llm.GenericForeignKeyDescriptorTests.test_taggeditem_created_by_is_generic_foreign_key prefetch_related.test_models_llm.GenericForeignKeyDescriptorTests.test_taggeditem_favorite_fkey_is_deferred_attribute prefetch_related.test_models_llm.GenericForeignKeyDescriptorTests.test_taggeditem_object_id_is_deferred_attribute
coverage json -o coverage.json
: '>>>>> End Test Output'
