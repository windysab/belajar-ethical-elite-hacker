#!/usr/bin/env python3
"""Sesi 10: Wazuh SIEM — Security Information and Event Management"""

import subprocess
import sys
import os
import re
from datetime import datetime


def banner():
    print("=" * 60)
    print("  ETHICAL ELITE HACKER v11 — Sesi 10")
    print("  Wazuh SIEM — Security Information & Event Management")
    print("=" * 60)
    print("  Referensi: X-Code Ethical Elite Hacker v11")
    print("=" * 60)


def check_tool(name, cmd_flag=None):
    cmd = name if cmd_flag is None else cmd_flag
    try:
        subprocess.check_output([cmd, "--version"], stderr=subprocess.STDOUT, timeout=5)
        return "✅ TERINSTAL"
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return "❌ TIDAK TERINSTAL"


def check_service(name):
    try:
        subprocess.check_output(["systemctl", "is-active", name],
                                stderr=subprocess.STDOUT, timeout=5)
        return "✅ ACTIVE"
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return "❌ TIDAK AKTIF"


def section(num, title):
    print(f"\n{'─' * 50}")
    print(f"  [{num}] {title}")
    print(f"{'─' * 50}")


# ── [1] SIEM Concept ──
def siem_concept():
    print("""
  💡 SIEM = Security Information and Event Management

  👉 Mengumpulkan log dari berbagai sumber (server, firewall, endpoint)
  👉 Menganalisis & mengkorelasikan event untuk deteksi ancaman
  👉 Memberi alert real-time jika mencurigakan

  Komponen SIEM:
    ├── Log Collection     → syslog, agent, API
    ├── Normalization      → format log diseragamkan
    ├── Correlation        → aturan deteksi ancaman
    ├── Alerting           → notifikasi real-time
    └── Dashboard          → visualisasi & reporting
    """)


# ── [2] Wazuh Architecture ──
def wazuh_architecture():
    print("  💡 Arsitektur Wazuh (Open Source SIEM + XDR):\n")

    print("  ╔═══════════════════════════════════════════════╗")
    print("  ║              🖥️  WA Z U H  S T A C K          ║")
    print("  ╠═══════════════════════════════════════════════╣")
    print("  ║                                               ║")
    print("  ║   ┌──────────┐    ┌──────────┐               ║")
    print("  ║   │ Wazuh    │◄───│ Wazuh    │               ║")
    print("  ║   │ Agent    │    │ Manager  │               ║")
    print("  ║   └──────────┘    └────┬─────┘               ║")
    print("  ║                        │                      ║")
    print("  ║                  ┌─────▼─────┐                ║")
    print("  ║                  │ Wazuh     │                ║")
    print("  ║                  │ Indexer   │                ║")
    print("  ║                  └─────┬─────┘                ║")
    print("  ║                        │                      ║")
    print("  ║                  ┌─────▼─────┐                ║")
    print("  ║                  │ Wazuh     │                ║")
    print("  ║                  │ Dashboard │                ║")
    print("  ║                  └───────────┘                ║")
    print("  ╚═══════════════════════════════════════════════╝\n")

    print(f"  {'Komponen':<20} {'Fungsi':<45} {'Port Default':<15}")
    print(f"  {'─' * 80}")
    components = [
        ("Wazuh Agent",     "Dijalankan di endpoint yang dimonitor",    "1514-1516"),
        ("Wazuh Manager",   "Server pusat: aturan, decoding, alert",   "55000 (API)"),
        ("Wazuh Indexer",   "Penyimpanan log (OpenSearch backend)",    "9200"),
        ("Wazuh Dashboard", "UI Grafis untuk visualisasi & analisis",  "443 (HTTPS)"),
    ]
    for comp, func, port in components:
        print(f"  {comp:<20} {func:<45} {port:<15}")
    print()


# ── [3] Check Local Wazuh ──
def check_local_wazuh():
    print("  💡 Pengecekan Wazuh di sistem lokal:\n")

    services = ["wazuh-manager", "wazuh-indexer", "wazuh-dashboard", "filebeat"]
    print(f"  {'Service':<25} {'Status':<20}")
    print(f"  {'─' * 45}")
    for svc in services:
        status = check_service(svc)
        print(f"  {svc:<25} {status:<20}")
    print()

    # Check Wazuh config paths
    config_paths = [
        "/var/ossec/etc/ossec.conf",
        "/var/ossec/etc/rules/",
        "/etc/wazuh-indexer/opensearch.yml",
    ]
    print(f"  {'Config Path':<40} {'Exists':<15}")
    print(f"  {'─' * 55}")
    for path in config_paths:
        exists = "✅ Ada" if os.path.exists(path) else "❌ Tidak ada"
        print(f"  {path:<40} {exists:<15}")
    print()


# ── [4] Alert Types Table ──
def alert_types():
    print("  💡 Tipe Alert Wazuh:\n")

    print(f"  {'Rule ID':<10} {'Level':<8} {'Deskripsi':<50}")
    print(f"  {'─' * 68}")
    alerts = [
        ("5712",  "3",  "SSH authentication failed"),
        ("5715",  "5",  "Multiple SSH authentication failures"),
        ("5501",  "10", "SSH Brute force detected"),
        ("80701", "12", "File integrity changed (FIM)"),
        ("86601", "7",  "Rootkit detected"),
        ("100002", "15", "Malware detected"),
        ("18150", "8",  "Port scan detected"),
        ("60011", "9",  "Process creation (auditd)"),
    ]
    for rid, level, desc in alerts:
        print(f"  {rid:<10} {level:<8} {desc:<50}")
    print()

    print("  🔥 Rule ID pentesting relevan:")
    print("     • 5710-5720  → SSH authentication monitoring")
    print("     • 80700-80800 → FIM (File Integrity Monitoring)")
    print("     • 86600-86700 → Rootkit detection")
    print("     • 18100-18199 → Network port scan detection")
    print()


# ── [5] Log Analysis Demo ──
def log_analysis():
    """Baca dan analisis /var/log/auth.log."""
    log_path = "/var/log/auth.log"
    print(f"  💡 Analisis log: {log_path}\n")

    if not os.path.exists(log_path):
        print("  ⚠️  /var/log/auth.log tidak ditemukan.")
        print("  ⚠️  Demo menggunakan data sintetis.\n")
        # Synthetic data
        sample_logs = [
            "Jul  9 08:12:33 server sshd[1234]: Failed password for root from 192.168.1.100 port 55678 ssh2",
            "Jul  9 08:12:34 server sshd[1235]: Failed password for admin from 10.0.0.50 port 55679 ssh2",
            "Jul  9 08:12:35 server sshd[1236]: Failed password for root from 192.168.1.100 port 55680 ssh2",
            "Jul  9 08:12:36 server sshd[1237]: Accepted password for ubuntu from 192.168.1.10 port 55681 ssh2",
            "Jul  9 08:12:37 server sshd[1238]: Failed password for root from 192.168.1.100 port 55682 ssh2",
            "Jul  9 08:12:38 server sshd[1239]: Received disconnect from 192.168.1.100: 11: Bye Bye",
        ]
        logs = sample_logs
    else:
        try:
            with open(log_path, "r") as f:
                logs = f.readlines()[-20:]  # Last 20 lines
        except PermissionError:
            print("  ⚠️  Permission denied. Gunakan sintetis.\n")
            logs = [
                "Jul  9 08:12:33 server sshd[1234]: Failed password for root from 192.168.1.100 port 55678 ssh2",
                "Jul  9 08:12:36 server sshd[1237]: Accepted password for ubuntu from 192.168.1.10 port 55681 ssh2",
            ]

    print(f"  {'Timestamp':<25} {'Event':<50}")
    print(f"  {'─' * 75}")
    for line in logs:
        line = line.strip()
        if not line:
            continue
        # Parse first 3 fields as timestamp
        parts = line.split()
        if len(parts) >= 3:
            ts = " ".join(parts[:3])
            rest = " ".join(parts[3:])
        else:
            ts = ""
            rest = line
        # Truncate if too long
        if len(rest) > 48:
            rest = rest[:45] + "..."
        print(f"  {ts:<25} {rest:<50}")
    print()

    # ── Analisis sederhana ──
    print("  🔥 Analisis log otomatis:")
    failed_count = sum(1 for line in logs if "Failed password" in line)
    accepted_count = sum(1 for line in logs if "Accepted password" in line)
    ips_failed = set()
    for line in logs:
        if "Failed password" in line:
            m = re.search(r"from (\S+)", line)
            if m:
                ips_failed.add(m.group(1))

    print(f"     Login gagal: {failed_count}")
    print(f"     Login sukses: {accepted_count}")
    print(f"     IP mencurigakan: {', '.join(sorted(ips_failed)) if ips_failed else 'N/A'}")
    print(f"     {'⚠️  Brute force terdeteksi!' if failed_count >= 5 else '✅ Tidak ada brute force signifikan'}")
    print()


# ── [6] Detection Rules Concept ──
def detection_rules():
    print("  💡 Contoh Rule Wazuh (XML):\n")
    print("""
  <rule id="100001" level="10">
    <decoded_as>sshd</decoded_as>
    <match>Failed password for root</match>
    <description>SSH brute force attempt on root</description>
    <group>authentication,failed,ssh,</group>
  </rule>
    """)

    print(f"  {'Komponen Rule':<20} {'Fungsi':<50}")
    print(f"  {'─' * 70}")
    rule_parts = [
        ("rule id",      "ID unik untuk rule"),
        ("level",        "Tingkat keparahan (0-15, makin besar makin kritis)"),
        ("decoded_as",   "Sumber log (sshd, apache, syslog...)"),
        ("match",        "Pattern string yang dicocokkan"),
        ("regex",        "Pattern regex untuk matching lebih kompleks"),
        ("if_matched",   "Rule hanya jalan jika rule lain match duluan"),
        ("group",        "Kategori alert"),
        ("description",  "Deskripsi yang muncul di alert"),
        ("mitre",        "Mapping ke MITRE ATT&CK"),
    ]
    for part, desc in rule_parts:
        print(f"  {part:<20} {desc:<50}")
    print()

    print("  🔥 Contoh rule detection untuk pentest:")
    print("     • Level 5: Multiple failed logins (5+ dalam 5 menit)")
    print("     • Level 10: Brute force atau known exploit pattern")
    print("     • Level 12: File integrity change (/etc/shadow)")
    print("     • Level 15: Malware/rootkit confirmed")
    print()


# ── [7] Wazuh API Demo ──
def wazuh_api_demo():
    print("  💡 Wazuh API — Interaksi programatik:\n")
    print("""
  # Contoh request API (REST):
  GET https://WAZUH_MANAGER:55000/security/user/authenticate
  Authorization: Bearer <token>

  # Endpoint penting:
  GET /agents                    → Daftar semua agent
  GET /agents/:id/syscheck       → File integrity data
  GET /agents/:id/rootcheck      → Rootkit scan results
  GET /sca/:agent_id             → Security Configuration Assessment
  """)

    print(f"  {'Endpoint':<35} {'Kegunaan':<45}")
    print(f"  {'─' * 80}")
    endpoints = [
        ("GET /agents",                  "Lihat semua endpoint terdaftar"),
        ("GET /agents/summary",          "Statistik agent (active/disconnected)"),
        ("GET /security/rules",          "Daftar semua rules"),
        ("GET /security/alerts",         "Alert history"),
        ("PUT /agents/:id/restart",      "Restart agent"),
        ("DELETE /agents/:id",           "Hapus agent dari manager"),
    ]
    for ep, use in endpoints:
        print(f"  {ep:<35} {use:<45}")
    print()


def analogi():
    print("""
  ╔══════════════════════════════════════════════════════════╗
  ║   📹 CCTV PINTAR (Wazuh SIEM)                          ║
  ║      → Banyak kamera (agent) di berbagai titik          ║
  ║      → Semua feed masuk ke ruang monitor (manager)      ║
  ║      → AI deteksi gerakan mencurigakan (rules)          ║
  ║      → Langsung alarm ke satpam (alert)                 ║
  ║                                                        ║
  ║   👮 SATPAM GRATIS (Open Source SIEM)                  ║
  ║      → Bisa pantau 24/7 tanpa bayar lisensi             ║
  ║      → Butuh konfigurasi sendiri                        ║
  ║      → Komunitas banyak: forum, rules update            ║
  ╚══════════════════════════════════════════════════════════╝
    """)


def main():
    banner()

    # ── [1] SIEM Concept ──
    section(1, "KONSEP SIEM")
    siem_concept()

    # ── [2] Wazuh Architecture ──
    section(2, "ARISTEKTUR WAZUH")
    wazuh_architecture()

    # ── [3] Local Check ──
    section(3, "PENGECEKAN WAZUH LOKAL")
    check_local_wazuh()

    # ── [4] Alert Types ──
    section(4, "TIPE ALERT WAZUH")
    alert_types()

    # ── [5] Log Analysis Demo ──
    section(5, "ANALISIS LOG (AUTH.LOG)")
    log_analysis()

    # ── [6] Detection Rules ──
    section(6, "DETECTION RULES CONCEPT")
    detection_rules()

    # ── [7] Wazuh API ──
    section(7, "WAZUH API")
    wazuh_api_demo()

    # ── [8] Analogi ──
    section(8, "ANALOGI")
    analogi()

    # ── Summary ──
    print("=" * 60)
    print("  ✅ SESI 10 SELESAI!")
    print("=" * 60)
    print("  👉 Recap:")
    print("    • SIEM: Sentralisasi log, deteksi ancaman, alerting")
    print("    • Wazuh: Agent → Manager → Indexer → Dashboard")
    print("    • Rules: level 0-15, match/regex, MITRE mapping")
    print("    • Log Analysis: Failed logins, IP tracking")
    print("    • API: REST endpoint untuk automasi")
    print()
    print("  📌 LATIHAN LANJUTAN:")
    print("    1. Install Wazuh di Docker (wazuh-docker-compose)")
    print("    2. Install Wazuh agent di VM target")
    print("    3. Buat custom rule untuk deteksi tool pentest")
    print("    4. Integrasikan Wazuh dengan TheHive (SOAR)")
    print("    5. Buat dashboard Kibana/OpenSearch kustom")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n[!] Error: {e}")
        sys.exit(1)
