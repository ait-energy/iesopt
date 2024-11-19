import iesopt

import pandas as pd
import hashlib


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

    def test_run_examples(self, tmp_path):
        checks = {
            "01_basic_single_node": {
                "status": "ModelStatus.OPTIMAL",
                "objective_value": 525.0,
                "hash": "61b2babb5f58c7fd44a0e9b98353a760320adcc623e1999703112600c51286a7",
            },
            "02_advanced_single_node": {
                "status": "ModelStatus.OPTIMAL",
                "objective_value": 1506.75,
                "hash": "db796af7bbc546f5273bee029753d8b9cb0e0490cc81a316a1b86da47ac26a86",
            },
            "03_basic_two_nodes": {
                "status": "ModelStatus.OPTIMAL",
                "objective_value": 1225.0,
                "hash": "4637add63e6f0a60df332af31e9602b60733f50032a92c2a167a7cbcb754c202",
            },
            "04_soft_constraints": {
                "status": "ModelStatus.OPTIMAL",
                "objective_value": 1000002975.0,
                "hash": "061919112bea66bac9b2f96f634c5eaff721524338e67e752062da4c6618d3c0",
            },
            "05_basic_two_nodes_1y": {
                "status": "ModelStatus.OPTIMAL",
                "objective_value": 667437.75,
                "hash": "8927bf59e2f49ff9183fbe072531c7563e56b8b664af556f7f47ea3cc2793c1e",
            },
            "06_recursion_h2": {
                "status": "ModelStatus.OPTIMAL",
                "objective_value": 18790.8,
                "hash": "f1eceeb55dfc5cf096faacc6b7bd126bfea8508c37e9a14549051e8d39036956",
            },
            "07_csv_filestorage": {
                "status": "ModelStatus.OPTIMAL",
                "objective_value": 667437.75,
                "hash": "8927bf59e2f49ff9183fbe072531c7563e56b8b664af556f7f47ea3cc2793c1e",
            },
            "08_basic_investment": {
                "status": "ModelStatus.OPTIMAL",
                "objective_value": 2015.642857142858,
                "hash": "61800693a41cba62b62a8a533449495a8410a67cdf402a01fa1148dea75aa608",
            },
            "09_csv_only": {
                "status": "ModelStatus.OPTIMAL",
                "objective_value": 667437.75,
                "hash": "8927bf59e2f49ff9183fbe072531c7563e56b8b664af556f7f47ea3cc2793c1e",
            },
            "10_basic_load_shedding": {
                "status": "ModelStatus.OPTIMAL",
                "objective_value": 26083.94444444445,
                "hash": "2948714ed032a5e77b04edcda81401dbe4b882a15c80bd7cf41068f2e00596ae",
            },
            "11_basic_unit_commitment": {
                "status": "ModelStatus.OPTIMAL",
                "objective_value": 1570.0,
                "hash": "b67e5103b67fe22c97c1ca73092e2bd3f3b9d00f28949681a06999598685735a",
            },
            "12_incremental_efficiency": {
                "status": "ModelStatus.OPTIMAL",
                "objective_value": 3570.0,
                "hash": "8e5b363573c4180cb681db91ac243ff73aa8a78426ebd3a0094ea91d71596818",
            },
            "15_varying_efficiency": {
                "status": "ModelStatus.OPTIMAL",
                "objective_value": 2131435.7798025194,
                "hash": "c2c57aae2a411bf2a8ebec6111c14201a6d61c243bf42b84e49e2024c58445a5",
            },
            "16_noncore_components": {
                "status": "ModelStatus.OPTIMAL",
                "objective_value": 4372.20640901404,
                "hash": "766f283aeda00468e38c9fcc9289da2fcb31d2cf5d93d1227ef028eea9f090c2",
            },
            "17_varying_connection_capacity": {
                "status": "ModelStatus.OPTIMAL",
                "objective_value": 300.0,
                "hash": "80cd1605c4081ada6c8469a407aee6bc804dac7312a01f86c4d399636608ec32",
            },
            "18_addons": {"status": "ModelStatus.OPTIMAL", "objective_value": 51.0, "hash": None},
            "20_chp": {
                "status": "ModelStatus.OPTIMAL",
                "objective_value": 16687.5,
                "hash": "1f9eaa3c5971d34963536203e4c2e64aaba797755ddc006d49d38903a1a8f604",
            },
            "22_snapshot_weights": {
                "status": "ModelStatus.OPTIMAL",
                "objective_value": 215.0,
                "hash": "734be715c9900ddfb23522a8ea763ae950f01570480cd7a7dfb6460de723d0d1",
            },
            "23_snapshots_from_csv": {
                "status": "ModelStatus.OPTIMAL",
                "objective_value": 215.0,
                "hash": "8ade2018d0efd4f4285a10ed6b29ac15d09d2484555acbc11206f3809f7c77f6",
            },
            "25_global_parameters": {
                "status": "ModelStatus.OPTIMAL",
                "objective_value": 50.0,
                "hash": "f6f2c825d60d1f3eb4649e802fde06e557cfe1d68caa8e89ec141c5713b99526",
            },
            "27_piecewise_linear_costs": {
                "status": "ModelStatus.OPTIMAL",
                "objective_value": 450.0,
                "hash": "121ad8052fd4252fdf2b8c2818201aa1ccdb0014f3c9db3526e75e2dd1ef264a",
            },
            "29_advanced_unit_commitment": {
                "status": "ModelStatus.OPTIMAL",
                "objective_value": 7000.0,
                "hash": "2494022e1bded1e072566050f8b79ea86cd2603239c7ff4e2a0b5fac44823250",
            },
            "31_exclusive_operation": {
                "status": "ModelStatus.OPTIMAL",
                "objective_value": -10.0,
                "hash": "7a0073ecd28bcbc6b98764c08060923b1fe4136a9b8bd7ec21bba216b98b479c",
            },
            "35_fixed_costs": {
                "status": "ModelStatus.OPTIMAL",
                "objective_value": 91539936.26783474,
                "hash": "4b3ba12112f436acb43fda8cc446d12bc8e8742d4ddfcaa6c27dfa74a8ee655c",
            },
            "37_certificates": {"status": "ModelStatus.OPTIMAL", "objective_value": 44376.75, "hash": None},
            "41_multiobjective_epsilon": {
                "status": "ModelStatus.OPTIMAL",
                "objective_value": "moa",
                "hash": "bba8f7e0a6bc2e4916a92f6fdf109a0f6fbe70a7db1582b860c35105f1212534",
            },
            "43_multiobjective_hierarchical": {
                "status": "ModelStatus.OPTIMAL",
                "objective_value": "moa",
                "hash": "46ada70f69c437a4221c2373a13a1829a3c3d5bac2215dcd4ab7a943a345389a",
            },
            "44_lossy_connections": {
                "status": "ModelStatus.OPTIMAL",
                "objective_value": 1233.75,
                "hash": "2de6bbd289b495d436c4e025bd91d3551e7b73543081477b97dfde41a5e571b5",
            },
            "45_result_extraction": {
                "status": "ModelStatus.OPTIMAL",
                "objective_value": 1427.9999999999998,
                "hash": "1736e5d7b6c797d354b3054698456e6ce68ca7a4ad9e0a25e930e169a8169019",
            },
            "46_constants_in_objective": {
                "status": "ModelStatus.OPTIMAL",
                "objective_value": 3015.642857142858,
                "hash": "61800693a41cba62b62a8a533449495a8410a67cdf402a01fa1148dea75aa608",
            },
            "47_disable_components": {
                "status": "ModelStatus.OPTIMAL",
                "objective_value": 550.0,
                "hash": "69150c32a10fd1c236c22ecf6fd7fcf065fd4afbe60dca6237e2198709cfc137",
            },
        }

        for ex in checks.keys():
            config_file = iesopt.make_example(ex, dst_dir=tmp_path, dst_name="config")
            model = iesopt.run(config_file, config={"general.verbosity.core": "error"})

            assert str(model.status) == checks[ex]["status"]

            obj = model.objective_value

            if checks[ex]["objective_value"] == "moa":
                assert obj is not None
                assert not isinstance(obj, float)
            else:
                assert (obj - checks[ex]["objective_value"]) < 1e-4

            if checks[ex]["hash"]:
                res = model.results.to_pandas()
                hash = hashlib.sha256(pd.util.hash_pandas_object(res, index=True).values).hexdigest()
                assert hash == checks[ex]["hash"]
