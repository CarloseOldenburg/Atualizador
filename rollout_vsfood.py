#!/usr/bin/env python3

import sys, os, subprocess, shutil, datetime, time

try:
    from rich.console import Console
    from textual.app import App, ComposeResult
    from textual.widgets import Button, Header, Footer, Static, Select, Label
except ImportError:
    print("\n[ERRO] Dependências Textual/Rich não foram encontradas (python3 -m pip install rich textual requests)")
    print("Por favor, rode o comando de instalação sugerido (bootstrap.sh) ou peça ajuda ao suporte.")
    sys.exit(1)

LOG_FILE = "install_log.txt"
BACKUP_DIR = "backup-vsfood"
console = Console()

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
    with open(LOG_FILE, "a") as f:
        f.write(msg+'\n')
    console.print(f"[bright_black][rollout][/bright_black] [green]{msg}[/green]")

def run(cmd, fail_ok=False):
    log(f"$ {cmd}")
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    log(result.stdout)
    if result.returncode != 0 and not fail_ok:
        log(f"Erro ao executar: {cmd}")
        if not fail_ok:
            raise Exception(f"Erro ao executar: {cmd}")

def check_root():
    if os.geteuid() != 0:
        console.print("[bold red]Execute como root (use sudo)![/bold red]")
        sys.exit(1)

def backup():
    if not os.path.exists("/opt/videosoft"):
        log("Pasta /opt/videosoft não existe, backup não realizado.")
        return
    if not os.path.exists(BACKUP_DIR):
        os.mkdir(BACKUP_DIR)
    now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    dest = os.path.join(BACKUP_DIR, now)
    log(f"Realizando backup: {dest}")
    shutil.copytree("/opt/videosoft", dest)
    log("Backup concluído.")

def sleep_count(count=5):
    for i in reversed(range(count+1)):
        console.print(f"[yellow]Reiniciando em {i}...[/yellow]")
        time.sleep(1)

def limpar_token():
    log("Limpando token/recovery do VSFood...")
    run("sudo rm -f /opt/videosoft/vs-os-interface/log/_database_token*", fail_ok=True)
    run("sudo rm -f /opt/videosoft/vs-os-interface/log/_database_recovery*", fail_ok=True)
    log("Tokens limpos.")

def limpar_cache():
    log("Limpando cache do Google Chrome/VSFood...")
    run("rm -rf ~/.cache/google-chrome/*", fail_ok=True)
    run("rm -rf ~/.config/google-chrome/*", fail_ok=True)
    log("Cache limpo.")

def remover_antigos():
    log("Removendo módulos e arquivos antigos com privilégios máximos...")
    run("sudo apt purge -y vsd-payment", fail_ok=True)
    run("sudo apt purge -y pinpad-server", fail_ok=True)
    run("sudo rm -rf /home/videosoft/.pinpad_server /home/terminal/.pinpad_server", fail_ok=True)
    run("sudo rm -f /home/videosoft/DesktopPlugin.db /home/terminal/DesktopPlugin.db", fail_ok=True)
    log("Remoção completa.")

def instalar_launcher():
    log("Instalando vsd-launcher (curl preferencial)...")
    try:
        run("curl -sSL -o vsd-launcher https://raw.githubusercontent.com/CarloseOldenburg/Ferramentas/refs/heads/main/VSD-Launcher")
    except Exception:
        log("Falha no curl, tentando com wget...")
        run("wget https://raw.githubusercontent.com/CarloseOldenburg/Ferramentas/refs/heads/main/VSD-Launcher -O vsd-launcher")
    run("sudo chmod 755 vsd-launcher")
    run("sudo mv vsd-launcher /usr/bin/")

def exec_launcher(params=""):
    run(f"sudo vsd-launcher {params}", fail_ok=True)

def instalar_deb(arquivo):
    log(f"Instalando {arquivo}...")
    run(f"sudo dpkg -i {arquivo}", fail_ok=True)
    run("sudo apt-get update -y", fail_ok=True)
    run("sudo apt-get install -f -y", fail_ok=True)

def baixar_modulo(nome_modulo, versao):
    url = MODS[nome_modulo][versao]
    arquivo = url.split("/")[-1]
    log(f"Baixando {nome_modulo} versão {versao}...")
    try:
        run(f"curl -sSL -o '{arquivo}' '{url}'")
    except Exception:
        log("curl falhou, tentando wget...")
        run(f"wget --inet4-only '{url}' -O '{arquivo}'")
    return arquivo

def reboot():
    log("*****************Instalação Concluída*****************")
    sleep_count()
    run("history -c", fail_ok=True)
    run("sudo reboot")

def health_check():
    log("Rodando health check...")
    services = ["vs-os-interface", "vs-autopag-se", "vsd-payment", "pinpad-server"]
    for svc in services:
        out = subprocess.run(f"systemctl is-active {svc}", shell=True, stdout=subprocess.PIPE, text=True)
        status = out.stdout.strip()
        log(f"Serviço {svc}: {status}")
    log("Health check encerrado.")

def alterar_url(tipo="food", versao="3", homolog=False):
    url_new = ""
    if tipo == "food":
        if versao == "2":
            url_new = "https://food2.homolog.vsd.app" if homolog else "https://food2.vsd.app"
        else:
            url_new = "https://food.homolog.vsd.app" if homolog else "https://food.vsd.app"
    elif tipo == "self":
        url_new = "https://selfcheckout.homolog.vsd.app" if homolog else "https://selfcheckout.vsd.app"
    path = "/opt/videosoft/vs-food-launcher/app/vs-food.sh"
    if os.path.isfile(path):
        run(f"sudo sed -i 's|^VS_URL_APP=.*|VS_URL_APP=\"{url_new}\"|' {path}")
        log(f"URL atualizada para: {url_new}")
    else:
        log(f"NÃO encontrado: {path}")

def rollout_ifood(versoes):
    backup()
    limpar_cache()
    limpar_token()
    instalar_launcher()
    exec_launcher("-s food")
    exec_launcher("--clear-cache")
    remover_antigos()
    for modulo, ver in versoes.items():
        arq = baixar_modulo(modulo, ver)
        instalar_deb(arq)
    alterar_url(tipo="food", versao="3")
    health_check()
    reboot()

def rollout_legado(versoes):
    backup()
    limpar_cache()
    limpar_token()
    instalar_launcher()
    exec_launcher("-s food")
    exec_launcher("--clear-cache")
    for modulo, ver in versoes.items():
        arq = baixar_modulo(modulo, ver)
        instalar_deb(arq)
    alterar_url(tipo="food", versao="3")
    health_check()
    reboot()

class RolloutApp(App):
    CSS_PATH = None

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("Rollout VSFood - Totem TX")  # Removi o 'style'!
        yield Static("Escolha o perfil do seu totem e as versões desejadas:", id="desc")
        yield Select(id="profile", options=[
            ("iFood", "ifood"),
            ("Cliente Legado (não-iFood)", "legado")
        ])
        yield Button("Iniciar Rollout", id="rollout", variant="success")
        yield Button("Apenas Atualização de Módulo", id="modulo", variant="primary")
        yield Button("Alterar URL/Realizar Limpeza", id="url", variant="primary")
        yield Button("Backup Manual", id="backup", variant="warning")
        yield Button("Ver Logs", id="logs", variant="primary")
        yield Button("Sair", id="sair", variant="error")
        yield Footer()

    def on_button_pressed(self, msg: Button.Pressed) -> None:
        if msg.button.id == "rollout":
            profile = self.query_one("#profile", Select).value
            versoes = {}
            if profile == "ifood":
                modlist = ["vs-os-interface", "vsd-payment", "pinpad-server"]
            else:
                modlist = ["vs-os-interface", "vs-autopag-se"]
            for m in modlist:
                versoes[m] = self.escolher_versao_textual(m)
            if profile == "ifood":
                rollout_ifood(versoes)
            else:
                rollout_legado(versoes)
        elif msg.button.id == "modulo":
            m = self.escolher_modulo_textual()
            v = self.escolher_versao_textual(m)
            arq = baixar_modulo(m, v)
            instalar_deb(arq)
            self.console.print(f"Módulo {m} ({v}) atualizado!")
        elif msg.button.id == "url":
            tipo = self.escolher_tipo_url()
            versao = self.escolher_versao_url()
            homolog = self.escolher_homolog()
            alterar_url(tipo, versao, homolog)
            limpar_cache()
            limpar_token()
            self.console.print("[green]URL atualizada e limpeza concluída!")
        elif msg.button.id == "backup":
            backup()
        elif msg.button.id == "logs":
            os.system(f"less {LOG_FILE}")
        elif msg.button.id == "sair":
            self.exit()

    def escolher_modulo_textual(self):
        opts = list(MODS.keys())
        idx = self.ask_select("Qual módulo atualizar?", opts)
        return opts[idx]

    def escolher_versao_textual(self, modulo):
        opts = list(MODS[modulo].keys())
        idx = self.ask_select(f"Versão para {modulo}:", opts)
        return opts[idx]

    def escolher_tipo_url(self):
        opts = ["food", "self"]
        idx = self.ask_select("Tipo de serviço (para URL):", opts)
        return opts[idx]

    def escolher_versao_url(self):
        opts = ["2", "3"]
        idx = self.ask_select("Qual versão do sistema?", opts)
        return opts[idx]

    def escolher_homolog(self):
        opts = ["Sim", "Não"]
        idx = self.ask_select("Ambiente de Homologação?", opts)
        return (idx == 0)

    def ask_select(self, msg, options):
        console.print(f"[cyan]{msg}")
        for i,opt in enumerate(options):
            print(f"  [{i+1}] {opt}")
        while True:
            v = input("Digite o número da opção: ")
            try:
                v = int(v)
                if 1 <= v <= len(options):
                    return v-1
            except:
                pass
            print("Opção inválida!")

if __name__ == "__main__":
    check_root()
    try:
        app = RolloutApp()
        app.run()
    except Exception as e:
        console.print(f"[red]Erro: {e}[/red]")
