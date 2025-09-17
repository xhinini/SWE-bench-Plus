def _add_nested_function_tests():

    class NestedForFunctionTests:

        class A:

            class B:

                @classmethod
                def cm(cls):
                    pass

                @staticmethod
                def sm():
                    pass

        class A2:

            class B:

                class C:

                    @classmethod
                    def cm(cls):
                        pass

                    @staticmethod
                    def sm():
                        pass

        class A3:

            class B:

                class C:

                    class D:

                        @classmethod
                        def cm(cls):
                            pass
    return NestedForFunctionTests
from django.db.migrations import serializer as _serializer_module
from django.db.migrations.writer import MigrationWriter
import sys as _sys
_this_module = _sys.modules[__name__]
WriterTests = getattr(_this_module, 'WriterTests')
WriterTests.NestedForFunctionTests = _add_nested_function_tests()

def test_nested_two_level_classmethod(self):
    value = self.NestedForFunctionTests.A.B.cm
    expected = ('migrations.test_writer.WriterTests.NestedForFunctionTests.A.B.cm', {'import migrations.test_writer'})
    self.assertSerializedResultEqual(value, expected)

def test_nested_two_level_staticmethod(self):
    value = self.NestedForFunctionTests.A.B.sm
    expected = ('migrations.test_writer.WriterTests.NestedForFunctionTests.A.B.sm', {'import migrations.test_writer'})
    self.assertSerializedResultEqual(value, expected)

def test_nested_three_level_classmethod(self):
    value = self.NestedForFunctionTests.A2.B.C.cm
    expected = ('migrations.test_writer.WriterTests.NestedForFunctionTests.A2.B.C.cm', {'import migrations.test_writer'})
    self.assertSerializedResultEqual(value, expected)

def test_nested_three_level_staticmethod(self):
    value = self.NestedForFunctionTests.A2.B.C.sm
    expected = ('migrations.test_writer.WriterTests.NestedForFunctionTests.A2.B.C.sm', {'import migrations.test_writer'})
    self.assertSerializedResultEqual(value, expected)

def test_nested_four_level_classmethod(self):
    value = self.NestedForFunctionTests.A3.B.C.D.cm
    expected = ('migrations.test_writer.WriterTests.NestedForFunctionTests.A3.B.C.D.cm', {'import migrations.test_writer'})
    self.assertSerializedResultEqual(value, expected)

def test_classmethod_via_alias(self):
    Alias = self.NestedForFunctionTests.A.B
    value = Alias.cm
    expected = ('migrations.test_writer.WriterTests.NestedForFunctionTests.A.B.cm', {'import migrations.test_writer'})
    self.assertSerializedResultEqual(value, expected)

def test_staticmethod_via_alias(self):
    Alias = self.NestedForFunctionTests.A2.B.C
    value = Alias.sm
    expected = ('migrations.test_writer.WriterTests.NestedForFunctionTests.A2.B.C.sm', {'import migrations.test_writer'})
    self.assertSerializedResultEqual(value, expected)

def test_multiple_aliasing_and_access(self):
    Alias1 = self.NestedForFunctionTests.A2
    Alias2 = Alias1.B.C
    value = Alias2.cm
    expected = ('migrations.test_writer.WriterTests.NestedForFunctionTests.A2.B.C.cm', {'import migrations.test_writer'})
    self.assertSerializedResultEqual(value, expected)

def test_repeated_access_on_class(self):
    cls = self.NestedForFunctionTests.A3.B.C.D
    value = cls.cm
    expected = ('migrations.test_writer.WriterTests.NestedForFunctionTests.A3.B.C.D.cm', {'import migrations.test_writer'})
    self.assertSerializedResultEqual(value, expected)

def test_staticmethod_and_classmethod_different_results(self):
    cm_value = self.NestedForFunctionTests.A.B.cm
    sm_value = self.NestedForFunctionTests.A.B.sm
    expected_cm = ('migrations.test_writer.WriterTests.NestedForFunctionTests.A.B.cm', {'import migrations.test_writer'})
    expected_sm = ('migrations.test_writer.WriterTests.NestedForFunctionTests.A.B.sm', {'import migrations.test_writer'})
    self.assertSerializedResultEqual(cm_value, expected_cm)
    self.assertSerializedResultEqual(sm_value, expected_sm)
funcs = [test_nested_two_level_classmethod, test_nested_two_level_staticmethod, test_nested_three_level_classmethod, test_nested_three_level_staticmethod, test_nested_four_level_classmethod, test_classmethod_via_alias, test_staticmethod_via_alias, test_multiple_aliasing_and_access, test_repeated_access_on_class, test_staticmethod_and_classmethod_different_results]
for f in funcs:
    setattr(WriterTests, f.__name__, f)