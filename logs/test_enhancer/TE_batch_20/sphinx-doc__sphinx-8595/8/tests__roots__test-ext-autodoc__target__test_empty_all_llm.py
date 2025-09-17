from sphinx.ext.autodoc import INSTANCEATTR, ModuleDocumenter, Options
import types
from sphinx.ext.autodoc import ModuleDocumenter, Options, INSTANCEATTR
import inspect as pyinspect
if __name__ == '__main__':
    test_empty___all_want_all_true_returns_false_and_marks_skipped()
    test_populated___all_only_unskipped_members_present()
    test_no___all_treated_as_implicit_members()
    test_annotation_only_member_in_empty___all_is_included_as_INSTANCEATTR_and_skipped()
    test___all_containing_nonexistent_name_does_not_raise_and_existing_not_skipped()
    test_want_all_false_and_members_option_specified_returns_only_those_members()
    test_want_all_false_and_no_members_returns_empty_list()
    test_returned_structure_is_tuple_and_second_element_is_list_for_various___all_states()