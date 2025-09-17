#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 validators.tests_llm.MaskedContains.__contains__ validators.tests_llm.URLValidatorMaskedContainsTests.setUp validators.tests_llm.URLValidatorMaskedContainsTests.test_cr_in_userinfo_masked validators.tests_llm.URLValidatorMaskedContainsTests.test_leading_newline_masked validators.tests_llm.URLValidatorMaskedContainsTests.test_multiple_unsafe_chars_masked validators.tests_llm.URLValidatorMaskedContainsTests.test_newline_after_netloc_masked validators.tests_llm.URLValidatorMaskedContainsTests.test_newline_after_port_masked validators.tests_llm.URLValidatorMaskedContainsTests.test_newline_between_user_and_host_masked validators.tests_llm.URLValidatorMaskedContainsTests.test_newline_in_path_masked validators.tests_llm.URLValidatorMaskedContainsTests.test_newline_in_scheme_masked validators.tests_llm.URLValidatorMaskedContainsTests.test_tab_in_fragment_masked validators.tests_llm.URLValidatorMaskedContainsTests.test_tab_in_netloc_masked
coverage json -o coverage.json
: '>>>>> End Test Output'
