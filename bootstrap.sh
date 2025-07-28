#!/bin/bash
set -e

# Instalando deps de sistema e pip
sudo apt update
sudo apt install -y python3 python3-pip curl

# Instala libs Python
pip3 install --upgrade pip
pip3 install --upgrade rich textual requests

# Baixa e executa app (sempre atual, sempre do GH)
cd /tmp
rm -f rollout_vsfood.py
curl -sSL https://raw.githubusercontent.com/CarloseOldenburg/rollout-vsfood/refs/heads/main/rollout_vsfood.py -o rollout_vsfood.py

sudo python3 rollout_vsfood.py
