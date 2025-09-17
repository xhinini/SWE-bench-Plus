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