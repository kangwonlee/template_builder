import argparse
import itertools
import os
import random
import subprocess
import sys
import tempfile
import urllib.parse as up

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


def test_copy_repo(tmpdir_factory):
    source_repo_folder = tmpdir_factory.mktemp('source')
    # prepare source repo

    subprocess.check_call(['git', 'init'], cwd=source_repo_folder)
    subprocess.check_call(['git', 'config', 'user.name', 'source'], cwd=source_repo_folder)
    subprocess.check_call(['git', 'config', 'user.email', 'source@testing.io'], cwd=source_repo_folder)

    source_files = []

    for _ in itertools.repeat(None, random.randint(3, 9)):

        filename = f'file_{random.randint(0, 99):02d}.txt'

        with open(os.path.join(source_repo_folder, filename), 'wt', encoding='utf-8') as f:
            f.write(
                str(
                    random.choices(
                        list(range(100)),
                        k=10
                    )
                )
            )
            f.write('\n')

        assert os.path.exists(
            os.path.join(source_repo_folder, filename)
        ), f"test file {filename} not created in {source_repo_folder}"

        source_files.append(filename)

        subprocess.check_call(['git', 'add', filename], cwd=source_repo_folder)
        subprocess.check_call(['git', 'commit', '-m', filename], cwd=source_repo_folder)
    # source now prepared

    # prepare a destination repo
    destination_repo_folder = tmpdir_factory.mktemp('destination')

    subprocess.check_call(['git', 'init'], cwd=destination_repo_folder)
    subprocess.check_call(['git', 'config', 'user.name', 'destination'], cwd=source_repo_folder)
    subprocess.check_call(['git', 'config', 'user.email', 'destination@testing.io'], cwd=destination_repo_folder)
    # destination now prepared

    # function under test
    bt.copy_repo(source_repo_folder, destination_repo_folder)

    # all files copied?
    for src_file in source_files:
        assert src_file in os.listdir(destination_repo_folder), f"File {src_file} missing in destination folder"


@pytest.fixture
def source_repo_url() -> str:
    return up.urlunparse(
        ('https', 'github.com', 'kangwonlee/to_test_template_builder', None, None, None)
    )

def test_build_template(tmp_path, source_repo_url):

    source_folder = os.path.join(tmp_path, 'source')
    assert not os.path.exists(source_folder)

    destination_folder = os.path.join(tmp_path, 'destination')
    assert not os.path.exists(destination_folder)

    bt.build_template(
        source_repo_url,
        source_folder,
        'master',
        destination_folder,
        'None'
    )

    assert os.path.exists(source_folder)
    assert os.path.exists(destination_folder)

    commit_log_message = subprocess.check_output(['git', 'log', '--oneline', '--all'], cwd=destination_folder)
    assert 1 == len(commit_log_message.splitlines()), (
        'more than one commit\n',
        commit_log_message
    )


if "__main__" == __name__:
    pytest.main()
