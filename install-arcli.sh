#!/bin/bash
set -e

check_internet() {
    if ! ping -c 1 -W 3 8.8.8.8 >/dev/null 2>&1; then
        echo -e "\033[1;31mNetwork connection unavailable\033[0m"
        exit 1
    fi
}

check_installed() {
    if [ -f "/usr/local/bin/arcli" ] && [ -d "/usr/share/arcli" ] && [ -f "/usr/share/arcli/font1.txt" ]; then
        return 0
    else
        return 1
    fi
}

install_arcli() {
    if check_installed; then
        echo -e "\033[1;33mARCLI already installed\033[0m"
        exit 0
    fi

    check_internet

    echo -e "\033[1;33mEstablishing connection to repository...\033[0m"

    rm -rf /tmp/arcli-install
    if ! git clone https://github.com/voratsa/arcli /tmp/arcli-install 2>/dev/null; then
        echo -e "\033[1;31mRepository access failed\033[0m"
        exit 1
    fi

    cd /tmp/arcli-install

    if [ ! -f "arcli.py" ] || [ ! -f "font1.txt" ]; then
        echo -e "\033[1;31mRequired files missing\033[0m"
        exit 1
    fi

    echo -e "\033[1;33mInitiating system integration...\033[0m"

    echo -e "\033[1;32m[1/3] Installing core executable...\033[0m"
    head -1 arcli.py | grep -q "python3" || sed -i '1i#!/usr/bin/env python3' arcli.py
    sudo install -Dm755 arcli.py /usr/local/bin/arcli

    echo -e "\033[1;32m[2/3] Creating font directory...\033[0m"
    sudo mkdir -p /usr/share/arcli

    echo -e "\033[1;32m[3/3] Deploying font assets...\033[0m"
    sudo install -Dm644 font*.txt /usr/share/arcli/

    rm -rf /tmp/arcli-install

    if check_installed; then
        echo -e "\033[1;36m[ INSTALLATION COMPLETE ]\033[0m"
        echo -e "\033[1;32mStatus: Operational\033[0m"
    else
        echo -e "\033[1;31mInstallation verification failed\033[0m"
        exit 1
    fi
}

uninstall_arcli() {
    if [ ! -f "/usr/local/bin/arcli" ] && [ ! -d "/usr/share/arcli" ]; then
        echo -e "\033[1;33mARCLI not installed\033[0m"
        exit 0
    fi

    echo -e "\033[1;33mInitiating removal sequence...\033[0m"

    echo -e "\033[1;32m[1/3] Removing core executable...\033[0m"
    sudo rm -f /usr/local/bin/arcli

    echo -e "\033[1;32m[2/3] Removing font assets...\033[0m"
    sudo rm -rf /usr/share/arcli

    echo -e "\033[1;32m[3/3] Clearing system registry...\033[0m"
    sleep 0.5

    echo -e "\033[1;36m[ UNINSTALLATION COMPLETE ]\033[0m"
    echo -e "\033[1;32mStatus: Removed\033[0m"
}

case "${1:-install}" in
    install)
        install_arcli
        ;;
    uninstall|remove|rm)
        uninstall_arcli
        ;;
    *)
        echo "Usage: $0 {install|uninstall|remove|rm}"
        exit 1
        ;;
esac
