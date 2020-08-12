#!/bin/bash
DIR='./venv'
if [ -d "$DIR" ];
else
echo "creating venv"
python -m venv venv
fi

echo "Updating venv packages"
venv/bin/pip install -r requirements.txt

echo "Ready to play"