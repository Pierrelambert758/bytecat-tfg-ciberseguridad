#!/bin/bash
#
# ByteCat - ZIP Hash Extractor & Base64 Detector
# Autor: Noemí Fernández (2026)
#
# Automatiza:
#  1. Detección de archivos ZIP protegidos
#  2. Extracción de hash (zip2john)
#  3. Identificación de contraseñas ofuscadas en Base64
#

TARGET_DIR="$1"

if [ -z "$TARGET_DIR" ]; then
    echo "Uso: $0 ruta_directorio"
    exit 1
fi

echo "=== ByteCat ZIP Analyzer ==="

for file in $(find "$TARGET_DIR" -name "*.zip"); do
    echo "[+] ZIP protegido detectado: $file"
    zip2john "$file" > "$file.hash"
    echo "    → Hash almacenado en: $file.hash"
done

echo
echo "[+] Buscando posibles contraseñas en Base64..."

grep -R "[A-Za-z0-9+/=]\{8,\}" "$TARGET_DIR" -n | while read line; do
    TEXT=$(echo "$line" | awk -F: '{print $3}')
    python3 - << EOF
import base64
try:
    decoded = base64.b64decode("$TEXT").decode()
    print("[Base64 detectado] →", "$TEXT", "→", decoded)
except:
    pass
EOF
done

