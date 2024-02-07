pip list --outdated  rem outdated packages
pip freeze | %{$_.split('==')[0]} | %{pip install --upgrade $_}  rem update all outdated packages
