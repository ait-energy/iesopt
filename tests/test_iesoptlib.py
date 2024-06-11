import iesopt


class TestIESoptLib:
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

    def test_run_example(self, tmp_path):
        config_file = iesopt.make_example("01_basic_single_node", dst_dir=tmp_path, dst_name="config")
        model = iesopt.run(config_file, verbosity=False)
        assert model is not None
        # assert model.status == "Optimal"
        # assert model.objective_value is not None
