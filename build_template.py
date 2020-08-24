"""
# Template builder

Out of an existing development repository, 
build a template repostiory with just one commit.

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
import subprocess
import typing
import urllib.parse as up


def get_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Template builder")
    parser.add_argument("-s", "--src_repo_url", type=str, help=f"URL to source development repository")
    parser.add_argument("-r", "--reference", type=str, default='master', help="Reference of source repository")
    parser.add_argument("-n", "--new_empty_folder", type=str, help="New empty folder")
    parser.add_argument("-d", "--dest_repo_url", type=str, help="URL to source development repository")
    return parser
