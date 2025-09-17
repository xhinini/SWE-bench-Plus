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

from django.contrib.admin.templatetags.admin_modify import submit_row
from django.template import Context
from django.test import SimpleTestCase

def _base_context():
    return {'is_popup': False, 'save_as': True, 'has_view_permission': True, 'has_add_permission': False, 'has_change_permission': False, 'has_delete_permission': False, 'show_save': True, 'show_save_and_continue': True, 'show_save_and_add_another': True, 'show_delete': True, 'add': False, 'change': True, 'has_editable_inline_admin_formsets': False}

from django.test import SimpleTestCase
from django.contrib.admin.templatetags.admin_modify import submit_row

def base_context():
    """
    Return a baseline context dictionary containing all keys submit_row expects.
    Tests will copy and modify this dict for different permutations.
    """
    return {'add': False, 'change': True, 'is_popup': False, 'save_as': True, 'show_save': True, 'show_save_and_add_another': True, 'show_save_and_continue': True, 'has_add_permission': False, 'has_change_permission': False, 'has_view_permission': True, 'has_delete_permission': False, 'has_editable_inline_admin_formsets': False}

from django.test import SimpleTestCase
from django.template import Context as TemplateContext
from django.contrib.admin.templatetags.admin_modify import submit_row
from django.test import SimpleTestCase
from django.template import Context as TemplateContext
from django.contrib.admin.templatetags.admin_modify import submit_row

def _base_context(**overrides):
    """
    Provide a baseline context with sensible defaults for submit_row,
    allowing overrides for specific test cases.
    """
    ctx = {'add': False, 'change': True, 'is_popup': False, 'save_as': True, 'show_save': True, 'show_save_and_add_another': True, 'show_save_and_continue': True, 'has_add_permission': False, 'has_change_permission': False, 'has_view_permission': True, 'has_delete_permission': False, 'has_editable_inline_admin_formsets': False, 'show_delete': True}
    ctx.update(overrides)
    return ctx

from django.contrib.admin.templatetags.admin_modify import submit_row
from django.test import SimpleTestCase
from django.template import Context

def make_context(**overrides):
    """
    Create a baseline context that resembles an admin change form context.
    The baseline values are chosen so that, with has_add_permission=True,
    show_save_as_new should be True (not a popup, save_as enabled, change=True).
    """
    ctx = {'add': False, 'change': True, 'is_popup': False, 'save_as': True, 'show_save': True, 'show_save_and_add_another': True, 'show_save_and_continue': True, 'has_add_permission': False, 'has_change_permission': False, 'has_view_permission': True, 'has_delete_permission': False, 'has_editable_inline_admin_formsets': False, 'show_delete': True}
    ctx.update(overrides)
    return Context(ctx)

from django.test import SimpleTestCase
from django.contrib.admin.templatetags.admin_modify import submit_row
from django.test import SimpleTestCase
from django.contrib.admin.templatetags.admin_modify import submit_row

def base_context():
    """
    Produces a baseline context representing a change form where:
    - the object is being changed (change=True)
    - the save_as feature is enabled (save_as=True)
    - the user has add permission but NOT change permission (has_add_permission=True, has_change_permission=False)
    - not a popup (is_popup=False)
    """
    return {'is_popup': False, 'save_as': True, 'has_view_permission': True, 'has_add_permission': True, 'has_change_permission': False, 'has_delete_permission': False, 'show_save': True, 'show_save_and_continue': True, 'show_save_and_add_another': True, 'show_delete': True, 'add': False, 'change': True, 'has_editable_inline_admin_formsets': False}