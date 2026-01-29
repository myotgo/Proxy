/* ─── Internationalization ───────────────────────────────────────────────── */

const translations = {
    en: {
        // Nav
        nav_overview: "Overview",
        nav_users: "Users",
        nav_bandwidth: "Bandwidth",
        nav_connections: "Connections",
        nav_service: "Service",
        logout: "Logout",

        // Overview
        overview_title: "System Overview",
        server_ip: "Server IP",
        uptime: "Uptime",
        layer: "Layer",
        os_label: "OS",
        cpu_usage: "CPU Usage",
        memory_usage: "Memory",
        disk_usage: "Disk",
        service_status: "Service Status",

        // Users
        users_title: "User Management",
        add_user: "Add User",
        total_users: "Total users",
        th_username: "Username",
        th_type: "Type",
        th_status: "Status",
        th_created: "Created",
        th_actions: "Actions",
        no_users: "No users found. Add your first user.",
        connected: "Connected",
        offline: "Offline",
        config: "Config",
        delete: "Delete",
        add_new_user: "Add New User",
        username: "Username",
        password: "Password",
        username_hint: "Alphanumeric, dash, underscore. 3-32 characters.",
        password_hint: "Minimum 8 characters.",
        cancel: "Cancel",
        adding_user: "Adding...",
        user_added: "User added successfully",
        user_deleted: "User deleted successfully",

        // Delete
        confirm_delete: "Confirm Delete",
        delete_confirm_text: "Are you sure you want to delete user",
        deleting: "Deleting...",

        // Config
        connection_config: "Connection Config",
        quick_connect: "Quick Connect URI",
        client_config: "Client Configuration",
        copy: "Copy",
        copy_config: "Copy Config",
        copied: "Copied!",
        close: "Close",

        // Bandwidth
        bandwidth_title: "Bandwidth Usage",
        system_bandwidth: "System Bandwidth",
        today: "Today",
        this_month: "This Month",
        all_time: "All Time",
        per_user_bandwidth: "Per-User Bandwidth",
        upload: "Upload",
        download: "Download",
        total_label: "Total",

        // Connections
        connections_title: "Active Connections",
        refresh: "Refresh",
        th_remote: "Remote Address",
        th_local: "Local Port",
        th_state: "State",
        th_process: "Process",
        active_connections: "Active connections",

        // Service
        service_title: "Service Control",
        restart_service: "Restart Service",
        restarting: "Restarting...",
        service_restarted: "Service restarted successfully",
        service_logs: "Service Logs",
        load_logs: "Load Logs",
        click_load_logs: "Click \"Load Logs\" to view service logs...",
    },
    fa: {
        nav_overview: "\u0646\u0645\u0627\u06cc \u06a9\u0644\u06cc",
        nav_users: "\u06a9\u0627\u0631\u0628\u0631\u0627\u0646",
        nav_bandwidth: "\u067e\u0647\u0646\u0627\u06cc \u0628\u0627\u0646\u062f",
        nav_connections: "\u0627\u062a\u0635\u0627\u0644\u0627\u062a",
        nav_service: "\u0633\u0631\u0648\u06cc\u0633",
        logout: "\u062e\u0631\u0648\u062c",

        overview_title: "\u0646\u0645\u0627\u06cc \u06a9\u0644\u06cc \u0633\u06cc\u0633\u062a\u0645",
        server_ip: "\u0622\u06cc\u067e\u06cc \u0633\u0631\u0648\u0631",
        uptime: "\u0632\u0645\u0627\u0646 \u0641\u0639\u0627\u0644\u06cc\u062a",
        layer: "\u0644\u0627\u06cc\u0647",
        os_label: "\u0633\u06cc\u0633\u062a\u0645 \u0639\u0627\u0645\u0644",
        cpu_usage: "\u0645\u0635\u0631\u0641 CPU",
        memory_usage: "\u062d\u0627\u0641\u0638\u0647",
        disk_usage: "\u062f\u06cc\u0633\u06a9",
        service_status: "\u0648\u0636\u0639\u06cc\u062a \u0633\u0631\u0648\u06cc\u0633\u200c\u0647\u0627",

        users_title: "\u0645\u062f\u06cc\u0631\u06cc\u062a \u06a9\u0627\u0631\u0628\u0631\u0627\u0646",
        add_user: "\u0627\u0641\u0632\u0648\u062f\u0646 \u06a9\u0627\u0631\u0628\u0631",
        total_users: "\u062a\u0639\u062f\u0627\u062f \u06a9\u0627\u0631\u0628\u0631\u0627\u0646",
        th_username: "\u0646\u0627\u0645 \u06a9\u0627\u0631\u0628\u0631\u06cc",
        th_type: "\u0646\u0648\u0639",
        th_status: "\u0648\u0636\u0639\u06cc\u062a",
        th_created: "\u062a\u0627\u0631\u06cc\u062e \u0633\u0627\u062e\u062a",
        th_actions: "\u0639\u0645\u0644\u06cc\u0627\u062a",
        no_users: "\u06a9\u0627\u0631\u0628\u0631\u06cc \u06cc\u0627\u0641\u062a \u0646\u0634\u062f. \u0627\u0648\u0644\u06cc\u0646 \u06a9\u0627\u0631\u0628\u0631 \u0631\u0627 \u0627\u0636\u0627\u0641\u0647 \u06a9\u0646\u06cc\u062f.",
        connected: "\u0645\u062a\u0635\u0644",
        offline: "\u0622\u0641\u0644\u0627\u06cc\u0646",
        config: "\u067e\u06cc\u06a9\u0631\u0628\u0646\u062f\u06cc",
        delete: "\u062d\u0630\u0641",
        add_new_user: "\u0627\u0641\u0632\u0648\u062f\u0646 \u06a9\u0627\u0631\u0628\u0631 \u062c\u062f\u06cc\u062f",
        username: "\u0646\u0627\u0645 \u06a9\u0627\u0631\u0628\u0631\u06cc",
        password: "\u0631\u0645\u0632 \u0639\u0628\u0648\u0631",
        username_hint: "\u062d\u0631\u0648\u0641 \u0627\u0646\u06af\u0644\u06cc\u0633\u06cc\u060c \u0639\u062f\u062f\u060c \u062e\u0637 \u062a\u06cc\u0631\u0647\u060c \u0632\u06cc\u0631\u062e\u0637. \u06f3 \u062a\u0627 \u06f3\u06f2 \u06a9\u0627\u0631\u0627\u06a9\u062a\u0631.",
        password_hint: "\u062d\u062f\u0627\u0642\u0644 \u06f8 \u06a9\u0627\u0631\u0627\u06a9\u062a\u0631.",
        cancel: "\u0627\u0646\u0635\u0631\u0627\u0641",
        adding_user: "\u062f\u0631 \u062d\u0627\u0644 \u0627\u0641\u0632\u0648\u062f\u0646...",
        user_added: "\u06a9\u0627\u0631\u0628\u0631 \u0628\u0627 \u0645\u0648\u0641\u0642\u06cc\u062a \u0627\u0636\u0627\u0641\u0647 \u0634\u062f",
        user_deleted: "\u06a9\u0627\u0631\u0628\u0631 \u0628\u0627 \u0645\u0648\u0641\u0642\u06cc\u062a \u062d\u0630\u0641 \u0634\u062f",

        confirm_delete: "\u062a\u0627\u06cc\u06cc\u062f \u062d\u0630\u0641",
        delete_confirm_text: "\u0622\u06cc\u0627 \u0627\u0632 \u062d\u0630\u0641 \u06a9\u0627\u0631\u0628\u0631 \u0627\u0637\u0645\u06cc\u0646\u0627\u0646 \u062f\u0627\u0631\u06cc\u062f\u061f",
        deleting: "\u062f\u0631 \u062d\u0627\u0644 \u062d\u0630\u0641...",

        connection_config: "\u067e\u06cc\u06a9\u0631\u0628\u0646\u062f\u06cc \u0627\u062a\u0635\u0627\u0644",
        quick_connect: "\u0644\u06cc\u0646\u06a9 \u0627\u062a\u0635\u0627\u0644 \u0633\u0631\u06cc\u0639",
        client_config: "\u062a\u0646\u0638\u06cc\u0645\u0627\u062a \u06a9\u0644\u0627\u06cc\u0646\u062a",
        copy: "\u06a9\u067e\u06cc",
        copy_config: "\u06a9\u067e\u06cc \u062a\u0646\u0638\u06cc\u0645\u0627\u062a",
        copied: "\u06a9\u067e\u06cc \u0634\u062f!",
        close: "\u0628\u0633\u062a\u0646",

        bandwidth_title: "\u0645\u0635\u0631\u0641 \u067e\u0647\u0646\u0627\u06cc \u0628\u0627\u0646\u062f",
        system_bandwidth: "\u067e\u0647\u0646\u0627\u06cc \u0628\u0627\u0646\u062f \u0633\u06cc\u0633\u062a\u0645",
        today: "\u0627\u0645\u0631\u0648\u0632",
        this_month: "\u0627\u06cc\u0646 \u0645\u0627\u0647",
        all_time: "\u06a9\u0644",
        per_user_bandwidth: "\u067e\u0647\u0646\u0627\u06cc \u0628\u0627\u0646\u062f \u0647\u0631 \u06a9\u0627\u0631\u0628\u0631",
        upload: "\u0622\u067e\u0644\u0648\u062f",
        download: "\u062f\u0627\u0646\u0644\u0648\u062f",
        total_label: "\u06a9\u0644",

        connections_title: "\u0627\u062a\u0635\u0627\u0644\u0627\u062a \u0641\u0639\u0627\u0644",
        refresh: "\u0628\u0631\u0648\u0632\u0631\u0633\u0627\u0646\u06cc",
        th_remote: "\u0622\u062f\u0631\u0633 \u0631\u0627\u0647 \u062f\u0648\u0631",
        th_local: "\u067e\u0648\u0631\u062a \u0645\u062d\u0644\u06cc",
        th_state: "\u0648\u0636\u0639\u06cc\u062a",
        th_process: "\u0641\u0631\u0622\u06cc\u0646\u062f",
        active_connections: "\u0627\u062a\u0635\u0627\u0644\u0627\u062a \u0641\u0639\u0627\u0644",

        service_title: "\u06a9\u0646\u062a\u0631\u0644 \u0633\u0631\u0648\u06cc\u0633",
        restart_service: "\u0631\u0627\u0647\u200c\u0627\u0646\u062f\u0627\u0632\u06cc \u0645\u062c\u062f\u062f",
        restarting: "\u062f\u0631 \u062d\u0627\u0644 \u0631\u0627\u0647\u200c\u0627\u0646\u062f\u0627\u0632\u06cc...",
        service_restarted: "\u0633\u0631\u0648\u06cc\u0633 \u0628\u0627 \u0645\u0648\u0641\u0642\u06cc\u062a \u0631\u0627\u0647\u200c\u0627\u0646\u062f\u0627\u0632\u06cc \u0634\u062f",
        service_logs: "\u0644\u0627\u06af\u200c\u0647\u0627\u06cc \u0633\u0631\u0648\u06cc\u0633",
        load_logs: "\u0628\u0627\u0631\u06af\u0630\u0627\u0631\u06cc \u0644\u0627\u06af",
        click_load_logs: "\u0628\u0631\u0627\u06cc \u0645\u0634\u0627\u0647\u062f\u0647 \u0644\u0627\u06af\u200c\u0647\u0627 \u0631\u0648\u06cc \"\u0628\u0627\u0631\u06af\u0630\u0627\u0631\u06cc \u0644\u0627\u06af\" \u06a9\u0644\u06cc\u06a9 \u06a9\u0646\u06cc\u062f...",
    }
};

let currentLang = localStorage.getItem("lang") || "en";
let currentLayerIsV2Ray = false;
let pendingDeleteUser = null;

/* ─── Language ──────────────────────────────────────────────────────────── */

function t(key) {
    return (translations[currentLang] && translations[currentLang][key]) || key;
}

function applyLang(lang) {
    currentLang = lang;
    localStorage.setItem("lang", lang);
    document.documentElement.lang = lang;
    document.documentElement.dir = lang === "fa" ? "rtl" : "ltr";

    const langToggle = document.getElementById("langToggle");
    if (langToggle) langToggle.textContent = lang === "en" ? "\u0641\u0627\u0631\u0633\u06cc" : "English";

    document.querySelectorAll("[data-i18n]").forEach(el => {
        const key = el.getAttribute("data-i18n");
        if (translations[lang] && translations[lang][key]) {
            el.textContent = translations[lang][key];
        }
    });
}

function toggleLang() {
    applyLang(currentLang === "en" ? "fa" : "en");
}

/* ─── Navigation ────────────────────────────────────────────────────────── */

function showSection(name, navEl) {
    // Hide all sections
    document.querySelectorAll(".section").forEach(s => s.classList.remove("active"));
    document.querySelectorAll(".nav-item[data-section]").forEach(n => n.classList.remove("active"));

    // Show selected
    const section = document.getElementById("section-" + name);
    if (section) section.classList.add("active");
    if (navEl) navEl.classList.add("active");

    // Close mobile sidebar
    document.getElementById("sidebar").classList.remove("open");

    // Load data for section
    if (name === "overview") loadOverview();
    else if (name === "users") loadUsers();
    else if (name === "bandwidth") loadBandwidth();
    else if (name === "connections") loadConnections();
}

/* ─── API Helper ────────────────────────────────────────────────────────── */

async function api(path, options = {}) {
    const defaults = {
        headers: {
            "Content-Type": "application/json",
            "X-Requested-With": "XMLHttpRequest"
        }
    };
    const resp = await fetch(path, { ...defaults, ...options });
    if (resp.status === 401) {
        window.location.href = "/login";
        return null;
    }
    return resp;
}

/* ─── Overview ──────────────────────────────────────────────────────────── */

async function loadOverview() {
    try {
        const [infoResp, statusResp] = await Promise.all([
            api("/api/system/info"),
            api("/api/system/status")
        ]);

        if (infoResp) {
            const info = await infoResp.json();
            document.getElementById("stat-ip").textContent = info.ip || "-";
            document.getElementById("stat-uptime").textContent = info.uptime || "-";
            document.getElementById("stat-layer").textContent = info.layer || "-";
            document.getElementById("stat-os").textContent = info.os || "-";

            // CPU
            const cpuPct = info.cpu_usage || 0;
            document.getElementById("stat-cpu").textContent = cpuPct + "%";
            const cpuBar = document.getElementById("cpu-bar");
            cpuBar.style.width = cpuPct + "%";
            cpuBar.className = "progress-fill" + (cpuPct > 80 ? " danger" : cpuPct > 60 ? " warn" : "");

            // Memory
            const mem = info.memory || {};
            const memPct = mem.percent || 0;
            document.getElementById("stat-mem").textContent = `${mem.used || 0} / ${mem.total || 0} GB (${memPct}%)`;
            const memBar = document.getElementById("mem-bar");
            memBar.style.width = memPct + "%";
            memBar.className = "progress-fill" + (memPct > 80 ? " danger" : memPct > 60 ? " warn" : "");

            // Disk
            const disk = info.disk || {};
            const diskPct = disk.percent || 0;
            document.getElementById("stat-disk").textContent = `${disk.used || 0} / ${disk.total || 0} GB (${diskPct}%)`;
            const diskBar = document.getElementById("disk-bar");
            diskBar.style.width = diskPct + "%";
            diskBar.className = "progress-fill" + (diskPct > 80 ? " danger" : diskPct > 60 ? " warn" : "");

            // Track layer type
            currentLayerIsV2Ray = (info.layer || "").startsWith("layer7");
        }

        if (statusResp) {
            const status = await statusResp.json();
            const container = document.getElementById("service-status-list");
            container.innerHTML = "";
            for (const [svc, st] of Object.entries(status)) {
                const dotClass = st === "active" ? "active" : st === "inactive" ? "inactive" : "unknown";
                container.innerHTML += `
                    <div class="service-badge">
                        <span class="service-dot ${dotClass}"></span>
                        <span>${svc}: ${st}</span>
                    </div>
                `;
            }
        }
    } catch (err) {
        console.error("Failed to load overview:", err);
    }
}

/* ─── Users ─────────────────────────────────────────────────────────────── */

async function loadUsers() {
    try {
        const resp = await api("/api/users");
        if (!resp) return;
        const users = await resp.json();
        const tbody = document.getElementById("users-tbody");
        const noUsers = document.getElementById("no-users");
        const countEl = document.getElementById("user-count");

        countEl.textContent = users.length;

        if (users.length === 0) {
            tbody.innerHTML = "";
            noUsers.style.display = "block";
            document.querySelector(".table-container")?.style && (document.querySelector("#section-users .table-container").style.display = "none");
            return;
        }

        noUsers.style.display = "none";
        const tableContainer = document.querySelector("#section-users .table-container");
        if (tableContainer) tableContainer.style.display = "";

        tbody.innerHTML = users.map(u => {
            const statusClass = u.connected ? "connected" : "offline";
            const statusText = u.connected ? t("connected") : t("offline");
            const configBtn = u.type === "v2ray"
                ? `<button class="btn btn-sm btn-secondary" onclick="showConfig('${u.username}')">${t("config")}</button>`
                : "";

            return `<tr>
                <td><strong>${escapeHtml(u.username)}</strong></td>
                <td>${u.type || "ssh"}</td>
                <td><span class="status-badge ${statusClass}">${statusText}</span></td>
                <td>${u.created || "-"}</td>
                <td>
                    <div class="user-actions">
                        ${configBtn}
                        <button class="btn btn-sm btn-danger" onclick="showDeleteModal('${escapeHtml(u.username)}')">${t("delete")}</button>
                    </div>
                </td>
            </tr>`;
        }).join("");
    } catch (err) {
        console.error("Failed to load users:", err);
    }
}

function showAddUserModal() {
    document.getElementById("addUserModal").style.display = "flex";
    document.getElementById("addUserError").style.display = "none";
    document.getElementById("addUserForm").reset();

    // Show/hide password field based on layer type
    const pwGroup = document.getElementById("passwordGroup");
    if (currentLayerIsV2Ray) {
        pwGroup.style.display = "none";
        document.getElementById("newPassword").required = false;
    } else {
        pwGroup.style.display = "block";
        document.getElementById("newPassword").required = true;
    }

    document.getElementById("newUsername").focus();
}

async function handleAddUser(e) {
    e.preventDefault();
    const btn = document.getElementById("addUserBtn");
    const errorDiv = document.getElementById("addUserError");
    const username = document.getElementById("newUsername").value.trim();
    const password = document.getElementById("newPassword").value;

    btn.disabled = true;
    btn.querySelector("span").textContent = t("adding_user");
    errorDiv.style.display = "none";

    try {
        const body = { username };
        if (!currentLayerIsV2Ray && password) {
            body.password = password;
        }

        const resp = await api("/api/users", {
            method: "POST",
            body: JSON.stringify(body)
        });

        const data = await resp.json();
        if (data.success) {
            closeModal("addUserModal");
            showToast(t("user_added"), "success");
            loadUsers();
        } else {
            errorDiv.textContent = data.error || "Failed to add user";
            errorDiv.style.display = "block";
        }
    } catch (err) {
        errorDiv.textContent = "Network error";
        errorDiv.style.display = "block";
    } finally {
        btn.disabled = false;
        btn.querySelector("span").textContent = t("add_user");
    }
}

function showDeleteModal(username) {
    pendingDeleteUser = username;
    document.getElementById("deleteUsername").textContent = username;
    document.getElementById("deleteError").style.display = "none";
    document.getElementById("deleteModal").style.display = "flex";
}

async function confirmDelete() {
    if (!pendingDeleteUser) return;
    const btn = document.getElementById("deleteBtn");
    const errorDiv = document.getElementById("deleteError");

    btn.disabled = true;
    btn.querySelector("span").textContent = t("deleting");

    try {
        const resp = await api(`/api/users/${encodeURIComponent(pendingDeleteUser)}`, {
            method: "DELETE"
        });

        const data = await resp.json();
        if (data.success) {
            closeModal("deleteModal");
            showToast(t("user_deleted"), "success");
            loadUsers();
        } else {
            errorDiv.textContent = data.error || "Failed to delete user";
            errorDiv.style.display = "block";
        }
    } catch (err) {
        errorDiv.textContent = "Network error";
        errorDiv.style.display = "block";
    } finally {
        btn.disabled = false;
        btn.querySelector("span").textContent = t("delete");
        pendingDeleteUser = null;
    }
}

async function showConfig(username) {
    try {
        const resp = await api(`/api/users/${encodeURIComponent(username)}/config`);
        if (!resp) return;
        const data = await resp.json();

        if (data.success) {
            document.getElementById("configUri").textContent = data.uri || "";
            document.getElementById("configJson").textContent = JSON.stringify(data.config, null, 2);
            document.getElementById("configModal").style.display = "flex";
        } else {
            showToast(data.error || "Failed to get config", "error");
        }
    } catch (err) {
        showToast("Network error", "error");
    }
}

/* ─── Bandwidth ─────────────────────────────────────────────────────────── */

function formatBytes(bytes) {
    if (!bytes || bytes === 0) return "0 B";
    const units = ["B", "KB", "MB", "GB", "TB"];
    let i = 0;
    let val = bytes;
    while (val >= 1024 && i < units.length - 1) {
        val /= 1024;
        i++;
    }
    return val.toFixed(1) + " " + units[i];
}

async function loadBandwidth() {
    try {
        const [sysResp, userResp] = await Promise.all([
            api("/api/bandwidth/system"),
            api("/api/bandwidth/users")
        ]);

        if (sysResp) {
            const sys = await sysResp.json();
            const todayTotal = (sys.today?.rx || 0) + (sys.today?.tx || 0);
            const monthTotal = (sys.month?.rx || 0) + (sys.month?.tx || 0);
            const allTotal = (sys.total?.rx || 0) + (sys.total?.tx || 0);

            document.getElementById("bw-today").textContent = formatBytes(todayTotal);
            document.getElementById("bw-month").textContent = formatBytes(monthTotal);
            document.getElementById("bw-total").textContent = formatBytes(allTotal);
        }

        if (userResp) {
            const users = await userResp.json();
            const tbody = document.getElementById("bandwidth-tbody");
            const chartContainer = document.getElementById("user-bandwidth-chart");

            const entries = Object.entries(users);

            if (entries.length === 0) {
                tbody.innerHTML = `<tr><td colspan="4" style="text-align:center;color:var(--text-dim)">No data</td></tr>`;
                chartContainer.innerHTML = `<p style="text-align:center;color:var(--text-dim)">No per-user data available</p>`;
                return;
            }

            tbody.innerHTML = entries.map(([name, data]) => {
                const up = data.uplink || data.uplink_session || 0;
                const down = data.downlink || data.downlink_session || 0;
                return `<tr>
                    <td><strong>${escapeHtml(name)}</strong></td>
                    <td>${formatBytes(up)}</td>
                    <td>${formatBytes(down)}</td>
                    <td>${formatBytes(up + down)}</td>
                </tr>`;
            }).join("");

            // Simple SVG bar chart
            renderBandwidthChart(chartContainer, entries);
        }
    } catch (err) {
        console.error("Failed to load bandwidth:", err);
    }
}

function renderBandwidthChart(container, entries) {
    if (entries.length === 0) {
        container.innerHTML = "";
        return;
    }

    const maxVal = Math.max(...entries.map(([, d]) => (d.uplink || 0) + (d.downlink || 0)), 1);
    const barHeight = 28;
    const gap = 8;
    const labelWidth = 120;
    const chartWidth = container.clientWidth - 40 || 500;
    const svgHeight = entries.length * (barHeight + gap) + 10;
    const barAreaWidth = chartWidth - labelWidth - 20;

    let svg = `<svg width="100%" height="${svgHeight}" viewBox="0 0 ${chartWidth} ${svgHeight}">`;

    entries.forEach(([name, data], i) => {
        const total = (data.uplink || 0) + (data.downlink || 0);
        const barW = Math.max((total / maxVal) * barAreaWidth, 2);
        const y = i * (barHeight + gap) + 5;

        // Label
        const displayName = name.length > 14 ? name.substring(0, 14) + "..." : name;
        svg += `<text x="${labelWidth - 8}" y="${y + barHeight / 2 + 4}" fill="#8b8fa3" font-size="12" text-anchor="end">${escapeHtml(displayName)}</text>`;

        // Bar
        svg += `<rect x="${labelWidth}" y="${y}" width="${barW}" height="${barHeight}" rx="4" fill="#5b8af5" opacity="0.8"/>`;

        // Value
        svg += `<text x="${labelWidth + barW + 8}" y="${y + barHeight / 2 + 4}" fill="#e4e6eb" font-size="11">${formatBytes(total)}</text>`;
    });

    svg += "</svg>";
    container.innerHTML = svg;
}

/* ─── Connections ───────────────────────────────────────────────────────── */

async function loadConnections() {
    try {
        const resp = await api("/api/connections");
        if (!resp) return;
        const connections = await resp.json();
        const tbody = document.getElementById("connections-tbody");
        const countEl = document.getElementById("conn-count");

        countEl.textContent = `${t("active_connections")}: ${connections.length}`;

        if (connections.length === 0) {
            tbody.innerHTML = `<tr><td colspan="4" style="text-align:center;color:var(--text-dim)">No active connections</td></tr>`;
            return;
        }

        tbody.innerHTML = connections.map(c => `<tr>
            <td>${escapeHtml(c.remote)}</td>
            <td>${escapeHtml(c.local)}</td>
            <td>${escapeHtml(c.state)}</td>
            <td>${escapeHtml(c.process || "-")}</td>
        </tr>`).join("");
    } catch (err) {
        console.error("Failed to load connections:", err);
    }
}

/* ─── Service Control ───────────────────────────────────────────────────── */

async function restartService() {
    const btn = document.getElementById("restartBtn");
    btn.disabled = true;
    btn.querySelector("span").textContent = t("restarting");

    try {
        const resp = await api("/api/service/restart", { method: "POST" });
        const data = await resp.json();
        if (data.success) {
            showToast(t("service_restarted"), "success");
        } else {
            showToast(data.error || "Failed to restart", "error");
        }
    } catch (err) {
        showToast("Network error", "error");
    } finally {
        btn.disabled = false;
        btn.querySelector("span").textContent = t("restart_service");
    }
}

async function loadLogs() {
    const viewer = document.getElementById("log-viewer");
    viewer.textContent = "Loading...";

    try {
        const resp = await api("/api/service/logs");
        if (!resp) return;
        const data = await resp.json();
        viewer.textContent = data.logs || "No logs available";
        viewer.scrollTop = viewer.scrollHeight;
    } catch (err) {
        viewer.textContent = "Failed to load logs";
    }
}

/* ─── Utilities ─────────────────────────────────────────────────────────── */

function closeModal(id) {
    document.getElementById(id).style.display = "none";
}

function escapeHtml(str) {
    const div = document.createElement("div");
    div.textContent = str || "";
    return div.innerHTML;
}

function copyText(elementId) {
    const text = document.getElementById(elementId).textContent;
    navigator.clipboard.writeText(text).then(() => {
        showToast(t("copied"), "success");
    }).catch(() => {
        // Fallback
        const ta = document.createElement("textarea");
        ta.value = text;
        document.body.appendChild(ta);
        ta.select();
        document.execCommand("copy");
        document.body.removeChild(ta);
        showToast(t("copied"), "success");
    });
}

function showToast(message, type = "success") {
    const toast = document.createElement("div");
    toast.className = `toast ${type}`;
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(() => {
        toast.remove();
    }, 3000);
}

async function handleLogout() {
    try {
        await fetch("/api/logout", { method: "POST" });
    } catch (e) {}
    window.location.href = "/login";
}

/* ─── Initialize ────────────────────────────────────────────────────────── */

document.addEventListener("DOMContentLoaded", () => {
    applyLang(currentLang);
    loadOverview();

    // Auto-refresh overview every 30 seconds
    setInterval(() => {
        const activeSection = document.querySelector(".section.active");
        if (activeSection && activeSection.id === "section-overview") {
            loadOverview();
        }
    }, 30000);
});

// Close modal on backdrop click
document.addEventListener("click", (e) => {
    if (e.target.classList.contains("modal-overlay")) {
        e.target.style.display = "none";
    }
});

// Close modal on Escape
document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
        document.querySelectorAll(".modal-overlay").forEach(m => m.style.display = "none");
    }
});
