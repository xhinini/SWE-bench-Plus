import xarray as xr
import pytest
import pytest
import xarray as xr

def test_override_shallow_share_nested_dict_identity():
    ds1 = xr.Dataset()
    nested = {'a': 1}
    ds1.attrs['nested'] = nested
    ds2 = xr.Dataset(attrs={'other': 2})
    merged = xr.merge([ds1, ds2], combine_attrs='override')
    assert merged.attrs['nested'] is ds1.attrs['nested']

def test_override_shallow_share_nested_dict_mutation_reflects_in_source():
    ds1 = xr.Dataset()
    ds1.attrs['nested'] = {'a': 1}
    ds2 = xr.Dataset(attrs={'other': 2})
    merged = xr.merge([ds1, ds2], combine_attrs='override')
    merged.attrs['nested']['a'] = 42
    assert ds1.attrs['nested']['a'] == 42

def test_override_shallow_share_nested_dict_mod_source_reflects_in_merged():
    ds1 = xr.Dataset()
    ds1.attrs['nested'] = {'a': 'orig'}
    ds2 = xr.Dataset(attrs={'other': 2})
    merged = xr.merge([ds1, ds2], combine_attrs='override')
    ds1.attrs['nested']['a'] = 'changed'
    assert merged.attrs['nested']['a'] == 'changed'

def test_override_shallow_share_nested_list_identity():
    ds1 = xr.Dataset()
    lst = [1, 2]
    ds1.attrs['lst'] = lst
    ds2 = xr.Dataset(attrs={'other': 3})
    merged = xr.merge([ds1, ds2], combine_attrs='override')
    assert merged.attrs['lst'] is ds1.attrs['lst']

def test_override_shallow_share_nested_list_mutation_reflects_in_source():
    ds1 = xr.Dataset()
    ds1.attrs['lst'] = [0]
    ds2 = xr.Dataset(attrs={'other': 3})
    merged = xr.merge([ds1, ds2], combine_attrs='override')
    merged.attrs['lst'].append(99)
    assert ds1.attrs['lst'] == [0, 99]

def test_override_with_empty_second_shares_first_nested():
    ds1 = xr.Dataset(attrs={'n': {'k': 'v'}})
    ds2 = xr.Dataset(attrs={})
    merged = xr.merge([ds1, ds2], combine_attrs='override')
    assert merged.attrs['n'] is ds1.attrs['n']
    merged.attrs['n']['k'] = 'changed'
    assert ds1.attrs['n']['k'] == 'changed'

def test_override_multiple_objects_first_precedence_and_shares():
    ds1 = xr.Dataset(attrs={'n': {'a': 1}, 'x': 0})
    ds2 = xr.Dataset(attrs={'n': {'a': 2}, 'y': 1})
    ds3 = xr.Dataset(attrs={'n': {'a': 3}, 'z': 2})
    merged = xr.merge([ds1, ds2, ds3], combine_attrs='override')
    assert merged.attrs['n'] is ds1.attrs['n']
    merged.attrs['n']['a'] = 99
    assert ds1.attrs['n']['a'] == 99

def test_override_shallow_shared_nested_preserved_across_calls():
    ds1 = xr.Dataset(attrs={'n': {'a': [1]}})
    ds2 = xr.Dataset(attrs={'b': 2})
    merged1 = xr.merge([ds1, ds2], combine_attrs='override')
    merged2 = xr.merge([ds1, ds2], combine_attrs='override')
    assert merged1.attrs['n'] is ds1.attrs['n']
    assert merged2.attrs['n'] is ds1.attrs['n']

# No additional imports required beyond standard pytest, numpy and xarray already used in the test suite.
import numpy as np
import xarray as xr
import pytest

def test_merge_attrs_override_shallow_nested_dict():
    ds1 = xr.Dataset(attrs={"nested": {"a": 1}})
    ds2 = xr.Dataset(attrs={"other": 2})
    ds3 = xr.merge([ds1, ds2], combine_attrs="override")
    # mutate nested dict in merged result
    ds3.attrs["nested"]["a"] = 99
    # shallow copy semantics: original nested dict should reflect change
    assert ds1.attrs["nested"]["a"] == 99

def test_merge_attrs_override_shallow_list():
    ds1 = xr.Dataset(attrs={"lst": [1, 2]})
    ds2 = xr.Dataset(attrs={"x": 0})
    ds3 = xr.merge([ds1, ds2], combine_attrs="override")
    ds3.attrs["lst"].append(3)
    assert ds1.attrs["lst"] == [1, 2, 3]

def test_merge_attrs_override_shallow_numpy_array_mutation():
    arr = np.array([1, 2])
    ds1 = xr.Dataset(attrs={"arr": arr})
    ds2 = xr.Dataset(attrs={"x": 0})
    ds3 = xr.merge([ds1, ds2], combine_attrs="override")
    ds3.attrs["arr"][0] = 42
    # same numpy array object should be shared under shallow copy
    assert ds1.attrs["arr"][0] == 42

def test_merge_attrs_override_shallow_mutable_in_list():
    inner = {"k": 1}
    ds1 = xr.Dataset(attrs={"complex": [inner]})
    ds2 = xr.Dataset(attrs={"y": 0})
    ds3 = xr.merge([ds1, ds2], combine_attrs="override")
    ds3.attrs["complex"][0]["k"] = 7
    assert ds1.attrs["complex"][0]["k"] == 7

def test_merge_attrs_override_shared_identity_for_nested_object():
    nested = {"a": 1}
    ds1 = xr.Dataset(attrs={"nested": nested})
    ds2 = xr.Dataset(attrs={})
    ds3 = xr.merge([ds1, ds2], combine_attrs="override")
    # nested object identity should be preserved (same object referenced)
    assert ds3.attrs["nested"] is ds1.attrs["nested"]

def test_merge_attrs_override_shallow_nested_with_multiple_merges():
    ds1 = xr.Dataset(attrs={"n": {"v": [1]}})
    ds2 = xr.Dataset(attrs={"a": 0})
    ds3 = xr.merge([ds1, ds2], combine_attrs="override")
    # perform another merge including ds3 to ensure shallow semantics persist
    ds4 = xr.merge([ds3, xr.Dataset(attrs={"b": 1})], combine_attrs="override")
    ds4.attrs["n"]["v"].append(2)
    # original should reflect nested change
    assert ds1.attrs["n"]["v"] == [1, 2]

def test_merge_attrs_override_shallow_with_priority_first_taken():
    # ensure override takes attributes from first dataset and shares nested objects
    nested = {"flag": False}
    ds1 = xr.Dataset(attrs={"shared": nested})
    ds2 = xr.Dataset(attrs={"shared": {"flag": True}})
    # override should pick ds1 attrs
    ds_merged = xr.merge([ds1, ds2], combine_attrs="override")
    assert ds_merged.attrs["shared"] is ds1.attrs["shared"]
    # mutating nested in merged should mutate ds1 nested
    ds_merged.attrs["shared"]["flag"] = True
    assert ds1.attrs["shared"]["flag"] == True

def test_merge_attrs_override_nested_mutation_after_top_level_assign():
    # changing top-level mapping in merged result should not change original mapping,
    # but mutating nested objects (that were shared) should still propagate.
    nested = {"count": 0}
    ds1 = xr.Dataset(attrs={"n": nested})
    ds2 = xr.Dataset(attrs={})
    ds3 = xr.merge([ds1, ds2], combine_attrs="override")
    # reassigning top-level key to new object should NOT affect original top-level mapping
    ds3.attrs["n"] = {"count": 999}
    assert ds1.attrs["n"]["count"] == 0
    # but if we mutate the nested object that was previously shared before assignment,
    # this demonstrates shallow-copy semantics (we recreate scenario where assignment happens after a shallow copy)
    ds1b = xr.Dataset(attrs={"m": nested})
    ds2b = xr.Dataset(attrs={})
    ds3b = xr.merge([ds1b, ds2b], combine_attrs="override")
    # mutate nested via merged view
    ds3b.attrs["m"]["count"] = 5
    assert ds1b.attrs["m"]["count"] == 5

def test_merge_attrs_override_shallow_nested_mutation_propagates_to_all_sources():
    # if multiple datasets reference same nested mutable object in their attrs,
    # merged result should share it (shallow) and mutating through merged should
    # affect all originals that referenced it.
    shared = {"x": [0]}
    ds1 = xr.Dataset(attrs={"s": shared})
    ds2 = xr.Dataset(attrs={"s": shared})
    merged = xr.merge([ds1, ds2], combine_attrs="override")
    merged.attrs["s"]["x"].append(1)
    assert ds1.attrs["s"]["x"] == [0, 1]
    assert ds2.attrs["s"]["x"] == [0, 1]

def test_merge_attrs_override_shallow_nested_mutation_of_sets():
    # sets are mutable; shallow copy should share the same set instance
    shared_set = {"a", "b"}
    ds1 = xr.Dataset(attrs={"ss": shared_set})
    ds2 = xr.Dataset(attrs={})
    merged = xr.merge([ds1, ds2], combine_attrs="override")
    merged.attrs["ss"].add("c")
    assert "c" in ds1.attrs["ss"]