## Visão Geral

Este projeto é um **instalador/atualizador interativo para módulos do ecossistema VSFood/iFood**.  
Funciona via terminal, com menus fáceis e automatização de limpeza, download, atualização e reboot dos totens Linux, a partir de uma base Python.  
Você poderá:
- Escolher módulos (vs-os-interface, vsd-payment, vs-autopag, pinpad-server)
- Selecionar versões homologadas (facilmente extensível)
- Instalar tudo de uma vez (rollout) ou apenas o que quiser
- Limpar tokens/caches, reinstalar o launcher, remover arquivos antigos
- Visualizar logs de instalação
- Fazer backup automático da instalação
- Realizar health check pós-rollout

---

## Instalação (no totem/servidor)

```bash
sudo apt update && sudo apt install python3 python3-pip -y
pip3 install questionary
wget https://raw.githubusercontent.com/CarloseOldenburg/rollout-vsfood/main/rollout.py
chmod +x rollout.py
sudo ./rollout.py
```

---

## Como funciona

- Menus interativos por setas e [Enter] (navegue fácil)
- Log detalhado da execução salvo em `install_log.txt`
- Backup completo da pasta /opt/videosoft/
- Escolha da versão de cada módulo
- Instalação e fix automatic da apt/dpkg
- Reboot automatizado (com contador regressivo)

---

## Estrutura dos Módulos

Basta alterar o dicionário `MODS` no início do script para adicionar/remover versões.

```python
MODS = {
    "vs-os-interface": {
        "2.28.7": "URL",
        "2.28.4": "URL",
        ...
    },
    ...
}
```

---

## Funcionalidades:

- **Rollout Completo**: Instala todos os módulos, limpa ambiente e faz reboot.
- **Atualizar Individualmente**: Só o módulo/versão desejado.
- **Limpar Token**: Limpa todos tokens/cache relevantes.
- **Remover Instalações Antigas**: Roda purge/clean clássico.
- **Instalar/Reinstalar Launcher**: Baixa e move para /usr/bin.
- **Backup Automático**: Salva /opt/videosoft/ para rollback rápido.
- **Health Check pós-instalação**: (Em desenvolvimento – ver TODO).
- **Registro de logs**: Para rastreabilidade, revisão e troubleshooting.

---

## Opções avançadas por linha de comando (opcional/futuramente)

Você poderá rodar direto:
```bash
sudo ./rollout.py --modulo vsd-payment --versao 1.7.0
sudo ./rollout.py --backup
sudo ./rollout.py --healthcheck
```
*(Hoje, tudo via menu. CLI por linha de comando pode ser adicionado fácil caso deseje – peça que ajusto.)*

---

## Backup automático

O script faz backup da raiz /opt/videosoft/ antes de qualquer rollout.  
Os backups vão para `backup-vsfood/` e usam timestamp.

---

## Health check pós-instalação

*(Em desenvolvimento!)*  
Poderá rodar um check após o reboot para garantir que serviços essenciais estão “up”, mostrar status e relatar falhas no log.

---

## Como personalizar/adicionar novas versões?

- Abra/edite o `rollout.py`
- No começo do código, atualize o dicionário MODS adicionando/removendo chaves para módulos/versões.
- Pronto! Novo menu será criado automaticamente.

---

## Suporte / Dúvidas

Qualquer dúvida, melhoria, ou necessidade de integração especial, solicite via Issue ou entre em contato:  
📧 carlos.eoldenburg@gmail.com

