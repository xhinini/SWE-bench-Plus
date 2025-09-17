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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_forms.test_models_llm.ArticleForm.__init__ model_forms.test_models_llm.ForeignKeyValidateTests.setUp model_forms.test_models_llm.WriterProfileForm.__init__ model_forms.test_models_llm.[] (model_forms.test_models_llm.ArticleForm) model_forms.test_models_llm.[] (model_forms.test_models_llm.WriterProfileForm)
coverage json -o coverage.json
: '>>>>> End Test Output'
