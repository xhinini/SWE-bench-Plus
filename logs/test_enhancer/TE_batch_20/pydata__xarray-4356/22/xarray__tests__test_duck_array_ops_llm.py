import numpy as np
import pytest
from xarray.core import nanops, dtypes
nat_dtypes = [dt for dt in dtypes.NAT_TYPES if getattr(dt, 'kind', None) in ('M', 'm')]
if not nat_dtypes:
    pytest.skip('No NAT dtypes available in this xarray build/environment')
cases = []
for dt in nat_dtypes:
    cases.extend([(dt, np.array([True, True]), 1), (dt, np.array([True, True, False]), 2), (dt, np.array([False, False, False]), 5), (dt, np.array([True, False]), 2), (dt, np.array([True]), 1)])