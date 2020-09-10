REM https://stackoverflow.com/questions/17063947/get-current-batchfile-directory
cd %~dp0
cd ..
"venv\Scripts\python" "main.py"