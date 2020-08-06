from os.path import abspath, dirname
from pathlib import Path
from shutil import rmtree

import nox

REPO_ROOT_PATH = dirname(abspath(__file__))

PYTHON_VERSION = "3.8"


nox.options.stop_on_first_error = True
nox.options.reuse_existing_virtualenvs = True

# Default workflow
nox.options.sessions = ["black", "isort", "lint", "test", "clean"]

lint_locations = ["beaconator/backend"]
format_locations = "beaconator", "tests", "noxfile.py"


@nox.session(python=False)
def black(session):
    args = session.posargs or format_locations
    session.install("black")
    session.run("black", *args)


@nox.session(python=False)
def isort(session):
    args = session.posargs or format_locations
    session.install("isort")
    session.run("isort", *args)


@nox.session(python=PYTHON_VERSION)
def lint(session):
    args = session.posargs or lint_locations
    session.install(
        "flake8",
        "flake8-bandit",
        "flake8-black",
        "flake8-bugbear",
        "flake8-isort",
        "flake8-annotations",
    )
    session.run("flake8", *args)


@nox.session(python=False)
def test(session):
    """Run development tests for the package."""
    if session.posargs:
        pytest_args = session.posargs
    else:
        pytest_args = ("--last-failed", "--last-failed-no-failures", "all")
    session.run("pytest", *pytest_args)


@nox.session(python=False)
def clean(session):
    """Remove all .venv's, build files and caches in the directory."""
    Path(".coverage").unlink(missing_ok=True)
    rmtree("build", ignore_errors=True)
    rmtree("dist", ignore_errors=True)
    rmtree(".mypy_cache", ignore_errors=True)
    rmtree(".pytest_cache", ignore_errors=True)
    rmtree(".venv", ignore_errors=True)
    session.run(
        "python3",
        "-c",
        "import pathlib;"
        + "[p.unlink() for p in pathlib.Path('%s').rglob('*.py[co]')]" % REPO_ROOT_PATH,
    )
    session.run(
        "python3",
        "-c",
        "import pathlib;"
        + "[p.rmdir() for p in pathlib.Path('%s').rglob('__pycache__')]"
        % REPO_ROOT_PATH,
    )
