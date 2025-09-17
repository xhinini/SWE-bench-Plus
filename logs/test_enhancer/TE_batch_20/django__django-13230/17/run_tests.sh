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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 syndication_tests.test_feeds_llm.Item.__init__ syndication_tests.test_feeds_llm.Item.__str__ syndication_tests.test_feeds_llm.Item.get_absolute_url syndication_tests.test_feeds_llm._render_feed syndication_tests.test_feeds_llm.test_atom_includes_comments syndication_tests.test_feeds_llm.test_author_name_branch_includes_comments syndication_tests.test_feeds_llm.test_custom_feed_url_includes_comments syndication_tests.test_feeds_llm.test_enclosure_and_comments_coexist_includes_comments syndication_tests.test_feeds_llm.test_guid_permalink_false_includes_comments syndication_tests.test_feeds_llm.test_guid_permalink_true_includes_comments syndication_tests.test_feeds_llm.test_naive_pubdate_is_made_aware_and_includes_comments syndication_tests.test_feeds_llm.test_naive_updateddate_is_made_aware_and_includes_comments syndication_tests.test_feeds_llm.test_rss091_includes_comments syndication_tests.test_feeds_llm.test_rss2_includes_comments
coverage json -o coverage.json
: '>>>>> End Test Output'
