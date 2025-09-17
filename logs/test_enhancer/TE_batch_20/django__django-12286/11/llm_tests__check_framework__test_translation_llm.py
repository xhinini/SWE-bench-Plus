import importlib
from unittest.mock import patch
import importlib
from unittest.mock import patch
from django.test import SimpleTestCase


class TranslationConsistencyReloadPatchTests(SimpleTestCase):
    def setUp(self):
        # Keep a reference to the module so we can reload it within tests.
        self.translation_mod = importlib.import_module('django.core.checks.translation')

    def tearDown(self):
        # Ensure the module is reloaded back to the unpatched state after each test.
        importlib.reload(self.translation_mod)

    def test_patch_raises_lookuperror_fr_language(self):
        with patch('django.utils.translation.get_supported_language_variant', side_effect=LookupError):
            importlib.reload(self.translation_mod)
            with self.settings(LANGUAGE_CODE='fr'):
                self.assertEqual(
                    self.translation_mod.check_language_settings_consistent(None),
                    [self.translation_mod.E004],
                )

    def test_patch_raises_lookuperror_en_us_language(self):
        with patch('django.utils.translation.get_supported_language_variant', side_effect=LookupError):
            importlib.reload(self.translation_mod)
            with self.settings(LANGUAGE_CODE='en-us'):
                self.assertEqual(
                    self.translation_mod.check_language_settings_consistent(None),
                    [self.translation_mod.E004],
                )

    def test_patch_raises_lookuperror_es_419_language(self):
        with patch('django.utils.translation.get_supported_language_variant', side_effect=LookupError):
            importlib.reload(self.translation_mod)
            with self.settings(LANGUAGE_CODE='es-419'):
                self.assertEqual(
                    self.translation_mod.check_language_settings_consistent(None),
                    [self.translation_mod.E004],
                )

    def test_patch_raises_lookuperror_zh_hans_language(self):
        with patch('django.utils.translation.get_supported_language_variant', side_effect=LookupError):
            importlib.reload(self.translation_mod)
            with self.settings(LANGUAGE_CODE='zh-Hans'):
                self.assertEqual(
                    self.translation_mod.check_language_settings_consistent(None),
                    [self.translation_mod.E004],
                )

    def test_patch_raises_lookuperror_ca_es_variant_language(self):
        with patch('django.utils.translation.get_supported_language_variant', side_effect=LookupError):
            importlib.reload(self.translation_mod)
            with self.settings(LANGUAGE_CODE='ca-ES-valencia'):
                self.assertEqual(
                    self.translation_mod.check_language_settings_consistent(None),
                    [self.translation_mod.E004],
                )

    # Variants using the patch as a decorator (still reload inside test)
    @patch('django.utils.translation.get_supported_language_variant', side_effect=LookupError)
    def test_decorator_patch_raises_lookuperror_it(self, _mock):
        importlib.reload(self.translation_mod)
        with self.settings(LANGUAGE_CODE='it'):
            self.assertEqual(
                self.translation_mod.check_language_settings_consistent(None),
                [self.translation_mod.E004],
            )

    @patch('django.utils.translation.get_supported_language_variant', side_effect=LookupError)
    def test_decorator_patch_raises_lookuperror_pt(self, _mock):
        importlib.reload(self.translation_mod)
        with self.settings(LANGUAGE_CODE='pt'):
            self.assertEqual(
                self.translation_mod.check_language_settings_consistent(None),
                [self.translation_mod.E004],
            )

    @patch('django.utils.translation.get_supported_language_variant', side_effect=LookupError)
    def test_decorator_patch_raises_lookuperror_ru(self, _mock):
        importlib.reload(self.translation_mod)
        with self.settings(LANGUAGE_CODE='ru'):
            self.assertEqual(
                self.translation_mod.check_language_settings_consistent(None),
                [self.translation_mod.E004],
            )

    @patch('django.utils.translation.get_supported_language_variant', side_effect=LookupError)
    def test_decorator_patch_raises_lookuperror_sv(self, _mock):
        importlib.reload(self.translation_mod)
        with self.settings(LANGUAGE_CODE='sv'):
            self.assertEqual(
                self.translation_mod.check_language_settings_consistent(None),
                [self.translation_mod.E004],
            )

    @patch('django.utils.translation.get_supported_language_variant', side_effect=LookupError)
    def test_decorator_patch_raises_lookuperror_ja(self, _mock):
        importlib.reload(self.translation_mod)
        with self.settings(LANGUAGE_CODE='ja'):
            self.assertEqual(
                self.translation_mod.check_language_settings_consistent(None),
                [self.translation_mod.E004],
            )

import importlib
from unittest.mock import patch
import importlib
from unittest.mock import patch
from django.test import SimpleTestCase

class TranslationConsistencyImportTests(SimpleTestCase):
    """
    Reload the django.core.checks.translation module with different
    behaviours patched onto django.utils.translation.get_supported_language_variant
    and django.utils.translation.trans_real.get_supported_language_variant,
    then assert the resulting behaviour of check_language_settings_consistent.
    """

    def _reload_checks_with(self, pub_side_effect=None, transreal_side_effect=None):
        """
        Helper to patch the public and trans_real get_supported_language_variant
        functions and reload the checks module so top-level imports are bound to
        the patched public function (when applicable).

        pub_side_effect / transreal_side_effect: if set to an exception class
        (e.g. LookupError) the patched function will raise that exception when
        called; if set to any other value it will be used as the return value.
        If None, the patched function returns 'ok' by default.
        """
        import django.utils.translation as translation
        import django.utils.translation.trans_real as trans_real
        if pub_side_effect is None:
            pub_patch = patch.object(translation, 'get_supported_language_variant', return_value='ok')
        elif isinstance(pub_side_effect, type) and issubclass(pub_side_effect, Exception):
            pub_patch = patch.object(translation, 'get_supported_language_variant', side_effect=pub_side_effect)
        else:
            pub_patch = patch.object(translation, 'get_supported_language_variant', return_value=pub_side_effect)
        if transreal_side_effect is None:
            trans_patch = patch.object(trans_real, 'get_supported_language_variant', return_value='ok')
        elif isinstance(transreal_side_effect, type) and issubclass(transreal_side_effect, Exception):
            trans_patch = patch.object(trans_real, 'get_supported_language_variant', side_effect=transreal_side_effect)
        else:
            trans_patch = patch.object(trans_real, 'get_supported_language_variant', return_value=transreal_side_effect)
        with pub_patch, trans_patch:
            return importlib.reload(importlib.import_module('django.core.checks.translation'))

    def test_public_ok_transreal_raises_fr(self):
        mod = self._reload_checks_with(pub_side_effect='ok', transreal_side_effect=LookupError)
        with self.settings(LANGUAGE_CODE='fr', LANGUAGES=[('en', 'English')]):
            self.assertEqual(mod.check_language_settings_consistent(None), [])

    def test_public_raises_transreal_ok_en_us(self):
        mod = self._reload_checks_with(pub_side_effect=LookupError, transreal_side_effect='ok')
        with self.settings(LANGUAGE_CODE='en-us', LANGUAGES=[('en', 'English')]):
            self.assertEqual(mod.check_language_settings_consistent(None), [mod.E004])

    def test_public_raises_transreal_ok_es_419(self):
        mod = self._reload_checks_with(pub_side_effect=LookupError, transreal_side_effect='ok')
        with self.settings(LANGUAGE_CODE='es-419', LANGUAGES=[('es', 'Spanish')]):
            self.assertEqual(mod.check_language_settings_consistent(None), [mod.E004])

    def test_public_ok_transreal_raises_zh_hans(self):
        mod = self._reload_checks_with(pub_side_effect='ok', transreal_side_effect=LookupError)
        with self.settings(LANGUAGE_CODE='zh-Hans', LANGUAGES=[('zh', 'Chinese')]):
            self.assertEqual(mod.check_language_settings_consistent(None), [])

    def test_public_raises_transreal_ok_sr_latn(self):
        mod = self._reload_checks_with(pub_side_effect=LookupError, transreal_side_effect='ok')
        with self.settings(LANGUAGE_CODE='sr-Latn', LANGUAGES=[('sr', 'Serbian')]):
            self.assertEqual(mod.check_language_settings_consistent(None), [mod.E004])

import sys
import types
from django.core.checks import Error
from django.core.checks.translation import check_language_settings_consistent
from django.test import SimpleTestCase, override_settings

class TranslationCheckMissingTransRealTests(SimpleTestCase):
    """
    Tests for check_language_settings_consistent that ensure a broken or missing
    django.utils.translation.trans_real (or missing get_supported_language_variant
    attribute on it) doesn't cause an exception and that the function returns
    the expected values. These catch the candidate patch which imports the
    function from django.utils.translation.trans_real inside the function.
    """

    def _inject_broken_trans_real(self):
        key = 'django.utils.translation.trans_real'
        original = sys.modules.get(key)
        sys.modules[key] = types.ModuleType(key)
        return (key, original)

    def test_inconsistent_language_settings_with_missing_trans_real_fr(self):
        msg = 'You have provided a value for the LANGUAGE_CODE setting that is not in the LANGUAGES setting.'
        key, original = self._inject_broken_trans_real()
        try:
            with self.settings(LANGUAGE_CODE='fr', LANGUAGES=[('en', 'English')]):
                self.assertEqual(check_language_settings_consistent(None), [Error(msg, id='translation.E004')])
        finally:
            self._restore_trans_real(key, original)

    def test_inconsistent_language_settings_with_missing_trans_real_zh(self):
        msg = 'You have provided a value for the LANGUAGE_CODE setting that is not in the LANGUAGES setting.'
        key, original = self._inject_broken_trans_real()
        try:
            with self.settings(LANGUAGE_CODE='zh-Hans', LANGUAGES=[('en', 'English')]):
                self.assertEqual(check_language_settings_consistent(None), [Error(msg, id='translation.E004')])
        finally:
            self._restore_trans_real(key, original)

    def test_inconsistent_language_settings_with_missing_trans_real_es(self):
        msg = 'You have provided a value for the LANGUAGE_CODE setting that is not in the LANGUAGES setting.'
        key, original = self._inject_broken_trans_real()
        try:
            with self.settings(LANGUAGE_CODE='es-419', LANGUAGES=[('en', 'English')]):
                self.assertEqual(check_language_settings_consistent(None), [Error(msg, id='translation.E004')])
        finally:
            self._restore_trans_real(key, original)

    def test_consistent_language_settings_with_missing_trans_real_en(self):
        key, original = self._inject_broken_trans_real()
        try:
            with self.settings(LANGUAGE_CODE='en', LANGUAGES=[('en', 'English')]):
                self.assertEqual(check_language_settings_consistent(None), [])
        finally:
            self._restore_trans_real(key, original)

    def test_consistent_language_settings_with_missing_trans_real_en_us(self):
        key, original = self._inject_broken_trans_real()
        try:
            with self.settings(LANGUAGE_CODE='en-us', LANGUAGES=[('en-us', 'English (US)')]):
                self.assertEqual(check_language_settings_consistent(None), [])
        finally:
            self._restore_trans_real(key, original)

    def test_consistent_language_settings_with_missing_trans_real_es(self):
        key, original = self._inject_broken_trans_real()
        try:
            with self.settings(LANGUAGE_CODE='es', LANGUAGES=[('es', 'Español')]):
                self.assertEqual(check_language_settings_consistent(None), [])
        finally:
            self._restore_trans_real(key, original)

    def test_inconsistent_language_settings_with_missing_trans_real_sv(self):
        msg = 'You have provided a value for the LANGUAGE_CODE setting that is not in the LANGUAGES setting.'
        key, original = self._inject_broken_trans_real()
        try:
            with self.settings(LANGUAGE_CODE='sv', LANGUAGES=[('en', 'English')]):
                self.assertEqual(check_language_settings_consistent(None), [Error(msg, id='translation.E004')])
        finally:
            self._restore_trans_real(key, original)

    def test_inconsistent_language_settings_with_missing_trans_real_pt(self):
        msg = 'You have provided a value for the LANGUAGE_CODE setting that is not in the LANGUAGES setting.'
        key, original = self._inject_broken_trans_real()
        try:
            with self.settings(LANGUAGE_CODE='pt', LANGUAGES=[('en', 'English')]):
                self.assertEqual(check_language_settings_consistent(None), [Error(msg, id='translation.E004')])
        finally:
            self._restore_trans_real(key, original)

    def test_consistent_language_settings_with_missing_trans_real_fr_fr(self):
        key, original = self._inject_broken_trans_real()
        try:
            with self.settings(LANGUAGE_CODE='fr-FR', LANGUAGES=[('fr-FR', 'Français (France)')]):
                self.assertEqual(check_language_settings_consistent(None), [])
        finally:
            self._restore_trans_real(key, original)

    def test_consistent_language_settings_with_missing_trans_real_custom_variant(self):
        key, original = self._inject_broken_trans_real()
        try:
            with self.settings(LANGUAGE_CODE='ca-ES-valencia', LANGUAGES=[('ca-ES-valencia', 'Valencià')]):
                self.assertEqual(check_language_settings_consistent(None), [])
        finally:
            self._restore_trans_real(key, original)

import importlib
import sys
import types
from django.core.checks import Error
from django.test import SimpleTestCase, override_settings

class TranslationConsistencyImportTests(SimpleTestCase):
    FALLBACK_SUPPORTED = {'en': 'en', 'en-us': 'en-us', 'fr': 'fr', 'fr-ca': 'fr-ca', 'zh-hans': 'zh-hans', 'es-419': 'es-419', 'ca-es-valencia': 'ca-es-valencia', 'sgn-ase': 'sgn-ase', 'mas': 'mas'}

    def _make_fallback_get_supported_language_variant(self):

        def get_supported_language_variant(tag):
            if not isinstance(tag, str):
                raise LookupError
            key = tag.lower()
            if key in self.FALLBACK_SUPPORTED:
                return self.FALLBACK_SUPPORTED[key]
            raise LookupError
        return get_supported_language_variant

import importlib
from django.utils import translation
import django.core.checks.translation as checks_mod
from django.test import SimpleTestCase, override_settings
from django.utils import translation
import importlib
import django.core.checks.translation as checks_mod

class TranslationGetSupportedVariantRegressionTests(SimpleTestCase):

    def setUp(self):
        self._orig_get_supported = translation.get_supported_language_variant

    def tearDown(self):
        translation.get_supported_language_variant = self._orig_get_supported
        importlib.reload(checks_mod)

    def test_en_reports_inconsistency_when_stub_rejects_it(self):
        self._assert_E004_for('en')

    def test_en_us_reports_inconsistency_when_stub_rejects_it(self):
        self._assert_E004_for('en-us')

    def test_fr_reports_inconsistency_when_stub_rejects_it(self):
        self._assert_E004_for('fr')

    def test_fr_ca_reports_inconsistency_when_stub_rejects_it(self):
        self._assert_E004_for('fr-CA')

    def test_zh_hans_reports_inconsistency_when_stub_rejects_it(self):
        self._assert_E004_for('zh-Hans')

    def test_es_419_reports_inconsistency_when_stub_rejects_it(self):
        self._assert_E004_for('es-419')

    def test_ca_es_valencia_reports_inconsistency_when_stub_rejects_it(self):
        self._assert_E004_for('ca-ES-valencia')

    def test_multiple_reloads_with_stub_rejecting_en(self):
        with self.settings(LANGUAGE_CODE='en'):

            def stub(code):
                raise LookupError('unsupported: %r' % (code,))
            translation.get_supported_language_variant = stub
            importlib.reload(checks_mod)
            importlib.reload(checks_mod)
            from django.core.checks.translation import check_language_settings_consistent, E004
            self.assertEqual(check_language_settings_consistent(None), [E004])

import builtins
from unittest import mock
from unittest import mock
import builtins
from django.core.checks import Error
from django.core.checks.translation import check_language_settings_consistent
from django.test import SimpleTestCase

class TranslationImportResilienceTests(SimpleTestCase):
    E004_msg = 'You have provided a value for the LANGUAGE_CODE setting that is not in the LANGUAGES setting.'

    def _block_trans_real_imports(self):
        real_import = builtins.__import__

        def fake_import(name, globals=None, locals=None, fromlist=(), level=0):
            if name.endswith('.trans_real') or (fromlist and 'trans_real' in name):
                raise ImportError('simulated missing trans_real')
            return real_import(name, globals, locals, fromlist, level)
        return mock.patch('builtins.__import__', side_effect=fake_import)

    def test_supported_language_exact_match_with_trans_real_blocked(self):
        with self._block_trans_real_imports():
            with self.settings(LANGUAGE_CODE='en', LANGUAGES=[('en', 'English')]):
                self.assertEqual(check_language_settings_consistent(None), [])

    def test_supported_language_region_match_with_trans_real_blocked(self):
        with self._block_trans_real_imports():
            with self.settings(LANGUAGE_CODE='fr-CA', LANGUAGES=[('fr-CA', 'Français (CA)')]):
                self.assertEqual(check_language_settings_consistent(None), [])

    def test_supported_language_fallback_base_language_with_trans_real_blocked(self):
        with self._block_trans_real_imports():
            with self.settings(LANGUAGE_CODE='en-us', LANGUAGES=[('en', 'English')]):
                self.assertEqual(check_language_settings_consistent(None), [])

    def test_inconsistent_language_simple_with_trans_real_blocked(self):
        with self._block_trans_real_imports():
            with self.settings(LANGUAGE_CODE='fr', LANGUAGES=[('en', 'English')]):
                self.assertEqual(check_language_settings_consistent(None), [Error(self.E004_msg, id='translation.E004')])

    def test_supported_complex_tag_with_trans_real_blocked(self):
        with self._block_trans_real_imports():
            with self.settings(LANGUAGE_CODE='ca-ES-valencia', LANGUAGES=[('ca-ES-valencia', 'Català (València)')]):
                self.assertEqual(check_language_settings_consistent(None), [])

    def test_supported_script_tag_with_trans_real_blocked(self):
        with self._block_trans_real_imports():
            with self.settings(LANGUAGE_CODE='zh-Hans', LANGUAGES=[('zh-Hans', 'Chinese (Simplified)')]):
                self.assertEqual(check_language_settings_consistent(None), [])

    def test_inconsistent_when_no_languages_listed_with_trans_real_blocked(self):
        with self._block_trans_real_imports():
            with self.settings(LANGUAGE_CODE='en', LANGUAGES=[]):
                self.assertEqual(check_language_settings_consistent(None), [Error(self.E004_msg, id='translation.E004')])

    def test_supported_when_multiple_languages_present_with_trans_real_blocked(self):
        with self._block_trans_real_imports():
            with self.settings(LANGUAGE_CODE='fr-CA', LANGUAGES=[('en', 'English'), ('fr-CA', 'Français (CA)')]):
                self.assertEqual(check_language_settings_consistent(None), [])