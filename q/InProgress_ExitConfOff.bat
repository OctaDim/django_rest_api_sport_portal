rem REG ADD HKEY_CURRENT_USER\Environment /v confirm /t REG_DWORD /d 0 /f
rem REG ADD HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\CritSec\Process\Verifier /v BreakOnCtrlC /t REG_DWORD /d 0 /f
rem
rem @echo off
rem exit
