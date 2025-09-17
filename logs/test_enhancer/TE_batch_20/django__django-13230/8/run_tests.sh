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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 syndication_tests.test_feeds_llm.CommentsFeedTests._render_feed syndication_tests.test_feeds_llm.CommentsFeedTests.setUp syndication_tests.test_feeds_llm.CommentsFeedTests.test_atom_feed_generates_without_error_and_includes_comments_string syndication_tests.test_feeds_llm.CommentsFeedTests.test_comments_from_item_extra_kwargs_when_method_missing syndication_tests.test_feeds_llm.CommentsFeedTests.test_default_feed_includes_comments_element syndication_tests.test_feeds_llm.CommentsFeedTests.test_item_comments_callable_with_arg syndication_tests.test_feeds_llm.CommentsFeedTests.test_item_comments_callable_without_arg syndication_tests.test_feeds_llm.CommentsFeedTests.test_item_extra_kwargs_with_comments_key_does_not_raise syndication_tests.test_feeds_llm.CommentsFeedTests.test_item_extra_kwargs_with_unrelated_keys_does_not_affect_comments syndication_tests.test_feeds_llm.CommentsFeedTests.test_multiple_items_all_render_without_error syndication_tests.test_feeds_llm.CommentsFeedTests.test_rss091_feed_includes_comments_element syndication_tests.test_feeds_llm.DummyItem.__init__ syndication_tests.test_feeds_llm.DummyItem.__str__ syndication_tests.test_feeds_llm.DummyItem.get_absolute_url
coverage json -o coverage.json
: '>>>>> End Test Output'
