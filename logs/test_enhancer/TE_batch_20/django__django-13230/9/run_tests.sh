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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 syndication_tests.test_feeds_llm.CommentsFeedTests.setUp syndication_tests.test_feeds_llm.CommentsFeedTests.test_atom_includes_replies_link syndication_tests.test_feeds_llm.CommentsFeedTests.test_comments_present_in_custom_feed_generator syndication_tests.test_feeds_llm.CommentsFeedTests.test_https_comments_when_request_is_secure syndication_tests.test_feeds_llm.CommentsFeedTests.test_item_comments_as_attribute syndication_tests.test_feeds_llm.CommentsFeedTests.test_item_comments_callable_with_item_arg syndication_tests.test_feeds_llm.CommentsFeedTests.test_item_comments_callable_without_args syndication_tests.test_feeds_llm.CommentsFeedTests.test_network_path_comments_get_protocol_added syndication_tests.test_feeds_llm.CommentsFeedTests.test_none_item_comments_is_omitted syndication_tests.test_feeds_llm.CommentsFeedTests.test_rss091_includes_comments_tag syndication_tests.test_feeds_llm.CommentsFeedTests.test_rss2_includes_comments_tag syndication_tests.test_feeds_llm.DummyItem.__init__ syndication_tests.test_feeds_llm.DummyItem.__str__ syndication_tests.test_feeds_llm.DummyItem.get_absolute_url syndication_tests.test_feeds_llm.DummyRequest.__init__ syndication_tests.test_feeds_llm.DummyRequest.is_secure syndication_tests.test_feeds_llm.render_feed_to_string
coverage json -o coverage.json
: '>>>>> End Test Output'
