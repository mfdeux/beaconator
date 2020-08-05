import nox

lint_locations = ["beaconator/backend"]
format_locations = "beaconator", "tests", "noxfile.py"


# @nox.session(python=["3.8"])
# def black(session):
#     args = session.posargs or format_locations
#     session.install("black")
#     session.run("black", *args)
#
#
# @nox.session(python=["3.8"])
# def isort(session):
#     args = session.posargs or format_locations
#     session.install("isort")
#     session.run("isort", *args)


@nox.session(python=["3.8"])
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
