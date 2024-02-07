git.exe add %1 %2 %3 %4 %5 %6 %7 %8 %9

@echo off
exit


rem if empty flags example
rem @echo off
rem if %1.==. and if %2.==. goto WithFlag
rem if %1.==. goto WithoutFlag

rem :WithFlag
rem @echo on
rem git.exe add %1 %2
rem @echo off
rem exit

rem :WithoutFlag
rem @echo on
rem git.exe add %1
rem @echo off
rem exit
