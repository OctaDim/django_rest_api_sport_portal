@echo off

if exist .gitignore (
    echo.
    @echo "QUICK COMMAND.BAT INFO: File '.gitignore' already exists"
    exit
    ) else (
        type Null > ".gitignore"
        echo.
        @echo "QUICK COMMAND.BAT INFO: Empty! file '.gitignore' was created"
    )

@echo off
exit
