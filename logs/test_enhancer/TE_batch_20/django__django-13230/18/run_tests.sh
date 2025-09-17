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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 syndication_tests.test_feeds_llm.CommentsBeforeCategoryTests._assert_comments_before_category syndication_tests.test_feeds_llm.CommentsBeforeCategoryTests._render_feed syndication_tests.test_feeds_llm.CommentsBeforeCategoryTests.setUp syndication_tests.test_feeds_llm.CommentsBeforeCategoryTests.test_language_feed_comments_before_category syndication_tests.test_feeds_llm.CommentsBeforeCategoryTests.test_multiple_enclosure_rss_feed_comments_before_category syndication_tests.test_feeds_llm.CommentsBeforeCategoryTests.test_rss091feed_comments_before_category syndication_tests.test_feeds_llm.CommentsBeforeCategoryTests.test_rss2feed_comments_before_category syndication_tests.test_feeds_llm.CommentsBeforeCategoryTests.test_rss2feed_with_guid_permalink_false_comments_before_category syndication_tests.test_feeds_llm.CommentsBeforeCategoryTests.test_rss2feed_with_guid_permalink_true_comments_before_category syndication_tests.test_feeds_llm.CommentsBeforeCategoryTests.test_single_enclosure_rss_feed_comments_before_category syndication_tests.test_feeds_llm.CommentsBeforeCategoryTests.test_single_enclosure_rss_feed_duplicate_check_comments_before_category syndication_tests.test_feeds_llm.CommentsBeforeCategoryTests.test_template_context_feed_comments_before_category syndication_tests.test_feeds_llm.CommentsBeforeCategoryTests.test_template_feed_comments_before_category
coverage json -o coverage.json
: '>>>>> End Test Output'
