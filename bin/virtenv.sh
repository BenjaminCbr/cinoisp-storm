#!/bin/sh
# This script set ups virtualenv in the project 
# You must give the version you'd like to install as first argument

VERSION=$1
VENV_FILENAME="virtualenv-$VERSION"
VENV_NAME="psi_venv"

curl -O https://pypi.python.org/packages/source/v/virtualenv/$VENV_FILENAME.tar.gz
tar xvfz $VENV_FILENAME.tar.gz
cd $VENV_FILENAME
python virtualenv.py $VENV_NAME
rm ../$VENV_FILENAME.tar.gz
