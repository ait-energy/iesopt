import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from iesopt.results import Results


class TestToPandas_Long:
    def test__to_pandas_with_regular_items(self, create_result):
        # WHEN: results has variables/constraints/expressions for every snapshot
        results = create_result(
            snapshots=[1, 2, 3],
            data={
                ("comp1", "var", "my_var1"): [1.0, 2.0, 3.0],
                ("comp2", "var", "my_var2"): [4.0, 5.0, 6.0],
                ("comp2", "con", "my_con"): [7.0, 8.0, 9.0],
                ("comp2", "exp", "my_exp"): [10.0, 11.0, 12.0],
            },
        )
        df = results.to_pandas(orientation="long")

        assert_frame_equal(
            df,
            pd.DataFrame(
                {
                    "snapshot": [1, 2, 3] * 4,
                    "component": ["comp1"] * 3 + ["comp2"] * 9,
                    "fieldtype": ["var"] * 6 + ["con"] * 3 + ["exp"] * 3,
                    "field": ["my_var1"] * 3 + ["my_var2"] * 3 + ["my_con"] * 3 + ["my_exp"] * 3,
                    "value": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0],
                    "mode": ["primal"] * 12,
                }
            ),
        )

    def test__to_pandas_with_single_variable(self, create_result):
        # WHEN: results has a mix of array and single variables
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
        # WHEN: results has a variable marked as dual
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

    def test__to_pandas_with_irregular_array_variable(self, create_result):
        # WHEN: a results variable is an array with len >0 and len != len(snapshots)
        results = create_result(
            snapshots=[1, 2, 3],
            data={
                ("comp1", "var", "my_var1"): [1.0, 2.0, 3.0],
                ("comp1", "var", "my_var2"): [5.0, 10.0],
            },
        )
        df = results.to_pandas(orientation="long")
        assert_frame_equal(
            df,
            pd.DataFrame(
                {
                    "snapshot": [1, 2, 3, None, None],
                    "component": ["comp1"] * 5,
                    "fieldtype": ["var"] * 5,
                    "field": ["my_var1"] * 3 + ["my_var2[i_0]", "my_var2[i_1]"],
                    "value": [1.0, 2.0, 3.0, 5.0, 10.0],
                    "mode": ["primal"] * 5,
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
