#!/usr/bin/env python3
"""Sesi 13: OWASP A6-A10 + Google Hacking Lanjutan"""

import subprocess
import sys
import os
import re
from datetime import datetime


def banner():
    print("=" * 60)
    print("  ETHICAL ELITE HACKER v11 — Sesi 13")
    print("  OWASP A6-A10 + Google Hacking Lanjutan")
    print("=" * 60)
    print("  Referensi: X-Code Ethical Elite Hacker v11")
    print("=" * 60)


def check_tool(name):
    try:
        subprocess.check_output([name, "--version"], stderr=subprocess.STDOUT, timeout=5)
        return "✅ TERINSTAL"
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return "❌ TIDAK TERINSTAL"


def section(num, title):
    print(f"\n{'─' * 50}")
    print(f"  [{num}] {title}")
    print(f"{'─' * 50}")


# ── [1] A6 — Vulnerable & Outdated Components ──
def a6_outdated():
    print("  💡 A6 — VULNERABLE & OUTDATED COMPONENTS:\\n")

    print("""
   ╔═══════════════════════════════════════════════════════╗
   ║  🚗 MOBIL TAHUN 80-an                               ║
   ║     Pakai komponen usang = mobil tahun 80-an yang   ║
   ║     dikendarai di jalan tol modern.                  ║
   ║     • Rem masih tromol → gampang blong               ║
   ║     • Sabuk pengaman tidak ada → fatal accident      ║
   ║     • Mesin karburator → boros & lemah               ║
   ║     Sama dengan aplikasi yang pakai library lama!    ║
   ╚═══════════════════════════════════════════════════════╝
    """)

    print("  Demo: Version Check Concept\\n")

    print("  💡 Cara cek versi komponen:")
    print("  $ curl -s http://target.com/ | head -5  # cek generator meta")
    print("  $ curl -sI http://target.com/ | grep -i server")
    print("  $ whatweb http://target.com/             # otomatis deteksi\n")

    print(f"  {'Komponen':<25} {'Versi Rentan':<30} {'CVE Terkait':<40}")
    print(f"  {'─' * 95}")
    components = [
        ("Apache",           "2.4.49",             "CVE-2021-41773 (Path Traversal)"),
        ("Apache",           "2.4.50",             "CVE-2021-42013 (RCE)"),
        ("Nginx",            "1.20.0",             "CVE-2021-23017 (DNS Resolver)"),
        ("OpenSSL",          "1.0.2",              "CVE-2014-0160 (Heartbleed)"),
        ("WordPress",        "< 5.8.3",            "CVE-2021-45416 (RCE via SQLi)"),
        ("PHP",              "< 8.1.0",            "CVE-2021-21703 (FPM RCE)"),
        ("Log4j",            "< 2.17.0",           "CVE-2021-44228 (Log4Shell)"),
        ("Node.js",          "< 16.13.0",           "CVE-2021-22960 (HTTP Hijack)"),
        ("Python",           "< 3.9.10",           "CVE-2021-3737 (HTTP Request Smuggle)"),
        ("OpenSSH",          "< 8.9",              "CVE-2021-41617 (Privilege Escalation)"),
    ]
    for comp, version, cve in components:
        print(f"  {comp:<25} {version:<30} {cve:<40}")
    print()

    print("  ✅ Pencegahan:")
    print("     • Pantau CVE secara rutin (cve.mitre.org, nvd.nist.gov)")
    print("     • Gunakan SBOM (Software Bill of Materials)")
    print("     • Update dependencies secara berkala")
    print("     • Jangan gunakan library yang sudah deprecated")
    print("     • Gunakan tool: OWASP Dependency-Check, Snyk, Trivy")
    print()


# ── [2] A7 — Identification & Auth Failures ──
def a7_auth_failure():
    print("  💡 A7 — IDENTIFICATION & AUTHENTICATION FAILURES:\\n")

    print("""
   ╔═══════════════════════════════════════════════════════╗
   ║  Ini masalah di cara aplikasi MEMVERIFIKASI          ║
   ║  identitas user (siapa kamu?) dan mengelola          ║
   ║  session (masihkah kamu yang tadi login?).           ║
   ╚═══════════════════════════════════════════════════════╝
    """)

    print(f"  {'Masalah':<30} {'Contoh':<40} {'Dampak':<30}")
    print(f"  {'─' * 100}")
    auth_issues = [
        ("Brute Force (no limit)",      "Login tanpa captcha/rate limit",       "Password ketebak"),
        ("Credential Stuffing",         "Password bocor dipake di mana-mana",   "Akun diretas massal"),
        ("Weak Password Policy",        "Min 2 karakter, no special char",      "Password gampang"),
        ("Session Fixation",            "Attacker kasih session ID ke korban",  "Hijack session"),
        ("Session not invalidated",     "Logout tapi session masih aktif",      "Session reuse"),
        ("JWT None Algorithm",          "alg: 'none' diterima server",          "Fake JWT → jadi admin"),
        ("OTP Brute Force",             "Kode 4 digit bisa ditebak",             "MFA bypass"),
        ("Remember Me insecure",        "Cookie 'remember_me' bisa didecode",   "Persistent session hijack"),
    ]
    for masalah, contoh, dampak in auth_issues:
        print(f"  {masalah:<30} {contoh:<40} {dampak:<30}")
    print()

    print("  ✅ Pencegahan:")
    print("     • Implementasi MFA (Multi-Factor Authentication)")
    print("     • Rate limiting — maks 5 percobaan per menit")
    print("     • Password policy: min 8 char, upper+lower+digit+symbol")
    print("     • JWT: gunakan RS256, jangan terima 'none' algorithm")
    print("     • Session: regenerate session ID setelah login")
    print("     • Gunakan OAuth 2.0 / OpenID Connect untuk SSO")
    print()


# ── [3] A8 — Software & Data Integrity Failures ──
def a8_integrity():
    print("  💡 A8 — SOFTWARE & DATA INTEGRITY FAILURES:\\n")

    print("""
   ╔═══════════════════════════════════════════════════════╗
   ║  📝 SURATIN MENTARI                                 ║
   ║     Kamu minta surat rekomendasi dari dosen.          ║
   ║     Tapi ternyata surat itu dipalsukan (tanda tangan ║
   ║     scan). Itulah integrity failure — data yang      ║
   ║     kamu terima belum diverifikasi keasliannya.      ║
   ╚═══════════════════════════════════════════════════════╝
    """)

    print(f"  {'Masalah Integrity':<30} {'Cara Serangan':<40} {'Dampak':<30}")
    print(f"  {'─' * 100}")
    integrity = [
        ("Supply Chain Attack",     "Library palsu di npm/PyPI",            "RCE via dependency"),
        ("CI/CD Poisoning",         "Inject code ke pipeline build",        "Malware in production"),
        ("Unsigned Updates",        "Update software tanpa signature check","Malware via update"),
        ("Insecure Deserialization","Object data dimanipulasi",              "RCE / DoS"),
        ("CSP Bypass",              "Load script dari untrusted source",    "XSS payload dijalankan"),
        ("SSTI (Server Template)",  "Template engine injection",            "RCE via template"),
    ]
    for masalah, cara, dampak in integrity:
        print(f"  {masalah:<30} {cara:<40} {dampak:<30}")
    print()

    print("  ✅ Pencegahan:")
    print("     • Code signing + verify signature sebelum eksekusi")
    print("     • Gunakan package manager dengan integrity check (sha256, GPG)")
    print("     • CI/CD: jangan percaya input dari luar pipeline")
    print("     • Subresource Integrity (SRI) untuk CDN scripts")
    print("     • Digital signature untuk semua update software")
    print()


# ── [4] A9 — Security Logging & Monitoring Failures ──
def a9_logging():
    print("  💡 A9 — SECURITY LOGGING & MONITORING FAILURES:\\n")

    print("""
   ╔═══════════════════════════════════════════════════════╗
   ║  Tanpa logging & monitoring yang baik, serangan      ║
   ║  bisa terjadi tanpa sepengetahuan admin.             ║
   ║  Attacker butuh WAKTU — logging adalah cara kita     ║
   ║  mendeteksi mereka sebelum semuanya hilang.          ║
   ╚═══════════════════════════════════════════════════════╝
    """)

    print("  Demo: Membaca /var/log/auth.log\\n")

    log_path = "/var/log/auth.log"
    print(f"  💡 Log file: {log_path}\\n")

    logs = []
    if os.path.exists(log_path):
        try:
            with open(log_path, "r") as f:
                logs = f.readlines()[-30:]
            print(f"  ✅ Berhasil membaca {len(logs)} baris terakhir\\n")
        except PermissionError:
            print("  ⚠️  Permission denied. Menggunakan data sintetis.\\n")
            logs = []
    else:
        print("  ⚠️  File tidak ditemukan. Menggunakan data sintetis.\\n")

    if not logs:
        logs = [
            "Jul  9 08:12:33 server sshd[1234]: Failed password for root from 192.168.1.100 port 55678 ssh2\n",
            "Jul  9 08:12:34 server sshd[1235]: Failed password for admin from 192.168.1.100 port 55679 ssh2\n",
            "Jul  9 08:12:35 server sshd[1236]: Failed password for root from 192.168.1.100 port 55680 ssh2\n",
            "Jul  9 08:12:36 server sshd[1237]: Accepted password for ubuntu from 192.168.1.10 port 55681 ssh2\n",
            "Jul  9 08:12:37 server sshd[1238]: Failed password for root from 192.168.1.100 port 55682 ssh2\n",
            "Jul  9 08:12:38 server sshd[1239]: Received disconnect from 192.168.1.100: 11: Bye Bye\n",
            "Jul  9 08:13:01 server CRON[1240]: pam_unix(cron:session): session opened for user root by (uid=0)\n",
            "Jul  9 08:14:22 server sudo[1241]: ubuntu : TTY=pts/0 ; PWD=/home/ubuntu ; USER=root ; COMMAND=/bin/su\n",
            "Jul  9 08:15:00 server sshd[1242]: Failed password for invalid user admin from 10.0.0.50 port 60000 ssh2\n",
            "Jul  9 08:15:01 server sshd[1243]: Failed password for invalid user admin from 10.0.0.50 port 60001 ssh2\n",
        ]

    # Parse dan analisis log
    lines_parsed = []
    for line in logs:
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) >= 5:
            ts = " ".join(parts[:3])
            service = parts[4] if len(parts) > 4 else "?"
            rest = " ".join(parts[5:]) if len(parts) > 5 else ""
            lines_parsed.append((ts, service, rest))
        else:
            lines_parsed.append((line, "", ""))

    print(f"  {'Timestamp':<22} {'Service/Proc':<20} {'Message / Event':<50}")
    print(f"  {'─' * 92}")
    for ts, svc, msg in lines_parsed:
        msg_short = msg[:48] if len(msg) > 48 else msg
        print(f"  {ts:<22} {svc:<20} {msg_short:<50}")
    print()

    # Analisis keamanan sederhana
    print("  🔥 Analisis Keamanan dari Log:\\n")

    failed_count = sum(1 for l in logs if "Failed password" in l)
    accepted_count = sum(1 for l in logs if "Accepted password" in l)
    invalid_count = sum(1 for l in logs if "invalid user" in l)
    sudo_count = sum(1 for l in logs if "sudo" in l)

    ips_failed = set()
    for l in logs:
        if "Failed password" in l:
            m = re.search(r"from (\S+)", l)
            if m:
                ips_failed.add(m.group(1))

    print(f"     {'Total login gagal':<30} {failed_count}")
    print(f"     {'Total login sukses':<30} {accepted_count}")
    print(f"     {'Invalid user attempts':<30} {invalid_count}")
    print(f"     {'Sudo commands':<30} {sudo_count}")
    print(f"     {'IP mencurigakan':<30} {', '.join(sorted(ips_failed)) if ips_failed else 'N/A'}")
    print()

    if failed_count >= 3:
        print("     ⚠️⚠️⚠️ Brute force attack TERDETEKSI!")
        print("     🔥 Rekomendasi: Blokir IP attacker via fail2ban atau iptables")
    else:
        print("     ✅ Tidak ada brute force signifikan terdeteksi")
    print()

    print("  ✅ Pencegahan Logging Failure:")
    print("     • Log semua event keamanan: login, logout, privilege change")
    print("     • Simpan log di central SIEM (Wazuh, ELK, Splunk)")
    print("     • Jangan log password/PII (personally identifiable info)")
    print("     • Gunakan format log terstruktur (JSON, syslog)")
    print("     • Protect log dari tampering (append-only, remote storage)")
    print()


# ── [5] A10 — SSRF (Server-Side Request Forgery) ──
def a10_ssrf():
    print("  💡 A10 — SERVER-SIDE REQUEST FORGERY (SSRF):\\n")

    print("""
  SSRF = Attacker memanfaatkan server untuk melakukan request
  ke resource internal yang seharusnya tidak bisa diakses dari luar.

  Contoh: Fitur "fetch URL" atau "import from URL" di aplikasi web.
    """)

    print(f"  {'Target':<25} {'Internal URL':<35} {'Dampak':<35}")
    print(f"  {'─' * 95}")
    targets = [
        ("AWS Metadata",       "http://169.254.169.254/latest/meta-data/", "Curi AWS credentials"),
        ("GCP Metadata",       "http://metadata.google.internal/computeMetadata/v1/", "Curi token GCP"),
        ("Internal DB",        "http://localhost:3306",                     "Akses MySQL internal"),
        ("Internal API",       "http://internal-api/admin/users",           "Akses API internal"),
        ("File Read",          "file:///etc/passwd",                        "Baca file server"),
        ("Redis/Memcached",    "gopher://localhost:6379/_SET key val",      "RCE via Redis"),
        ("Cloudflare Bypass",  "http://localhost:8080",                     "Bypass WAF/CDN"),
        ("Container Escape",   "http://localhost:2375/containers/json",     "Akses Docker API"),
    ]
    for target, url, dampak in targets:
        print(f"  {target:<25} {url:<35} {dampak:<35}")
    print()

    print("  ✅ Pencegahan SSRF:")
    print("     • Block IP range private (10.x.x.x, 172.16-31.x.x, 192.168.x.x)")
    print("     • Block localhost / 127.0.0.1 / 0.0.0.0")
    print("     • Block metadata endpoints (169.254.169.254)")
    print("     • Whitelist URL yang bisa di-fetch (bukan blacklist)")
    print("     • Jangan follow redirect secara otomatis")
    print("     • Gunakan network policy / firewall untuk membatasi request keluar")
    print()


# ── [6] Google Hacking Lanjutan ──
def google_hacking():
    print("  💡 GOOGLE HACKING LANJUTAN — Advanced Search Operators:\\n")

    print(f"  {'Operator':<18} {'Fungsi':<35} {'Contoh Query':<45}")
    print(f"  {'─' * 98}")
    operators = [
        ("site:",            "Batasi ke domain tertentu",            "site:target.com inurl:admin"),
        ("inurl:",           "Cari string di URL",                  "inurl:php?id="),
        ("intitle:",         "Cari string di title halaman",        "intitle:\"index of\" /etc"),
        ("intext:",          "Cari string di body teks",            "intext:\"mysql_connect\" ext:php"),
        ("filetype:",        "Filter jenis file",                   "filetype:sql password"),
        ("ext:",             "Filter ekstensi file",                "ext:log \"error\""),
        ("cache:",           "Lihat cache Google",                  "cache:target.com"),
        ("link:",            "Domain yang nge-link ke target",      "link:target.com"),
        ("related:",         "Domain mirip dengan target",          "related:target.com"),
        ("info:",            "Info page dari Google",               "info:target.com"),
        ("allinurl:",         "Semua kata di URL",                  "allinurl:admin config"),
        ("allintitle:",      "Semua kata di title",                 "allintitle:login admin panel"),
        ("before:",          "Halaman sebelum tanggal",             "before:2023 target.com"),
        ("after:",           "Halaman setelah tanggal",             "after:2023 target.com"),
        ("\"quoted\"",       "Exact phrase match",                  "\"confidential\" filetype:pdf"),
    ]
    for op, func, contoh in operators:
        print(f"  {op:<18} {func:<35} {contoh:<45}")
    print()

    print("  🔥 Advanced Google Dorking Combinations:\\n")
    print(f"  {'Tujuan':<40} {'Dork Query':<55}")
    print(f"  {'─' * 95}")
    combos = [
        ("SQL file with credentials",           "filetype:sql \"INSERT INTO\" password --"),
        ("PHP files with DB connection",         "ext:php intext:\"mysqli_connect\" -github.com"),
        ("Exposed .env files",                   "filetype:env DB_PASSWORD -git"),
        ("Exposed .git folder",                  "inurl:\".git\" intitle:\"Index of\" config"),
        ("Open FTP servers",                     "intitle:\"index of\" inurl:ftp"),
        ("Config files with passwords",          "ext:cfg \"password\" OR ext:conf \"password\""),
        ("Backup files",                         "ext:bak OR ext:old OR ext:backup"),
        ("Login pages with parameter",           "inurl:login.php? OR inurl:admin.php?"),
        ("PHPInfo files (sensitive)",            "intitle:\"phpinfo()\" ext:php"),
        ("Directory listing",                    "intitle:\"Index of\" \"parent directory\""),
    ]
    for tujuan, dork in combos:
        print(f"  {tujuan:<40} {dork:<55}")
    print()

    print("  ⚠️ Peringatan Etis:")
    print("     • Google Dorking adalah teknik OSINT (legal untuk research)")
    print("     • Mengeksploitasi data yang ditemukan = ILEGAL")
    print("     • Gunakan hanya untuk target yang kamu punya izin")
    print()


# ── [7] Real-world Attack Scenarios ──
def real_scenarios():
    print("  💡 SKENARIO SERANGAN REAL-WORLD untuk A6-A10:\\n")

    print(f"  {'Skenario':<35} {'OWASP':<10} {'Deskripsi':<45}")
    print(f"  {'─' * 90}")
    scenarios = [
        ("Log4Shell (Log4j)",       "A6",   "RCE via logging library vuln"),
        ("SolarWinds (2020)",       "A8",   "Supply chain — malware via update"),
        ("Capital One (2019)",      "A10",  "SSRF ke AWS metadata → 100M data bocor"),
        ("Magecart",                "A8",   "CI/CD poisoned → credit card skimmer"),
        ("Equifax (2017)",          "A6",   "Apache Struts CVE → 147M data bocor"),
        ("NPM package hijack",      "A8",   "Typo-squatting + malicious package"),
        ("Kaseya (2021)",           "A8",   "REvil ransomware via software update"),
        ("Twitter (2020)",          "A9",   "Social engineering via support tool"),
    ]
    for skenario, owasp, desc in scenarios:
        print(f"  {skenario:<35} {owasp:<10} {desc:<45}")
    print()


# ── [8] Analogi ──
def analogi():
    print("""
   ╔══════════════════════════════════════════════════════════╗
   ║   🚗 MOBIL TAHUN 80-an (A6 — Outdated Components)     ║
   ║      • Komponen usang = rem tromol, mesin karburator    ║
   ║      • Gampang disusul attacker                         ║
   ║                                                        ║
   ║   🔑 CEK IDENTITAS (A7 — Auth Failure)                 ║
   ║      • Satpam yang tidur — gak ngecek KTP dengan benar ║
   ║                                                        ║
   ║   📝 SURATIN MENTARI (A8 — Integrity Failure)          ║
   ║      • Surat palsu yang dikasih ke pihak berwenang     ║
   ║                                                        ║
   ║   📹 CCTV MATI (A9 — Logging Failure)                  ║
   ║      • Maling masuk tapi CCTV mati — gak ada bukti     ║
   ║                                                        ║
   ║   🏢 KURIR PALSU (A10 — SSRF)                          ║
   ║      • Attacker jadi kurir, masuk ke dalam gedung      ║
   ║        yang seharusnya restricted area                 ║
   ╚══════════════════════════════════════════════════════════╝
    """)


def main():
    banner()

    # ── [1] A6 Outdated Components ──
    section(1, "A6 — VULNERABLE & OUTDATED COMPONENTS")
    a6_outdated()

    # ── [2] A7 Auth Failure ──
    section(2, "A7 — IDENTIFICATION & AUTH FAILURES")
    a7_auth_failure()

    # ── [3] A8 Software & Data Integrity ──
    section(3, "A8 — SOFTWARE & DATA INTEGRITY FAILURES")
    a8_integrity()

    # ── [4] A9 Logging & Monitoring ──
    section(4, "A9 — SECURITY LOGGING & MONITORING FAILURES")
    a9_logging()

    # ── [5] A10 SSRF ──
    section(5, "A10 — SERVER-SIDE REQUEST FORGERY (SSRF)")
    a10_ssrf()

    # ── [6] Google Hacking Lanjutan ──
    section(6, "GOOGLE HACKING LANJUTAN")
    google_hacking()

    # ── [7] Real-World Scenarios ──
    section(7, "SKENARIO SERANGAN REAL-WORLD")
    real_scenarios()

    # ── [8] Analogi ──
    section(8, "ANALOGI LENGKAP")
    analogi()

    # ── Summary ──
    print("=" * 60)
    print("  ✅ SESI 13 SELESAI!")
    print("=" * 60)
    print("  👉 Recap:")
    print("    • A6 Outdated: Cek versi, update library, pantau CVE")
    print("    • A7 Auth Failure: MFA, rate limiting, JWT security")
    print("    • A8 Integrity: Code signing, SRI, supply chain security")
    print("    • A9 Logging: Baca auth.log, deteksi brute force")
    print("    • A10 SSRF: Block private IP, metadata endpoints")
    print("    • Google Hacking: site:, inurl:, filetype:, intitle:")
    print()
    print("  📌 LATIHAN LANJUTAN:")
    print("    1. Cari CVE terbaru: search.cve.mitre.org")
    print("    2. Coba OWASP Dependency-Check di project Java")
    print("    3. Baca /var/log/auth.log dan analisis manual")
    print("    4. Coba SSRF di aplikasi yang punya fitur fetch URL")
    print("    5. Praktik Google Dork: filetype:env DB_PASSWORD -git")
    print("    6. Install fail2ban dan lihat log-nya")
    print("    7. Cek versi library yang kamu pakai di project sendiri")
    print("    8. Baca laporan SolarWinds / Log4Shell untuk case study")
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
