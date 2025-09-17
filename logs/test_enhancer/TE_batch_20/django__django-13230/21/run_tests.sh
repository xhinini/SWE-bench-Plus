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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 syndication_tests.test_feeds_llm.CommentsRenderingTests._render_feed syndication_tests.test_feeds_llm.CommentsRenderingTests.setUp syndication_tests.test_feeds_llm.CommentsRenderingTests.test_atom_feed_contains_comments syndication_tests.test_feeds_llm.CommentsRenderingTests.test_feed_url_feed_contains_comments syndication_tests.test_feeds_llm.CommentsRenderingTests.test_item_extra_kwargs_with_comments_does_not_cause_typeerror syndication_tests.test_feeds_llm.CommentsRenderingTests.test_latest_feed_contains_comments syndication_tests.test_feeds_llm.CommentsRenderingTests.test_no_pubdate_feed_contains_comments syndication_tests.test_feeds_llm.CommentsRenderingTests.test_rss091_feed_contains_comments syndication_tests.test_feeds_llm.CommentsRenderingTests.test_rss2_feed_contains_comments syndication_tests.test_feeds_llm.CommentsRenderingTests.test_template_context_feed_contains_comments syndication_tests.test_feeds_llm.CommentsRenderingTests.test_template_feed_contains_comments syndication_tests.test_feeds_llm.CommentsRenderingTests.test_tz_aware_dates_feed_contains_comments
coverage json -o coverage.json
: '>>>>> End Test Output'
