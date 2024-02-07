git.exe rm --cached -r %1 %2 %3 %4 %5 %6 %7 %8 %9

@echo off
exit

rem INFO:
rem -r (-recursive) with subfolders
rem git.exe rm --cached -r %1 %2 %3 %4 %5 %6 %7 %8 %9 rem Remove index and file(s) from remote, stay ignored by index in local
rem git.exe rm -r %1 %2 %3 %4 %5 %6 %7 %8 %9 rem Remove index and file(s) from remote and local

rem .gitignore settings eg:
rem static/*
rem !static/<apps1>
rem !static/<apps2>
