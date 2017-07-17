@echo off
SETLOCAL

set PY=""

IF DEFINED PYTHON3 (
        echo using env variable
        set PY=%PYTHON3%
     ) ELSE (
        echo Using default windows settings
        set PY=py

     )
 echo Using %PY%

echo Creating virtualenv
call %PY% -m venv .validator

echo Entering virtualenv
call .validator/Scripts/activate.bat

echo Updating pip and setuptools
pip install --upgrade pip setuptools

echo Installing validator
python setup.py install

call :validate

EXIT /B %ERRORLEVEL%


:validate
echo Validating msi file(s)

for %%f in (*.msi) do (
    call python validate_msi.py ^"%%f^" frozen.yml && (
        echo success
    ) || (
        echo failure
        EXIT /B 1
    )
)
EXIT /B 0