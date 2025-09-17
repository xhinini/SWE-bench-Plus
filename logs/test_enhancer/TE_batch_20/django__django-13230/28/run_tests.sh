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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 syndication_tests.test_feeds_llm.FakeRequest.__init__ syndication_tests.test_feeds_llm.FakeRequest.is_secure syndication_tests.test_feeds_llm.render_feed syndication_tests.test_feeds_llm.test_defaultfeed_comments_before_category syndication_tests.test_feeds_llm.test_rss201rev2_comments_before_category syndication_tests.test_feeds_llm.test_rss201rev2_comments_before_category_no_copyright syndication_tests.test_feeds_llm.test_rss201rev2_comments_before_category_with_list_categories syndication_tests.test_feeds_llm.test_rss201rev2_comments_before_copyright syndication_tests.test_feeds_llm.test_rss201rev2_comments_before_multiple_categories_and_copyright syndication_tests.test_feeds_llm.test_rss201rev2_comments_before_single_category syndication_tests.test_feeds_llm.test_rss201rev2_comments_contains_url syndication_tests.test_feeds_llm.test_rss201rev2_no_comments_when_none syndication_tests.test_feeds_llm.test_rssuserland091_comments_before_category
coverage json -o coverage.json
: '>>>>> End Test Output'
