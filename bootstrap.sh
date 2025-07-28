#!/bin/bash
set -e

echo "→ Limpando bibliotecas duplicadas (user+root)"
python3 -m pip uninstall -y rich textual requests || true
sudo python3 -m pip uninstall -y rich textual requests || true

sudo apt update
sudo apt install -y python3 python3-pip curl

sudo python3 -m pip install --upgrade pip
sudo python3 -m pip install --upgrade rich textual requests

echo "→ Teste de importação das libs antes de rodar o rollout"
sudo python3 -c "import rich, textual, requests; print('Sucesso ao importar rich, textual, requests!')"

cd /tmp
rm -f rollout_vsfood.py
curl -sSL https://raw.githubusercontent.com/CarloseOldenburg/rollout-vsfood/refs/heads/main/rollout_vsfood.py -o rollout_vsfood.py

echo "→ Rodando rollout_vsfood.py"
sudo python3 /tmp/rollout_vsfood.py
