import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from iesopt.results import Results


class TestToPandas_Long:
    def test__to_pandas_with_snapshot_variables(self, create_result):
        results = create_result(
            snapshots=[1, 2, 3],
            data={
                ("comp1", "var", "my_var1"): [1.0, 2.0, 3.0],
                ("comp2", "var", "my_var2"): [4.0, 5.0, 6.0],
            },
        )
        df = results.to_pandas(orientation="long")

        assert_frame_equal(
            df,
            pd.DataFrame(
                {
                    "snapshot": [1, 2, 3] * 2,
                    "component": ["comp1"] * 3 + ["comp2"] * 3,
                    "fieldtype": ["var"] * 6,
                    "field": ["my_var1"] * 3 + ["my_var2"] * 3,
                    "value": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
                    "mode": ["primal"] * 6,
                }
            ),
        )

    def test__to_pandas_with_single_variable(self, create_result):
        results = create_result(
            snapshots=[1, 2, 3],
            data={
                ("comp1", "var", "my_var1"): 4.0,
                ("comp2", "var", "my_var2"): [1.0, 2.0, 3.0],
            },
        )
        df = results.to_pandas(orientation="long")
        assert_frame_equal(
            df,
            pd.DataFrame(
                {
                    "snapshot": [None, 1, 2, 3],
                    "component": ["comp1"] + ["comp2"] * 3,
                    "fieldtype": ["var"] * 4,
                    "field": ["my_var1"] + ["my_var2"] * 3,
                    "value": [4.0, 1.0, 2.0, 3.0],
                    "mode": ["primal"] * 4,
                }
            ),
        )

    def test__to_pandas_with_dual_variable(self, create_result):
        results = create_result(
            snapshots=[1, 2, 3],
            data={
                ("comp1", "var", "my_var1__dual"): [1.0, 2.0, 3.0],
            },
        )
        df = results.to_pandas(orientation="long")
        assert_frame_equal(
            df,
            pd.DataFrame(
                {
                    "snapshot": [1, 2, 3],
                    "component": ["comp1"] * 3,
                    "fieldtype": ["var"] * 3,
                    "field": ["my_var1"] * 3,
                    "value": [1.0, 2.0, 3.0],
                    "mode": ["dual"] * 3,
                }
            ),
        )


@pytest.fixture
def create_result(mocker):
    def _create_result(snapshots, data):
        r = Results(model=mocker.MagicMock())
        r._snapshots = snapshots
        r.to_dict = lambda *args: data
        return r

    return _create_result
