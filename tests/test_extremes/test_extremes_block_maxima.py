# pyextremes, Extreme Value Analysis in Python
# Copyright (C), 2020 Georgii Bocharov
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import logging
import os

import numpy as np
import pandas as pd
import pytest

from pyextremes.extremes import get_extremes

# Set up logging
logger = logging.getLogger('pyextremes.extremes')
logger.setLevel(logging.CRITICAL)

test_data = pd.read_csv(
    os.sep.join([*os.path.realpath(__file__).split(os.sep)[:-2], 'data', 'battery_wl.csv']),
    index_col=0, parse_dates=True, squeeze=True
)


def test_get_extremes():
    # Test BM with wrong extremes_type value
    with pytest.raises(ValueError):
        get_extremes(
            method='BM',
            ts=test_data,
            extremes_type='BAD TYPE',
            block_size='1Y',
            errors='coerce'
        )

    # Test BM with wrong block_size type
    with pytest.raises(TypeError):
        get_extremes(
            method='BM',
            ts=test_data,
            extremes_type='high',
            block_size=1,
            errors='coerce'
        )

    # Test wrong errors value
    with pytest.raises(ValueError):
        get_extremes(
            method='BM',
            ts=test_data,
            extremes_type='high',
            block_size='1Y',
            errors='BAD ERROR'
        )

    # Test errorrs raise
    with pytest.raises(ValueError):
        get_extremes(
            method='BM',
            ts=test_data,
            extremes_type='high',
            block_size='1Y',
            errors='raise'
        )

    # Test BM with extremes_type=high/low and errors=ignore/coerce
    for extremes_type in ['high', 'low']:
        extremes_ignored = get_extremes(
            method='BM',
            ts=test_data,
            block_size='1Y',
            extremes_type=extremes_type,
            errors='ignore'
        )
        assert len(extremes_ignored) == 96

        extremes_coerced = get_extremes(
            method='BM',
            ts=test_data,
            block_size='1Y',
            extremes_type=extremes_type,
            errors='coerce'
        )
        assert len(extremes_coerced) == 100

        assert np.isclose(extremes_ignored.max(), extremes_coerced.max())
        assert np.isclose(extremes_ignored.mean(), extremes_coerced.mean())