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

import copy
import pytest
import xarray as xr
from xarray.core import merge as merge_module

def test_shallow_copy_preserves_nested_identity():
    ds1 = xr.Dataset(attrs={'nested': {'v': 1}})
    ds2 = xr.Dataset(attrs={})
    merged = xr.merge([ds1, ds2], combine_attrs='override')
    assert merged.attrs['nested'] is ds1.attrs['nested']

def test_inplace_nested_mutation_propagates_to_source_under_shallow_copy():
    ds1 = xr.Dataset(attrs={'nested': {'v': 1}})
    ds2 = xr.Dataset(attrs={})
    merged = xr.merge([ds1, ds2], combine_attrs='override')
    merged.attrs['nested']['v'] = 99
    assert ds1.attrs['nested']['v'] == 99

def test_result_attrs_is_distinct_object_but_nested_objects_shared():
    ds1 = xr.Dataset(attrs={'n': {'a': 1}, 'b': 2})
    ds2 = xr.Dataset(attrs={})
    merged = xr.merge([ds1, ds2], combine_attrs='override')
    assert merged.attrs is not ds1.attrs
    assert merged.attrs['n'] is ds1.attrs['n']

import xarray as xr
import pytest
import xarray as xr
import pytest

def test_merge_attrs_override_nested_dict_mutation_is_shared_with_original():
    ds1 = xr.Dataset(attrs={'nested': {'a': 1}})
    ds2 = xr.Dataset(attrs={'other': 2})
    merged = xr.merge([ds1, ds2], combine_attrs='override')
    merged.attrs['nested']['a'] = 42
    assert ds1.attrs['nested']['a'] == 42

def test_merge_attrs_override_nested_list_mutation_is_shared_with_original():
    ds1 = xr.Dataset(attrs={'lst': [1, 2, 3]})
    ds2 = xr.Dataset(attrs={'z': 0})
    merged = xr.merge([ds1, ds2], combine_attrs='override')
    merged.attrs['lst'][0] = 99
    assert ds1.attrs['lst'][0] == 99

def test_merge_attrs_override_nested_custom_object_mutation_is_shared_with_original():

    class MutableObj:

        def __init__(self, value):
            self.value = value
    obj = MutableObj(7)
    ds1 = xr.Dataset(attrs={'obj': obj})
    ds2 = xr.Dataset(attrs={'k': 1})
    merged = xr.merge([ds1, ds2], combine_attrs='override')
    merged.attrs['obj'].value = 123
    assert ds1.attrs['obj'].value == 123

def test_merge_attrs_override_deep_nested_structure_mutation_is_shared():
    ds1 = xr.Dataset(attrs={'a': {'b': [{'c': 1}]}})
    ds2 = xr.Dataset(attrs={'other': 0})
    merged = xr.merge([ds1, ds2], combine_attrs='override')
    merged.attrs['a']['b'][0]['c'] = 77
    assert ds1.attrs['a']['b'][0]['c'] == 77

def test_merge_attrs_override_deleting_nested_key_reflects_original():
    ds1 = xr.Dataset(attrs={'info': {'keep': 1, 'drop': 2}})
    ds2 = xr.Dataset(attrs={})
    merged = xr.merge([ds1, ds2], combine_attrs='override')
    del merged.attrs['info']['drop']
    assert 'drop' not in ds1.attrs['info']
    assert 'keep' in ds1.attrs['info']

def test_merge_attrs_override_with_dataarray_attrs_nested_shared():
    da = xr.DataArray(0, name='v', attrs={'meta': {'n': 5}})
    ds = xr.Dataset(attrs={'other': 1})
    merged = xr.merge([da, ds], combine_attrs='override')
    merged.attrs['meta']['n'] = 999
    assert da.attrs['meta']['n'] == 999

def test_merge_attrs_override_nested_containing_mutable_objects_shared_across_reference():
    shared_inner = {'x': [1]}
    ds1 = xr.Dataset(attrs={'outer': shared_inner})
    ds2 = xr.Dataset(attrs={'y': 2})
    merged = xr.merge([ds1, ds2], combine_attrs='override')
    merged.attrs['outer']['x'].append(42)
    assert ds1.attrs['outer']['x'][-1] == 42

def test_merge_attrs_override_mutate_then_replace_top_level_behaviour():
    ds1 = xr.Dataset(attrs={'nested': {'a': 1}})
    ds2 = xr.Dataset(attrs={'foo': 0})
    merged = xr.merge([ds1, ds2], combine_attrs='override')
    merged.attrs['nested']['a'] = 8
    assert ds1.attrs['nested']['a'] == 8
    merged.attrs['nested'] = {'a': 100}
    assert ds1.attrs['nested']['a'] == 8

import xarray as xr
import pytest
import pytest
import xarray as xr

def test_override_shallow_shared_nested_dict_mutation():
    nested = {'inner': 10}
    ds1 = xr.Dataset(attrs={'nested': nested})
    ds2 = xr.Dataset(attrs={})
    merged = xr.merge([ds1, ds2], combine_attrs='override')
    assert merged.attrs['nested'] is not ds1.attrs
    assert merged.attrs['nested'] is ds1.attrs['nested']
    merged.attrs['nested']['inner'] = 20
    assert ds1.attrs['nested']['inner'] == 20

def test_override_shallow_shared_list_mutation():
    lst = [1, 2, 3]
    ds1 = xr.Dataset(attrs={'mylist': lst})
    ds2 = xr.Dataset(attrs={})
    merged = xr.merge([ds1, ds2], combine_attrs='override')
    assert merged.attrs['mylist'] is ds1.attrs['mylist']
    merged.attrs['mylist'].append(4)
    assert ds1.attrs['mylist'] == [1, 2, 3, 4]

def test_override_multiple_datasets_shallow_sharing_from_first():
    nested = {'v': 5}
    ds1 = xr.Dataset(attrs={'x': 0, 'nested': nested})
    ds2 = xr.Dataset(attrs={'x': 1})
    ds3 = xr.Dataset(attrs={'x': 2})
    merged = xr.merge([ds1, ds2, ds3], combine_attrs='override')
    merged.attrs['x'] = -1
    assert ds1.attrs['x'] == 0
    assert merged.attrs['nested'] is ds1.attrs['nested']
    merged.attrs['nested']['v'] = 42
    assert ds1.attrs['nested']['v'] == 42

def test_override_with_dataarray_uses_first_attrs_shallow_sharing():
    nested = {'key': 'val'}
    ds = xr.Dataset(attrs={'nested': nested})
    da = xr.DataArray([1, 2], name='vals', attrs={})
    merged = xr.merge([ds, da.to_dataset()], combine_attrs='override')
    assert merged.attrs['nested'] is ds.attrs['nested']
    merged.attrs['nested']['key'] = 'changed'
    assert ds.attrs['nested']['key'] == 'changed'

def test_override_shallow_shared_custom_mutable_object():

    class MutableObj:

        def __init__(self, value):
            self.value = value
    obj = MutableObj(7)
    ds1 = xr.Dataset(attrs={'o': obj})
    ds2 = xr.Dataset(attrs={})
    merged = xr.merge([ds1, ds2], combine_attrs='override')
    assert merged.attrs['o'] is ds1.attrs['o']
    merged.attrs['o'].value = 123
    assert ds1.attrs['o'].value == 123

def test_override_shared_identity_of_nested_mutable_between_merged_and_source():
    nested = {'x': [0]}
    ds1 = xr.Dataset(attrs={'nested': nested})
    merged = xr.merge([ds1], combine_attrs='override')
    assert merged.attrs['nested'] is ds1.attrs['nested']
    ds1.attrs['nested']['x'].append(1)
    assert merged.attrs['nested']['x'] == [0, 1]

def test_override_top_level_copy_is_a_shallow_mapping_copy():
    nested = {'inner': {'a': 1}}
    ds1 = xr.Dataset(attrs={'nested': nested})
    merged = xr.merge([ds1], combine_attrs='override')
    assert merged.attrs is not ds1.attrs
    assert merged.attrs['nested'] is ds1.attrs['nested']

import copy
import pytest
import xarray as xr
from xarray.core.merge import merge_attrs, merge_core

def test_merge_attrs_override_nested_shared_direct():
    nested = {'a': 1}
    original = {'nested': nested}
    variable_attrs = [original]
    result = merge_attrs(variable_attrs, 'override')
    result['nested']['a'] = 99
    assert original['nested']['a'] == 99

def test_merge_attrs_override_list_shared_direct():
    lst = [1]
    original = {'lst': lst}
    variable_attrs = [original]
    result = merge_attrs(variable_attrs, 'override')
    result['lst'].append(2)
    assert original['lst'] == [1, 2]

def test_merge_core_attrs_nested_shared():
    ds1 = xr.Dataset(attrs={'nested': {'val': 10}})
    ds2 = xr.Dataset(attrs={})
    result = merge_core([ds1, ds2], combine_attrs='override')
    merged_attrs = result.attrs
    merged_attrs['nested']['val'] = 42
    assert ds1.attrs['nested']['val'] == 42

def test_merge_core_attrs_list_shared():
    ds1 = xr.Dataset(attrs={'lst': [0]})
    ds2 = xr.Dataset(attrs={})
    result = merge_core([ds1, ds2], combine_attrs='override')
    merged_attrs = result.attrs
    merged_attrs['lst'].append(1)
    assert ds1.attrs['lst'] == [0, 1]

def test_merge_attrs_override_deepcopy_difference_detection():
    nested = {'inner': {'v': 7}}
    original = {'nested': nested}
    result = merge_attrs([original], 'override')
    result['nested']['inner']['v'] = 123
    assert original['nested']['inner']['v'] == 123

import numpy as np
import pandas as pd
import pytest
import xarray as xr

def test_merge_attrs_override_nested_identity_dict():
    nested = {'a': [1, 2]}
    ds1 = xr.Dataset(attrs={'nested': nested})
    ds2 = xr.Dataset(attrs={})
    ds3 = xr.merge([ds1, ds2], combine_attrs='override')
    assert ds3.attrs['nested'] is nested
    ds3.attrs['nested']['a'][0] = 999
    assert nested['a'][0] == 999
    assert ds1.attrs['nested']['a'][0] == 999

def test_merge_attrs_override_nested_identity_list():
    lst = [1, 2, 3]
    ds1 = xr.Dataset(attrs={'lst': lst})
    ds3 = xr.merge([ds1], combine_attrs='override')
    assert ds3.attrs['lst'] is lst
    lst.append(4)
    assert ds3.attrs['lst'][-1] == 4

def test_merge_attrs_override_nested_identity_numpy_array():
    arr = np.array([1, 2, 3])
    ds1 = xr.Dataset(attrs={'arr': arr})
    ds3 = xr.merge([ds1], combine_attrs='override')
    assert ds3.attrs['arr'] is arr
    ds3.attrs['arr'][0] = 42
    assert arr[0] == 42
    assert ds1.attrs['arr'][0] == 42

def test_merge_attrs_override_nested_identity_pandas_index():
    idx = pd.Index([10, 20])
    ds1 = xr.Dataset(attrs={'idx': idx})
    ds3 = xr.merge([ds1], combine_attrs='override')
    assert ds3.attrs['idx'] is idx

def test_merge_attrs_override_nested_identity_custom_object():

    class Custom:

        def __init__(self, v):
            self.v = v
    obj = Custom(5)
    ds1 = xr.Dataset(attrs={'obj': obj})
    ds3 = xr.merge([ds1], combine_attrs='override')
    assert ds3.attrs['obj'] is obj
    ds3.attrs['obj'].v = 7
    assert ds1.attrs['obj'].v == 7

def test_merge_attrs_override_multiple_inputs_preserve_first_nested_identity():
    nested = {'k': 'v'}
    ds1 = xr.Dataset(attrs={'shared': nested})
    ds2 = xr.Dataset(attrs={'shared': {'k': 'v'}, 'other': 1})
    ds3 = xr.merge([ds1, ds2], combine_attrs='override')
    assert ds3.attrs['shared'] is ds1.attrs['shared']

def test_merge_attrs_override_shared_nested_structure_reflects_changes():
    nested = {'child': [0]}
    ds1 = xr.Dataset(attrs={'shared': nested})
    ds3 = xr.merge([ds1], combine_attrs='override')
    nested['child'].append(1)
    assert ds3.attrs['shared']['child'] == [0, 1]

def test_merge_attrs_override_shallow_vs_deepcopy_behavior():
    nested = {'m': {'n': [1]}}
    ds1 = xr.Dataset(attrs={'nested': nested})
    ds3 = xr.merge([ds1], combine_attrs='override')
    assert ds3.attrs is not ds1.attrs
    assert ds3.attrs['nested'] is nested

import xarray as xr
import pytest
import numpy as np
import xarray as xr
import numpy as np
import pytest

def test_override_shallow_copy_nested_dict_mutation():
    ds1 = xr.Dataset()
    ds1.attrs['nested'] = {'a': 1}
    ds2 = xr.Dataset(attrs={'b': 2})
    merged = xr.merge([ds1, ds2], combine_attrs='override')
    merged.attrs['nested']['a'] = 999
    assert ds1.attrs['nested']['a'] == 999

def test_override_shallow_copy_nested_list_mutation():
    ds1 = xr.Dataset()
    ds1.attrs['nested_list'] = [0, 1, [2, 3]]
    ds2 = xr.Dataset(attrs={'other': 0})
    merged = xr.merge([ds1, ds2], combine_attrs='override')
    merged.attrs['nested_list'][2][0] = 42
    assert ds1.attrs['nested_list'][2][0] == 42

def test_override_shallow_copy_multiple_nested_levels():
    ds1 = xr.Dataset()
    ds1.attrs['a'] = {'inner': {'lst': [1, {'k': 'v'}]}}
    ds2 = xr.Dataset(attrs={})
    merged = xr.merge([ds1, ds2], combine_attrs='override')
    merged.attrs['a']['inner']['lst'][1]['k'] = 'changed'
    assert ds1.attrs['a']['inner']['lst'][1]['k'] == 'changed'

def test_override_shallow_copy_with_dataarray_attrs():
    da = xr.DataArray([1, 2], dims=('x',), name='v')
    da.attrs['meta'] = {'tags': ['foo', 'bar']}
    merged = xr.merge([da], combine_attrs='override')
    merged.attrs['meta']['tags'][0] = 'baz'
    assert da.attrs['meta']['tags'][0] == 'baz'

def test_override_shallow_copy_list_of_datasets_nested_share():
    ds1 = xr.Dataset()
    ds1.attrs['L'] = [[1, 2], {'x': [3, 4]}]
    ds2 = xr.Dataset(attrs={'other': 0})
    merged = xr.merge([ds1, ds2], combine_attrs='override')
    merged.attrs['L'][1]['x'].append(5)
    assert 5 in ds1.attrs['L'][1]['x']

def test_override_shallow_copy_preserves_shared_reference_identity():
    nested = {'foo': [1]}
    ds1 = xr.Dataset(attrs={'nested': nested})
    ds2 = xr.Dataset(attrs={'other': 0})
    merged = xr.merge([ds1, ds2], combine_attrs='override')
    assert merged.attrs['nested'] is ds1.attrs['nested']
    merged.attrs['nested']['foo'].append(9)
    assert 9 in ds1.attrs['nested']['foo']

def test_override_shallow_copy_with_mutable_values_in_lists():
    ds1 = xr.Dataset()
    ds1.attrs['complex'] = [{'a': 1}, {'b': 2}]
    merged = xr.merge([ds1], combine_attrs='override')
    merged.attrs['complex'][0]['a'] = 99
    assert ds1.attrs['complex'][0]['a'] == 99

def test_override_shallow_copy_combined_with_non_nested_values():
    ds1 = xr.Dataset(attrs={'alpha': {'x': 1}})
    ds2 = xr.Dataset(attrs={'beta': 2})
    merged = xr.merge([ds1, ds2], combine_attrs='override')
    merged.attrs['alpha']['x'] = 7
    assert ds1.attrs['alpha']['x'] == 7
    merged.attrs['gamma'] = 100
    assert 'gamma' not in ds1.attrs

def test_override_shallow_copy_after_multiple_merges_sharing_same_nested():
    nested = {'a': [0]}
    ds1 = xr.Dataset(attrs={'n': nested})
    ds2 = xr.Dataset(attrs={'other': 0})
    merged1 = xr.merge([ds1, ds2], combine_attrs='override')
    merged2 = xr.merge([merged1, ds2], combine_attrs='override')
    merged2.attrs['n']['a'].append(100)
    assert 100 in ds1.attrs['n']['a']

import pytest
import xarray as xr
import numpy as np
import copy
import pytest
import xarray as xr
import numpy as np
from xarray.core.merge import MergeError

def test_override_attrs_shallow_nested_dict_mutation_reflects_original():
    ds1 = xr.Dataset(attrs={'a': {'k': {'inner': 1}}})
    ds2 = xr.Dataset(attrs={'b': 2})
    merged = xr.merge([ds1, ds2], combine_attrs='override')
    merged.attrs['a']['k']['inner'] = 99
    assert ds1.attrs['a']['k']['inner'] == 99

def test_override_attrs_shallow_nested_list_mutation_reflects_original():
    ds1 = xr.Dataset(attrs={'a': {'lst': [1, 2, 3]}})
    ds2 = xr.Dataset(attrs={'b': 2})
    merged = xr.merge([ds1, ds2], combine_attrs='override')
    merged.attrs['a']['lst'][0] = 42
    assert ds1.attrs['a']['lst'][0] == 42

def test_override_attrs_shallow_mutating_original_nested_reflects_merged():
    ds1 = xr.Dataset(attrs={'a': {'m': [10, 20]}})
    ds2 = xr.Dataset(attrs={})
    merged = xr.merge([ds1, ds2], combine_attrs='override')
    ds1.attrs['a']['m'].append(30)
    assert merged.attrs['a']['m'][-1] == 30

def test_override_attrs_shallow_mutating_original_list_reflects_merged():
    ds1 = xr.Dataset(attrs={'a': {'m': [0]}})
    ds2 = xr.Dataset(attrs={})
    merged = xr.merge([ds1, ds2], combine_attrs='override')
    ds1.attrs['a']['m'][0] = 77
    assert merged.attrs['a']['m'][0] == 77

def test_override_attrs_shallow_pop_from_nested_changes_original():
    ds1 = xr.Dataset(attrs={'a': {'m': {'x': 1, 'y': 2}}})
    ds2 = xr.Dataset(attrs={})
    merged = xr.merge([ds1, ds2], combine_attrs='override')
    merged.attrs['a']['m'].pop('x')
    assert 'x' not in ds1.attrs['a']['m']
    assert 'y' in ds1.attrs['a']['m']

def test_override_attrs_shallow_clear_nested_changes_original():
    ds1 = xr.Dataset(attrs={'a': {'m': {'x': 1}}})
    ds2 = xr.Dataset(attrs={})
    merged = xr.merge([ds1, ds2], combine_attrs='override')
    merged.attrs['a']['m'].clear()
    assert ds1.attrs['a']['m'] == {}

def test_override_attrs_shallow_merge_keeps_other_keys():
    ds1 = xr.Dataset(attrs={'a': {'m': [1]}, 'c': 5})
    ds2 = xr.Dataset(attrs={'other': 10})
    merged = xr.merge([ds1, ds2], combine_attrs='override')
    assert merged.attrs['c'] == 5
    merged.attrs['a']['m'][0] = 999
    assert ds1.attrs['a']['m'][0] == 999

def test_override_attrs_shallow_with_multiple_datasets_uses_first_attrs_and_shares_nested():
    ds1 = xr.Dataset(attrs={'a': {'m': [7]}, 'keep': 'first'})
    ds2 = xr.Dataset(attrs={'a': {'m': [0]}, 'keep': 'second'})
    ds3 = xr.Dataset(attrs={'z': 1})
    merged = xr.merge([ds1, ds2, ds3], combine_attrs='override')
    assert merged.attrs['keep'] == 'first'
    merged.attrs['a']['m'].append(8)
    assert ds1.attrs['a']['m'][-1] == 8

import pytest
import xarray as xr
from xarray.core import dtypes
from xarray.core.merge import dataset_merge_method, merge_core

def test_shallow_copy_nested_mutation_propagates_to_source():
    nested = {'inner': {'x': 1}}
    ds1 = xr.Dataset(attrs={'nested': nested['inner']})
    ds2 = xr.Dataset(attrs={'other': 2})
    merged = xr.merge([ds1, ds2], combine_attrs='override')
    merged.attrs['nested']['x'] = 999
    assert ds1.attrs['nested']['x'] == 999

import pytest
import xarray as xr

def test_override_shallow_copy_nested_dict_mutation():
    ds1 = xr.Dataset(attrs={'nested': {'a': 1}})
    ds2 = xr.Dataset(attrs={'other': 2})
    merged = xr.merge([ds1, ds2], combine_attrs='override')
    merged.attrs['nested']['a'] = 42
    assert ds1.attrs['nested']['a'] == 42

def test_override_shallow_copy_nested_list_mutation():
    ds1 = xr.Dataset(attrs={'lst': [1, 2]})
    ds2 = xr.Dataset(attrs={})
    merged = xr.merge([ds1, ds2], combine_attrs='override')
    merged.attrs['lst'].append(3)
    assert ds1.attrs['lst'] == [1, 2, 3]

def test_override_shallow_copy_nested_list_in_dict_mutation():
    ds1 = xr.Dataset(attrs={'d': {'l': [0]}})
    ds2 = xr.Dataset(attrs={'x': 7})
    merged = xr.merge([ds1, ds2], combine_attrs='override')
    merged.attrs['d']['l'].append(99)
    assert ds1.attrs['d']['l'] == [0, 99]

def test_override_shallow_copy_list_of_dicts_mutation():
    ds1 = xr.Dataset(attrs={'a': [{'b': 1}]})
    ds2 = xr.Dataset(attrs={})
    merged = xr.merge([ds1, ds2], combine_attrs='override')
    merged.attrs['a'][0]['b'] = 10
    assert ds1.attrs['a'][0]['b'] == 10

def test_override_shallow_copy_nested_set_mutation():
    ds1 = xr.Dataset(attrs={'s': set([1])})
    ds2 = xr.Dataset(attrs={})
    merged = xr.merge([ds1, ds2], combine_attrs='override')
    merged.attrs['s'].add(2)
    assert ds1.attrs['s'] == set([1, 2])

def test_override_shallow_copy_deeply_nested_mutation():
    ds1 = xr.Dataset(attrs={'a': {'b': {'c': [0]}}})
    ds2 = xr.Dataset(attrs={})
    merged = xr.merge([ds1, ds2], combine_attrs='override')
    merged.attrs['a']['b']['c'].append(7)
    assert ds1.attrs['a']['b']['c'] == [0, 7]

def test_override_shallow_copy_single_dataset_mutation():
    ds1 = xr.Dataset(attrs={'nested': {'x': 1}})
    merged = xr.merge([ds1], combine_attrs='override')
    merged.attrs['nested']['x'] = 99
    assert ds1.attrs['nested']['x'] == 99

def test_override_shallow_copy_with_other_dataset_preserves_shallow_reference():
    ds1 = xr.Dataset(attrs={'inner': {'val': [1]}})
    ds2 = xr.Dataset(attrs={'meta': 0})
    merged = xr.merge([ds1, ds2], combine_attrs='override')
    merged.attrs['inner']['val'].append(5)
    assert ds1.attrs['inner']['val'] == [1, 5]