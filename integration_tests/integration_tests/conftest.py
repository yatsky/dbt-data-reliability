import pathlib

import pytest
from dbt.version import __version__
from packaging import version

from .dbt_project import DbtProject

DBT_PROJECT_DIR = pathlib.Path(__file__).parent.parent


def pytest_addoption(parser):
    parser.addoption(
        "--project-dir",
        action="store",
        default=str(DBT_PROJECT_DIR),
        help="dbt project dir to use",
    )
    parser.addoption(
        "--target", action="store", default="postgres", help="dbt project target to use"
    )


@pytest.fixture(scope="session")
def dbt_version():
    return version.parse(__version__)


@pytest.fixture(scope="session")
def dbt_target(request):
    return request.config.getoption("--target")


@pytest.fixture(scope="session")
def dbt_project_dir(request):
    return request.config.getoption("--project-dir")


@pytest.fixture(scope="session")
def dbt_project(dbt_project_dir, dbt_target):
    project = DbtProject(project_dir=dbt_project_dir, target=dbt_target)
    project.clear_test_env()
    yield project
    project.cleanup()
