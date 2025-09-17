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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 syndication_tests.test_feeds_llm.CommentsRenderingTests._render_feed syndication_tests.test_feeds_llm.CommentsRenderingTests.setUp syndication_tests.test_feeds_llm.CommentsRenderingTests.tearDown syndication_tests.test_feeds_llm.CommentsRenderingTests.test_atom_single_comments_link_once syndication_tests.test_feeds_llm.CommentsRenderingTests.test_comments_not_duplicated_with_templates syndication_tests.test_feeds_llm.CommentsRenderingTests.test_comments_properly_prefixed_with_domain syndication_tests.test_feeds_llm.CommentsRenderingTests.test_comments_rendered_once_when_item_extra_kwargs_provided syndication_tests.test_feeds_llm.CommentsRenderingTests.test_item_comments_callable_with_item_arg syndication_tests.test_feeds_llm.CommentsRenderingTests.test_item_comments_callable_without_item_arg syndication_tests.test_feeds_llm.CommentsRenderingTests.test_no_comments_absent syndication_tests.test_feeds_llm.CommentsRenderingTests.test_rss2_multiple_items_each_single_comment syndication_tests.test_feeds_llm.CommentsRenderingTests.test_rss2_single_comments_once syndication_tests.test_feeds_llm.DummyItem.__init__ syndication_tests.test_feeds_llm.DummyItem.__str__ syndication_tests.test_feeds_llm.DummyItem.get_absolute_url syndication_tests.test_feeds_llm.FakeRequest.__init__ syndication_tests.test_feeds_llm.FakeRequest.is_secure syndication_tests.test_feeds_llm._stub_site
coverage json -o coverage.json
: '>>>>> End Test Output'
