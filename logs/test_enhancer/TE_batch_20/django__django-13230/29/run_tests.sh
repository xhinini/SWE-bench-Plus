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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 syndication_tests.test_feeds_llm.CommentsOrderingTests._assert_comments_before_category syndication_tests.test_feeds_llm.CommentsOrderingTests._make_item syndication_tests.test_feeds_llm.CommentsOrderingTests._make_request syndication_tests.test_feeds_llm.CommentsOrderingTests.setUp syndication_tests.test_feeds_llm.CommentsOrderingTests.test_comments_before_category_atom syndication_tests.test_feeds_llm.CommentsOrderingTests.test_comments_before_category_author_missing syndication_tests.test_feeds_llm.CommentsOrderingTests.test_comments_before_category_multiple_items syndication_tests.test_feeds_llm.CommentsOrderingTests.test_comments_before_category_rss091 syndication_tests.test_feeds_llm.CommentsOrderingTests.test_comments_before_category_rss2 syndication_tests.test_feeds_llm.CommentsOrderingTests.test_comments_before_category_template_like syndication_tests.test_feeds_llm.CommentsOrderingTests.test_comments_before_category_with_custom_feed_url syndication_tests.test_feeds_llm.CommentsOrderingTests.test_comments_before_category_with_item_extra_kwargs syndication_tests.test_feeds_llm.CommentsOrderingTests.test_comments_before_category_with_language
coverage json -o coverage.json
: '>>>>> End Test Output'
