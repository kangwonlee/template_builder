"""
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
