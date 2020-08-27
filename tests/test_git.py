import os
import subprocess
import sys

import pytest

sys.path.insert(
        0,
        os.path.abspath(
            os.path.join(os.path.basename(__file__), os.pardir)
        )
    )

import build_template as bt


@pytest.fixture
def git() -> bt.Git:
    return bt.Git()


def test_git_type_check(git):

    assert isinstance(git, bt.Git)


def test_git_status_type_check(git):

    r = git.status()

    assert isinstance(r, str), r


if "__main__" == __name__:
    pytest.main()
