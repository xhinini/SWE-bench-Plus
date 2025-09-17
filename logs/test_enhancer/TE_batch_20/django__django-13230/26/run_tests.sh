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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 syndication_tests.test_feeds_llm._make_item syndication_tests.test_feeds_llm._make_request syndication_tests.test_feeds_llm._render_feed_to_string syndication_tests.test_feeds_llm.test_atom_feed_includes_item_comments syndication_tests.test_feeds_llm.test_custom_feed_generator_includes_comments syndication_tests.test_feeds_llm.test_default_feed_includes_item_comments syndication_tests.test_feeds_llm.test_feed_with_custom_feed_url_includes_comments syndication_tests.test_feeds_llm.test_feed_with_item_author_branches_and_comments syndication_tests.test_feeds_llm.test_feed_without_item_author_name_still_includes_comments syndication_tests.test_feeds_llm.test_naive_pubdate_made_aware_and_comments_present syndication_tests.test_feeds_llm.test_naive_updateddate_made_aware_and_comments_present syndication_tests.test_feeds_llm.test_rss091_feed_includes_item_comments syndication_tests.test_feeds_llm.test_template_based_feed_includes_item_comments_and_templates_do_not_break
coverage json -o coverage.json
: '>>>>> End Test Output'
