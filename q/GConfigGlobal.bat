git config --global user.name "Dima Mezhevich"
git config --global user.email "octadim@gmail.com"
git config --global core.editor "C:/Windows/notepad.exe"
git config -- push.autoSetupRemote true

@echo off
exit

rem git config –global core.editor “atom –wait”
rem git config –global core.editor “emacs”
rem git config –global core.editor “mate -w”
rem git config –global core.editor “vim”

rem Config levels:
rem workingtree
rem local
rem global
rem system
rem portable

rem NOTE:
rem Since workingtree and local git scopes are more specific than global,
rem any variable set in these files will override the git config global scope.
rem So if you need a specific Git config username or email for a given repository,
rem or you want special settings for an added Git worktree, the local
rem or workingtree scopes can be used.
