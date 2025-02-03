import pytest
import re
import os
from unittest import mock


@mock.patch.dict(os.environ, {"IESOPT_DOCS_NOEXEC": "True"})
def test_julia_ci_version_consistent_with_python_package(project_root_path):
    import iesopt

    julia_python = iesopt.config.Config.DEFAULTS["IESOPT_JULIA"]

    # parse the CI action that sets the julia version
    julia_ci = "unknown"
    with open(f"{project_root_path}/.github/actions/set-versions/action.yml") as f:
        for line in f.readlines():
            if "VERSION_JULIA" in line:
                julia_ci = re.search('.*VERSION_JULIA=(.*)"', line).group(1)
                break

    assert julia_python == julia_ci, "CI Julia differs from Python Julia"


@pytest.fixture
def project_root_path(request):
    return request.config.rootpath
