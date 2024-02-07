@echo off
if exist applications (
    @echo on
    cd applications
    python.exe ../manage.py startapp %1 %2 %3 %4 %5 %6 %7 %8 %9
    cd ..
    @echo off
)

@echo off
if exist apps (
    @echo on
    cd apps
    python.exe ../manage.py startapp %1 %2 %3 %4 %5 %6 %7 %8 %9
    cd ..
        @echo off
)
