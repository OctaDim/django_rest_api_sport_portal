@echo off
if exist requirements.txt (
    echo.
    @echo "QUICK COMMAND.BAT INFO: File 'requirements.txt' already exists"
    exit
    ) else (
        type Null > "requirements.txt"
        echo.
        @echo "QUICK COMMAND.BAT INFO: Empty! file 'requirements.txt' was created"
    )

@echo off
exit
