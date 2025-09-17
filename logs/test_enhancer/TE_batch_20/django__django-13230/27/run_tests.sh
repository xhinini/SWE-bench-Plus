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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 syndication_tests.test_feeds_llm.CommentsTests.test_atom_explicit_overrides_item_extra_kwargs syndication_tests.test_feeds_llm.CommentsTests.test_atom_includes_comments syndication_tests.test_feeds_llm.CommentsTests.test_comments_iri_conversion_and_domain_added syndication_tests.test_feeds_llm.CommentsTests.test_comments_present_when_no_author syndication_tests.test_feeds_llm.CommentsTests.test_comments_present_with_multiple_items syndication_tests.test_feeds_llm.CommentsTests.test_rss091_explicit_overrides_item_extra_kwargs syndication_tests.test_feeds_llm.CommentsTests.test_rss091_includes_comments syndication_tests.test_feeds_llm.CommentsTests.test_rss2_explicit_overrides_item_extra_kwargs syndication_tests.test_feeds_llm.CommentsTests.test_rss2_includes_comments syndication_tests.test_feeds_llm.SimpleItem.__init__ syndication_tests.test_feeds_llm.SimpleItem.__str__ syndication_tests.test_feeds_llm.SimpleItem.get_absolute_url syndication_tests.test_feeds_llm.render_feed
coverage json -o coverage.json
: '>>>>> End Test Output'
