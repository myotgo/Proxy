#!/usr/bin/env python3
"""
Proxy Management Panel - Web-based CRM for proxy user management.
Zero external dependencies - uses only Python3 standard library.
"""

import http.server
import socketserver
import ssl
import json
import os
import sys
import subprocess
import time
import hmac
import hashlib
import base64
import threading
import re
import crypt
import struct
import ctypes
import ctypes.util
from urllib.parse import urlparse, parse_qs, unquote
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# ─── Configuration ────────────────────────────────────────────────────────────

PANEL_DIR = Path("/opt/proxy-panel")
CONFIG_FILE = PANEL_DIR / "panel.conf"
DATA_DIR = PANEL_DIR / "data"
TEMPLATES_DIR = PANEL_DIR / "templates"
STATIC_DIR = PANEL_DIR / "static"
LOG_FILE = "/var/log/proxy-panel.log"

# ─── Logging ──────────────────────────────────────────────────────────────────

def log(message, level="INFO"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] [{level}] {message}"
    try:
        with open(LOG_FILE, "a") as f:
            f.write(line + "\n")
    except Exception:
        pass
    print(line)

# ─── Config Management ───────────────────────────────────────────────────────

class Config:
    def __init__(self):
        self.port = 8443
        self.layer = "unknown"
        self.secret_key = os.urandom(32).hex()
        self.session_timeout = 86400
        self.service_type = "ssh"
        self.user_management = "ssh"
        self.xray_stats_port = 10085
        self.scripts_dir = "/opt/proxy-panel/scripts"

    @classmethod
    def load(cls):
        config = cls()
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE) as f:
                    data = json.load(f)
                for key, val in data.items():
                    if hasattr(config, key):
                        setattr(config, key, val)
            except Exception as e:
                log(f"Failed to load config: {e}", "ERROR")
        return config

    def save(self):
        data = {
            "port": self.port,
            "layer": self.layer,
            "secret_key": self.secret_key,
            "session_timeout": self.session_timeout,
            "service_type": self.service_type,
            "user_management": self.user_management,
            "xray_stats_port": self.xray_stats_port,
            "scripts_dir": self.scripts_dir,
        }
        CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_FILE, "w") as f:
            json.dump(data, f, indent=2)

# ─── PAM Authentication ──────────────────────────────────────────────────────

class Authenticator:
    """Authenticate against Linux system credentials."""

    def __init__(self):
        self._pam = None
        self._load_pam()
        self.failed_attempts = defaultdict(list)  # ip -> [timestamps]
        self.lockout_until = {}  # ip -> unlock_time

    def _load_pam(self):
        """Try to load libpam via ctypes."""
        try:
            pam_path = ctypes.util.find_library("pam")
            if pam_path:
                self._pam = ctypes.CDLL(pam_path)
                log("PAM library loaded successfully")
            else:
                log("PAM library not found, using fallback auth", "WARN")
        except Exception as e:
            log(f"Failed to load PAM: {e}", "WARN")

    def is_locked_out(self, ip):
        """Check if IP is locked out."""
        if ip in self.lockout_until:
            if time.time() < self.lockout_until[ip]:
                return True
            else:
                del self.lockout_until[ip]
                self.failed_attempts.pop(ip, None)
        return False

    def record_failure(self, ip):
        """Record a failed login attempt."""
        now = time.time()
        self.failed_attempts[ip] = [
            t for t in self.failed_attempts[ip] if now - t < 600
        ]
        self.failed_attempts[ip].append(now)
        if len(self.failed_attempts[ip]) >= 5:
            self.lockout_until[ip] = now + 900  # 15 min lockout
            log(f"IP {ip} locked out after 5 failed attempts", "WARN")

    def _is_admin_user(self, username):
        """Check if user is root or in sudo/adm group."""
        if username == "root":
            return True
        try:
            result = subprocess.run(
                ["id", "-Gn", username],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                groups = result.stdout.strip().split()
                return any(g in ("sudo", "adm", "wheel", "root") for g in groups)
        except Exception:
            pass
        return False

    def authenticate(self, username, password):
        """Authenticate user against system credentials."""
        if not self._is_admin_user(username):
            return False

        # Try shadow file first (works when running as root)
        try:
            with open("/etc/shadow") as f:
                for line in f:
                    parts = line.strip().split(":")
                    if parts[0] == username and len(parts) > 1:
                        stored_hash = parts[1]
                        if stored_hash in ("!", "*", "!!", ""):
                            return False
                        computed = crypt.crypt(password, stored_hash)
                        return hmac.compare_digest(computed, stored_hash)
        except PermissionError:
            pass
        except Exception as e:
            log(f"Shadow auth error: {e}", "WARN")

        # Fallback: use su command
        try:
            proc = subprocess.run(
                ["su", "-c", "true", username],
                input=password + "\n",
                capture_output=True, text=True, timeout=10
            )
            return proc.returncode == 0
        except Exception as e:
            log(f"su auth error: {e}", "WARN")
            return False

# ─── Session Management ──────────────────────────────────────────────────────

class SessionManager:
    def __init__(self, secret_key, timeout=86400):
        self.secret = bytes.fromhex(secret_key) if isinstance(secret_key, str) else secret_key
        self.timeout = timeout

    def create_token(self, username):
        payload = json.dumps({
            "user": username,
            "exp": time.time() + self.timeout,
            "iat": time.time()
        })
        payload_b64 = base64.b64encode(payload.encode()).decode()
        sig = hmac.new(self.secret, payload.encode(), hashlib.sha256).hexdigest()
        return f"{payload_b64}.{sig}"

    def validate_token(self, token):
        try:
            parts = token.split(".")
            if len(parts) != 2:
                return None
            payload_b64, sig = parts
            payload = base64.b64decode(payload_b64).decode()
            expected_sig = hmac.new(self.secret, payload.encode(), hashlib.sha256).hexdigest()
            if not hmac.compare_digest(sig, expected_sig):
                return None
            data = json.loads(payload)
            if data.get("exp", 0) < time.time():
                return None
            return data.get("user")
        except Exception:
            return None

# ─── Layer Detection & User Management ────────────────────────────────────────

class LayerManager:
    def __init__(self, config):
        self.config = config
        self.layer = config.layer

    def detect_layer(self):
        """Auto-detect installed proxy layer."""
        checks = [
            ("layer7-v2ray-vless", self._check_xray_vless),
            ("layer7-v2ray-vmess", self._check_xray_vmess),
            ("layer7-real-domain", self._check_xray_real_domain),
            ("layer6-stunnel", self._check_stunnel),
            ("layer4-nginx", self._check_nginx_stream),
            ("layer3-basic", self._check_basic_ssh),
        ]
        for name, check_fn in checks:
            if check_fn():
                self.layer = name
                return name
        return self.layer

    def _check_xray_vless(self):
        config_path = "/usr/local/etc/xray/config.json"
        if os.path.exists(config_path):
            try:
                with open(config_path) as f:
                    cfg = json.load(f)
                for inb in cfg.get("inbounds", []):
                    if inb.get("protocol") == "vless":
                        server_cfg = "/usr/local/etc/xray/server-config.json"
                        if os.path.exists(server_cfg):
                            with open(server_cfg) as f:
                                sc = json.load(f)
                            if sc.get("domain", "") == "":
                                return True
            except Exception:
                pass
        return False

    def _check_xray_vmess(self):
        config_path = "/usr/local/etc/xray/config.json"
        if os.path.exists(config_path):
            try:
                with open(config_path) as f:
                    cfg = json.load(f)
                for inb in cfg.get("inbounds", []):
                    if inb.get("protocol") == "vmess":
                        return True
            except Exception:
                pass
        return False

    def _check_xray_real_domain(self):
        config_path = "/usr/local/etc/xray/config.json"
        server_cfg = "/usr/local/etc/xray/server-config.json"
        if os.path.exists(config_path) and os.path.exists(server_cfg):
            try:
                with open(server_cfg) as f:
                    sc = json.load(f)
                return sc.get("domain", "") != ""
            except Exception:
                pass
        return False

    def _check_stunnel(self):
        return os.path.exists("/etc/stunnel/stunnel.conf")

    def _check_nginx_stream(self):
        return os.path.exists("/etc/nginx/stream.d/ssh_443.conf")

    def _check_basic_ssh(self):
        return os.path.exists("/root/proxy-installation-info.txt")

    def is_v2ray_layer(self):
        return self.layer.startswith("layer7")

    def get_service_name(self):
        if self.is_v2ray_layer():
            return "xray"
        elif "stunnel" in self.layer:
            return "stunnel4"
        elif "nginx" in self.layer:
            return "nginx"
        return "ssh"

    def list_users(self):
        """List all proxy users."""
        if self.is_v2ray_layer():
            return self._list_v2ray_users()
        else:
            return self._list_ssh_users()

    def _list_ssh_users(self):
        users = []
        proxy_dir = Path("/root/proxy-users")
        if proxy_dir.exists():
            for f in proxy_dir.glob("*.txt"):
                username = f.stem
                user_info = {"username": username, "type": "ssh", "connected": False}
                try:
                    content = f.read_text()
                    for line in content.splitlines():
                        if "Created:" in line:
                            user_info["created"] = line.split("Created:")[-1].strip()
                except Exception:
                    pass
                # Check if connected
                try:
                    result = subprocess.run(
                        ["who"], capture_output=True, text=True, timeout=5
                    )
                    if username in result.stdout:
                        user_info["connected"] = True
                except Exception:
                    pass
                users.append(user_info)
        return users

    def _list_v2ray_users(self):
        users = []
        users_file = "/usr/local/etc/xray/users.json"
        if os.path.exists(users_file):
            try:
                with open(users_file) as f:
                    data = json.load(f)
                for username, uuid in data.items():
                    users.append({
                        "username": username,
                        "uuid": uuid,
                        "type": "v2ray",
                        "connected": False
                    })
            except Exception as e:
                log(f"Error reading users.json: {e}", "ERROR")
        return users

    def add_user(self, username, password=None):
        """Add a proxy user using existing scripts."""
        if self.is_v2ray_layer():
            return self._add_v2ray_user(username)
        else:
            if not password:
                return {"success": False, "error": "Password required for SSH users"}
            return self._add_ssh_user(username, password)

    def _add_ssh_user(self, username, password):
        script = self._find_script("add-user.sh", "common")
        if not script:
            return {"success": False, "error": "add-user.sh script not found"}
        try:
            result = subprocess.run(
                ["bash", script, username, password],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode == 0:
                log(f"User '{username}' added successfully (SSH)")
                return {"success": True, "output": result.stdout}
            else:
                return {"success": False, "error": result.stderr or result.stdout}
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Script timed out"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _add_v2ray_user(self, username):
        # Find the correct add-user.sh for this layer
        layer_dir = self.layer
        script = self._find_script("add-user.sh", layer_dir)
        if not script:
            return {"success": False, "error": "add-user.sh script not found"}
        try:
            result = subprocess.run(
                ["bash", script, username],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode == 0:
                log(f"User '{username}' added successfully (V2Ray)")
                # Read users.json to get the UUID
                users_file = "/usr/local/etc/xray/users.json"
                uuid = None
                if os.path.exists(users_file):
                    with open(users_file) as f:
                        data = json.load(f)
                    uuid = data.get(username)
                return {
                    "success": True,
                    "output": result.stdout,
                    "uuid": uuid
                }
            else:
                return {"success": False, "error": result.stderr or result.stdout}
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Script timed out"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def delete_user(self, username):
        """Delete a proxy user."""
        if self.is_v2ray_layer():
            return self._delete_v2ray_user(username)
        else:
            return self._delete_ssh_user(username)

    def _delete_ssh_user(self, username):
        script = self._find_script("delete-user.sh", "common")
        if not script:
            return {"success": False, "error": "delete-user.sh script not found"}
        try:
            result = subprocess.run(
                ["bash", script, username],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode == 0:
                log(f"User '{username}' deleted (SSH)")
                return {"success": True, "output": result.stdout}
            else:
                return {"success": False, "error": result.stderr or result.stdout}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _delete_v2ray_user(self, username):
        """Delete V2Ray user by removing from config and users.json."""
        try:
            # Remove from users.json
            users_file = "/usr/local/etc/xray/users.json"
            if os.path.exists(users_file):
                with open(users_file) as f:
                    users = json.load(f)
                uuid = users.pop(username, None)
                if uuid is None:
                    return {"success": False, "error": "User not found"}
                with open(users_file, "w") as f:
                    json.dump(users, f, indent=2)

                # Remove from config.json
                config_file = "/usr/local/etc/xray/config.json"
                if os.path.exists(config_file):
                    with open(config_file) as f:
                        cfg = json.load(f)
                    for inb in cfg.get("inbounds", []):
                        clients = inb.get("settings", {}).get("clients", [])
                        inb["settings"]["clients"] = [
                            c for c in clients if c.get("id") != uuid
                        ]
                    with open(config_file, "w") as f:
                        json.dump(cfg, f, indent=2)

                # Restart xray
                subprocess.run(
                    ["systemctl", "restart", "xray"],
                    capture_output=True, timeout=15
                )
                log(f"User '{username}' deleted (V2Ray)")
                return {"success": True}
            return {"success": False, "error": "Users file not found"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_user_config(self, username):
        """Get V2Ray user connection configuration."""
        if not self.is_v2ray_layer():
            return {"success": False, "error": "Not a V2Ray layer"}

        users_file = "/usr/local/etc/xray/users.json"
        server_cfg_file = "/usr/local/etc/xray/server-config.json"

        try:
            with open(users_file) as f:
                users = json.load(f)
            uuid = users.get(username)
            if not uuid:
                return {"success": False, "error": "User not found"}

            server_cfg = {}
            if os.path.exists(server_cfg_file):
                with open(server_cfg_file) as f:
                    server_cfg = json.load(f)

            domain = server_cfg.get("domain", "")
            ws_path = server_cfg.get("ws_path", "/")
            protocol = server_cfg.get("protocol", "vless")
            server_ip = self._get_server_ip()
            host = domain if domain else server_ip

            # Build connection URI
            if protocol == "vless":
                uri = f"vless://{uuid}@{host}:443?type=ws&security=tls&path={ws_path}"
                if domain:
                    uri += f"&sni={domain}"
                uri += f"#{username}"
            else:
                uri = f"vmess://{uuid}@{host}:443"

            # Build client configs
            ios_config = {
                "protocol": protocol,
                "uuid": uuid,
                "address": host,
                "port": 443,
                "transport": "ws",
                "ws_path": ws_path,
                "tls": True,
                "sni": domain if domain else host
            }

            return {
                "success": True,
                "uuid": uuid,
                "uri": uri,
                "config": ios_config,
                "host": host,
                "protocol": protocol
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _get_server_ip(self):
        try:
            result = subprocess.run(
                ["hostname", "-I"],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                ips = result.stdout.strip().split()
                if ips:
                    return ips[0]
        except Exception:
            pass
        try:
            result = subprocess.run(
                ["curl", "-s", "--max-time", "5", "ifconfig.me"],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except Exception:
            pass
        return "SERVER_IP"

    def _find_script(self, name, subdir):
        """Find a management script."""
        # Check scripts dir first
        scripts_dir = Path(self.config.scripts_dir)
        if (scripts_dir / name).exists():
            return str(scripts_dir / name)
        # Check repo paths
        for base in ["/opt/proxy-panel/scripts", "/root/proxy"]:
            path = Path(base) / subdir / name
            if path.exists():
                return str(path)
            path = Path(base) / name
            if path.exists():
                return str(path)
        return None

# ─── System Information ───────────────────────────────────────────────────────

class SystemInfo:
    @staticmethod
    def get_info():
        info = {
            "ip": "",
            "uptime": "",
            "os": "",
            "hostname": "",
            "cpu_usage": 0,
            "memory": {"total": 0, "used": 0, "percent": 0},
            "disk": {"total": 0, "used": 0, "percent": 0},
        }
        try:
            # IP
            result = subprocess.run(["hostname", "-I"], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                ips = result.stdout.strip().split()
                info["ip"] = ips[0] if ips else ""

            # Uptime
            with open("/proc/uptime") as f:
                uptime_sec = float(f.read().split()[0])
            days = int(uptime_sec // 86400)
            hours = int((uptime_sec % 86400) // 3600)
            mins = int((uptime_sec % 3600) // 60)
            info["uptime"] = f"{days}d {hours}h {mins}m"

            # OS
            result = subprocess.run(
                ["lsb_release", "-ds"],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                info["os"] = result.stdout.strip().strip('"')

            # Hostname
            result = subprocess.run(["hostname"], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                info["hostname"] = result.stdout.strip()

            # CPU
            with open("/proc/stat") as f:
                line = f.readline()
            parts = line.split()
            idle = int(parts[4])
            total = sum(int(p) for p in parts[1:])
            info["cpu_usage"] = round(100 * (1 - idle / total), 1) if total else 0

            # Memory
            with open("/proc/meminfo") as f:
                meminfo = f.read()
            total_match = re.search(r"MemTotal:\s+(\d+)", meminfo)
            avail_match = re.search(r"MemAvailable:\s+(\d+)", meminfo)
            if total_match and avail_match:
                total_kb = int(total_match.group(1))
                avail_kb = int(avail_match.group(1))
                used_kb = total_kb - avail_kb
                info["memory"] = {
                    "total": round(total_kb / 1048576, 1),
                    "used": round(used_kb / 1048576, 1),
                    "percent": round(100 * used_kb / total_kb, 1) if total_kb else 0
                }

            # Disk
            result = subprocess.run(
                ["df", "-B1", "/"],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                lines = result.stdout.strip().splitlines()
                if len(lines) >= 2:
                    parts = lines[1].split()
                    total_bytes = int(parts[1])
                    used_bytes = int(parts[2])
                    info["disk"] = {
                        "total": round(total_bytes / (1024**3), 1),
                        "used": round(used_bytes / (1024**3), 1),
                        "percent": round(100 * used_bytes / total_bytes, 1) if total_bytes else 0
                    }
        except Exception as e:
            log(f"Error getting system info: {e}", "ERROR")

        return info

    @staticmethod
    def get_service_status(service_name):
        """Get systemd service status."""
        try:
            result = subprocess.run(
                ["systemctl", "is-active", service_name],
                capture_output=True, text=True, timeout=5
            )
            return result.stdout.strip()
        except Exception:
            return "unknown"

    @staticmethod
    def get_all_services_status():
        services = {}
        for svc in ["ssh", "sshd", "nginx", "stunnel4", "xray"]:
            status = SystemInfo.get_service_status(svc)
            if status != "unknown" or svc in ("ssh", "xray"):
                services[svc] = status
        return services

# ─── Bandwidth Monitoring ─────────────────────────────────────────────────────

class BandwidthMonitor:
    def __init__(self, config):
        self.config = config
        self.data_file = DATA_DIR / "bandwidth.json"
        self._data = self._load_data()

    def _load_data(self):
        if self.data_file.exists():
            try:
                with open(self.data_file) as f:
                    return json.load(f)
            except Exception:
                pass
        return {"users": {}, "last_update": 0}

    def _save_data(self):
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        try:
            with open(self.data_file, "w") as f:
                json.dump(self._data, f, indent=2)
        except Exception as e:
            log(f"Error saving bandwidth data: {e}", "ERROR")

    def get_system_bandwidth(self):
        """Get system-wide bandwidth from vnstat."""
        result = {"today": {"rx": 0, "tx": 0}, "month": {"rx": 0, "tx": 0}, "total": {"rx": 0, "tx": 0}}
        try:
            # Try vnstat JSON output
            proc = subprocess.run(
                ["vnstat", "--json"],
                capture_output=True, text=True, timeout=10
            )
            if proc.returncode == 0:
                data = json.loads(proc.stdout)
                interfaces = data.get("interfaces", [])
                if interfaces:
                    iface = interfaces[0]
                    traffic = iface.get("traffic", {})

                    # Today
                    days = traffic.get("day", [])
                    if days:
                        today = days[-1]
                        result["today"]["rx"] = today.get("rx", 0)
                        result["today"]["tx"] = today.get("tx", 0)

                    # This month
                    months = traffic.get("month", [])
                    if months:
                        month = months[-1]
                        result["month"]["rx"] = month.get("rx", 0)
                        result["month"]["tx"] = month.get("tx", 0)

                    # Total
                    total = traffic.get("total", {})
                    result["total"]["rx"] = total.get("rx", 0)
                    result["total"]["tx"] = total.get("tx", 0)
        except FileNotFoundError:
            log("vnstat not installed", "WARN")
        except Exception as e:
            log(f"Error getting system bandwidth: {e}", "ERROR")

        return result

    def get_user_bandwidth(self):
        """Get per-user bandwidth."""
        if self.config.user_management == "v2ray":
            return self._get_xray_user_bandwidth()
        else:
            return self._get_ssh_user_bandwidth()

    def _get_xray_user_bandwidth(self):
        """Get V2Ray per-user bandwidth from Xray Stats API."""
        users = {}
        users_file = "/usr/local/etc/xray/users.json"
        if not os.path.exists(users_file):
            return users

        try:
            with open(users_file) as f:
                user_data = json.load(f)

            stats_port = self.config.xray_stats_port
            for username in user_data:
                email = f"{username}@proxy"
                uplink = 0
                downlink = 0

                # Query uplink
                try:
                    result = subprocess.run(
                        ["xray", "api", "statsquery",
                         f"--server=127.0.0.1:{stats_port}",
                         f"-pattern=user>>>{email}>>>traffic>>>uplink"],
                        capture_output=True, text=True, timeout=10
                    )
                    if result.returncode == 0:
                        match = re.search(r'"value":\s*"?(\d+)"?', result.stdout)
                        if match:
                            uplink = int(match.group(1))
                except Exception:
                    pass

                # Query downlink
                try:
                    result = subprocess.run(
                        ["xray", "api", "statsquery",
                         f"--server=127.0.0.1:{stats_port}",
                         f"-pattern=user>>>{email}>>>traffic>>>downlink"],
                        capture_output=True, text=True, timeout=10
                    )
                    if result.returncode == 0:
                        match = re.search(r'"value":\s*"?(\d+)"?', result.stdout)
                        if match:
                            downlink = int(match.group(1))
                except Exception:
                    pass

                # Add persistent data
                persistent = self._data.get("users", {}).get(username, {})
                users[username] = {
                    "uplink": uplink + persistent.get("uplink_acc", 0),
                    "downlink": downlink + persistent.get("downlink_acc", 0),
                    "uplink_session": uplink,
                    "downlink_session": downlink,
                }
        except Exception as e:
            log(f"Error getting xray user bandwidth: {e}", "ERROR")

        return users

    def _get_ssh_user_bandwidth(self):
        """Get SSH per-user bandwidth from iptables accounting."""
        users = {}
        proxy_dir = Path("/root/proxy-users")
        if not proxy_dir.exists():
            return users

        for f in proxy_dir.glob("*.txt"):
            username = f.stem
            uplink = 0
            downlink = 0

            try:
                # Check iptables chain
                result = subprocess.run(
                    ["iptables", "-L", f"PROXY_USER_{username}", "-v", "-n", "-x"],
                    capture_output=True, text=True, timeout=5
                )
                if result.returncode == 0:
                    for line in result.stdout.splitlines()[2:]:
                        parts = line.split()
                        if len(parts) >= 2:
                            bytes_count = int(parts[1])
                            uplink += bytes_count
            except Exception:
                pass

            persistent = self._data.get("users", {}).get(username, {})
            users[username] = {
                "uplink": uplink + persistent.get("uplink_acc", 0),
                "downlink": downlink + persistent.get("downlink_acc", 0),
            }

        return users

    def persist_stats(self):
        """Persist current stats to survive restarts."""
        if self.config.user_management == "v2ray":
            users_file = "/usr/local/etc/xray/users.json"
            if os.path.exists(users_file):
                try:
                    with open(users_file) as f:
                        user_data = json.load(f)
                    for username in user_data:
                        bw = self._get_xray_user_bandwidth().get(username, {})
                        if username not in self._data["users"]:
                            self._data["users"][username] = {}
                        self._data["users"][username]["uplink_acc"] = bw.get("uplink", 0)
                        self._data["users"][username]["downlink_acc"] = bw.get("downlink", 0)
                except Exception:
                    pass
        self._data["last_update"] = time.time()
        self._save_data()

    def get_connections(self):
        """Get active connections."""
        connections = []
        try:
            result = subprocess.run(
                ["ss", "-tnp"],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                for line in result.stdout.splitlines()[1:]:
                    parts = line.split()
                    if len(parts) >= 5:
                        state = parts[0]
                        local = parts[3]
                        remote = parts[4]
                        # Filter for proxy port connections
                        if ":443" in local or ":22" in local:
                            connections.append({
                                "state": state,
                                "local": local,
                                "remote": remote,
                                "process": parts[5] if len(parts) > 5 else ""
                            })
        except Exception as e:
            log(f"Error getting connections: {e}", "ERROR")
        return connections

# ─── Background Bandwidth Collector ───────────────────────────────────────────

class BandwidthCollector(threading.Thread):
    def __init__(self, bandwidth_monitor):
        super().__init__(daemon=True)
        self.monitor = bandwidth_monitor

    def run(self):
        while True:
            try:
                self.monitor.persist_stats()
            except Exception as e:
                log(f"Bandwidth collector error: {e}", "ERROR")
            time.sleep(300)  # Every 5 minutes

# ─── HTTP Request Handler ─────────────────────────────────────────────────────

# Global references (set in main())
_config = None
_auth = None
_sessions = None
_layer_mgr = None
_bandwidth = None

class PanelHandler(http.server.BaseHTTPRequestHandler):
    """Main HTTP request handler with routing."""

    def log_message(self, format, *args):
        """Override default logging."""
        pass

    def _get_client_ip(self):
        return self.client_address[0]

    def _send_json(self, data, status=200):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_html(self, html, status=200):
        body = html.encode()
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_file(self, filepath, content_type):
        try:
            with open(filepath, "rb") as f:
                body = f.read()
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "public, max-age=3600")
            self.end_headers()
            self.wfile.write(body)
        except FileNotFoundError:
            self.send_error(404)

    def _redirect(self, location):
        self.send_response(302)
        self.send_header("Location", location)
        self.end_headers()

    def _get_session_user(self):
        cookies = self.headers.get("Cookie", "")
        for part in cookies.split(";"):
            part = part.strip()
            if part.startswith("session="):
                token = part[len("session="):]
                return _sessions.validate_token(token)
        return None

    def _require_auth(self):
        user = self._get_session_user()
        if not user:
            return None
        return user

    def _check_csrf(self):
        return self.headers.get("X-Requested-With") == "XMLHttpRequest"

    def _read_body(self):
        length = int(self.headers.get("Content-Length", 0))
        if length > 0:
            return self.rfile.read(length)
        return b""

    # ── Routes ────────────────────────────────────────────────────────────────

    def do_GET(self):
        path = urlparse(self.path).path

        # Static files
        if path.startswith("/static/"):
            filename = path[len("/static/"):]
            # Prevent directory traversal
            if ".." in filename or filename.startswith("/"):
                self.send_error(403)
                return
            filepath = STATIC_DIR / filename
            ext = filepath.suffix.lower()
            content_types = {
                ".css": "text/css",
                ".js": "application/javascript",
                ".ico": "image/x-icon",
                ".png": "image/png",
                ".svg": "image/svg+xml",
            }
            self._send_file(str(filepath), content_types.get(ext, "application/octet-stream"))
            return

        # Pages
        if path == "/" or path == "/login":
            if self._get_session_user():
                self._redirect("/dashboard")
            else:
                self._send_file(str(TEMPLATES_DIR / "login.html"), "text/html; charset=utf-8")
            return

        if path == "/dashboard":
            if not self._get_session_user():
                self._redirect("/login")
            else:
                self._send_file(str(TEMPLATES_DIR / "dashboard.html"), "text/html; charset=utf-8")
            return

        # API endpoints
        if path.startswith("/api/"):
            self._handle_api_get(path)
            return

        self.send_error(404)

    def do_POST(self):
        path = urlparse(self.path).path

        if path == "/api/login":
            self._handle_login()
            return

        if path == "/api/logout":
            self._handle_logout()
            return

        # All other POST endpoints require auth + CSRF
        user = self._require_auth()
        if not user:
            self._send_json({"error": "Unauthorized"}, 401)
            return
        if not self._check_csrf():
            self._send_json({"error": "CSRF check failed"}, 403)
            return

        if path == "/api/users":
            self._handle_add_user()
        elif path == "/api/service/restart":
            self._handle_service_restart()
        else:
            self.send_error(404)

    def do_DELETE(self):
        path = urlparse(self.path).path
        user = self._require_auth()
        if not user:
            self._send_json({"error": "Unauthorized"}, 401)
            return
        if not self._check_csrf():
            self._send_json({"error": "CSRF check failed"}, 403)
            return

        # DELETE /api/users/<username>
        match = re.match(r"^/api/users/([a-zA-Z0-9_-]+)$", path)
        if match:
            username = match.group(1)
            self._handle_delete_user(username)
        else:
            self.send_error(404)

    # ── API GET Handlers ──────────────────────────────────────────────────────

    def _handle_api_get(self, path):
        user = self._require_auth()
        if not user:
            self._send_json({"error": "Unauthorized"}, 401)
            return

        if path == "/api/system/info":
            info = SystemInfo.get_info()
            info["layer"] = _layer_mgr.layer
            info["service"] = _layer_mgr.get_service_name()
            self._send_json(info)

        elif path == "/api/system/status":
            self._send_json(SystemInfo.get_all_services_status())

        elif path == "/api/users":
            self._send_json(_layer_mgr.list_users())

        elif path.startswith("/api/users/") and path.endswith("/config"):
            username = path[len("/api/users/"):-len("/config")]
            username = unquote(username)
            self._send_json(_layer_mgr.get_user_config(username))

        elif path == "/api/bandwidth/system":
            self._send_json(_bandwidth.get_system_bandwidth())

        elif path == "/api/bandwidth/users":
            self._send_json(_bandwidth.get_user_bandwidth())

        elif path == "/api/connections":
            self._send_json(_bandwidth.get_connections())

        elif path == "/api/service/logs":
            self._handle_service_logs()

        else:
            self.send_error(404)

    # ── API POST/DELETE Handlers ──────────────────────────────────────────────

    def _handle_login(self):
        ip = self._get_client_ip()
        if _auth.is_locked_out(ip):
            self._send_json({"error": "Too many failed attempts. Try again later."}, 429)
            return

        try:
            body = json.loads(self._read_body())
        except Exception:
            self._send_json({"error": "Invalid request"}, 400)
            return

        username = body.get("username", "").strip()
        password = body.get("password", "")

        if not username or not password:
            self._send_json({"error": "Username and password required"}, 400)
            return

        if _auth.authenticate(username, password):
            token = _sessions.create_token(username)
            log(f"Login successful: {username} from {ip}")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header(
                "Set-Cookie",
                f"session={token}; Path=/; HttpOnly; Secure; SameSite=Strict; Max-Age=86400"
            )
            body = json.dumps({"success": True, "user": username}).encode()
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            _auth.record_failure(ip)
            log(f"Login failed: {username} from {ip}", "WARN")
            self._send_json({"error": "Invalid credentials"}, 401)

    def _handle_logout(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header(
            "Set-Cookie",
            "session=; Path=/; HttpOnly; Secure; SameSite=Strict; Max-Age=0"
        )
        body = json.dumps({"success": True}).encode()
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _handle_add_user(self):
        try:
            body = json.loads(self._read_body())
        except Exception:
            self._send_json({"error": "Invalid request"}, 400)
            return

        username = body.get("username", "").strip()
        password = body.get("password", "")

        # Validate username
        if not re.match(r"^[a-zA-Z0-9_-]{3,32}$", username):
            self._send_json({
                "error": "Invalid username. Use 3-32 alphanumeric characters, dash, or underscore."
            }, 400)
            return

        # Validate password for SSH layers
        if not _layer_mgr.is_v2ray_layer():
            if len(password) < 8:
                self._send_json({"error": "Password must be at least 8 characters"}, 400)
                return

        result = _layer_mgr.add_user(username, password if password else None)
        status = 200 if result.get("success") else 400
        self._send_json(result, status)

    def _handle_delete_user(self, username):
        if not re.match(r"^[a-zA-Z0-9_-]{3,32}$", username):
            self._send_json({"error": "Invalid username"}, 400)
            return
        result = _layer_mgr.delete_user(username)
        status = 200 if result.get("success") else 400
        self._send_json(result, status)

    def _handle_service_restart(self):
        service = _layer_mgr.get_service_name()
        try:
            result = subprocess.run(
                ["systemctl", "restart", service],
                capture_output=True, text=True, timeout=15
            )
            if result.returncode == 0:
                log(f"Service '{service}' restarted via panel")
                self._send_json({"success": True, "service": service})
            else:
                self._send_json({"success": False, "error": result.stderr}, 500)
        except Exception as e:
            self._send_json({"success": False, "error": str(e)}, 500)

    def _handle_service_logs(self):
        service = _layer_mgr.get_service_name()
        try:
            result = subprocess.run(
                ["journalctl", "-u", service, "-n", "100", "--no-pager"],
                capture_output=True, text=True, timeout=10
            )
            logs = result.stdout if result.returncode == 0 else "Failed to read logs"
            self._send_json({"logs": logs, "service": service})
        except Exception as e:
            self._send_json({"logs": str(e), "service": service})

# ─── Threaded HTTPS Server ────────────────────────────────────────────────────

class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True

# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    global _config, _auth, _sessions, _layer_mgr, _bandwidth

    _config = Config.load()
    _auth = Authenticator()
    _sessions = SessionManager(_config.secret_key, _config.session_timeout)
    _layer_mgr = LayerManager(_config)
    _bandwidth = BandwidthMonitor(_config)

    # Auto-detect layer if not set
    if _config.layer == "unknown":
        detected = _layer_mgr.detect_layer()
        _config.layer = detected
        if detected.startswith("layer7"):
            _config.service_type = "xray"
            _config.user_management = "v2ray"
        else:
            _config.service_type = "ssh"
            _config.user_management = "ssh"
        _config.save()
        log(f"Auto-detected layer: {detected}")

    # Ensure data directory exists
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Start bandwidth collector
    collector = BandwidthCollector(_bandwidth)
    collector.start()

    # Create HTTPS server
    server = ThreadedHTTPServer(("0.0.0.0", _config.port), PanelHandler)

    # Set up SSL
    cert_file = PANEL_DIR / "certs" / "panel.pem"
    key_file = PANEL_DIR / "certs" / "panel.key"

    if cert_file.exists() and key_file.exists():
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ctx.minimum_version = ssl.TLSVersion.TLSv1_2
        ctx.load_cert_chain(str(cert_file), str(key_file))
        server.socket = ctx.wrap_socket(server.socket, server_side=True)
        log(f"Panel started on https://0.0.0.0:{_config.port} (HTTPS)")
    else:
        log(f"Panel started on http://0.0.0.0:{_config.port} (HTTP - no certs found)", "WARN")

    log(f"Layer: {_config.layer} | Service: {_config.service_type} | User mgmt: {_config.user_management}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        log("Panel shutting down")
        server.shutdown()

if __name__ == "__main__":
    main()
