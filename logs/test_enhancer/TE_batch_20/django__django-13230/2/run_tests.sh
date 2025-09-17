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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 syndication_tests.test_feeds_llm.BaseCommentsFeed.item_link syndication_tests.test_feeds_llm.BaseCommentsFeed.items syndication_tests.test_feeds_llm.DummyItem.__init__ syndication_tests.test_feeds_llm.DummyItem.__str__ syndication_tests.test_feeds_llm.DummyItem.get_absolute_url syndication_tests.test_feeds_llm.DummyRequest.is_secure syndication_tests.test_feeds_llm.FeedCommentsTests._get_comments_from_feed syndication_tests.test_feeds_llm.FeedCommentsTests.setUp syndication_tests.test_feeds_llm.TestCommentsFeedAtom.item_comments syndication_tests.test_feeds_llm.TestCommentsFeedCallableNoArg.item_comments syndication_tests.test_feeds_llm.TestCommentsFeedCallableOneArg.item_comments syndication_tests.test_feeds_llm.TestCommentsFeedCustomFeedType.item_comments syndication_tests.test_feeds_llm.TestCommentsFeedRss091.item_comments syndication_tests.test_feeds_llm.TestCommentsFeedSimple.item_comments syndication_tests.test_feeds_llm.TestCommentsFeedUnicodeComment.item_comments syndication_tests.test_feeds_llm.TestCommentsFeedWithExtraKwargs.item_comments syndication_tests.test_feeds_llm.TestCommentsFeedWithExtraKwargs.item_extra_kwargs syndication_tests.test_feeds_llm.TestCommentsFeedWithMultipleItems.item_comments syndication_tests.test_feeds_llm.TestCommentsFeedWithMultipleItems.items syndication_tests.test_feeds_llm.[] (syndication_tests.test_feeds_llm.TestCommentsFeedCustomFeedType)
coverage json -o coverage.json
: '>>>>> End Test Output'
