import iesopt


class TestPythonJuliaConversion:
    def test_kwargs_dict(self, tmp_path):
        # Refer to: https://github.com/ait-energy/IESopt.jl/issues/66

        configs = [
            {"a": 1, "b": 2.0, "c": "string"},
            {"a": 1, "c": "string"} | {"b": 2.0},
            {"b": 2.0} | {"a": 1, "c": "string"},
        ]

        for config in configs:
            model = iesopt.Model("", config=config)
            assert type(model._kwargs["config"]["a"]) is int
