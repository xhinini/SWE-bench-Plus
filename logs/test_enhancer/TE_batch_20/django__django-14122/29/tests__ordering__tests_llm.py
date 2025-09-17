from django.db.models.functions import Upper, Random
from django.db.models import Count, Value, F
from django.test import TestCase
from .models import Article, Author
from django.db.models.functions import Upper, Random

def _get_group_by_fragment(sql):
    """
    Extract the GROUP BY fragment from the SQL (uppercase) and return it.
    If no GROUP BY is present, return an empty string.
    """
    sql = sql.upper()
    idx = sql.find('GROUP BY')
    if idx == -1:
        return ''
    end_idx = len(sql)
    for token in (' HAVING ', ' ORDER BY ', ' LIMIT ', ')'):
        t = sql.find(token, idx + 8)
        if t != -1 and t < end_idx:
            end_idx = t
    return sql[idx:end_idx]

from django.db.models import Count, Max, Value, F
from django.db.models import Count, Max, Value, F
from django.test import TestCase
from .models import Article, Author, ChildArticle, OrderedByFArticle

def _group_by_columns_from_sql(sql):
    """
    Extract a lower-cased, comma-separated list of GROUP BY column fragments
    from the SQL. Returns a list of column fragment strings.
    """
    sql_lower = sql.lower()
    idx = sql_lower.find('group by')
    if idx == -1:
        return []
    end_idx = len(sql_lower)
    for marker in (' having', ' order by', ' limit', ') subquery'):
        m = sql_lower.find(marker, idx)
        if m != -1:
            end_idx = min(end_idx, m)
    grp = sql_lower[idx + len('group by'):end_idx].strip()
    parts = [p.strip().strip(')"\'') for p in grp.split(',') if p.strip()]
    return parts

import re
from django.db.models import Count, Value, CharField
from django.db.models.functions import Upper
from datetime import datetime
import re
from django.db.models import Count, Value, CharField
from django.db.models.functions import Upper
from django.test import TestCase
from .models import Article, Author

def _extract_group_by(sql):
    """
    Extract the GROUP BY clause (uppercased) from a SQL string.
    Returns the text of the GROUP BY clause (after 'GROUP BY ') or an
    empty string if no GROUP BY is present.
    """
    s = sql.upper()
    m = re.search('\\bGROUP BY\\b(.*?)(\\bHAVING\\b|\\bORDER BY\\b|$)', s, re.S)
    if not m:
        return ''
    return m.group(1).strip()

import re
from datetime import datetime
from operator import attrgetter
import re
from django.db.models import Count, Value, Max
from django.test import TestCase
from .models import Article, Author, ChildArticle, OrderedByFArticle

def _group_by_columns_from_sql(sql):
    """
    Extract the GROUP BY clause from the SQL and return a list of columns
    (split on commas) with whitespace stripped. Return empty list if no GROUP BY.
    """
    m = re.search('\\bGROUP BY\\b(.*?)(?:\\bHAVING\\b|\\bORDER BY\\b|$)', sql, re.IGNORECASE | re.DOTALL)
    if not m:
        return []
    cols_fragment = m.group(1).strip()
    cols_fragment = cols_fragment.strip().strip('() ')
    cols = [c.strip() for c in cols_fragment.split(',') if c.strip()]
    return cols

from datetime import datetime
from operator import attrgetter
from django.db.models import Count, F, Value, CharField
from django.db.models.functions import Upper
from django.test import TestCase
from .models import Article, Author, ChildArticle, OrderedByFArticle, Reference, OrderedByFArticle

def _group_by_fragment(qs):
    """
    Return normalized GROUP BY fragment (uppercase) of the SQL for the given queryset.
    If there is no GROUP BY, return an empty string.
    """
    sql = str(qs.query).upper()
    if 'GROUP BY' not in sql:
        return ''
    start = sql.find('GROUP BY')
    end = sql.find('ORDER BY', start)
    if end == -1:
        return sql[start:].strip()
    return sql[start:end].strip()

from datetime import datetime
from operator import attrgetter
from django.db.models import Count, Max, Value
from django.db.models.functions import Upper
from django.test import TestCase
from .models import Article, Author, ChildArticle

def _group_by_fragment_from_sql(sql):
    """
    Extract the GROUP BY clause fragment from the SQL string (uppercase).
    Returns the string between "GROUP BY" and the next SQL clause token
    (HAVING, ORDER BY, LIMIT/OFFSET keywords or end).
    """
    sql = sql.upper()
    gb_idx = sql.find('GROUP BY')
    if gb_idx == -1:
        return ''
    end_idx = len(sql)
    for token in ('HAVING', 'ORDER BY', 'LIMIT', 'OFFSET'):
        t_idx = sql.find(token, gb_idx + 8)
        if t_idx != -1:
            end_idx = min(end_idx, t_idx)
    return sql[gb_idx:end_idx]

from django.test import TestCase
from django.db.models import Count, Max, Value
from django.db.models.functions import Upper
from .models import Article, Author, OrderedByFArticle

def _get_group_by_clause(qs):
    """
    Return the GROUP BY clause from the SQL of the given queryset as a
    lowercase string (or an empty string if no GROUP BY).
    """
    sql = str(qs.query).lower()
    idx = sql.find('group by')
    if idx == -1:
        return ''
    end_tokens = [' having', ' order by', ' limit', ' offset', ')']
    end_idx = len(sql)
    for tok in end_tokens:
        pos = sql.find(tok, idx)
        if pos != -1:
            end_idx = min(end_idx, pos)
    return sql[idx:end_idx]