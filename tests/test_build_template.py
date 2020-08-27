import argparse
import os
import sys
import tempfile

import pytest

sys.path.insert(
        0,
        os.path.abspath(
            os.path.join(os.path.basename(__file__), os.pardir)
        )
    )

import build_template as bt


@pytest.fixture
def parser() -> argparse.ArgumentParser:
    return bt.get_arg_parser()


def test_get_arg_parser_type_check(parser):

    assert isinstance(parser, argparse.ArgumentParser)


def test_get_arg_parser_arguments(parser):
    src_url = 'https://github.com/kangwonlee/build_template'
    ref = 'develop'
    new_folder = 'build_here'
    dest_url = 'https://github.com/kangwonlee/new_template'

    parsed = parser.parse_args(
        [
            '-s', src_url,
            '-r', ref,
            '-n', new_folder,
            '-d', dest_url,
        ]
    )

    assert parsed.src_repo_url == src_url
    assert parsed.reference == ref
    assert parsed.new_empty_folder == new_folder
    assert parsed.dest_repo_url == dest_url


if "__main__" == __name__:
    pytest.main()
