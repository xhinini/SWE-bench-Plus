#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_writer_llm.NestedClassMethodQualnameTests._exec_serialized migrations.test_writer_llm.NestedClassMethodQualnameTests.test_outera_exec_bound_method migrations.test_writer_llm.NestedClassMethodQualnameTests.test_outera_serialization_string_and_imports migrations.test_writer_llm.NestedClassMethodQualnameTests.test_outerb_exec_bound_method migrations.test_writer_llm.NestedClassMethodQualnameTests.test_outerb_serialization_string_and_imports migrations.test_writer_llm.NestedClassMethodQualnameTests.test_outerc_exec_bound_method migrations.test_writer_llm.NestedClassMethodQualnameTests.test_outerc_serialization_string_and_imports migrations.test_writer_llm.NestedClassMethodQualnameTests.test_outerd_exec_bound_method migrations.test_writer_llm.NestedClassMethodQualnameTests.test_outerd_serialization_string_and_imports migrations.test_writer_llm.NestedClassMethodQualnameTests.test_outere_exec_bound_method migrations.test_writer_llm.NestedClassMethodQualnameTests.test_outere_serialization_string_and_imports migrations.test_writer_llm.method'] (migrations.test_writer_llm.OuterA.['InnerA) migrations.test_writer_llm.method'] (migrations.test_writer_llm.OuterD.['InnerD) migrations.test_writer_llm.method'] (migrations.test_writer_llm.OuterE.['InnerE) migrations.test_writer_llm.method']"] (migrations.test_writer_llm.OuterB.["Middle.['InnerB) migrations.test_writer_llm.method\']"]'] (migrations.test_writer_llm.OuterC.['Middle1.["Middle2.[\'InnerC)
coverage json -o coverage.json
: '>>>>> End Test Output'
