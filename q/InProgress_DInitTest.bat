@echo off

echo.
@echo *** NOTE: CURRENT DIRECTORY: %cd%


:ENTER_USER_CHOICE

set user_choice=""
@set /p user_choice="INITIATE DJANGO PROJECT, APPLICATIONS MAIN MODULE and BASE DIRECTORIES ? [y(yes)/n(no,exit)]: "

if %user_choice% == n set exit_result=true
if %user_choice% == N set exit_result=true
if %user_choice% == no set exit_result=true
if %user_choice% == No set exit_result=true
if %user_choice% == exit set exit_result=true
if %user_choice% == quit set exit_result=true
if defined exit_result exit

if %user_choice% == "" (
    echo.
    @echo *** ERROR: EMPTY VALUE: Choose again or exit
    rem echo.
    goto ENTER_USER_CHOICE
    )

if not %user_choice% == y if not %user_choice% == yes (
    echo.
    @echo *** ERROR: WRONG VALUE: Choose again or exit
    rem echo.
    goto ENTER_USER_CHOICE
    )


echo.

:ENTER_PROJECT_NAME

set Proj_Name=""
@set /p Proj_Name="CHOOSE OR ENTER NEW DJANGO PROJECT NAME [1='config' / enter custom project name / exit (to exit)]: "

if %Proj_Name% == exit set BoolResult=true
if %Proj_Name% == quit set BoolResult=true
rem if %Proj_Name% == no set BoolResult=true
if defined BoolResult exit

if %Proj_Name% == "" (
    echo.
    @echo *** ERROR: EMPTY VALUE. Choose / enter project name again or exit
    goto ENTER_PROJECT_NAME
    )

if %Proj_Name% == 1 (
    echo.
    @echo QUICK COMMAND.BAT INFO: EXECUTED COMMAND: django-admin startproject config .
    @echo on
    django-admin startproject config .
    ) else (
        echo.
        @echo QUICK COMMAND.BAT INFO: EXECUTED COMMAND: django-admin startproject %Proj_Name% .
        @echo on
        django-admin startproject %Proj_Name% .
        )


@echo off
echo.
@echo *** NOTE: CURRENT DIRECTORY: %cd%

:ENTER_APPS_MODULE_NAME

set App_Def_Dir=""
@echo CHOOSE OR ENTER NAME FOR THE MAIN DJANGO APPLICATIONS MODULE PACKAGE:
@set /p App_Def_Dir="[1='applications' / 2='apps' / enter custom module name / exit (to exit)]: "

if %App_Def_Dir% == exit set BoolResult=true
if %App_Def_Dir% == quit set BoolResult=true
rem if %App_Def_Dir% == no set BoolResult=true
if defined BoolResult exit

if %App_Def_Dir% == "" (
    echo.
    @echo *** ERROR: EMPTY VALUE. Choose / enter applications module package name again or exit
    rem echo.
    goto ENTER_APPS_MODULE_NAME
    )

if %App_Def_Dir% == 1 (
    md applications
    cd applications
    echo.
    if not exist __init__.py (
        type Null > "__init__.py"
        )
    if not exist router.py (
        type Null > "router.py"
        rem echo.
        @echo QUICK COMMAND.BAT INFO: Empty! file 'router.py' was created
        )
    cd ..
    echo.
    @echo QUICK COMMAND.BAT INFO: CREATED APPLICATIONS MODULE PACKAGE: 'applications'
    )

if %App_Def_Dir% == 2 (
    md apps
    cd apps
    echo.
    if not exist __init__.py (
        type Null > "__init__.py"
        )
    if not exist router.py (
        type Null > "router.py"
        rem echo.
        @echo QUICK COMMAND.BAT INFO: Empty! file 'router.py' was created
        )
    cd ..
    echo.
    @echo QUICK COMMAND.BAT INFO: CREATED APPLICATIONS MODULE PACKAGE: 'apps'
    )

if not %App_Def_Dir% == 1 if not %App_Def_Dir% == 2 (
    @echo %App_Def_Dir%
    md %App_Def_Dir%
    cd %App_Def_Dir%
    echo.
    if not exist __init__.py (
        type Null > "__init__.py"
        )
    if not exist router.py (
        type Null > "router.py"
        rem echo.
        @echo QUICK COMMAND.BAT INFO: Empty! file 'router.py' was created

        )
    cd ..
    echo.
    @echo QUICK COMMAND.BAT INFO: CREATED APPLICATIONS MODULE PACKAGE: '%App_Def_Dir%'
    )

echo.
if exist templates (
    echo.
    @echo QUICK COMMAND.BAT INFO: Directory 'templates' already exists
    ) else (
        md "templates"
        rem echo.
        @echo QUICK COMMAND.BAT INFO: Empty! directory 'templates' was created
    )

rem echo.
rem if exist static (
rem     echo.
rem     @echo QUICK COMMAND.BAT INFO: Directory 'static' already exists
rem     ) else (
rem         md "static/app1_rename/images"
rem         md "static/app1_rename/css"
rem         md "static/app1_rename/js"
rem
rem         md "static/app2_rename/images"
rem         md "static/app2_rename/css"
rem         md "static/app2_rename/js"
rem
rem         md "static/app3_rename/images"
rem         md "static/app3_rename/css"
rem         md "static/app3_rename/js"
rem         rem echo.
rem         @echo QUICK COMMAND.BAT INFO: Empty! directory 'static' was created
rem     )

rem echo.
rem if exist media (
rem     echo.
rem     @echo QUICK COMMAND.BAT INFO: Directory 'media' already exists
rem     ) else (
rem         md "media"
rem         rem echo.
rem         @echo QUICK COMMAND.BAT INFO: Empty! directory 'media' was created
rem     )

echo.
if exist "requirements.txt" (
    echo.
    @echo QUICK COMMAND.BAT INFO: File 'requirements.txt' already exists
    ) else (
        type Null > "requirements.txt"
        rem echo.
        @echo QUICK COMMAND.BAT INFO: Empty! file 'requirements.txt' was created
    )

echo.
if exist ".env" (
    echo.
    @echo QUICK COMMAND.BAT INFO: File '.env' already exists
    ) else (
        type Null > ".env"
        rem echo.
        @echo QUICK COMMAND.BAT INFO: Empty! file '.env' was created
    )

echo.
if exist ".gitignore" (
    echo.
    @echo QUICK COMMAND.BAT INFO: File '.gitignore' already exists
    ) else (
        type Null > ".gitignore"
        rem echo.
        @echo QUICK COMMAND.BAT INFO: Empty! file '.gitignore' was created
    )

echo.
@echo *** DJANGO PROJECT, MAIN APPLICATIONS MODULE PACKAGE and BASE DIRECTORIES WERE INITIALISED
echo.

exit
