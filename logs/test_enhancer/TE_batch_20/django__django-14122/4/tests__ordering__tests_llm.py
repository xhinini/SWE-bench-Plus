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