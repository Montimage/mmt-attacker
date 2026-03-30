#!/bin/bash
# ============================================================================
# entrypoint.sh — start all target services and keep the container running
# ============================================================================

set -e

echo "[matcha-target] Starting services..."

# SSH
service ssh start
echo "[matcha-target] SSH (port 22) — ready"

# nginx HTTP
service nginx start
echo "[matcha-target] HTTP (port 80) — ready"

# vsftpd FTP
service vsftpd start
echo "[matcha-target] FTP (port 21) — ready"

echo ""
echo "============================================================"
echo " matcha-target is running"
echo "  HTTP  : http://\$(hostname -i):80"
echo "  SSH   : ssh demo@\$(hostname -i)  (password: password123)"
echo "  FTP   : ftp://\$(hostname -i):21  (anonymous)"
echo ""
echo " This container is intentionally configured as a vulnerable"
echo " target for security education demos. Use only in isolated"
echo " lab environments with explicit authorization."
echo "============================================================"
echo ""

# Keep the container alive
exec tail -f /dev/null
