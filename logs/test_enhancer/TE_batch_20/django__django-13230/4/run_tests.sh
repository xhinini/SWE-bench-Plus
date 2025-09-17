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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 syndication_tests.test_feeds_llm.make_request syndication_tests.test_feeds_llm.render_feed syndication_tests.test_feeds_llm.test_comments_before_category_attribute_string syndication_tests.test_feeds_llm.test_comments_before_category_callable_no_args syndication_tests.test_feeds_llm.test_comments_before_category_callable_object syndication_tests.test_feeds_llm.test_comments_before_category_callable_with_item syndication_tests.test_feeds_llm.test_comments_before_category_rss091 syndication_tests.test_feeds_llm.test_comments_before_category_with_guid_is_permalink_false syndication_tests.test_feeds_llm.test_comments_before_category_with_guid_is_permalink_true syndication_tests.test_feeds_llm.test_comments_content_appears syndication_tests.test_feeds_llm.test_comments_once_per_item_and_ordering_multiple_items syndication_tests.test_feeds_llm.test_no_comments_tag_when_none
coverage json -o coverage.json
: '>>>>> End Test Output'
