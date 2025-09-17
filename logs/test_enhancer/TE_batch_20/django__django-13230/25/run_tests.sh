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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 syndication_tests.test_feeds_llm.FeedCommentsTests._render_feed syndication_tests.test_feeds_llm.FeedCommentsTests.setUp syndication_tests.test_feeds_llm.FeedCommentsTests.test_atom_does_not_crash_and_mentions_comment_link syndication_tests.test_feeds_llm.FeedCommentsTests.test_feed_call_sets_last_modified_header_when_pubdates_present syndication_tests.test_feeds_llm.FeedCommentsTests.test_item_comments_as_attribute syndication_tests.test_feeds_llm.FeedCommentsTests.test_item_comments_callable_no_args syndication_tests.test_feeds_llm.FeedCommentsTests.test_item_comments_callable_with_item syndication_tests.test_feeds_llm.FeedCommentsTests.test_no_type_error_when_generating_feed_with_item_comments syndication_tests.test_feeds_llm.FeedCommentsTests.test_rss091_includes_comments_element syndication_tests.test_feeds_llm.FeedCommentsTests.test_rss2_comments_before_category_order syndication_tests.test_feeds_llm.FeedCommentsTests.test_rss2_includes_comments_element
coverage json -o coverage.json
: '>>>>> End Test Output'
