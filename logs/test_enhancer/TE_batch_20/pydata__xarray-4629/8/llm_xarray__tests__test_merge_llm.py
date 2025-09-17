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

import pytest
import xarray as xr

def test_merge_override_shallow_nested_dict_shared_xr_merge():
    ds1 = xr.Dataset()
    ds1.attrs = {'nested': {'a': 1}, 'top': 0}
    ds2 = xr.Dataset(attrs={'other': 'v'})
    res = xr.merge([ds1, ds2], combine_attrs='override')
    assert res.attrs is not ds1.attrs
    assert res.attrs['nested'] is ds1.attrs['nested']
    res.attrs['nested']['a'] = 2
    assert ds1.attrs['nested']['a'] == 2

def test_merge_override_shallow_nested_list_shared_xr_merge():
    ds1 = xr.Dataset()
    ds1.attrs = {'lst': [1, 2], 'top': 5}
    ds2 = xr.Dataset(attrs={'other': 'v'})
    res = xr.merge([ds1, ds2], combine_attrs='override')
    assert res.attrs is not ds1.attrs
    assert res.attrs['lst'] is ds1.attrs['lst']
    res.attrs['lst'].append(3)
    assert ds1.attrs['lst'] == [1, 2, 3]

def test_merge_override_shallow_nested_dict_shared_with_dataarray_inputs():
    da1 = xr.DataArray([1], name='a')
    da1.attrs = {'nested': {'alpha': 10}}
    da2 = xr.DataArray([2], name='b')
    da2.attrs = {'other': 'x'}
    res = xr.merge([da1, da2], combine_attrs='override')
    assert res.attrs is not da1.attrs
    assert res.attrs['nested'] is da1.attrs['nested']
    res.attrs['nested']['alpha'] = 99
    assert da1.attrs['nested']['alpha'] == 99

def test_merge_override_shallow_nested_multi_merge_first_wins_shallow_refs():
    ds1 = xr.Dataset()
    ds1.attrs = {'compound': {'n': [0]}, 'keep': True}
    ds2 = xr.Dataset(attrs={'compound': {'n': [1]}, 'other': 1})
    ds3 = xr.Dataset(attrs={'extra': 3})
    res = xr.merge([ds1, ds2, ds3], combine_attrs='override')
    assert res.attrs is not ds1.attrs
    assert res.attrs['compound'] is ds1.attrs['compound']
    res.attrs['compound']['n'].append(2)
    assert ds1.attrs['compound']['n'] == [0, 2]

def test_merge_override_shallow_nested_identity_and_mutation_check():
    ds1 = xr.Dataset()
    nested = {'a': [1, 2]}
    ds1.attrs = {'nested': nested}
    ds2 = xr.Dataset(attrs={'other': 'x'})
    res = xr.merge([ds1, ds2], combine_attrs='override')
    assert res.attrs is not ds1.attrs
    assert res.attrs['nested'] is nested
    res.attrs['nested']['a'].append(3)
    assert nested['a'] == [1, 2, 3]

def test_merge_override_shallow_nested_multiple_mutations():
    ds1 = xr.Dataset()
    ds1.attrs = {'deep': {'lst': [0]}}
    ds2 = xr.Dataset(attrs={'x': 1})
    res = xr.merge([ds1, ds2], combine_attrs='override')
    res.attrs['deep']['lst'].extend([1, 2, 3])
    assert ds1.attrs['deep']['lst'] == [0, 1, 2, 3]

def test_merge_override_shallow_nested_preserves_reference_across_merges():
    ds1 = xr.Dataset()
    nested_obj = {'k': {'sub': 5}}
    ds1.attrs = {'k': nested_obj['k']}
    ds2 = xr.Dataset(attrs={'other': 0})
    res = xr.merge([ds1, ds2], combine_attrs='override')
    assert res.attrs['k'] is ds1.attrs['k']
    res.attrs['k']['sub'] = 42
    assert ds1.attrs['k']['sub'] == 42

import xarray as xr
import numpy as np
import pytest
import numpy as np
import xarray as xr
import pytest

def test_override_nested_mutation_is_shared_shallow_copy():
    nested = {'a': 1}
    ds1 = xr.Dataset(attrs={'nested': nested})
    ds2 = xr.Dataset(attrs={})
    merged = xr.merge([ds1, ds2], combine_attrs='override')
    assert merged.attrs is not ds1.attrs
    merged.attrs['nested']['a'] = 99
    assert ds1.attrs['nested']['a'] == 99

def test_override_list_mutation_is_shared_shallow_copy():
    lst = [1, 2]
    ds1 = xr.Dataset(attrs={'lst': lst})
    ds2 = xr.Dataset(attrs={})
    merged = xr.merge([ds1, ds2], combine_attrs='override')
    merged.attrs['lst'].append(3)
    assert ds1.attrs['lst'] == [1, 2, 3]

def test_override_numpy_array_mutation_is_shared_shallow_copy():
    arr = np.array([0, 1, 2])
    ds1 = xr.Dataset(attrs={'arr': arr})
    ds2 = xr.Dataset(attrs={})
    merged = xr.merge([ds1, ds2], combine_attrs='override')
    merged.attrs['arr'][0] = 9
    assert ds1.attrs['arr'][0] == 9

def test_override_empty_attrs_copy_behavior():
    ds1 = xr.Dataset(attrs={})
    ds2 = xr.Dataset(attrs={'a': {'inner': 1}})
    merged = xr.merge([ds2, ds1], combine_attrs='override')
    assert merged.attrs is not ds2.attrs
    merged.attrs['a']['inner'] = 7
    assert ds2.attrs['a']['inner'] == 7

def test_override_with_dataarray_promotes_and_shallow_copies_attrs():
    da = xr.DataArray([1], dims=('x',), name='v')
    da.attrs = {'nested': {'val': 5}}
    ds = xr.Dataset(attrs={})
    merged = xr.merge([da, ds], combine_attrs='override')
    assert merged.attrs is not da.attrs
    merged.attrs['nested']['val'] = 42
    assert da.attrs['nested']['val'] == 42

def test_override_multiple_datasets_shallow_copy_behavior():
    nested = {'k': [1]}
    ds1 = xr.Dataset(attrs={'nested': nested, 'top': 0})
    ds2 = xr.Dataset(attrs={'other': 2})
    ds3 = xr.Dataset(attrs={'other': 3})
    merged = xr.merge([ds1, ds2, ds3], combine_attrs='override')
    merged.attrs['top'] = 5
    assert ds1.attrs['top'] == 0
    merged.attrs['nested']['k'].append(2)
    assert ds1.attrs['nested']['k'] == [1, 2]

def test_override_identity_of_nested_object_matches_original():
    nested = {'inner': {'x': 1}}
    ds1 = xr.Dataset(attrs={'nested': nested})
    ds2 = xr.Dataset(attrs={})
    merged = xr.merge([ds1, ds2], combine_attrs='override')
    assert merged.attrs['nested'] is ds1.attrs['nested']

import xarray as xr
from xarray.core import merge as merge_mod
import pytest
import xarray as xr
from xarray.core import merge as merge_mod


def test_xr_merge_override_shallow_copy_nested_dict():
    ds1 = xr.Dataset(attrs={"nested": {"a": 1}})
    ds2 = xr.Dataset(attrs={"b": 2})
    merged = xr.merge([ds1, ds2], combine_attrs="override")
    # mutate nested value on merged attrs -> should affect original ds1 under shallow-copy semantics
    merged.attrs["nested"]["a"] = 99
    assert ds1.attrs["nested"]["a"] == 99


def test_dataset_merge_override_shallow_copy_nested_dict_method():
    ds1 = xr.Dataset(attrs={"nested": {"a": 10}})
    ds2 = xr.Dataset(attrs={"b": "x"})
    merged = ds1.merge(ds2)  # Dataset.merge uses combine_attrs="override" by default
    merged.attrs["nested"]["a"] = 77
    assert ds1.attrs["nested"]["a"] == 77


def test_xr_merge_override_shallow_copy_nested_list():
    ds1 = xr.Dataset(attrs={"lst": [1, 2]})
    ds2 = xr.Dataset(attrs={"z": 0})
    merged = xr.merge([ds1, ds2], combine_attrs="override")
    merged.attrs["lst"].append(3)
    assert ds1.attrs["lst"] == [1, 2, 3]


def test_dataset_merge_override_shallow_copy_nested_list_method():
    ds1 = xr.Dataset(attrs={"lst": ["a"]})
    ds2 = xr.Dataset(attrs={"other": 1})
    merged = ds1.merge(ds2)
    merged.attrs["lst"].extend(["b", "c"])
    assert ds1.attrs["lst"] == ["a", "b", "c"]


def test_merge_core_override_shallow_copy_nested_dict():
    ds1 = xr.Dataset(attrs={"nested": {"inner": {"v": 1}}})
    ds2 = xr.Dataset(attrs={"other": 2})
    result = merge_mod.merge_core([ds1, ds2], compat="broadcast_equals", join="outer")
    # result.attrs should be a shallow copy of ds1.attrs so nested dict references are shared
    result.attrs["nested"]["inner"]["v"] = -1
    assert ds1.attrs["nested"]["inner"]["v"] == -1


def test_dataset_update_method_override_shallow_copy():
    ds1 = xr.Dataset(attrs={"meta": {"k": "orig"}})
    # other can be a mapping; dataset_update_method will call merge_core with combine_attrs="override"
    other = {"dummy": ("x", [1])}
    result = merge_mod.dataset_update_method(ds1, other)
    result.attrs["meta"]["k"] = "changed"
    assert ds1.attrs["meta"]["k"] == "changed"


def test_merge_data_and_coords_override_shallow_copy():
    ds1 = xr.Dataset(attrs={"coords_meta": {"x": 0}})
    # coords can be empty mapping; merge_data_and_coords passes through to merge_core
    result = merge_mod.merge_data_and_coords(ds1, {})
    result.attrs["coords_meta"]["x"] = 42
    assert ds1.attrs["coords_meta"]["x"] == 42


def test_xr_merge_override_shallow_copy_multi_level_nested_dict():
    ds1 = xr.Dataset(attrs={"a": {"b": {"c": [1, 2]}}})
    ds2 = xr.Dataset(attrs={})
    merged = xr.merge([ds1, ds2], combine_attrs="override")
    # modify deep nested list -> should reflect in original ds1 under shallow-copy semantics
    merged.attrs["a"]["b"]["c"].append(3)
    assert ds1.attrs["a"]["b"]["c"] == [1, 2, 3]


def test_dataset_merge_override_shallow_copy_multi_level_nested_list():
    ds1 = xr.Dataset(attrs={"outer": [{"id": 1}]})
    ds2 = xr.Dataset(attrs={})
    merged = ds1.merge(ds2)
    merged.attrs["outer"][0]["id"] = 99
    assert ds1.attrs["outer"][0]["id"] == 99


def test_xr_merge_override_shallow_copy_from_dataset_created_by_dataarray():
    # convert a DataArray to a Dataset (promote attrs) and then merge;
    # top-level attrs are a shallow copy, nested values should be shared.
    da = xr.DataArray([1], dims=("x",), name="a")
    da.attrs = {"nested": {"flag": True}}
    ds_from_da = da.to_dataset(promote_attrs=True)
    ds2 = xr.Dataset(attrs={"irrelevant": 0})
    merged = xr.merge([ds_from_da, ds2], combine_attrs="override")
    merged.attrs["nested"]["flag"] = False
    # The promoted dataset holds the attrs, so mutation should be visible there
    assert ds_from_da.attrs["nested"]["flag"] is False

import threading
import threading
import numpy as np
import pytest
import xarray as xr

def test_override_shallow_copy_nested_list_is_shared():
    nested = {'lst': [1, 2, 3]}
    ds1 = xr.Dataset(attrs={'meta': nested})
    ds2 = xr.Dataset(attrs={'other': 1})
    merged = xr.merge([ds1, ds2], combine_attrs='override')
    merged.attrs['meta']['lst'][0] = 999
    assert ds1.attrs['meta']['lst'][0] == 999
    assert merged.attrs['meta'] is ds1.attrs['meta']

def test_override_shallow_copy_nested_dict_is_shared():
    nested = {'a': {'b': 2}}
    ds1 = xr.Dataset(attrs={'meta': nested})
    merged = xr.merge([ds1], combine_attrs='override')
    merged.attrs['meta']['a']['b'] = -1
    assert ds1.attrs['meta']['a']['b'] == -1
    assert merged.attrs['meta'] is ds1.attrs['meta']

def test_override_shallow_copy_numpy_array_is_shared():
    arr = np.array([1, 2, 3])
    ds1 = xr.Dataset(attrs={'arr': arr})
    merged = xr.merge([ds1], combine_attrs='override')
    merged.attrs['arr'][0] = 42
    assert ds1.attrs['arr'][0] == 42
    assert merged.attrs['arr'] is ds1.attrs['arr']

def test_override_shallow_copy_custom_object_is_shared():
    obj = MutableObj(10)
    ds1 = xr.Dataset(attrs={'obj': obj})
    merged = xr.merge([ds1], combine_attrs='override')
    merged.attrs['obj'].value = 77
    assert ds1.attrs['obj'].value == 77
    assert merged.attrs['obj'] is ds1.attrs['obj']

def test_override_shallow_copy_dataarray_in_attrs_is_shared():
    da = xr.DataArray([1, 2, 3], name='a')
    ds1 = xr.Dataset(attrs={'da': da})
    merged = xr.merge([ds1], combine_attrs='override')
    merged.attrs['da'].values[0] = 123
    assert ds1.attrs['da'].values[0] == 123
    assert merged.attrs['da'] is ds1.attrs['da']

def test_override_non_deepcopyable_object_does_not_raise():
    lock = threading.Lock()
    ds1 = xr.Dataset(attrs={'lock': lock})
    merged = xr.merge([ds1], combine_attrs='override')
    assert merged.attrs['lock'] is lock
    assert ds1.attrs['lock'] is lock

def test_override_identity_of_nested_reference_is_preserved():
    nested = {'inner': [0]}
    ds1 = xr.Dataset(attrs={'meta': nested})
    ds2 = xr.Dataset(attrs={})
    merged = xr.merge([ds1, ds2], combine_attrs='override')
    assert merged.attrs['meta'] is ds1.attrs['meta']

def test_override_multiple_datasets_preserve_first_attrs_reference_for_override():
    nested = {'shared': {'x': 5}}
    ds1 = xr.Dataset(attrs={'shared': nested})
    ds2 = xr.Dataset(attrs={'shared': {'x': 10}})
    merged = xr.merge([ds1, ds2], combine_attrs='override')
    assert merged.attrs['shared'] is ds1.attrs['shared']
    merged.attrs['shared']['x'] = 999
    assert ds1.attrs['shared']['x'] == 999

def test_override_changes_in_original_after_merge_are_seen_in_merged():
    nested = {'lst': [7]}
    ds1 = xr.Dataset(attrs={'meta': nested})
    merged = xr.merge([ds1], combine_attrs='override')
    ds1.attrs['meta']['lst'][0] = 55
    assert merged.attrs['meta']['lst'][0] == 55

import pytest
import xarray as xr

def test_shallow_copy_preserves_nested_mutation_on_merge_xr_merge():
    nested = {'inner': {'val': 1}}
    ds1 = xr.Dataset(attrs={'nested': nested['inner']})
    ds2 = xr.Dataset(attrs={'other': 2})
    merged = xr.merge([ds1, ds2], combine_attrs='override')
    merged.attrs['nested']['val'] = 999
    assert ds1.attrs['nested']['val'] == 999