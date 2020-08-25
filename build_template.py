"""
# Template builder

Out of an existing development repository, 
build a template repostiory with just one commit.

## Arguments

usage: build_template.py [-h] [-s SRC_REPO_URL] [-r REFERENCE]
                         [-n NEW_EMPTY_FOLDER] [-d DEST_REPO_URL]

Template builder

optional arguments:
  -h, --help            show this help message and exit
  -s SRC_REPO_URL, --src_repo_url SRC_REPO_URL
                        URL to source development repository
  -r REFERENCE, --reference REFERENCE
                        Reference of source repository
  -n NEW_EMPTY_FOLDER, --new_empty_folder NEW_EMPTY_FOLDER
                        New empty folder
  -d DEST_REPO_URL, --dest_repo_url DEST_REPO_URL
                        URL to source development repository

## Procedure example

git clone <existing remote repository>
pushd <local repository>
git switch <reference>
mkdir <new empty folder>
pushd <new empty folder>
git init
git config user.name <user name>
git config user.email<user email>
popd
copy all contents to <new empty folder> except .git/ folder 
pushd <new empty folder>
git add --all .
git commit -m "initial commit"
git remote add origin <new remote repository>
git push origin
"""


import argparse
import configparser
import dataclasses
import os
import subprocess
import sys
import typing
import urllib.parse as up
from typing import List, Union


@dataclasses.dataclass
class Git(object):
    git_cmd:str='git'

    def run_list(self, arg_list:List[str], cwd=None) -> subprocess.CompletedProcess:
        return subprocess.run(
            [self.git_cmd] + arg_list,
            capture_output=subprocess.PIPE, check=True,
            cwd=cwd,
        )

    def status(self) -> str:
        return self.run_list(['status']).stdout.decode()

    def clone(self, source_url, dest_folder):
        assert not os.path.exists(dest_folder), f"destination folder {dest_folder} exists"
        return self.run_list(['clone', source_url, dest_folder])


def main(argv:List[str]=sys.argv):
    parser = get_arg_parser()
    parsed = parser.parse_args(argv[1:])


def get_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Template builder")
    parser.add_argument("-s", "--src_repo_url", type=str, help=f"URL to source development repository")
    parser.add_argument("-c", "--clone_folder", type=str, help=f"Clone the source development repository to here")
    parser.add_argument("-r", "--reference", type=str, default='master', help="Reference of source repository")
    parser.add_argument("-n", "--new_empty_folder", type=str, help="New empty folder")
    parser.add_argument("-d", "--dest_repo_url", type=str, help="URL to source development repository")
    return parser


if "__main__" == __name__:
    main(sys.argv)
