import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import numpy.ma as ma
from decimal import Decimal
import datetime
import matplotlib.dates as mdates
import datetime
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy.ma as ma
from decimal import Decimal
if __name__ == '__main__':
    test_bar_all_nan_single()
    test_bar_all_nan_then_valid()
    test_bar_leading_nan_masked_widths()
    test_barh_all_nan_horizontal_then_valid()
    test_broken_barh_timedelta_units()
    test_bar_timedelta_width_and_xerr()
    test_bar_decimal_widths_center_align()
    test_bar_masked_x_and_width_mixed()
    test_bar_nan_and_masked_combination_autoscale()