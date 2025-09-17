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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 syndication_tests.test_feeds_llm.CommentsRenderingTests.assert_response_contains_comments syndication_tests.test_feeds_llm.CommentsRenderingTests.assert_response_not_contains_comments_tag syndication_tests.test_feeds_llm.CommentsRenderingTests.setUpTestData syndication_tests.test_feeds_llm.CommentsRenderingTests.test_atom_feed_includes_item_comments syndication_tests.test_feeds_llm.CommentsRenderingTests.test_feed_url_feed_includes_comments_with_custom_feed_url syndication_tests.test_feeds_llm.CommentsRenderingTests.test_latest_feed_includes_item_comments_when_updated_used syndication_tests.test_feeds_llm.CommentsRenderingTests.test_no_pubdate_feed_without_item_comments_definition syndication_tests.test_feeds_llm.CommentsRenderingTests.test_rss091_feed_includes_item_comments syndication_tests.test_feeds_llm.CommentsRenderingTests.test_rss2_feed_includes_item_comments syndication_tests.test_feeds_llm.CommentsRenderingTests.test_single_enclosure_atom_feed_still_includes_comments syndication_tests.test_feeds_llm.CommentsRenderingTests.test_single_enclosure_rss_feed_still_includes_comments syndication_tests.test_feeds_llm.CommentsRenderingTests.test_template_context_feed_renders_comments_with_custom_context syndication_tests.test_feeds_llm.CommentsRenderingTests.test_template_feed_renders_comments_when_templates_used syndication_tests.test_feeds_llm.make_request
coverage json -o coverage.json
: '>>>>> End Test Output'
