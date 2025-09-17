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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 syndication_tests.test_feeds_llm.CommentsFeedTests._render_feed syndication_tests.test_feeds_llm.CommentsFeedTests.setUp syndication_tests.test_feeds_llm.CommentsFeedTests.test_atom_includes_comments_link_once_per_item syndication_tests.test_feeds_llm.CommentsFeedTests.test_comments_are_fully_qualified_urls syndication_tests.test_feeds_llm.CommentsFeedTests.test_custom_feed_generator_preserves_comments syndication_tests.test_feeds_llm.CommentsFeedTests.test_item_extra_kwargs_non_conflicting_preserves_comments syndication_tests.test_feeds_llm.CommentsFeedTests.test_item_extra_kwargs_with_comments_key_does_not_crash syndication_tests.test_feeds_llm.CommentsFeedTests.test_multiple_enclosure_feeds_still_include_comments syndication_tests.test_feeds_llm.CommentsFeedTests.test_no_comments_when_item_comments_returns_none syndication_tests.test_feeds_llm.CommentsFeedTests.test_rss091_includes_comments_once_per_item syndication_tests.test_feeds_llm.CommentsFeedTests.test_rss2_includes_comments_once_per_item syndication_tests.test_feeds_llm.CommentsFeedTests.test_template_feed_with_comments
coverage json -o coverage.json
: '>>>>> End Test Output'
