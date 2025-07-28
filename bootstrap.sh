#!/bin/bash
set -e

sudo apt update
sudo apt install -y python3 python3-pip curl

sudo pip3 install --upgrade pip
sudo pip3 install --upgrade rich textual requests

cd /tmp
rm -f rollout_vsfood.py
curl -sSL https://raw.githubusercontent.com/CarloseOldenburg/rollout-vsfood/refs/heads/main/rollout_vsfood.py -o rollout_vsfood.py

sudo python3 rollout_vsfood.py
