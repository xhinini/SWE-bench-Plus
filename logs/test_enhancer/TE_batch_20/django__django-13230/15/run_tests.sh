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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 syndication_tests.test_feeds_llm.CommentsRegressionTests._render syndication_tests.test_feeds_llm.CommentsRegressionTests.setUp syndication_tests.test_feeds_llm.CommentsRegressionTests.test_articles_feed_without_get_absolute_url_raises_for_item_link_but_comments_still_present syndication_tests.test_feeds_llm.CommentsRegressionTests.test_atom_includes_replies_link_for_comments syndication_tests.test_feeds_llm.CommentsRegressionTests.test_feed_with_custom_feed_url_includes_comments syndication_tests.test_feeds_llm.CommentsRegressionTests.test_item_comments_as_attribute_included syndication_tests.test_feeds_llm.CommentsRegressionTests.test_item_comments_callable_zero_arg syndication_tests.test_feeds_llm.CommentsRegressionTests.test_multiple_enclosure_atom_includes_comments syndication_tests.test_feeds_llm.CommentsRegressionTests.test_rss091_includes_comments_tag syndication_tests.test_feeds_llm.CommentsRegressionTests.test_rss2_includes_comments_tag syndication_tests.test_feeds_llm.CommentsRegressionTests.test_single_enclosure_rss_includes_comments syndication_tests.test_feeds_llm.CommentsRegressionTests.test_template_feed_still_includes_comments
coverage json -o coverage.json
: '>>>>> End Test Output'
