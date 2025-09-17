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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 syndication_tests.test_feeds_llm.DummyItem.__init__ syndication_tests.test_feeds_llm.DummyItem.__str__ syndication_tests.test_feeds_llm.DummyItem.get_absolute_url syndication_tests.test_feeds_llm.make_feed_class syndication_tests.test_feeds_llm.render_feed_xml syndication_tests.test_feeds_llm.test_comments_before_category_in_rss091 syndication_tests.test_feeds_llm.test_comments_before_category_in_rss2 syndication_tests.test_feeds_llm.test_comments_before_category_when_no_author_rss091 syndication_tests.test_feeds_llm.test_comments_before_category_when_no_author_rss2 syndication_tests.test_feeds_llm.test_comments_before_category_with_multiple_categories_rss091 syndication_tests.test_feeds_llm.test_comments_before_category_with_multiple_categories_rss2 syndication_tests.test_feeds_llm.test_comments_before_copyright_in_rss091 syndication_tests.test_feeds_llm.test_comments_before_copyright_in_rss2 syndication_tests.test_feeds_llm.test_no_comments_tag_when_item_comments_returns_none_rss2
coverage json -o coverage.json
: '>>>>> End Test Output'
