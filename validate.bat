@echo off
SETLOCAL

set PY=""
set RC=0
set RUNTIME_DIRECTORY=.validator

if "%~1" == "-i" (
    set arg=-i
)

IF DEFINED PYTHON3 (
        echo using env variable
        set PY=%PYTHON3%
     ) ELSE (
        echo Using default windows settings
        set PY=py

     )
 echo Using %PY%

echo Creating virtualenv
call %PY% -m venv %RUNTIME_DIRECTORY%
::call %PY% -m venv .validator

echo Entering virtualenv
call .validator/Scripts/activate.bat

echo Updating pip and setuptools
pip install --upgrade pip setuptools

echo Installing validator
python setup.py install

call :validate
call :clean
EXIT /B %RC%

:clean
echo Cleaning up
@RD /S /Q %RUNTIME_DIRECTORY%
EXIT /B 0

:validate
echo Validating msi file(s)

for %%f in (*.msi) do (
    call python validate_msi.py ^"%%f^" frozen.yml %arg% && (
        echo success
        set RC=0
    ) || (
        echo failure
        set RC=2
        EXIT /B 1
    )
)
EXIT /B 0