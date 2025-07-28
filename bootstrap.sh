#!/bin/bash
set -e

# Limpando possíveis instalações em duplicidade
python3 -m pip uninstall -y rich textual requests || true
sudo python3 -m pip uninstall -y rich textual requests || true

sudo apt update
sudo apt install -y python3 python3-pip curl

# Instala dependências globais, evitando user/site_packages separados
sudo python3 -m pip install --upgrade pip
sudo python3 -m pip install --upgrade rich textual requests

cd /tmp
rm -f rollout_vsfood.py
curl -sSL https://raw.githubusercontent.com/CarloseOldenburg/rollout-vsfood/refs/heads/main/rollout_vsfood.py -o rollout_vsfood.py

sudo python3 /tmp/rollout_vsfood.py
