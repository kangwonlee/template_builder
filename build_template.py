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
import shutil
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

    def checkout(self, local_repo_path:str, ref:str='master'):
        assert os.path.exists(local_repo_path)
        return self.run_list(['checkout', ref], cwd=local_repo_path)

    def init(self, dest_path:str):
        assert os.path.exists(dest_path)
        assert not os.listdir(dest_path), f"Destination folder {dest_path} not empty\n{os.listdir(dest_path)}"
        return self.run_list(['init'], cwd=dest_path)

    def add_all(self, dest_path:str):
        assert os.path.exists(dest_path)
        assert (('.git' in os.listdir(dest_path)) and os.path.isdir(os.path.join(dest_path, '.git'))), f"Destination folder does not have '.git/'"
        return self.run_list(['add', '--all'], cwd=dest_path)

    def commit(self, dest_path:str, message:str='initial commit'):
        assert os.path.exists(dest_path)
        assert (('.git' in os.listdir(dest_path)) and os.path.isdir(os.path.join(dest_path, '.git'))), f"Destination folder does not have '.git/'"
        return self.run_list(['commit', '--message', message], cwd=dest_path)

    def remote_add(self, new_repo_path:str, remote_url:str, remote_name:str='origin'):
        assert os.path.exists(new_repo_path)
        assert (('.git' in os.listdir(new_repo_path)) and os.path.isdir(os.path.join(new_repo_path, '.git'))), f"Destination folder {new_repo_path} does not have '.git/'"
        return self.run_list(['remote', 'add', remote_name, remote_url], cwd=new_repo_path)


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


def copy_repo(src_repo_path:str, dest_repo_path:str):
    assert os.path.exists(src_repo_path), f"Source folder {src_repo_path} does not exist"
    assert (('.git' in os.listdir(src_repo_path)) and os.path.isdir(os.path.join(src_repo_path, '.git'))), f"Source folder {src_repo_path} does not have '.git/'"
    assert os.path.exists(dest_repo_path), f"Destination folder {dest_repo_path} does not exist"
    assert (('.git' in os.listdir(dest_repo_path)) and os.path.isdir(os.path.join(dest_repo_path, '.git'))), f"Destination folder {dest_repo_path} does not have '.git/'"

    def ignore_git(folder):
        return '.git' in folder.split(os.sep)

    return shutil.copytree(src_repo_path, dest_repo_path, ignore=ignore_git)


if "__main__" == __name__:
    main(sys.argv)
