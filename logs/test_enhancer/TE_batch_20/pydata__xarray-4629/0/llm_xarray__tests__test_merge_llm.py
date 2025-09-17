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