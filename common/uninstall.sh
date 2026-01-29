#!/bin/bash
set -euo pipefail

# ============================================
# SSH SOCKS Proxy - Uninstall Script
# Remove all proxy components
# ============================================

SCRIPT_VERSION="2.0.0"
LOG_FILE="/var/log/ssh-proxy.log"
SSHD_CONFIG="/etc/ssh/sshd_config"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

echo "============================================"
echo " SSH SOCKS Proxy - Uninstaller v$SCRIPT_VERSION"
echo "============================================"
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "Error: This script must be run as root"
    exit 1
fi

echo "WARNING: This will remove:"
echo "  - All proxy users and their configurations"
echo "  - Nginx stream configurations (if installed)"
echo "  - Stunnel configurations (if installed)"
echo "  - Xray/V2Ray (if installed)"
echo "  - Firewall rules added by the installer"
echo ""
echo "SSH server will remain, but proxy configurations will be removed"
echo ""

log "=== Starting uninstallation ==="

# Backup current config
cp "$SSHD_CONFIG" "$SSHD_CONFIG.backup-uninstall-$(date +%s)"

# Remove all proxy users
if [ -d /root/proxy-users ]; then
    echo ""
    echo "Removing proxy users..."
    for user_file in /root/proxy-users/*.txt; do
        if [ -f "$user_file" ]; then
            username=$(basename "$user_file" .txt)
            if id "$username" &>/dev/null; then
                echo "  Removing user: $username"
                pkill -9 -u "$username" || true
                deluser --remove-home "$username" || true
            fi
        fi
    done
    rm -rf /root/proxy-users
fi

# Remove Match User blocks from sshd_config
echo "Cleaning SSH configuration..."
sed -i '/^Match User /,/^$/d' "$SSHD_CONFIG"

# Remove our added lines
sed -i '/^AllowTcpForwarding yes$/d' "$SSHD_CONFIG"
sed -i '/^PermitTunnel no$/d' "$SSHD_CONFIG"
sed -i '/^X11Forwarding no$/d' "$SSHD_CONFIG"

# Restart SSH
systemctl restart ssh
log "SSH configuration cleaned"

# Remove Xray/V2Ray
if command -v xray &>/dev/null; then
    echo "Removing Xray..."
    systemctl stop xray || true
    systemctl disable xray || true
    bash <(curl -fsSL https://github.com/XTLS/Xray-install/raw/main/install-release.sh) remove --purge || true
    rm -rf /usr/local/etc/xray /etc/xray
    log "Xray removed"
fi

# Remove stunnel
if command -v stunnel4 &>/dev/null; then
    echo "Removing stunnel..."
    service stunnel4 stop || true
    apt purge -y stunnel4 || true
    rm -rf /etc/stunnel
    # Remove cron job
    crontab -l 2>/dev/null | grep -v stunnel4 | crontab - || true
    log "Stunnel removed"
fi

# Remove Nginx stream config (but keep Nginx installed)
if [ -f /etc/nginx/stream.d/ssh_443.conf ]; then
    echo "Removing Nginx stream configuration..."
    rm -f /etc/nginx/stream.d/ssh_443.conf
    # Remove stream block from nginx.conf
    sed -i '/^stream {/,/^}/d' /etc/nginx/nginx.conf
    nginx -t && systemctl reload nginx || true
    log "Nginx stream configuration removed"
fi

# Unmask services that were masked
echo "Unmasking services..."
for svc in nginx apache2 httpd plesk psa sw-cp-server sw-engine; do
    systemctl unmask $svc 2>/dev/null || true
done

# Note: We don't modify firewall rules automatically as they might be needed for other services
echo ""
echo "============================================"
echo " ✓ Uninstallation complete"
echo "============================================"
echo ""
echo "Notes:"
echo "  - SSH server is still running normally"
echo "  - Nginx is still installed (if it was before)"
echo "  - Apache/Plesk have been unmasked"
echo "  - Firewall rules were NOT modified (manage manually if needed)"
echo "  - Backup of SSH config: $SSHD_CONFIG.backup-uninstall-*"
echo ""
echo "To remove firewall rules manually:"
echo "  ufw status numbered"
echo "  ufw delete <number>"
echo ""

log "=== Uninstallation completed ==="
