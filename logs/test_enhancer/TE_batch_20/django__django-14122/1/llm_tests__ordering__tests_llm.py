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