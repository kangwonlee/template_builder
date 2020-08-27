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

    def push(self, new_repo_path:str, remote_name:str='origin'):
        assert os.path.exists(new_repo_path)
        assert (('.git' in os.listdir(new_repo_path)) and os.path.isdir(os.path.join(new_repo_path, '.git'))), f"Destination folder {new_repo_path} does not have '.git/'"
        return self.run_list(['push', remote_name], cwd=new_repo_path)


def main(argv:List[str]=sys.argv):
    parser = get_arg_parser()
    parsed = parser.parse_args(argv[1:])


def build_template(src_url:str, src_repo_folder:str, src_ref:str, dest_folder:str, dest_url:str):

    assert up.urlparse(src_url), f"unable to parse {src_url}"

    parsed_url = up.urlparse(src_url.strip('/'))
    print(parsed_url.path.split('/')[-1])

    assert not os.path.exists(src_repo_folder), f"folder already exists : {src_repo_folder}"
    assert not os.path.exists(dest_folder), f"folder already exists : {dest_folder}"

    git = Git()

    git.clone(src_url, src_repo_folder)

    assert os.path.exists(src_repo_folder), f"git clone folder does not exist : {src_repo_folder}"

    git.checkout(src_repo_folder, src_ref)

    os.makedirs(dest_folder)

    git.init(dest_folder)

    copy_repo(src_repo_folder, dest_folder)

    git.add_all(dest_folder)

    git.commit(dest_folder)


def get_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Template builder")
    parser.add_argument("-s", "--src_repo_url", type=str, help=f"URL to source development repository")
    parser.add_argument("-c", "--clone_folder", type=str, help=f"Clone the source development repository to here")
    parser.add_argument("-r", "--reference", type=str, default='master', help="Reference of source repository")
    parser.add_argument("-n", "--new_empty_folder", type=str, help="New empty folder")
    parser.add_argument("-d", "--dest_repo_url", type=str, default=None, help="URL to source development repository")
    return parser


def copy_repo(src_repo_path:str, dest_repo_path:str):
    assert os.path.exists(src_repo_path), f"Source folder {src_repo_path} does not exist"
    assert (('.git' in os.listdir(src_repo_path)) and os.path.isdir(os.path.join(src_repo_path, '.git'))), f"Source folder {src_repo_path} does not have '.git/'"
    assert os.path.exists(dest_repo_path), f"Destination folder {dest_repo_path} does not exist"
    assert (('.git' in os.listdir(dest_repo_path)) and os.path.isdir(os.path.join(dest_repo_path, '.git'))), f"Destination folder {dest_repo_path} does not have '.git/'"

    for src_root, _, src_filenames in os.walk(src_repo_path):
        if '.git' not in src_root.split(os.sep):

            rel_path = os.path.relpath(src_repo_path, src_root)

            dest_root = os.path.join(dest_repo_path, rel_path)

            os.makedirs(dest_root, exist_ok=True)

            for filename in src_filenames:
                dest_filename = os.path.join(dest_repo_path, filename)

                shutil.copy(
                    os.path.join(src_root, filename),
                    dest_filename,
                )


if "__main__" == __name__:
    main(sys.argv)
