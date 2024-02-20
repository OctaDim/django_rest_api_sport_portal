python -m venv venv
.venv\Scripts\activate

pip freeze > "requirements.txt"
pip uninstall -r "requirements.txt"
pip uninstall -r "requirements.txt" -y

pip install -r "requirements.txt"

pip install django-enumchoicefield

pip install wheel setuptools pip --upgrade
pip install setuptools pip --upgrade
pip install pip --upgrade


git checkout my_branch rem Go to the branch my_branch
git rebase master rem Rebasing all commits to the master
git checkout master rem Go to the branch master
git merge my_branch —ff rem (fast forward merge) rem To merge with my_branch WITHOUT merging commit
git merge my_branch —no-ff rem (no fast forward merge) rem To merge with my_branch WITH merging commit
git branch -d my_branch rem Deleting feat branch

pip install djangorestframework-simplejwt

pip install django-annoying

cd apps/api
python.exe ../../manage.py startapp gender
