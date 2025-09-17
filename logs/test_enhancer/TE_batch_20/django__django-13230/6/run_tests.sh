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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 syndication_tests.test_feeds_llm.CommentsKwargRegressionTests._assert_comments_and_categories_present syndication_tests.test_feeds_llm.CommentsKwargRegressionTests.setUp syndication_tests.test_feeds_llm.CommentsKwargRegressionTests.setUpTestData syndication_tests.test_feeds_llm.CommentsKwargRegressionTests.test_atom_feed_has_comments_kwarg syndication_tests.test_feeds_llm.CommentsKwargRegressionTests.test_guid_permalink_false_feed_has_comments_kwarg syndication_tests.test_feeds_llm.CommentsKwargRegressionTests.test_guid_permalink_true_feed_has_comments_kwarg syndication_tests.test_feeds_llm.CommentsKwargRegressionTests.test_latest_feed_has_comments_kwarg syndication_tests.test_feeds_llm.CommentsKwargRegressionTests.test_rss091feed_has_comments_kwarg syndication_tests.test_feeds_llm.CommentsKwargRegressionTests.test_rss2feed_has_comments_kwarg syndication_tests.test_feeds_llm.CommentsKwargRegressionTests.test_single_enclosure_atom_feed_has_comments_kwarg syndication_tests.test_feeds_llm.CommentsKwargRegressionTests.test_single_enclosure_rss_feed_has_comments_kwarg syndication_tests.test_feeds_llm.CommentsKwargRegressionTests.test_template_context_feed_has_comments_kwarg syndication_tests.test_feeds_llm.CommentsKwargRegressionTests.test_template_feed_has_comments_kwarg
coverage json -o coverage.json
: '>>>>> End Test Output'
