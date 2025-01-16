#!/bin/bash

if [[ $EUID -ne 0 ]]; then
    echo "[!] Installer must be run as root. Please use sudo."
    exit 1
fi

check_success() {
    if [ $? -ne 0 ]; then
        echo "[!] $1 failed. Exiting."
        exit 1
    fi
}

if ! pip3 show argon2-cffi > /dev/null 2>&1; then
    echo "[*] Installing argon2-cffi..."
    pip3 install argon2-cffi
    check_success "[+] argon2-cffi installation"
else
    echo "[+] argon2-cffi is already installed."
fi

if [ -f "hashipyon.py" ]; then
    cp hashipyon.py /usr/local/bin/hashipyon
    echo "[*] Cloning hashipyon.py to /usr/local/bin"
    chmod +x /usr/local/bin/hashipyon
    echo "[*] Setting executable permissions"

    echo "[+] Hashipyon has been successfully installed. Please type 'hashipyon' to confirm the installation."
else
    echo "[*] hashipyon.py not found in the current directory."
    exit 1
fi

