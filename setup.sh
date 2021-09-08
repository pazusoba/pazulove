#!/bin/bash

python3 -m venv .env
chmod 755 .env/bin/activate
source .env/bin/activate
# update pip just in case
pip install --upgrade pip
# install all dependencies
pip install -r requirement.txt
