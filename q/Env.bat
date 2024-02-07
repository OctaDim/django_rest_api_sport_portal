@echo off
echo.

if exist .env (
    rem echo.
    @echo QUICK COMMAND.BAT INFO: File '.env' already exists
    echo.
    ) else (
        type Null > "requirements.txt"
        goto TEXT_BLOCK
        :APPEND_BLOCK
        rem echo.
        @echo QUICK COMMAND.BAT INFO: File '.env' with typycal environment DB variables was created
        echo.
        )

@echo off
exit

:TEXT_BLOCK
@echo # ################ APPENDED FROM QUICK COMMAND.BAT ##################### >> ".env"
@echo POSTGRES=True  # Postgres flag to choose, which db working with >> ".env"
@echo DB_USER_POSTGRES=  # Define >> ".env"
@echo DB_PASSWORD_POSTGRES=  # Define >> ".env"
@echo DB_HOST_POSTGRES=localhost  # Change, if necessary >> ".env"
@echo DB_PORT_POSTGRES=5432  # Change, if necessary >> ".env"
@echo DB_NAME_POSTGRES=  # Define >> ".env"

@echo SECRET_KEY=  # Define here, except settings.py >> ".env"
@echo ALLOWED_HOST_1=127.0.0.1  # Change, if necessary >> ".env"
@echo ALLOWED_HOST_2=localhost  # Change, if necessary >> ".env"
@echo DEBUG=True  # Change, if necessary >> ".env"
@echo # ###################################################################### >> ".env"

goto APPEND_BLOCK
