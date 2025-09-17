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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 syndication_tests.test_feeds_llm.FakeRequest.__init__ syndication_tests.test_feeds_llm.FakeRequest.is_secure syndication_tests.test_feeds_llm.FeedCommentsTests._render_feed syndication_tests.test_feeds_llm.FeedCommentsTests.setUp syndication_tests.test_feeds_llm.FeedCommentsTests.tearDown syndication_tests.test_feeds_llm.FeedCommentsTests.test_item_comments_callable_with_item_arg syndication_tests.test_feeds_llm.FeedCommentsTests.test_rss091_includes_comments syndication_tests.test_feeds_llm.Item.__init__ syndication_tests.test_feeds_llm.Item.__str__ syndication_tests.test_feeds_llm.Item.get_absolute_url
coverage json -o coverage.json
: '>>>>> End Test Output'
