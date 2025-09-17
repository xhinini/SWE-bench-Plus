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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 syndication_tests.test_feeds_llm.CommentsPositionTests._make_item syndication_tests.test_feeds_llm.CommentsPositionTests._render_feed syndication_tests.test_feeds_llm.CommentsPositionTests.setUp syndication_tests.test_feeds_llm.CommentsPositionTests.test_comments_before_category_for_custom_atom_generator syndication_tests.test_feeds_llm.CommentsPositionTests.test_comments_before_category_in_atom_feed syndication_tests.test_feeds_llm.CommentsPositionTests.test_comments_before_category_with_custom_feed_url syndication_tests.test_feeds_llm.CommentsPositionTests.test_comments_before_category_with_naive_dates_atom syndication_tests.test_feeds_llm.CommentsPositionTests.test_comments_before_category_with_tzaware_dates_atom
coverage json -o coverage.json
: '>>>>> End Test Output'
