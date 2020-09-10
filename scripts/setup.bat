cd %~dp0
cd ..
IF NOT EXIST "venv\" (
    echo "creating venv"
    py -m venv venv
)

mkdir .private
xcopy /s "scripts\.config.json" ".private\config.json" /y

echo "Updating venv packages"
"venv\Scripts\pip.exe" install -r requirements.txt

echo "Ready to use"