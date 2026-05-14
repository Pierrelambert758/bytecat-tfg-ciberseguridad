#!/usr/bin/env python3
#
# ByteCat - Log Security Analyzer
# Autor: Noemí Fernández (2026)
#
# Este script analiza logs Nginx y SSH para detectar patrones de ataque:
#  - Intentos de SQL Injection
#  - Intentos de XSS
#  - Accesos a rutas sensibles
#  - Conexiones SSH desde IP sospechosas
#

import re
import sys

LOG_NGINX = "/var/log/nginx/bytecat_access.log"
LOG_SSH = "/var/log/auth.log"

# Patrones maliciosos
patterns = {
    "SQLi": r"(union(\s+)select|or(\s+)1=1|sleep\(|concat\(|information_schema)",
    "XSS": r"(<script>|javascript:|onerror=|onload=)",
    "Rutas sensibles": r"(/\.env|/config|/backup|/admin|/debug)",
}

SSH_SUSPICIOUS = r"Accepted .* from ((?!192\.168\.20).)*"   # Cualquier IP no corporativa

def analyze_nginx():
    print("\n[+] Analizando logs de Nginx...")
    with open(LOG_NGINX, "r") as f:
        for line in f:
            for name, pattern in patterns.items():
                if re.search(pattern, line, re.IGNORECASE):
                    print(f"[ALERTA][{name}] → {line.strip()}")

def analyze_ssh():
    print("\n[+] Analizando logs de SSH...")
    with open(LOG_SSH, "r") as f:
        for line in f:
            if re.search(SSH_SUSPICIOUS, line):
                print(f"[ALERTA][SSH sospechoso] → {line.strip()}")

if __name__ == "__main__":
    print("=== ByteCat Security Log Analyzer ===")
    analyze_nginx()
    analyze_ssh()
    print("\nAnálisis finalizado.")

