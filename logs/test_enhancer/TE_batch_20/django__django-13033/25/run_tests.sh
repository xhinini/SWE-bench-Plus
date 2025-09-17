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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 ordering.test_models_llm.FindOrderingNameTests._compile_first_sql ordering.test_models_llm.FindOrderingNameTests._find_ordering_name ordering.test_models_llm.FindOrderingNameTests._get_compiler_for_model ordering.test_models_llm.FindOrderingNameTests.setUp ordering.test_models_llm.FindOrderingNameTests.test_editor__id_returns_single_ordering ordering.test_models_llm.FindOrderingNameTests.test_editor__pk_does_not_expand_to_related_default ordering.test_models_llm.FindOrderingNameTests.test_editor__pk_returns_single_ordering ordering.test_models_llm.FindOrderingNameTests.test_editor_id_no_join_single_ordering ordering.test_models_llm.FindOrderingNameTests.test_editor_returns_multiple_orderings_due_to_related_model_default ordering.test_models_llm.FindOrderingNameTests.test_negative_editor__id_is_descending ordering.test_models_llm.FindOrderingNameTests.test_negative_second_author__pk_descending ordering.test_models_llm.FindOrderingNameTests.test_nested_editor__editor__id_single_ordering ordering.test_models_llm.FindOrderingNameTests.test_second_author__id_on_article_single_ordering ordering.test_models_llm.FindOrderingNameTests.test_second_author__pk_on_article_single_ordering
coverage json -o coverage.json
: '>>>>> End Test Output'
