@echo off

rem Change to the directory containing the script
cd %~dp0

rem Create virtual environment if it doesn't exist, else delete and recreate
if not exist env (
    python -m venv env
) else (
    rmdir /s /q env
    python -m venv env
)

rem Activate virtual environment
call env\Scripts\activate

rem Install requirements
pip install -r requirements.txt

rem Run Python script
python src/hostServer.py

rem Deactivate virtual environment
deactivate
