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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 syndication_tests.test_feeds_llm.DummyItem.__init__ syndication_tests.test_feeds_llm.DummyItem.__str__ syndication_tests.test_feeds_llm.DummyItem.get_absolute_url syndication_tests.test_feeds_llm.FeedCommentsTests._render_feed syndication_tests.test_feeds_llm.FeedCommentsTests.setUp syndication_tests.test_feeds_llm.FeedCommentsTests.test_atom_item_comments_method_with_item_arg syndication_tests.test_feeds_llm.FeedCommentsTests.test_rss091_item_comments_method_with_item_arg syndication_tests.test_feeds_llm.FeedCommentsTests.test_rss2_item_comments_attribute_on_feed syndication_tests.test_feeds_llm.FeedCommentsTests.test_rss2_item_comments_callable_object syndication_tests.test_feeds_llm.FeedCommentsTests.test_rss2_item_comments_empty_string syndication_tests.test_feeds_llm.FeedCommentsTests.test_rss2_item_comments_method_no_args syndication_tests.test_feeds_llm.FeedCommentsTests.test_rss2_item_comments_method_with_item_arg syndication_tests.test_feeds_llm.FeedCommentsTests.test_rss2_item_comments_via_item_extra_kwargs syndication_tests.test_feeds_llm.FeedCommentsTests.test_rss2_item_comments_with_item_extra_kwargs_present syndication_tests.test_feeds_llm.FeedCommentsTests.test_rss2_multiple_items_each_have_comments
coverage json -o coverage.json
: '>>>>> End Test Output'
