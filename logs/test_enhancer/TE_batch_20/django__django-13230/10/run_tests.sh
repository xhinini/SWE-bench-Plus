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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 syndication_tests.test_feeds_llm.CommentsRegressionTests._perform syndication_tests.test_feeds_llm.CommentsRegressionTests.setUp syndication_tests.test_feeds_llm.CommentsRegressionTests.test_atom_feed_comments_present syndication_tests.test_feeds_llm.CommentsRegressionTests.test_custom_feed_generator_comments_present syndication_tests.test_feeds_llm.CommentsRegressionTests.test_get_feed_direct_call syndication_tests.test_feeds_llm.CommentsRegressionTests.test_item_comments_none_does_not_error syndication_tests.test_feeds_llm.CommentsRegressionTests.test_item_extra_kwargs_with_comments_key_does_not_error syndication_tests.test_feeds_llm.CommentsRegressionTests.test_last_modified_header_set_when_item_pubdate_defined syndication_tests.test_feeds_llm.CommentsRegressionTests.test_multiple_items_comments_present_for_each_item syndication_tests.test_feeds_llm.CommentsRegressionTests.test_rss091_feed_comments_present syndication_tests.test_feeds_llm.CommentsRegressionTests.test_rss2_feed_comments_present syndication_tests.test_feeds_llm.Item.__init__ syndication_tests.test_feeds_llm.Item.__str__ syndication_tests.test_feeds_llm.Item.get_absolute_url
coverage json -o coverage.json
: '>>>>> End Test Output'
