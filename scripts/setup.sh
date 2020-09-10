#!/bin/bash
DIR='./venv'
cd "${0%/*/*}"

if [ -d "$DIR" ];
else
echo "creating venv"
python -m venv venv
fi

mkdir .private
cp -i scripts/.config.json .private/config.json

echo "Updating venv packages"
venv/bin/pip install -r requirements.txt

echo "Ready to use"