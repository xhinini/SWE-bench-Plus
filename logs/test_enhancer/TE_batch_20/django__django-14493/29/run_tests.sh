#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 staticfiles_tests.test_storage_llm.TempHashedStorage.__init__ staticfiles_tests.test_storage_llm.TempManifestStorage.__init__ staticfiles_tests.test_storage_llm.TestManifestMaxPostProcessZero.setUp staticfiles_tests.test_storage_llm.TestManifestMaxPostProcessZero.tearDown staticfiles_tests.test_storage_llm.TestMaxPostProcessZero._save_files staticfiles_tests.test_storage_llm.TestMaxPostProcessZero.setUp staticfiles_tests.test_storage_llm.TestMaxPostProcessZero.tearDown staticfiles_tests.test_storage_llm.TestMaxPostProcessZero.test_css_with_fragment_processed
coverage json -o coverage.json
: '>>>>> End Test Output'
