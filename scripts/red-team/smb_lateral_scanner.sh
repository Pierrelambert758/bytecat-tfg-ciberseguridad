#!/bin/bash
#
# ByteCat - SMB Lateral Movement Scanner
# Autor: Noemí Fernández (2026)
#
# Escanea hosts corporativos y enumera recursos SMB accesibles
# usando las credenciales comprometidas del usuario.
#

USER="$1"
PASS="$2"

if [ -z "$USER" ] || [ -z "$PASS" ]; then
    echo "Uso: $0 usuario contraseña"
    exit 1
fi

echo "=== ByteCat SMB Scanner ==="
for HOST in $(seq 1 254); do
    IP="192.168.20.$HOST"
    echo -n "[*] Probing $IP ... "

    smbclient -L "//$IP" -U "$USER%$PASS" --option='client min protocol=NT1' -g 2>/dev/null | grep "Disk" >/dev/null

    if [ $? -eq 0 ]; then
        echo "ACCESIBLE"
        echo "[+] Recursos compartidos:"
        smbclient -L "//$IP" -U "$USER%$PASS" --option='client min protocol=NT1' -g | grep "Disk"
        echo
    else
        echo "No accesible"
    fi
done

