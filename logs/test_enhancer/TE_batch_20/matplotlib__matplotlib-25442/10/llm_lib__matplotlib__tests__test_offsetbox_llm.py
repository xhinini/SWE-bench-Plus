import types
from collections import namedtuple
import pytest
import matplotlib.pyplot as plt
from matplotlib.offsetbox import DraggableAnnotation, DraggableOffsetBox, DraggableBase, TextArea
Mouse = namedtuple('Mouse', 'x y')
PickEvent = namedtuple('PickEvent', 'artist mouseevent')