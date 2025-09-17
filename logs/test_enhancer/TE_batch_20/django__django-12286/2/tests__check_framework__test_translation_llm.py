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