@echo off

rem Change to the directory containing the script
cd %~dp0

rem Create virtual environment if it doesn't exist, else delete and recreate
if not exist env-dev (
    python -m venv env-dev
) else (
    rmdir /s /q env-dev
    python -m venv env-dev
)

rem Activate virtual environment
call env-dev\Scripts\activate

rem Install requirements
pip install -r requirements-dev.txt

rem Deactivate virtual environment
deactivate
