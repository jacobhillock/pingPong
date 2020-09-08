#!/bin/bash
DIR='./venv'
cd ..
if [ -d "$DIR" ];
else
echo "creating venv"
python -m venv venv
fi

cp -i scripts/.config.json config.json

echo "Updating venv packages"
venv/bin/pip install -r requirements.txt

echo "Ready to use"