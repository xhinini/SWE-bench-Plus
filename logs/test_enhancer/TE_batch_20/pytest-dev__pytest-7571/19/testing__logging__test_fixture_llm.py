import logging
import pytest
for i in range(1, 9):
    globals()[f'test_restore_order_named_{i}'] = _make_named_logger_test(f'my.custom.logger.{i}')