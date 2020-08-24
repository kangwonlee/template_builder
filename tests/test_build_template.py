import argparse
import os
import sys

import pytest

sys.path.insert(
        0,
        os.path.abspath(
            os.path.join(os.path.basename(__file__), os.pardir)
        )
    )

import build_template as bt


def test_get_arg_parser_type_check():
    parser = bt.get_arg_parser()

    assert isinstance(parser, argparse.ArgumentParser)


if "__main__" == __name__:
    pytest.main()
