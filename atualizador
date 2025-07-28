#!/usr/bin/env python3
import os, sys, subprocess, time, shutil
import datetime

try:
    import questionary
except ImportError:
    print("Instalando dependências Python (questionary)...")
    os.system("pip3 install questionary")
    import questionary

LOG_FILE = "install_log.txt"
BACKUP_DIR = "backup-vsfood"

MODS = {
    "vs-os-interface": {
        "2.28.7": "https://cdn.vsd.app/softwares/vs-os-interface/2.28.7/vs-os-interface_2.28.7_amd64.deb",
        "2.28.4": "https://cdn.vsd.app/softwares/vs-os-interface/2.28.4/vs-os-interface_2.28.4_amd64.deb",
        "2.28.3": "https://cdn.vsd.app/softwares/vs-os-interface/2.28.3/vs-os-interface_2.28.3_amd64.deb",
        "2.28.2": "https://cdn.vsd.app/softwares/vs-os-interface/2.28.2/vs-os-interface_2.28.2_amd64.deb"
    },
    "vs-autopag-se": {
        "2.33.8": "https://cdn.vsd.app/softwares/vs-autopag-se/2.33.8/vs-autopag-se_2.33.8_amd64.deb",
        "2.33.7": "https://cdn.vsd.app/softwares/vs-autopag-se/2.33.7/vs-autopag-se_2.33.7_amd64.deb",
        "2.33.6": "https://cdn.vsd.app/softwares/vs-autopag-se/2.33.6/vs-autopag-se_2.33.6_amd64.deb",
        "2.33.5": "https://cdn.vsd.app/softwares/vs-autopag-se/2.33.5/vs-autopag-se_2.33.5_amd64.deb"
    },
    "vsd-payment": {
        "1.7.0": "https://cdn.vsd.app/softwares/vsd-payment/prod/vsd-payment_1.7.0_amd64.deb",
        "1.6.0": "https://cdn.vsd.app/softwares/vsd-payment/prod/vsd-payment_1.6.0_amd64.deb",
        "1.5.0": "https://cdn.vsd.app/softwares/vsd-payment/prod/vsd-payment_1.5.0_amd64.deb",
        "1.4.0": "https://cdn.vsd.app/softwares/vsd-payment/prod/vsd-payment_1.4.0_amd64.deb"
    },
    "pinpad-server": {
        "3.11.0": "https://github.com/getzoop/zoop-package-public/releases/download/zoop-desktop-server_3.11.0/pinpad-server-installer_linux_3.11.0.deb",
        "3.10.0-beta": "https://github.com/getzoop/zoop-package-public/releases/download/zoop-desktop-server_3.10.0-beta/pinpad-server-installer_linux_3.10.0-beta.deb",
        "3.9.0-beta": "https://github.com/getzoop/zoop-package-public/releases/download/zoop-desktop-server_3.9.0-beta/pinpad-server-installer_linux_3.9.0-beta.deb"
    }
}

def log(msg):
    print(msg)
    with open(LOG_FILE, "a") as f:
        f.write(msg + '\n')

def run(cmd, fail_ok=False):
    log(f"$ {cmd}")
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    log(result.stdout)
    if result.returncode != 0 and not fail_ok:
        log(f"Erro ao executar: {cmd}")
        sys.exit(result.returncode)
    return result

def check_root():
    if os.geteuid() != 0:
        print("Execute como root (use sudo).")
        sys.exit(1)

def backup():
    if not os.path.exists("/opt/videosoft"):
        log("Pasta /opt/videosoft não existe, backup não realizado.")
        return
    if not os.path.exists(BACKUP_DIR):
        os.mkdir(BACKUP_DIR)
    now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    dest = os.path.join(BACKUP_DIR, now)
    log(f"Realizando backup de /opt/videosoft para {dest}")
    shutil.copytree("/opt/videosoft", dest)
    log("Backup concluído.")

def sleep_count(count=5):
    for i in reversed(range(count+1)):
        print(f"Reiniciando em {i}...")
        time.sleep(1)

def limpar_token():
    log("Limpando token e recovery...")
    run("sudo rm -f /opt/videosoft/vs-os-interface/log/_database_token*", fail_ok=True)
    run("sudo rm -f /opt/videosoft/vs-os-interface/log/_database_recovery*", fail_ok=True)
    log("Tokens limpos.")

def health_check():
    log("Rodando health check...")
    services = ["vs-os-interface", "vs-autopag-se"]
    for svc in services:
        out = run(f"systemctl is-active {svc}", fail_ok=True)
        status = out.stdout.strip()
        log(f"Serviço {svc}: {status}")
        print(f"Serviço {svc}: {status}")
    log("Health check encerrado.")

def baixar_modulo(nome_modulo, versao):
    url = MODS[nome_modulo][versao]
    arquivo = url.split("/")[-1]
    log(f"Baixando {nome_modulo} versão {versao}...")
    run(f"wget --inet4-only '{url}' -O '{arquivo}'")
    return arquivo

def instalar_deb(arquivo):
    log(f"Instalando {arquivo}...")
    run(f"sudo dpkg -i {arquivo}", fail_ok=True)
    run("sudo apt-get install -f -y", fail_ok=True)

def instalar_launcher():
    log("Baixando e instalando vsd-launcher...")
    run("wget https://raw.githubusercontent.com/CarloseOldenburg/Ferramentas/refs/heads/main/VSD-Launcher -O vsd-launcher")
    run("sudo chmod 755 vsd-launcher")
    run("sudo mv vsd-launcher /usr/bin/")

def exec_launcher(params=""):
    run(f"sudo vsd-launcher {params}", fail_ok=True)

def remover_antigos():
    log("Removendo módulos e arquivos antigos...")
    run("sudo apt purge -y vsd-payment", fail_ok=True)
    run("sudo apt purge -y pinpad-server", fail_ok=True)
    run("sudo rm -rf /home/videosoft/.pinpad_server /home/terminal/.pinpad_server", fail_ok=True)
    run("sudo rm -f /home/videosoft/DesktopPlugin.db /home/terminal/DesktopPlugin.db", fail_ok=True)

def reboot():
    log("*****************Instalação Concluída*****************")
    sleep_count()
    run("sudo reboot")

def escolher_modulo():
    return questionary.select(
        "Qual módulo você quer instalar/atualizar?",
        choices=list(MODS.keys())
    ).ask()

def escolher_versao(modulo):
    return questionary.select(
        f"Escolha a versão para {modulo}:",
        choices=list(MODS[modulo].keys())
    ).ask()

def menu():
    check_root()
    while True:
        opcao = questionary.select(
            "O que deseja fazer?",
            choices=[
                "Rollout Completo (Backup + Update + HealthCheck)",
                "Atualizar Só Um Módulo",
                "Fazer Apenas Backup",
                "Limpar Token",
                "Remover Instalações Antigas",
                "Instalar/Reinstalar Launcher",
                "HealthCheck Pós-Instalação",
                "Sair"
            ]
        ).ask()
        if opcao == "Rollout Completo (Backup + Update + HealthCheck)":
            backup()
            limpeza_total()
            health_check()
        elif opcao == "Atualizar Só Um Módulo":
            atualizar_individual()
        elif opcao == "Fazer Apenas Backup":
            backup()
        elif opcao == "Limpar Token":
            limpar_token()
        elif opcao == "Remover Instalações Antigas":
            remover_antigos()
        elif opcao == "Instalar/Reinstalar Launcher":
            instalar_launcher()
        elif opcao == "HealthCheck Pós-Instalação":
            health_check()
        elif opcao == "Sair":
            break

def limpeza_total():
    log("========= Rollout Completo =========")
    limpar_token()
    instalar_launcher()
    exec_launcher("-s food")
    exec_launcher("--clear-cache")
    remover_antigos()
    arquivos = []
    for m in MODS:
        v = escolher_versao(m)
        arquivos.append(baixar_modulo(m, v))
    for arq in arquivos:
        instalar_deb(arq)
    reboot()

def atualizar_individual():
    mod = escolher_modulo()
    versao = escolher_versao(mod)
    arquivo = baixar_modulo(mod, versao)
    instalar_deb(arquivo)
    print("Atualização concluída!")

if __name__ == "__main__":
    menu()
