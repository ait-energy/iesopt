import iesopt
from pathlib import Path


class TestExamples:
    def write_to_file(self, tmp_path):
        model = iesopt.Model(iesopt.make_example("01_basic_single_node", dst_dir=tmp_path))
        assert Path(model.write_to_file()).exists()
        assert Path(model.write_to_file(tmp_path / "my_problem.LP")).exists()
        assert Path(model.write_to_file(tmp_path / "my_problem.foo", format="mof")).exists()
