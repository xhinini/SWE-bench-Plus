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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 syndication_tests.test_feeds_llm._assert_comments_before_category_and_copyright syndication_tests.test_feeds_llm._get_first_item_children syndication_tests.test_feeds_llm.test_articles_feed_comments_position syndication_tests.test_feeds_llm.test_language_feed_comments_position syndication_tests.test_feeds_llm.test_multiple_enclosure_rss_feed_comments_position syndication_tests.test_feeds_llm.test_rss091_comments_position syndication_tests.test_feeds_llm.test_rss2_comments_position syndication_tests.test_feeds_llm.test_rss2_with_guid_permalink_false_comments_position syndication_tests.test_feeds_llm.test_rss2_with_guid_permalink_true_comments_position syndication_tests.test_feeds_llm.test_single_enclosure_rss_feed_comments_position syndication_tests.test_feeds_llm.test_template_context_feed_comments_position syndication_tests.test_feeds_llm.test_template_feed_comments_position
coverage json -o coverage.json
: '>>>>> End Test Output'
