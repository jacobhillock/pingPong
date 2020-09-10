#!/bin/bash
# https://stackoverflow.com/questions/6393551/what-is-the-meaning-of-0-in-a-bash-script?noredirect=1&lq=1
cd "${0%/*/*}"
venv/bin/python main.py