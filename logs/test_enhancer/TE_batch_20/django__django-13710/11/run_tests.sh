#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_inlines.tests_llm.InlineInitVerboseTests.make_inline admin_inlines.tests_llm.InlineInitVerboseTests.test_verbose_name_provided_equal_to_model_meta_uses_verbose_to_derive_plural admin_inlines.tests_llm._FakeAdminSite.__init__ admin_inlines.tests_llm._FakeAdminSite.is_registered admin_inlines.tests_llm._FakeMeta.__init__ admin_inlines.tests_llm._FakeModel.__init__
coverage json -o coverage.json
: '>>>>> End Test Output'
