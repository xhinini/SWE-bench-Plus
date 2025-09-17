def test_readonly_nonexistent_index_one_modeladmin(self):

    class XAdmin(admin.ModelAdmin):
        readonly_fields = ('title', 'missing_field_two')
    errors = XAdmin(Song, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[1]' refers to 'missing_field_two', which is not a callable, an attribute of 'XAdmin', or an attribute of 'admin_checks.Song'.", obj=XAdmin, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_readonly_nonexistent_list_modeladmin(self):

    class YAdmin(admin.ModelAdmin):
        readonly_fields = ['does_not_exist']
    errors = YAdmin(Song, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[0]' refers to 'does_not_exist', which is not a callable, an attribute of 'YAdmin', or an attribute of 'admin_checks.Song'.", obj=YAdmin, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_readonly_nonexistent_tabular_inline(self):

    class MissingFieldInline(admin.TabularInline):
        model = City
        readonly_fields = ['not_here']
    errors = MissingFieldInline(State, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[0]' refers to 'not_here', which is not a callable, an attribute of 'MissingFieldInline', or an attribute of 'admin_checks.City'.", obj=MissingFieldInline, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_readonly_nonexistent_stacked_inline(self):

    class OtherMissingFieldInline(admin.StackedInline):
        model = City
        readonly_fields = ('absent_field',)
    errors = OtherMissingFieldInline(State, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[0]' refers to 'absent_field', which is not a callable, an attribute of 'OtherMissingFieldInline', or an attribute of 'admin_checks.City'.", obj=OtherMissingFieldInline, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_readonly_multiple_missing_fields_modeladmin(self):

    class MultiMissingAdmin(admin.ModelAdmin):
        readonly_fields = ('nope1', 'nope2')
    errors = MultiMissingAdmin(Song, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[0]' refers to 'nope1', which is not a callable, an attribute of 'MultiMissingAdmin', or an attribute of 'admin_checks.Song'.", obj=MultiMissingAdmin, id='admin.E035'), checks.Error("The value of 'readonly_fields[1]' refers to 'nope2', which is not a callable, an attribute of 'MultiMissingAdmin', or an attribute of 'admin_checks.Song'.", obj=MultiMissingAdmin, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_readonly_missing_field_custom_admin_name(self):

    class CustomNamedAdmin(admin.ModelAdmin):
        readonly_fields = ['missing_custom']
    errors = CustomNamedAdmin(Song, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[0]' refers to 'missing_custom', which is not a callable, an attribute of 'CustomNamedAdmin', or an attribute of 'admin_checks.Song'.", obj=CustomNamedAdmin, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_readonly_missing_field_inline_multiple_indices(self):

    class InlineMultiMissing(admin.TabularInline):
        model = City
        readonly_fields = ('one_missing', 'two_missing')
    errors = InlineMultiMissing(State, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[0]' refers to 'one_missing', which is not a callable, an attribute of 'InlineMultiMissing', or an attribute of 'admin_checks.City'.", obj=InlineMultiMissing, id='admin.E035'), checks.Error("The value of 'readonly_fields[1]' refers to 'two_missing', which is not a callable, an attribute of 'InlineMultiMissing', or an attribute of 'admin_checks.City'.", obj=InlineMultiMissing, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_readonly_missing_field_index_zero_modeladmin_list(self):

    class ListAdmin(admin.ModelAdmin):
        readonly_fields = ['missing_zero']
    errors = ListAdmin(Song, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[0]' refers to 'missing_zero', which is not a callable, an attribute of 'ListAdmin', or an attribute of 'admin_checks.Song'.", obj=ListAdmin, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_readonly_missing_field_on_different_model(self):

    class BookMissingAdmin(admin.ModelAdmin):
        readonly_fields = ('no_book_field',)
    errors = BookMissingAdmin(Book, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[0]' refers to 'no_book_field', which is not a callable, an attribute of 'BookMissingAdmin', or an attribute of 'admin_checks.Book'.", obj=BookMissingAdmin, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_readonly_missing_field_dynamic_class_name(self):

    class DynamicNamedAdmin(admin.ModelAdmin):
        readonly_fields = ('dyn_missing',)
    errors = DynamicNamedAdmin(Song, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[0]' refers to 'dyn_missing', which is not a callable, an attribute of 'DynamicNamedAdmin', or an attribute of 'admin_checks.Song'.", obj=DynamicNamedAdmin, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_readonly_missing_field_index_zero(self):

    class MissingIndexZeroAdmin(admin.ModelAdmin):
        readonly_fields = ('does_not_exist',)
    errors = MissingIndexZeroAdmin(Song, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[0]' refers to 'does_not_exist', which is not a callable, an attribute of 'MissingIndexZeroAdmin', or an attribute of 'admin_checks.Song'.", obj=MissingIndexZeroAdmin, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_readonly_missing_field_index_one(self):

    class MissingIndexOneAdmin(admin.ModelAdmin):
        readonly_fields = ('title', 'missing_one')
    errors = MissingIndexOneAdmin(Song, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[1]' refers to 'missing_one', which is not a callable, an attribute of 'MissingIndexOneAdmin', or an attribute of 'admin_checks.Song'.", obj=MissingIndexOneAdmin, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_readonly_missing_field_on_custom_named_admin(self):

    class CustomNamedAdmin(admin.ModelAdmin):
        readonly_fields = ('no_such_field',)
    errors = CustomNamedAdmin(Song, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[0]' refers to 'no_such_field', which is not a callable, an attribute of 'CustomNamedAdmin', or an attribute of 'admin_checks.Song'.", obj=CustomNamedAdmin, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_readonly_missing_field_on_inline_index_two(self):

    class InlineMissingFields(admin.TabularInline):
        model = City
        readonly_fields = ['a', 'b', 'missing_inline']
    errors = InlineMissingFields(State, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[2]' refers to 'missing_inline', which is not a callable, an attribute of 'InlineMissingFields', or an attribute of 'admin_checks.City'.", obj=InlineMissingFields, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_readonly_missing_field_inherited_admin_name_in_message(self):

    class BaseAdmin(admin.ModelAdmin):
        pass

    class InheritedAdmin(BaseAdmin):
        readonly_fields = ('missing_in_inherited',)
    errors = InheritedAdmin(Song, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[0]' refers to 'missing_in_inherited', which is not a callable, an attribute of 'InheritedAdmin', or an attribute of 'admin_checks.Song'.", obj=InheritedAdmin, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_readonly_missing_field_multiple_on_modeladmin(self):

    class MultipleMissingAdmin(admin.ModelAdmin):
        readonly_fields = ('missing_a', 'missing_b', 'missing_c')
    errors = MultipleMissingAdmin(Song, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[0]' refers to 'missing_a', which is not a callable, an attribute of 'MultipleMissingAdmin', or an attribute of 'admin_checks.Song'.", obj=MultipleMissingAdmin, id='admin.E035'), checks.Error("The value of 'readonly_fields[1]' refers to 'missing_b', which is not a callable, an attribute of 'MultipleMissingAdmin', or an attribute of 'admin_checks.Song'.", obj=MultipleMissingAdmin, id='admin.E035'), checks.Error("The value of 'readonly_fields[2]' refers to 'missing_c', which is not a callable, an attribute of 'MultipleMissingAdmin', or an attribute of 'admin_checks.Song'.", obj=MultipleMissingAdmin, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_readonly_missing_field_on_tabular_inline_shows_inline_class_name(self):

    class CityInlineMissing(admin.TabularInline):
        model = City
        readonly_fields = ('no_city_field',)
    errors = CityInlineMissing(State, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[0]' refers to 'no_city_field', which is not a callable, an attribute of 'CityInlineMissing', or an attribute of 'admin_checks.City'.", obj=CityInlineMissing, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_readonly_missing_field_on_stacked_inline_shows_inline_class_name(self):

    class CityStackedInlineMissing(admin.StackedInline):
        model = City
        readonly_fields = ('no_city_stacked',)
    errors = CityStackedInlineMissing(State, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[0]' refers to 'no_city_stacked', which is not a callable, an attribute of 'CityStackedInlineMissing', or an attribute of 'admin_checks.City'.", obj=CityStackedInlineMissing, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_readonly_missing_field_label_and_fieldname_with_special_chars(self):

    class SpecialCharsAdmin(admin.ModelAdmin):
        readonly_fields = ('missing_field_123',)
    errors = SpecialCharsAdmin(Song, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[0]' refers to 'missing_field_123', which is not a callable, an attribute of 'SpecialCharsAdmin', or an attribute of 'admin_checks.Song'.", obj=SpecialCharsAdmin, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_missing_readonly_field_message_contains_fieldname_single(self):

    class SongAdmin(admin.ModelAdmin):
        readonly_fields = ('nonexistent_field',)
    errors = SongAdmin(Song, AdminSite()).check()
    self.assertEqual(len(errors), 1)
    err = errors[0]
    self.assertEqual(err.id, 'admin.E035')
    self.assertIn('nonexistent_field', err.msg)
    self.assertIn('readonly_fields[0]', err.msg)

def test_missing_readonly_fields_message_contains_fieldnames_multiple(self):

    class SongAdmin(admin.ModelAdmin):
        readonly_fields = ('missing_one', 'missing_two', 'missing_three')
    errors = SongAdmin(Song, AdminSite()).check()
    self.assertEqual(len(errors), 3)
    msgs = [e.msg for e in errors]
    self.assertTrue(any(('missing_one' in m for m in msgs)))
    self.assertTrue(any(('missing_two' in m for m in msgs)))
    self.assertTrue(any(('missing_three' in m for m in msgs)))
    self.assertTrue(any(('readonly_fields[0]' in m for m in msgs)))
    self.assertTrue(any(('readonly_fields[1]' in m for m in msgs)))
    self.assertTrue(any(('readonly_fields[2]' in m for m in msgs)))

def test_inline_missing_readonly_field_message_contains_fieldname_single(self):

    class CityInline(admin.TabularInline):
        model = City
        readonly_fields = ['does_not_exist']
    errors = CityInline(State, AdminSite()).check()
    self.assertEqual(len(errors), 1)
    err = errors[0]
    self.assertEqual(err.id, 'admin.E035')
    self.assertIn('does_not_exist', err.msg)
    self.assertIn('readonly_fields[0]', err.msg)

def test_inline_missing_readonly_fields_message_contains_fieldnames_multiple(self):

    class CityInline(admin.TabularInline):
        model = City
        readonly_fields = ['nope_one', 'nope_two']
    errors = CityInline(State, AdminSite()).check()
    self.assertEqual(len(errors), 2)
    msgs = [e.msg for e in errors]
    self.assertTrue(any(('nope_one' in m for m in msgs)))
    self.assertTrue(any(('nope_two' in m for m in msgs)))
    self.assertTrue(any(('readonly_fields[0]' in m for m in msgs)))
    self.assertTrue(any(('readonly_fields[1]' in m for m in msgs)))

def test_property_readonly_fields_missing_field_contains_name(self):

    class SongAdmin(admin.ModelAdmin):

        @property
        def readonly_fields(self):
            return ('prop_missing',)
    errors = SongAdmin(Song, AdminSite()).check()
    self.assertEqual(len(errors), 1)
    err = errors[0]
    self.assertEqual(err.id, 'admin.E035')
    self.assertIn('prop_missing', err.msg)
    self.assertIn('readonly_fields[0]', err.msg)

def test_readonly_missing_field_index_label_in_message(self):

    class SongAdmin(admin.ModelAdmin):
        readonly_fields = ('a', 'b', 'the_missing_one')
    errors = SongAdmin(Song, AdminSite()).check()
    found = False
    for e in errors:
        if 'readonly_fields[2]' in e.msg:
            self.assertIn('the_missing_one', e.msg)
            found = True
    self.assertTrue(errors)

def test_readonly_field_message_includes_model_label_and_fieldname_exact(self):

    class SongAdmin(admin.ModelAdmin):
        readonly_fields = ('title', 'missing_exact')
    errors = SongAdmin(Song, AdminSite()).check()
    for e in errors:
        if 'missing_exact' in e.msg:
            expected = "The value of 'readonly_fields[1]' refers to 'missing_exact', which is not a callable, an attribute of 'SongAdmin', or an attribute of 'admin_checks.Song'."
            self.assertEqual(e.msg, expected)
            self.assertEqual(e.id, 'admin.E035')
            break
    else:
        self.fail("Expected error for 'missing_exact' not found.")

def test_readonly_inline_message_contains_inline_classname_and_field(self):

    class CityInline(admin.TabularInline):
        model = City
        readonly_fields = ['bogus_field']
    errors = CityInline(State, AdminSite()).check()
    self.assertEqual(len(errors), 1)
    e = errors[0]
    self.assertIn('bogus_field', e.msg)
    self.assertIn('readonly_fields[0]', e.msg)
    self.assertEqual(e.id, 'admin.E035')

def test_readonly_fields_missing_with_callable_name_collision_still_includes_field(self):

    class SongAdmin(admin.ModelAdmin):
        readonly_fields = ('display',)
    errors = SongAdmin(Song, AdminSite()).check()
    self.assertEqual(len(errors), 1)
    err = errors[0]
    self.assertEqual(err.id, 'admin.E035')
    self.assertIn('display', err.msg)
    self.assertIn('readonly_fields[0]', err.msg)

def test_nonexistent_field_index_zero_message(self):

    class SongAdmin(admin.ModelAdmin):
        readonly_fields = ('i_do_not_exist',)
    errors = SongAdmin(Song, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[0]' refers to 'i_do_not_exist', which is not a callable, an attribute of 'SongAdmin', or an attribute of 'admin_checks.Song'.", obj=SongAdmin, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_nonexistent_field_list_type_message(self):

    class SongAdmin(admin.ModelAdmin):
        readonly_fields = ['i_do_not_exist_list']
    errors = SongAdmin(Song, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[0]' refers to 'i_do_not_exist_list', which is not a callable, an attribute of 'SongAdmin', or an attribute of 'admin_checks.Song'.", obj=SongAdmin, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_multiple_readonly_fields_second_index_message(self):

    class SongAdmin(admin.ModelAdmin):
        readonly_fields = ('title', 'missing_second')
    errors = SongAdmin(Song, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[1]' refers to 'missing_second', which is not a callable, an attribute of 'SongAdmin', or an attribute of 'admin_checks.Song'.", obj=SongAdmin, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_readonly_fields_from_property_message(self):

    class SongAdmin(admin.ModelAdmin):

        @property
        def readonly_fields(self):
            return ('prop_missing',)
    errors = SongAdmin(Song, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[0]' refers to 'prop_missing', which is not a callable, an attribute of 'SongAdmin', or an attribute of 'admin_checks.Song'.", obj=SongAdmin, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_nonexistent_field_on_tabular_inline_message(self):

    class MyInline(admin.TabularInline):
        model = City
        readonly_fields = ['dont_exist_inline']
    errors = MyInline(State, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[0]' refers to 'dont_exist_inline', which is not a callable, an attribute of 'MyInline', or an attribute of 'admin_checks.City'.", obj=MyInline, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_inherited_modeladmin_nonexistent_field_message(self):

    class ParentAdmin(admin.ModelAdmin):
        pass

    class ChildAdmin(ParentAdmin):
        readonly_fields = ('child_missing',)
    errors = ChildAdmin(Song, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[0]' refers to 'child_missing', which is not a callable, an attribute of 'ChildAdmin', or an attribute of 'admin_checks.Song'.", obj=ChildAdmin, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_tabular_inline_classname_in_message(self):

    class CitiesInline(admin.TabularInline):
        model = City
        readonly_fields = ['nope_city']
    errors = CitiesInline(State, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[0]' refers to 'nope_city', which is not a callable, an attribute of 'CitiesInline', or an attribute of 'admin_checks.City'.", obj=CitiesInline, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_readonly_callable_no_error(self):

    @admin.display
    def display_fn(obj):
        return 'x'

    class SongAdmin(admin.ModelAdmin):
        readonly_fields = (display_fn,)
    errors = SongAdmin(Song, AdminSite()).check()
    self.assertEqual(errors, [])

def test_readonly_field_on_model_attribute_no_error(self):

    class SongAdmin(admin.ModelAdmin):
        readonly_fields = ('title',)
    errors = SongAdmin(Song, AdminSite()).check()
    self.assertEqual(errors, [])

def test_nonexistent_field_complex_class_name_message(self):

    class ComplexAdminName123(admin.ModelAdmin):
        readonly_fields = ('complex_missing',)
    errors = ComplexAdminName123(Song, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[0]' refers to 'complex_missing', which is not a callable, an attribute of 'ComplexAdminName123', or an attribute of 'admin_checks.Song'.", obj=ComplexAdminName123, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_missing_readonly_field_includes_field_name_modeladmin(self):

    class MissingFieldAdmin(admin.ModelAdmin):
        readonly_fields = ('does_not_exist',)
    errors = MissingFieldAdmin(Song, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[0]' refers to 'does_not_exist', which is not a callable, an attribute of 'MissingFieldAdmin', or an attribute of 'admin_checks.Song'.", obj=MissingFieldAdmin, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_missing_readonly_field_includes_field_name_tabularinline(self):

    class CityInlineMissing(admin.TabularInline):
        model = City
        readonly_fields = ['no_such_field']
    errors = CityInlineMissing(State, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[0]' refers to 'no_such_field', which is not a callable, an attribute of 'CityInlineMissing', or an attribute of 'admin_checks.City'.", obj=CityInlineMissing, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_multiple_missing_readonly_fields_have_correct_labels_and_field_names(self):

    class MultiMissingAdmin(admin.ModelAdmin):
        readonly_fields = ('title', 'missing_one', 'missing_two')
    errors = MultiMissingAdmin(Song, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[1]' refers to 'missing_one', which is not a callable, an attribute of 'MultiMissingAdmin', or an attribute of 'admin_checks.Song'.", obj=MultiMissingAdmin, id='admin.E035'), checks.Error("The value of 'readonly_fields[2]' refers to 'missing_two', which is not a callable, an attribute of 'MultiMissingAdmin', or an attribute of 'admin_checks.Song'.", obj=MultiMissingAdmin, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_missing_readonly_field_message_includes_admin_class_name(self):

    class CustomAdminName(admin.ModelAdmin):
        readonly_fields = ('absent_field',)
    errors = CustomAdminName(Song, AdminSite()).check()
    self.assertEqual(errors, [checks.Error("The value of 'readonly_fields[0]' refers to 'absent_field', which is not a callable, an attribute of 'CustomAdminName', or an attribute of 'admin_checks.Song'.", obj=CustomAdminName, id='admin.E035')])

def test_missing_readonly_field_message_includes_model_label(self):

    class ModelLabelAdmin(admin.ModelAdmin):
        readonly_fields = ('nope_field',)
    errors = ModelLabelAdmin(Song, AdminSite()).check()
    self.assertEqual(errors, [checks.Error("The value of 'readonly_fields[0]' refers to 'nope_field', which is not a callable, an attribute of 'ModelLabelAdmin', or an attribute of 'admin_checks.Song'.", obj=ModelLabelAdmin, id='admin.E035')])

def test_multiple_missing_readonly_fields_order_and_labels_for_inline(self):

    class InlineMultiMissing(admin.TabularInline):
        model = City
        readonly_fields = ('first_missing', 'second_missing')
    errors = InlineMultiMissing(State, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[0]' refers to 'first_missing', which is not a callable, an attribute of 'InlineMultiMissing', or an attribute of 'admin_checks.City'.", obj=InlineMultiMissing, id='admin.E035'), checks.Error("The value of 'readonly_fields[1]' refers to 'second_missing', which is not a callable, an attribute of 'InlineMultiMissing', or an attribute of 'admin_checks.City'.", obj=InlineMultiMissing, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_missing_readonly_field_at_higher_index(self):

    class HighIndexAdmin(admin.ModelAdmin):
        readonly_fields = ('ok_field', 'also_ok', 'missing_at_two')
    errors = HighIndexAdmin(Song, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[2]' refers to 'missing_at_two', which is not a callable, an attribute of 'HighIndexAdmin', or an attribute of 'admin_checks.Song'.", obj=HighIndexAdmin, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_missing_readonly_fields_with_similar_names_do_not_confuse_labels(self):

    class SimilarNamesAdmin(admin.ModelAdmin):
        readonly_fields = ('field', 'field_extra_missing', 'field')
    errors = SimilarNamesAdmin(Song, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[1]' refers to 'field_extra_missing', which is not a callable, an attribute of 'SimilarNamesAdmin', or an attribute of 'admin_checks.Song'.", obj=SimilarNamesAdmin, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_missing_readonly_field_on_inline_class_with_custom_name(self):

    class FancyInline(admin.StackedInline):
        model = City
        readonly_fields = ('completely_missing',)
    errors = FancyInline(State, AdminSite()).check()
    self.assertEqual(errors, [checks.Error("The value of 'readonly_fields[0]' refers to 'completely_missing', which is not a callable, an attribute of 'FancyInline', or an attribute of 'admin_checks.City'.", obj=FancyInline, id='admin.E035')])

def test_readonly_missing_field_message_includes_field_name_index_two(self):

    class SongAdmin(admin.ModelAdmin):
        readonly_fields = ('title', 'original_release', 'not_a_field')
    errors = SongAdmin(Song, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[2]' refers to 'not_a_field', which is not a callable, an attribute of 'SongAdmin', or an attribute of 'admin_checks.Song'.", obj=SongAdmin, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_readonly_missing_field_message_on_inline_index_one(self):

    class CityInline(admin.TabularInline):
        model = City
        readonly_fields = ['name', 'i_dont_exist']
    errors = CityInline(State, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[1]' refers to 'i_dont_exist', which is not a callable, an attribute of 'CityInline', or an attribute of 'admin_checks.City'.", obj=CityInline, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_readonly_missing_field_message_tuple_single_item(self):

    class SongAdmin(admin.ModelAdmin):
        readonly_fields = ('completely_missing',)
    errors = SongAdmin(Song, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[0]' refers to 'completely_missing', which is not a callable, an attribute of 'SongAdmin', or an attribute of 'admin_checks.Song'.", obj=SongAdmin, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_readonly_missing_field_message_multiple_missing_fields(self):

    class SongAdmin(admin.ModelAdmin):
        readonly_fields = ('does_not_exist', 'also_missing')
    errors = SongAdmin(Song, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[0]' refers to 'does_not_exist', which is not a callable, an attribute of 'SongAdmin', or an attribute of 'admin_checks.Song'.", obj=SongAdmin, id='admin.E035'), checks.Error("The value of 'readonly_fields[1]' refers to 'also_missing', which is not a callable, an attribute of 'SongAdmin', or an attribute of 'admin_checks.Song'.", obj=SongAdmin, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_readonly_missing_field_message_with_admin_dynamic_getattr(self):

    class SongAdmin(admin.ModelAdmin):
        readonly_fields = ('missing_dynamic',)

        def __getattr__(self, item):
            if item == 'other_dynamic':

                @admin.display
                def method(obj):
                    pass
                return method
            raise AttributeError
    errors = SongAdmin(Song, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[0]' refers to 'missing_dynamic', which is not a callable, an attribute of 'SongAdmin', or an attribute of 'admin_checks.Song'.", obj=SongAdmin, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_readonly_missing_field_message_on_custom_inline_class(self):

    class CustomInline(admin.StackedInline):
        model = City
        readonly_fields = ('nope_field',)
    errors = CustomInline(State, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[0]' refers to 'nope_field', which is not a callable, an attribute of 'CustomInline', or an attribute of 'admin_checks.City'.", obj=CustomInline, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_readonly_missing_field_message_when_model_has_similar_attr(self):

    class TempModel:
        pass

    class SongAdmin(admin.ModelAdmin):
        readonly_fields = ('similar_but_missing',)
    errors = SongAdmin(Song, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[0]' refers to 'similar_but_missing', which is not a callable, an attribute of 'SongAdmin', or an attribute of 'admin_checks.Song'.", obj=SongAdmin, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_readonly_missing_field_message_for_index_zero_and_different_admin_name(self):

    class AnotherNameAdmin(admin.ModelAdmin):
        readonly_fields = ['no_field_here']
    errors = AnotherNameAdmin(Song, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[0]' refers to 'no_field_here', which is not a callable, an attribute of 'AnotherNameAdmin', or an attribute of 'admin_checks.Song'.", obj=AnotherNameAdmin, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_readonly_missing_field_message_with_mixed_types(self):

    class SongAdmin(admin.ModelAdmin):
        readonly_fields = ['title', 'still_missing', lambda obj: 'ok']
    errors = SongAdmin(Song, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[1]' refers to 'still_missing', which is not a callable, an attribute of 'SongAdmin', or an attribute of 'admin_checks.Song'.", obj=SongAdmin, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_nonexistent_field_index0_includes_field_name(self):

    class SongAdminIndex0(admin.ModelAdmin):
        readonly_fields = ('no_such_field',)
    errors = SongAdminIndex0(Song, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[0]' refers to 'no_such_field', which is not a callable, an attribute of 'SongAdminIndex0', or an attribute of 'admin_checks.Song'.", obj=SongAdminIndex0, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_nonexistent_field_index2_includes_field_name(self):

    class SongAdminIndex2(admin.ModelAdmin):
        readonly_fields = ('title', 'album', 'missing_three')
    errors = SongAdminIndex2(Song, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[2]' refers to 'missing_three', which is not a callable, an attribute of 'SongAdminIndex2', or an attribute of 'admin_checks.Song'.", obj=SongAdminIndex2, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_nonexistent_field_in_tuple_index1_includes_field_name(self):

    class SongAdminTuple(admin.ModelAdmin):
        readonly_fields = ('title', 'does_not_exist', 'original_release')
    errors = SongAdminTuple(Song, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[1]' refers to 'does_not_exist', which is not a callable, an attribute of 'SongAdminTuple', or an attribute of 'admin_checks.Song'.", obj=SongAdminTuple, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_nonexistent_field_on_custom_inline_includes_field_name(self):

    class CustomCityInline(admin.TabularInline):
        model = City
        readonly_fields = ['i_am_missing']
    errors = CustomCityInline(State, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[0]' refers to 'i_am_missing', which is not a callable, an attribute of 'CustomCityInline', or an attribute of 'admin_checks.City'.", obj=CustomCityInline, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_multiple_missing_readonly_fields_index_order_includes_field_name(self):

    class SongAdminMultiple(admin.ModelAdmin):
        readonly_fields = ('missing_one', 'missing_two')
    errors = SongAdminMultiple(Song, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[0]' refers to 'missing_one', which is not a callable, an attribute of 'SongAdminMultiple', or an attribute of 'admin_checks.Song'.", obj=SongAdminMultiple, id='admin.E035'), checks.Error("The value of 'readonly_fields[1]' refers to 'missing_two', which is not a callable, an attribute of 'SongAdminMultiple', or an attribute of 'admin_checks.Song'.", obj=SongAdminMultiple, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_inline_missing_field_with_different_class_name_includes_field_name(self):

    class AnotherInline(admin.StackedInline):
        model = City
        readonly_fields = ('no_field_here',)
    errors = AnotherInline(State, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[0]' refers to 'no_field_here', which is not a callable, an attribute of 'AnotherInline', or an attribute of 'admin_checks.City'.", obj=AnotherInline, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_readonly_field_nonexistent_on_book_model_includes_field_name(self):

    class BookAdminReadonly(admin.ModelAdmin):
        readonly_fields = ('not_a_field_on_book',)
    errors = BookAdminReadonly(Book, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[0]' refers to 'not_a_field_on_book', which is not a callable, an attribute of 'BookAdminReadonly', or an attribute of 'admin_checks.Book'.", obj=BookAdminReadonly, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_readonly_field_nonexistent_on_inline_using_tabular_includes_field_name(self):

    class CityTabularInline(admin.TabularInline):
        model = City
        readonly_fields = ['this_field_is_missing']
    errors = CityTabularInline(State, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[0]' refers to 'this_field_is_missing', which is not a callable, an attribute of 'CityTabularInline', or an attribute of 'admin_checks.City'.", obj=CityTabularInline, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_readonly_field_nonexistent_with_similar_names_includes_exact_field_name(self):

    class SongAdminSimilar(admin.ModelAdmin):
        readonly_fields = ('title_similar', 'title')
    errors = SongAdminSimilar(Song, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[0]' refers to 'title_similar', which is not a callable, an attribute of 'SongAdminSimilar', or an attribute of 'admin_checks.Song'.", obj=SongAdminSimilar, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_readonly_nonexistent_field_index1_includes_field_name(self):

    class SongAdmin(admin.ModelAdmin):
        readonly_fields = ('title', 'missing_field_one')
    errors = SongAdmin(Song, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[1]' refers to 'missing_field_one', which is not a callable, an attribute of 'SongAdmin', or an attribute of 'admin_checks.Song'.", obj=SongAdmin, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_readonly_nonexistent_field_tuple_index0_includes_field_name(self):

    class TupleAdmin(admin.ModelAdmin):
        readonly_fields = ('missing_in_tuple',)
    errors = TupleAdmin(Song, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[0]' refers to 'missing_in_tuple', which is not a callable, an attribute of 'TupleAdmin', or an attribute of 'admin_checks.Song'.", obj=TupleAdmin, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_readonly_nonexistent_field_inline_index0_includes_field_name(self):

    class CityInline(admin.TabularInline):
        model = City
        readonly_fields = ['i_dont_exist_inline']
    errors = CityInline(State, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[0]' refers to 'i_dont_exist_inline', which is not a callable, an attribute of 'CityInline', or an attribute of 'admin_checks.City'.", obj=CityInline, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_readonly_nonexistent_field_index9_includes_field_name(self):
    missing_name = 'last_missing_field'
    entries = ['f%d' % i for i in range(9)] + [missing_name]

    class LongListAdmin(admin.ModelAdmin):
        readonly_fields = entries
    errors = LongListAdmin(Song, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[9]' refers to '%s', which is not a callable, an attribute of 'LongListAdmin', or an attribute of 'admin_checks.Song'." % missing_name, obj=LongListAdmin, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_readonly_nonexistent_field_special_chars_name_includes_field_name(self):
    special = 'weird.field-name!'

    class SpecialNameAdmin(admin.ModelAdmin):
        readonly_fields = (special,)
    errors = SpecialNameAdmin(Song, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[0]' refers to '%s', which is not a callable, an attribute of 'SpecialNameAdmin', or an attribute of 'admin_checks.Song'." % special, obj=SpecialNameAdmin, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_readonly_nonexistent_field_classname_in_message(self):

    class CustomNamedAdmin(admin.ModelAdmin):
        readonly_fields = ('no_such_field',)
    errors = CustomNamedAdmin(Song, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[0]' refers to 'no_such_field', which is not a callable, an attribute of 'CustomNamedAdmin', or an attribute of 'admin_checks.Song'.", obj=CustomNamedAdmin, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_readonly_nonexistent_field_model_label_in_message(self):

    class ModelLabelAdmin(admin.ModelAdmin):
        readonly_fields = ('this_field_does_not_exist',)
    errors = ModelLabelAdmin(Song, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[0]' refers to 'this_field_does_not_exist', which is not a callable, an attribute of 'ModelLabelAdmin', or an attribute of 'admin_checks.Song'.", obj=ModelLabelAdmin, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_readonly_nonexistent_field_multiple_missing_reports_all(self):

    class MultiMissingAdmin(admin.ModelAdmin):
        readonly_fields = ('missing_a', 'missing_b')
    errors = MultiMissingAdmin(Song, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[0]' refers to 'missing_a', which is not a callable, an attribute of 'MultiMissingAdmin', or an attribute of 'admin_checks.Song'.", obj=MultiMissingAdmin, id='admin.E035'), checks.Error("The value of 'readonly_fields[1]' refers to 'missing_b', which is not a callable, an attribute of 'MultiMissingAdmin', or an attribute of 'admin_checks.Song'.", obj=MultiMissingAdmin, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_readonly_nonexistent_field_inline_custom_classname_in_message(self):

    class CustomInlineName(admin.StackedInline):
        model = Influence
        readonly_fields = ['no_field_here']
    errors = CustomInlineName(Song, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[0]' refers to 'no_field_here', which is not a callable, an attribute of 'CustomInlineName', or an attribute of 'admin_checks.Influence'.", obj=CustomInlineName, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_missing_readonly_field_message_includes_field_name_index1(self):

    class A(admin.ModelAdmin):
        readonly_fields = ('title', 'ghost_field')
    errors = A(Song, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[1]' refers to 'ghost_field', which is not a callable, an attribute of 'A', or an attribute of 'admin_checks.Song'.", obj=A, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_missing_readonly_field_message_includes_field_name_index0(self):

    class B(admin.ModelAdmin):
        readonly_fields = ('missing0',)
    errors = B(Song, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[0]' refers to 'missing0', which is not a callable, an attribute of 'B', or an attribute of 'admin_checks.Song'.", obj=B, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_multiple_missing_readonly_fields_produce_two_errors(self):

    class C(admin.ModelAdmin):
        readonly_fields = ('missingA', 'missingB')
    errors = C(Song, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[0]' refers to 'missingA', which is not a callable, an attribute of 'C', or an attribute of 'admin_checks.Song'.", obj=C, id='admin.E035'), checks.Error("The value of 'readonly_fields[1]' refers to 'missingB', which is not a callable, an attribute of 'C', or an attribute of 'admin_checks.Song'.", obj=C, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_callable_first_then_missing_field_index1(self):

    class D(admin.ModelAdmin):
        readonly_fields = (lambda obj: 'x', 'missing_after_callable')
    errors = D(Song, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[1]' refers to 'missing_after_callable', which is not a callable, an attribute of 'D', or an attribute of 'admin_checks.Song'.", obj=D, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_missing_readonly_field_on_inline(self):

    class CityInline(admin.TabularInline):
        model = City
        readonly_fields = ['i_dont_exist_2']
    errors = CityInline(State, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[0]' refers to 'i_dont_exist_2', which is not a callable, an attribute of 'CityInline', or an attribute of 'admin_checks.City'.", obj=CityInline, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_missing_readonly_field_on_custom_admin_name(self):

    class MySpecialAdmin(admin.ModelAdmin):
        readonly_fields = ['ghostX']
    errors = MySpecialAdmin(Song, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[0]' refers to 'ghostX', which is not a callable, an attribute of 'MySpecialAdmin', or an attribute of 'admin_checks.Song'.", obj=MySpecialAdmin, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_missing_readonly_field_model_label_includes_app_label(self):

    class E(admin.ModelAdmin):
        readonly_fields = ['ghostY']
    errors = E(Song, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[0]' refers to 'ghostY', which is not a callable, an attribute of 'E', or an attribute of 'admin_checks.Song'.", obj=E, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_missing_readonly_field_with_special_characters_in_name(self):

    class F(admin.ModelAdmin):
        readonly_fields = ['weird-field!']
    errors = F(Song, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[0]' refers to 'weird-field!', which is not a callable, an attribute of 'F', or an attribute of 'admin_checks.Song'.", obj=F, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_multiple_missing_readonly_fields_on_inline_with_names_and_indices(self):

    class InlineMultiple(admin.StackedInline):
        model = Influence
        readonly_fields = ['nope1', 'nope2']
    errors = InlineMultiple(Song, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[0]' refers to 'nope1', which is not a callable, an attribute of 'InlineMultiple', or an attribute of 'admin_checks.Influence'.", obj=InlineMultiple, id='admin.E035'), checks.Error("The value of 'readonly_fields[1]' refers to 'nope2', which is not a callable, an attribute of 'InlineMultiple', or an attribute of 'admin_checks.Influence'.", obj=InlineMultiple, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_readonly_missing_field_includes_field_name_modeladmin_variant1(self):

    class SongAdminMissing(admin.ModelAdmin):
        readonly_fields = ('nonexistent2',)
    errors = SongAdminMissing(Song, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[0]' refers to 'nonexistent2', which is not a callable, an attribute of 'SongAdminMissing', or an attribute of 'admin_checks.Song'.", obj=SongAdminMissing, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_readonly_missing_field_includes_field_name_modeladmin_variant2(self):

    class SongAdminMissingTwo(admin.ModelAdmin):
        readonly_fields = ('title', 'missing_field_two')
    errors = SongAdminMissingTwo(Song, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[1]' refers to 'missing_field_two', which is not a callable, an attribute of 'SongAdminMissingTwo', or an attribute of 'admin_checks.Song'.", obj=SongAdminMissingTwo, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_readonly_missing_field_includes_field_name_inline_custom_class(self):

    class CustomCityInline(admin.TabularInline):
        model = City
        readonly_fields = ['i_am_missing_custom']
    errors = CustomCityInline(State, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[0]' refers to 'i_am_missing_custom', which is not a callable, an attribute of 'CustomCityInline', or an attribute of 'admin_checks.City'.", obj=CustomCityInline, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_readonly_missing_field_includes_field_name_on_different_model(self):

    class BookAdminMissing(admin.ModelAdmin):
        readonly_fields = ('no_such_field',)
    errors = BookAdminMissing(Book, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[0]' refers to 'no_such_field', which is not a callable, an attribute of 'BookAdminMissing', or an attribute of 'admin_checks.Book'.", obj=BookAdminMissing, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_readonly_missing_field_with_callable_present_in_sequence(self):

    class SongAdminCallable(admin.ModelAdmin):
        readonly_fields = (lambda obj: 'x', 'missing_with_callable')
    errors = SongAdminCallable(Song, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[1]' refers to 'missing_with_callable', which is not a callable, an attribute of 'SongAdminCallable', or an attribute of 'admin_checks.Song'.", obj=SongAdminCallable, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_readonly_missing_field_dynamic_getattr_admin(self):

    class DynamicAdmin(admin.ModelAdmin):
        readonly_fields = ('dynamic_missing',)

        def __getattr__(self, name):
            if name == 'other':

                @admin.display
                def other_method(obj):
                    pass
                return other_method
            raise AttributeError
    errors = DynamicAdmin(Song, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[0]' refers to 'dynamic_missing', which is not a callable, an attribute of 'DynamicAdmin', or an attribute of 'admin_checks.Song'.", obj=DynamicAdmin, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_readonly_missing_field_in_stacked_inline_includes_field_name(self):

    class StackCityInline(admin.StackedInline):
        model = City
        readonly_fields = ['missing_stack']
    errors = StackCityInline(State, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[0]' refers to 'missing_stack', which is not a callable, an attribute of 'StackCityInline', or an attribute of 'admin_checks.City'.", obj=StackCityInline, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_readonly_missing_field_field_name_with_digits(self):

    class SongAdminDigits(admin.ModelAdmin):
        readonly_fields = ('field123',)
    errors = SongAdminDigits(Song, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[0]' refers to 'field123', which is not a callable, an attribute of 'SongAdminDigits', or an attribute of 'admin_checks.Song'.", obj=SongAdminDigits, id='admin.E035')]
    self.assertEqual(errors, expected)

def test_readonly_missing_field_index_two_reports_correct_label(self):

    class SongAdminIndex2(admin.ModelAdmin):
        readonly_fields = ('one', 'two', 'missing_index_two')
    errors = SongAdminIndex2(Song, AdminSite()).check()
    expected = [checks.Error("The value of 'readonly_fields[2]' refers to 'missing_index_two', which is not a callable, an attribute of 'SongAdminIndex2', or an attribute of 'admin_checks.Song'.", obj=SongAdminIndex2, id='admin.E035')]
    self.assertEqual(errors, expected)