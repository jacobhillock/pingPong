cd ..
IF NOT EXIST "venv\" (
    echo "creating venv"
    python -m venv venv
)

echo "Updating venv packages"
"venv\Scripts\pip.exe" install -r requirements.txt

echo "Ready to use"