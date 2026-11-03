import iesopt


def _check_example_model(name: str, dst_dir, checks: dict, mode: str = "check"):
    config_file = iesopt.make_example(name, dst_dir=str(dst_dir), dst_name="config")
    model = iesopt.run(config_file, config={"general.verbosity.core": "error"})

    if mode == "check":
        assert str(model.status) == checks["status"]
    else:
        assert mode == "print"
        print(str(model.status))

    obj = model.objective_value

    if checks and (checks["objective_value"] == "moa"):
        if mode == "check":
            assert obj is not None
            assert not isinstance(obj, float)
        else:
            print(obj)
    else:
        if mode == "check":
            assert (obj - checks["objective_value"]) < 1e-4
        else:
            print(obj)

    return model


class TestExamples:
    def test_example_list(self):
        example_list = iesopt.examples()
        assert isinstance(example_list, list)
        assert len(example_list) > 0
        assert all(isinstance(it, str) for it in example_list)

    def test_make_example(self, tmp_path):
        example_list = iesopt.examples()
        example = example_list[0]

        config_file = iesopt.make_example(example, dst_dir=tmp_path)
        assert config_file.exists()
        assert (tmp_path / f"{example}.iesopt.yaml").exists()
        assert (tmp_path / "files").exists()

        iesopt.make_example(example, dst_dir=tmp_path / "examples", dst_name="config")
        assert (tmp_path / "examples" / "config.iesopt.yaml").exists()
        assert (tmp_path / "examples" / "files").exists()

    def test_example_01(self, tmp_path):
        # _check_example_model("01_basic_single_node", "/tmp/iesopt-tmp/", None, "print")
        model = _check_example_model(
            "01_basic_single_node",
            tmp_path,
            {"status": "ModelStatus.OPTIMAL", "objective_value": 525.0},
        )
        # test get_component(s)
        node = model.get_component("node")
        assert node.name == "node"
        all_components = model.get_components()
        assert len(all_components) == 8
        node_components = model.get_components("Node")
        assert len(node_components) == 3
        no_componens = model.get_components(["Unit", "Profile"])
        assert len(no_componens) == 0

    def test_example_02(self, tmp_path):
        # _check_example_model("02_advanced_single_node", "/tmp/iesopt-tmp/", None, "print")
        _check_example_model(
            "02_advanced_single_node",
            tmp_path,
            {"status": "ModelStatus.OPTIMAL", "objective_value": 1506.75},
        )

    def test_example_03(self, tmp_path):
        # _check_example_model("03_basic_two_nodes", "/tmp/iesopt-tmp/", None, "print")
        _check_example_model(
            "03_basic_two_nodes",
            tmp_path,
            {"status": "ModelStatus.OPTIMAL", "objective_value": 1225.0},
        )

    def test_example_04(self, tmp_path):
        # _check_example_model("04_soft_constraints", "/tmp/iesopt-tmp/", None, "print")
        _check_example_model(
            "04_soft_constraints",
            tmp_path,
            {"status": "ModelStatus.OPTIMAL", "objective_value": 1000002975.0},
        )

    def test_example_05(self, tmp_path):
        # _check_example_model("05_basic_two_nodes_1y", "/tmp/iesopt-tmp/", None, "print")
        _check_example_model(
            "05_basic_two_nodes_1y",
            tmp_path,
            {"status": "ModelStatus.OPTIMAL", "objective_value": 667437.75},
        )

    def test_example_06(self, tmp_path):
        # _check_example_model("06_recursion_h2", "/tmp/iesopt-tmp/", None, "print")
        _check_example_model(
            "06_recursion_h2",
            tmp_path,
            {"status": "ModelStatus.OPTIMAL", "objective_value": 18790.8},
        )

    def test_example_07(self, tmp_path):
        # _check_example_model("07_csv_filestorage", "/tmp/iesopt-tmp/", None, "print")
        _check_example_model(
            "07_csv_filestorage",
            tmp_path,
            {"status": "ModelStatus.OPTIMAL", "objective_value": 667437.75},
        )

    def test_example_08(self, tmp_path):
        # _check_example_model("08_basic_investment", "/tmp/iesopt-tmp/", None, "print")
        _check_example_model(
            "08_basic_investment",
            tmp_path,
            {"status": "ModelStatus.OPTIMAL", "objective_value": 2015.642857142858},
        )

    def test_example_09(self, tmp_path):
        # _check_example_model("09_csv_only", "/tmp/iesopt-tmp/", None, "print")
        _check_example_model(
            "09_csv_only",
            tmp_path,
            {"status": "ModelStatus.OPTIMAL", "objective_value": 667437.75},
        )

    def test_example_10(self, tmp_path):
        # _check_example_model("10_basic_load_shedding", "/tmp/iesopt-tmp/", None, "print")
        _check_example_model(
            "10_basic_load_shedding",
            tmp_path,
            {"status": "ModelStatus.OPTIMAL", "objective_value": 26083.94444444445},
        )

    def test_example_11(self, tmp_path):
        # _check_example_model("11_basic_unit_commitment", "/tmp/iesopt-tmp/", None, "print")
        _check_example_model(
            "11_basic_unit_commitment",
            tmp_path,
            {"status": "ModelStatus.OPTIMAL", "objective_value": 1570.0},
        )

    def test_example_12(self, tmp_path):
        # _check_example_model("12_incremental_efficiency", "/tmp/iesopt-tmp/", None, "print")
        _check_example_model(
            "12_incremental_efficiency",
            tmp_path,
            {"status": "ModelStatus.OPTIMAL", "objective_value": 3570.0},
        )

    def test_example_15(self, tmp_path):
        # _check_example_model("15_varying_efficiency", "/tmp/iesopt-tmp/", None, "print")
        _check_example_model(
            "15_varying_efficiency",
            tmp_path,
            {"status": "ModelStatus.OPTIMAL", "objective_value": 2131435.7798025194},
        )

    def test_example_16(self, tmp_path):
        # _check_example_model("16_noncore_components", "/tmp/iesopt-tmp/", None, "print")
        _check_example_model(
            "16_noncore_components",
            tmp_path,
            {"status": "ModelStatus.OPTIMAL", "objective_value": 4372.20640901404},
        )

    def test_example_17(self, tmp_path):
        # _check_example_model("17_varying_connection_capacity", "/tmp/iesopt-tmp/", None, "print")
        _check_example_model(
            "17_varying_connection_capacity",
            tmp_path,
            {"status": "ModelStatus.OPTIMAL", "objective_value": 300.0},
        )

    def test_example_18(self, tmp_path):
        # _check_example_model("18_addons", "/tmp/iesopt-tmp/", None, "print")
        _check_example_model(
            "18_addons",
            tmp_path,
            {"status": "ModelStatus.OPTIMAL", "objective_value": 51.0},
        )

    def test_example_20(self, tmp_path):
        # _check_example_model("20_chp", "/tmp/iesopt-tmp/", None, "print")
        _check_example_model(
            "20_chp",
            tmp_path,
            {"status": "ModelStatus.OPTIMAL", "objective_value": 16687.5},
        )

    def test_example_22(self, tmp_path):
        # _check_example_model("22_snapshot_weights", "/tmp/iesopt-tmp/", None, "print")
        _check_example_model(
            "22_snapshot_weights",
            tmp_path,
            {"status": "ModelStatus.OPTIMAL", "objective_value": 215.0},
        )

    def test_example_23(self, tmp_path):
        # _check_example_model("23_snapshots_from_csv", "/tmp/iesopt-tmp/", None, "print")
        _check_example_model(
            "23_snapshots_from_csv",
            tmp_path,
            {"status": "ModelStatus.OPTIMAL", "objective_value": 215.0},
        )

    def test_example_25(self, tmp_path):
        # _check_example_model("25_global_parameters", "/tmp/iesopt-tmp/", None, "print")
        _check_example_model(
            "25_global_parameters",
            tmp_path,
            {"status": "ModelStatus.OPTIMAL", "objective_value": 50.0},
        )

    def test_example_27(self, tmp_path):
        # _check_example_model("27_piecewise_linear_costs", "/tmp/iesopt-tmp/", None, "print")
        _check_example_model(
            "27_piecewise_linear_costs",
            tmp_path,
            {"status": "ModelStatus.OPTIMAL", "objective_value": 450.0},
        )

    def test_example_29(self, tmp_path):
        # _check_example_model("29_advanced_unit_commitment", "/tmp/iesopt-tmp/", None, "print")
        _check_example_model(
            "29_advanced_unit_commitment",
            tmp_path,
            {"status": "ModelStatus.OPTIMAL", "objective_value": 7000.0},
        )

    def test_example_31(self, tmp_path):
        # _check_example_model("31_exclusive_operation", "/tmp/iesopt-tmp/", None, "print")
        _check_example_model(
            "31_exclusive_operation",
            tmp_path,
            {"status": "ModelStatus.OPTIMAL", "objective_value": -10.0},
        )

    # def test_example_35(self, tmp_path):
    #     _check_example_model(
    #         "35_fixed_costs",
    #         tmp_path,
    #         {
    #             "status": "ModelStatus.OPTIMAL",
    #             "objective_value": 91539936.26783474,
    #         },
    #     )

    def test_example_37(self, tmp_path):
        # _check_example_model("37_certificates", "/tmp/iesopt-tmp/", None, "print")
        _check_example_model(
            "37_certificates",
            tmp_path,
            {"status": "ModelStatus.OPTIMAL", "objective_value": 44376.75},
        )

    def test_example_41(self, tmp_path):
        # _check_example_model("41_multiobjective_epsilon", "/tmp/iesopt-tmp/", None, "print")
        model = _check_example_model(
            "41_multiobjective_epsilon",
            tmp_path,
            {"status": "ModelStatus.OPTIMAL", "objective_value": "moa"},
        )

        assert len(model.objective_value) == 2
        assert abs(model.objective_value[0] - 2625.0) < 1e-4
        assert abs(model.objective_value[1] - 7.5) < 1e-4

    def test_example_43(self, tmp_path):
        # _check_example_model("43_multiobjective_hierarchical", "/tmp/iesopt-tmp/", None, "print")
        model = _check_example_model(
            "43_multiobjective_hierarchical",
            tmp_path,
            {"status": "ModelStatus.OPTIMAL", "objective_value": "moa"},
        )

        assert len(model.objective_value) == 3
        assert abs(model.objective_value[0] - 3281.25) < 1e-4
        assert abs(model.objective_value[1] - 7.459780388151175) < 1e-4
        assert abs(model.objective_value[2] - 52.298901940755876) < 1e-4

    def test_example_44(self, tmp_path):
        # _check_example_model("44_lossy_connections", "/tmp/iesopt-tmp/", None, "print")
        _check_example_model(
            "44_lossy_connections",
            tmp_path,
            {"status": "ModelStatus.OPTIMAL", "objective_value": 1233.75},
        )

    def test_example_45(self, tmp_path):
        # _check_example_model("45_result_extraction", "/tmp/iesopt-tmp/", None, "print")
        _check_example_model(
            "45_result_extraction",
            tmp_path,
            {"status": "ModelStatus.OPTIMAL", "objective_value": 1427.9999999999998},
        )

    def test_example_46(self, tmp_path):
        # _check_example_model("46_constants_in_objective", "/tmp/iesopt-tmp/", None, "print")
        _check_example_model(
            "46_constants_in_objective",
            tmp_path,
            {"status": "ModelStatus.OPTIMAL", "objective_value": 3015.642857142858},
        )

    def test_example_47(self, tmp_path):
        # _check_example_model("47_disable_components", "/tmp/iesopt-tmp/", None, "print")
        _check_example_model(
            "47_disable_components",
            tmp_path,
            {"status": "ModelStatus.OPTIMAL", "objective_value": 550.0},
        )
