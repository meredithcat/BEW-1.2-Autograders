#!/usr/bin/env bash

echo "Running: apt -y update"
apt -y update

echo "Running: apt-get install -y python3 python3-dev"
apt-get install -y python3 python3-dev

echo "Running: apt install -y python3-pip"
apt install -y python3-pip 

echo "Running: pip3 install subprocess32 gradescope-utils django djangorestframework"
pip3 install subprocess32 gradescope-utils django djangorestframework

echo "Done!"
