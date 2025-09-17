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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.tests_llm.FieldOrderingModelMixTests._assert_no_model_before_model model_fields.tests_llm.FieldOrderingModelMixTests._make_model_meta model_fields.tests_llm.FieldOrderingModelMixTests.test_binaryfield_mixed_model_ordering model_fields.tests_llm.FieldOrderingModelMixTests.test_booleanfield_mixed_model_ordering model_fields.tests_llm.FieldOrderingModelMixTests.test_charfield_mixed_model_ordering model_fields.tests_llm.FieldOrderingModelMixTests.test_datefield_mixed_model_ordering model_fields.tests_llm.FieldOrderingModelMixTests.test_datetimefield_mixed_model_ordering model_fields.tests_llm.FieldOrderingModelMixTests.test_decimalfield_mixed_model_ordering model_fields.tests_llm.FieldOrderingModelMixTests.test_field_base_mixed_model_ordering model_fields.tests_llm.FieldOrderingModelMixTests.test_integerfield_mixed_model_ordering model_fields.tests_llm.FieldOrderingModelMixTests.test_timefield_mixed_model_ordering model_fields.tests_llm.FieldOrderingModelMixTests.test_uuidfield_mixed_model_ordering
coverage json -o coverage.json
: '>>>>> End Test Output'
