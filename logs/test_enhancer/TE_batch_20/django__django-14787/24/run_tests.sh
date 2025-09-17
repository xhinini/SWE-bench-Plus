#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 decorators.tests_llm.RegressionMethodDecoratorTests.test_annotations_preserved decorators.tests_llm.RegressionMethodDecoratorTests.test_decorator_added_attributes_with_wraps_visible decorators.tests_llm.RegressionMethodDecoratorTests.test_docstring_preserved decorators.tests_llm.RegressionMethodDecoratorTests.test_dunder_call_preserved decorators.tests_llm.RegressionMethodDecoratorTests.test_module_preserved decorators.tests_llm.RegressionMethodDecoratorTests.test_multiple_wraps_chain_preserved decorators.tests_llm.RegressionMethodDecoratorTests.test_qualname_preserved decorators.tests_llm.RegressionMethodDecoratorTests.test_signature_preserved_for_inspect decorators.tests_llm.RegressionMethodDecoratorTests.test_wrapped_chain_ends_at_original_function_object decorators.tests_llm.RegressionMethodDecoratorTests.test_wraps_preserves_name_and_wrapped
coverage json -o coverage.json
: '>>>>> End Test Output'
