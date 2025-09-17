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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 syndication_tests.test_feeds_llm.FeedCommentsTests._render_feed syndication_tests.test_feeds_llm.FeedCommentsTests.setUp syndication_tests.test_feeds_llm.FeedCommentsTests.test_atom_includes_replies_link syndication_tests.test_feeds_llm.FeedCommentsTests.test_comments_present_when_author_name_none syndication_tests.test_feeds_llm.FeedCommentsTests.test_comments_present_with_feed_url_override syndication_tests.test_feeds_llm.FeedCommentsTests.test_comments_with_custom_atom_feed_generator syndication_tests.test_feeds_llm.FeedCommentsTests.test_item_comments_callable_object syndication_tests.test_feeds_llm.FeedCommentsTests.test_item_comments_no_arg_method syndication_tests.test_feeds_llm.FeedCommentsTests.test_item_comments_plain_attribute syndication_tests.test_feeds_llm.FeedCommentsTests.test_item_comments_returns_none syndication_tests.test_feeds_llm.FeedCommentsTests.test_multiple_items_all_include_comments syndication_tests.test_feeds_llm.FeedCommentsTests.test_rss2_includes_comments_element
coverage json -o coverage.json
: '>>>>> End Test Output'
