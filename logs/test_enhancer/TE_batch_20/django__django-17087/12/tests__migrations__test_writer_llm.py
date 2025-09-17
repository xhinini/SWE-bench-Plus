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

def test_serialize_nested_class_method_two_levels(self):

    class Outer:

        class Inner:

            def method(self):
                return 'ok'
    module = Outer.Inner.__module__
    expected = ('%s.%s.%s' % (module, Outer.Inner.__qualname__, 'method'), {'import %s' % module})
    self.assertSerializedResultEqual(Outer.Inner.method, expected)

def test_serialize_nested_class_method_three_levels(self):

    class A:

        class B:

            class C:

                def foo(self):
                    return 'three'
    module = A.B.C.__module__
    expected = ('%s.%s.%s' % (module, A.B.C.__qualname__, 'foo'), {'import %s' % module})
    self.assertSerializedResultEqual(A.B.C.foo, expected)

def test_serialize_nested_class_method_four_levels(self):

    class L1:

        class L2:

            class L3:

                class L4:

                    def deep(self):
                        return 'deep'
    cls = L1.L2.L3.L4
    module = cls.__module__
    expected = ('%s.%s.%s' % (module, cls.__qualname__, 'deep'), {'import %s' % module})
    self.assertSerializedResultEqual(cls.deep, expected)

def test_serialize_nested_class_classmethod(self):

    class Out:

        class In:

            @classmethod
            def cm(cls):
                return 'cm'
    module = Out.In.__module__
    expected = ('%s.%s.%s' % (module, Out.In.__qualname__, 'cm'), {'import %s' % module})
    self.assertSerializedResultEqual(Out.In.cm, expected)

def test_serialize_nested_class_staticmethod(self):

    class Out2:

        class In2:

            @staticmethod
            def sm():
                return 'sm'
    module = Out2.In2.__module__
    expected = ('%s.%s.%s' % (module, Out2.In2.__qualname__, 'sm'), {'import %s' % module})
    self.assertSerializedResultEqual(Out2.In2.sm, expected)

def test_serialize_classmethod_three_levels(self):

    class X:

        class Y:

            class Z:

                @classmethod
                def cmethod(cls):
                    return 'c'
    cls = X.Y.Z
    module = cls.__module__
    expected = ('%s.%s.%s' % (module, cls.__qualname__, 'cmethod'), {'import %s' % module})
    self.assertSerializedResultEqual(cls.cmethod, expected)

def test_serialize_staticmethod_three_levels(self):

    class P:

        class Q:

            class R:

                @staticmethod
                def sstatic():
                    return 's'
    cls = P.Q.R
    module = cls.__module__
    expected = ('%s.%s.%s' % (module, cls.__qualname__, 'sstatic'), {'import %s' % module})
    self.assertSerializedResultEqual(cls.sstatic, expected)

def test_local_class_method_raises_value_error(self):

    def factory():

        class Local:

            def method(self):
                return 'local'
        return Local
    Local = factory()
    with self.assertRaisesMessage(ValueError, 'Could not find function method in migrations.test_writer'):
        from django.db.migrations.writer import MigrationWriter
        MigrationWriter.serialize(Local.method)

def test_local_class_classmethod_raises_value_error(self):

    def make():

        class Local2:

            @classmethod
            def cm(cls):
                return 'localcm'
        return Local2
    Local2 = make()
    with self.assertRaisesMessage(ValueError, 'Could not find function cm in migrations.test_writer'):
        from django.db.migrations.writer import MigrationWriter
        MigrationWriter.serialize(Local2.cm)

def test_nested_class_method_in_testcase_style(self):

    class OuterTC:

        class InnerTC:

            class InnerMost:

                def m(self):
                    return 'x'
    cls = OuterTC.InnerTC.InnerMost
    module = cls.__module__
    expected = ('%s.%s.%s' % (module, cls.__qualname__, 'm'), {'import %s' % module})
    self.assertSerializedResultEqual(cls.m, expected)

def _make_classmethod_class(qualname, method_name='cm'):
    """
    Create a class object with a classmethod attribute. The class and method
    objects are given a synthetic __qualname__ and __module__ to emulate
    nested classes defined in the migrations.test_writer module.
    """
    cls = type('X', (), {})

    def _method(cls):
        return None
    setattr(cls, method_name, classmethod(_method))
    cls.__qualname__ = qualname
    cls.__module__ = 'migrations.test_writer'
    return cls

def _make_regular_method_class(qualname, method_name='m'):
    """
    Create a class object with an unbound function (regular method) assigned
    as an attribute. The function's __qualname__ and __module__ are set to
    emulate a method defined on a nested class.
    """

    def _method(self):
        return None
    _method.__name__ = method_name
    _method.__qualname__ = '%s.%s' % (qualname, method_name)
    _method.__module__ = 'migrations.test_writer'
    cls = type('X', (), {method_name: _method})
    cls.__qualname__ = qualname
    cls.__module__ = 'migrations.test_writer'
    return cls

def _make_static_method_class(qualname, method_name='st'):
    """
    Create a class object with a staticmethod attribute. The underlying
    function's __qualname__ and __module__ emulate a nested path.
    """

    def _method():
        return None
    _method.__name__ = method_name
    _method.__qualname__ = '%s.%s' % (qualname, method_name)
    _method.__module__ = 'migrations.test_writer'
    cls = type('X', (), {method_name: staticmethod(_method)})
    cls.__qualname__ = qualname
    cls.__module__ = 'migrations.test_writer'
    return cls

def _make_bound_classmethod(qualname, module='migrations.test_writer', method_name='my_method'):
    """
    Create a class with a classmethod whose class __qualname__ and __module__
    are set to the provided values. Return the attribute from the class so
    the serializer sees a bound method (with __self__ being the class).
    """

    def impl(cls):
        return 'ok'
    cls = type(qualname.split('.')[-1], (), {})
    setattr(cls, method_name, classmethod(impl))
    cls.__qualname__ = qualname
    cls.__module__ = module
    return getattr(cls, method_name)