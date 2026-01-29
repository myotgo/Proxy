#!/bin/bash
set -euo pipefail

# ============================================
# Layer 7: V2Ray VLESS + WebSocket + TLS
# Modern protocol with high stealth
# ============================================

SCRIPT_VERSION="2.0.0"
LOG_FILE="/var/log/ssh-proxy.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

preflight_check() {
    log "Running pre-flight checks..."

    if ! grep -q "Ubuntu" /etc/os-release 2>/dev/null; then
        echo "Warning: Designed for Ubuntu, continuing anyway..."
    fi

    [ "$EUID" -ne 0 ] && { echo "Error: Run as root"; exit 1; }

    AVAILABLE=$(df / | tail -1 | awk '{print $4}')
    [ "$AVAILABLE" -lt 1048576 ] && { echo "Error: Need 1GB+ disk space"; exit 1; }

    if ss -tulpn | grep -q ":443 "; then
        echo "Warning: Port 443 in use. Will be freed."
    fi

    log "Pre-flight checks passed"
}

main() {
    echo "============================================"
    echo " Layer 7: V2Ray VLESS + WebSocket + TLS"
    echo " Version: $SCRIPT_VERSION"
    echo "============================================"
    echo ""
    echo "This will:"
    echo "  • Install Xray (V2Ray core)"
    echo "  • Configure VLESS protocol"
    echo "  • Enable WebSocket transport"
    echo "  • Create TLS certificate"
    echo "  • Use port 443 (HTTPS)"
    echo ""
    echo "Highest stealth level - looks like normal HTTPS traffic"
    echo ""

    preflight_check

    log "=== Starting Layer 7 VLESS installation ==="

    # Remove conflicting services
    echo ""
    echo "Removing conflicting services..."
    systemctl stop stunnel4 2>/dev/null || true
    systemctl disable stunnel4 2>/dev/null || true
    apt purge -y stunnel4 2>/dev/null || true
    rm -rf /etc/stunnel

    for svc in nginx apache2 httpd plesk psa sw-cp-server sw-engine; do
        systemctl stop "$svc" 2>/dev/null || true
        systemctl disable "$svc" 2>/dev/null || true
        systemctl mask "$svc" 2>/dev/null || true
    done
    log "Conflicting services removed"

    # Install dependencies
    echo ""
    echo "Installing dependencies..."
    apt update -y
    apt install -y curl unzip openssl ufw jq
    log "Dependencies installed"

    # Install Xray
    echo "Installing Xray..."
    bash <(curl -fsSL https://github.com/XTLS/Xray-install/raw/main/install-release.sh) || {
        log "ERROR: Xray installation failed"
        exit 1
    }
    log "Xray installed"

    # Generate WebSocket path
    WS_PATH="/$(cat /proc/sys/kernel/random/uuid | cut -d'-' -f1)"

    # Create certificate
    echo "Creating TLS certificate..."
    mkdir -p /etc/xray/certs

    openssl req -new -x509 -nodes -days 3650 \
      -keyout /etc/xray/certs/private.key \
      -out /etc/xray/certs/cert.pem \
      -subj "/C=XX/ST=Self/L=Self/O=PrivateProxy/CN=proxy.local"

    # Fix permissions
    chmod 755 /usr /usr/local /usr/local/etc
    mkdir -p /usr/local/etc/xray
    chmod 755 /usr/local/etc/xray

    chown -R nobody:nogroup /etc/xray /usr/local/etc/xray
    chmod 644 /etc/xray/certs/cert.pem /etc/xray/certs/private.key

    log "Certificate created"

    # Create Xray config
    echo "Configuring Xray..."
    cat > /usr/local/etc/xray/config.json <<EOF
{
  "log": {
    "loglevel": "warning"
  },
  "inbounds": [
    {
      "listen": "0.0.0.0",
      "port": 443,
      "protocol": "vless",
      "settings": {
        "clients": [],
        "decryption": "none"
      },
      "streamSettings": {
        "network": "ws",
        "security": "tls",
        "tlsSettings": {
          "certificates": [
            {
              "certificateFile": "/etc/xray/certs/cert.pem",
              "keyFile": "/etc/xray/certs/private.key"
            }
          ]
        },
        "wsSettings": {
          "path": "$WS_PATH"
        }
      }
    }
  ],
  "outbounds": [
    { "protocol": "freedom" }
  ]
}
EOF

    chown nobody:nogroup /usr/local/etc/xray/config.json
    chmod 644 /usr/local/etc/xray/config.json

    # Save empty user database and server config
    mkdir -p /usr/local/etc/xray
    echo "{}" > /usr/local/etc/xray/users.json
    chmod 644 /usr/local/etc/xray/users.json

    # Save server config for add-user script
    cat > /usr/local/etc/xray/server-config.json <<EOF
{
  "ws_path": "$WS_PATH",
  "protocol": "vless",
  "tls": "self-signed"
}
EOF
    chmod 644 /usr/local/etc/xray/server-config.json

    log "Xray configured"

    # Allow Xray (running as nobody) to read certs via systemd override
    mkdir -p /etc/systemd/system/xray.service.d
    cat > /etc/systemd/system/xray.service.d/override.conf <<OVERRIDE
[Service]
ReadOnlyPaths=/etc/xray/certs
OVERRIDE

    # Start Xray
    echo "Starting Xray..."
    systemctl daemon-reexec
    systemctl daemon-reload
    systemctl enable xray
    systemctl restart xray

    sleep 3

    if ! systemctl is-active --quiet xray; then
        log "ERROR: Xray failed to start"
        echo "Error: Xray failed"
        journalctl -xe -u xray --no-pager | tail -30
        exit 1
    fi

    log "Xray started successfully"

    # Firewall
    echo "Configuring firewall..."
    ufw allow 443/tcp
    ufw --force enable
    log "Firewall configured"

    # Save installation info
    SERVER_IP=$(curl -s --max-time 5 ifconfig.me 2>/dev/null || echo "Unknown")
    cat > /root/proxy-installation-info.txt <<EOF
Installation Details
====================
Date: $(date)
Layer: 7 (V2Ray VLESS)
Port: 443
Protocol: VLESS + WebSocket + TLS
Script Version: $SCRIPT_VERSION

Server IP: $SERVER_IP
WebSocket Path: $WS_PATH

Config Location: /usr/local/etc/xray/config.json
Users Database: /usr/local/etc/xray/users.json
Server Config: /usr/local/etc/xray/server-config.json
EOF

    touch "$LOG_FILE"

    log "=== Layer 7 VLESS installation completed ==="

    # Install management panel
    log "Installing management panel..."
    PANEL_SCRIPT_URL="https://raw.githubusercontent.com/myotgo/Proxy/main/panel/install-panel.sh"
    curl -fsSL "$PANEL_SCRIPT_URL" -o /tmp/install-panel.sh && bash /tmp/install-panel.sh --layer=layer7-v2ray-vless || log "WARN: Panel installation failed (non-critical)"
    rm -f /tmp/install-panel.sh

    # Final output
    echo ""
    echo "============================================"
    echo " Installation Complete!"
    echo "============================================"
    echo ""
    echo "V2Ray VLESS proxy is now active on port 443"
    echo ""
    echo "Server IP: $SERVER_IP"
    echo "Port: 443"
    echo "Protocol: VLESS + WebSocket + TLS"
    echo ""
    echo "Next step: Add a user to get connection config"
    echo ""
    echo "Management Panel:"
    echo "  URL: https://${SERVER_IP}:8443"
    echo "  Login with your server root credentials"
    echo ""
    echo "CLI Management commands:"
    echo "-------------------"
    echo "  Add user:    curl -fsSL https://raw.githubusercontent.com/myotgo/Proxy/main/layer7-v2ray-vless/add-user.sh -o add-user.sh && bash add-user.sh"
    echo "  Delete user: curl -fsSL https://raw.githubusercontent.com/myotgo/Proxy/main/layer7-v2ray-vless/delete-user.sh -o delete-user.sh && bash delete-user.sh <username>"
    echo "  Status:      systemctl status xray"
    echo ""
    echo "============================================"
}

trap 'log "ERROR: Installation failed at line $LINENO"; exit 1' ERR
main "$@"
