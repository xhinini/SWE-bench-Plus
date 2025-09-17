from django.test import SimpleTestCase
from django.template import Context as TemplateContext
from django.contrib.admin.templatetags.admin_modify import submit_row

def _base_context():
    """
    Return a default context dict containing all keys used by submit_row.
    Tests will override specific keys as needed.
    """
    return {'add': False, 'change': True, 'is_popup': False, 'save_as': True, 'show_save': True, 'show_save_and_add_another': True, 'show_save_and_continue': True, 'has_add_permission': False, 'has_change_permission': False, 'has_view_permission': True, 'has_delete_permission': False, 'has_editable_inline_admin_formsets': False}

from django.test import SimpleTestCase
from django.template import Context
from django.contrib.admin.templatetags.admin_modify import submit_row

def _base_context(**kwargs):
    base = {'is_popup': False, 'save_as': True, 'has_view_permission': True, 'has_add_permission': False, 'has_change_permission': False, 'has_delete_permission': False, 'show_save': True, 'show_save_and_continue': True, 'show_save_and_add_another': True, 'show_delete': True, 'add': False, 'change': True}
    base.update(kwargs)
    return base

from django.contrib.admin.templatetags.admin_modify import submit_row
from django.test import SimpleTestCase

def _base_context():
    """
    Return a baseline context dict containing all keys expected by submit_row.
    Tests will copy and modify this dict as needed.
    """
    return {'add': False, 'change': True, 'is_popup': False, 'save_as': True, 'show_save': True, 'show_save_and_continue': True, 'show_save_and_add_another': True, 'show_delete': True, 'has_view_permission': True, 'has_add_permission': False, 'has_change_permission': False, 'has_delete_permission': False, 'has_editable_inline_admin_formsets': False}