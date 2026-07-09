#!/usr/bin/env python3
"""Sesi 11: Web Information Gathering — Reconnaissance Aplikasi Web"""

import subprocess
import sys
import os
from datetime import datetime


def banner():
    print("=" * 60)
    print("  ETHICAL ELITE HACKER v11 — Sesi 11")
    print("  Web Information Gathering — Reconnaissance")
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


# ── [1] Information Gathering Concept ──
def konsep_recon():
    print("""
  💡 WEB INFORMATION GATHERING = Mengumpulkan informasi sebanyak-banyaknya
     tentang target aplikasi web SEBELUM menyerang.

  👉 Passive Recon: Tidak menyentuh server target (Google, WHOIS, Shodan)
  👉 Active Recon: Berinteraksi langsung (scan port, directory brute force)

  🔥 Pepatah Hacker: "Knowledge is power. The more you know, the more
     attack surface you can exploit."

   ╔═══════════════════════════════════════════════════════╗
   ║  🔍 JADI DETEKTIF                                    ║
   ║     • Cari profil korban (WHOIS, social media)       ║
   ║     • Cek pagar rumah (WAF, firewall detection)      ║
   ║     • Ejek-ejek pintu (directory brute force)        ║
   ║     • Lihat jendela yang terbuka (open ports)        ║
   ╚═══════════════════════════════════════════════════════╝
    """)


# ── [2] WHOIS Concept ──
def whois_concept():
    print("  💡 WHOIS — Domain Registration Lookup:\\n")

    whois_status = check_tool("whois")

    print(f"  {'Tool':<15} {'Status':<20}")
    print(f"  {'─' * 35}")
    print(f"  {'whois':<15} {whois_status:<20}")
    print()

    print("  Informasi yang didapat dari WHOIS:")
    print(f"  {'Field':<25} {'Contoh':<35}")
    print(f"  {'─' * 60}")
    fields = [
        ("Registrant Name",     "John Doe / PT XYZ"),
        ("Organization",        "Perusahaan Target"),
        ("Email",               "admin@target.com"),
        ("Phone",               "+62 21 1234 5678"),
        ("Name Server",         "ns1.target.com"),
        ("Creation Date",       "2010-03-15"),
        ("Expiry Date",         "2028-03-15"),
        ("Registrar",           "Namecheap, GoDaddy"),
    ]
    for field, example in fields:
        print(f"  {field:<25} {example:<35}")
    print()

    print("  🔥 OSINT via WHOIS:")
    print("     • Cari email admin → bisa untuk phishing/social engineering")
    print("     • Cek expiry date → domain expired? Bisa dibajak!")
    print("     • Cek name server → subdomain takeover potential")
    print()

    print("  Contoh CLI:")
    print("    $ whois target.com")
    print("    $ whois 192.168.1.1     # IP WHOIS (ARIN/RIPE/APNIC)")
    print()


# ── [3] Google Dorking Examples ──
def google_dorking():
    print("  💡 GOOGLE DORKING — Search Engine Hacking:\\n")

    print(f"  {'Dork':<45} {'Hasil':<35}")
    print(f"  {'─' * 80}")
    dorks = [
        ("site:target.com filetype:pdf",       "Semua PDF di domain target"),
        ("site:target.com intitle:login",      "Halaman login tersembunyi"),
        ("inurl:admin.php",                    "Admin panel (sering lupa dilindungi)"),
        ("intitle:\"Index of\" /etc",           "Directory listing sensitif"),
        ("filetype:sql \"INSERT INTO\"",        "SQL dump bocor"),
        ("site:target.com ext:log",            "Log file terekspos"),
        ("inurl:wp-content/uploads",           "Upload folder WordPress"),
        ("site:target.com inurl:php?param=",   "Parameter rentan SQLi/XSS"),
        ("intitle:\"phpMyAdmin\"",              "phpMyAdmin tanpa login"),
        ("site:target.com \"password\" filetype:txt", "Password bocor via TXT"),
    ]
    for dork, hasil in dorks:
        print(f"  {dork:<45} {hasil:<35}")
    print()

    print("  🔥 Google Dorking = Google Hacking Database (GHDB)")
    print("     • Sumber: exploit-db.com/google-hacking-database")
    print("     • Cari dork baru: site:target.com \"confidential\"")
    print("     • Gunakan boolean: AND, OR, - (minus untuk exclude)")
    print()


# ── [4] Subdomain Enumeration ──
def subdomain_enum():
    print("  💡 SUBDOMAIN ENUMERATION:\\n")

    tools = ["subfinder", "amass", "sublist3r", "dnsrecon", "dnsenum"]
    print(f"  {'Tool':<15} {'Status':<20} {'Fungsi':<40}")
    print(f"  {'─' * 75}")
    for tool in tools:
        status = check_tool(tool)
        desc = {
            "subfinder": "Fast passive subdomain enumeration",
            "amass": "Deep subdomain discovery (OWASP)",
            "sublist3r": "Subdomain via search engines",
            "dnsrecon": "DNS record enumeration",
            "dnsenum": "DNS brute force + zone transfer",
        }.get(tool, "")
        print(f"  {tool:<15} {status:<20} {desc:<40}")
    print()

    print("  💡 Subdomain penting untuk ditemukan:")
    items = [
        ("admin.target.com",     "Panel admin (bisa di-brute force)"),
        ("dev.target.com",       "Dev server (sering lebih lemah)"),
        ("api.target.com",       "API endpoint (bocor data)"),
        ("test.target.com",      "Test server (default creds)"),
        ("mail.target.com",      "Mail server (phishing target)"),
        ("git.target.com",       "Git server (source code bocor)"),
    ]
    for sub, why in items:
        print(f"     👉 {sub:<25} → {why}")
    print()


# ── [5] WAF Detection ──
def waf_detection():
    print("  💡 WAF DETECTION — Web Application Firewall:\\n")

    waf_status = check_tool("wafw00f")
    print(f"  {'Tool':<15} {'Status':<20}")
    print(f"  {'─' * 35}")
    print(f"  {'wafw00f':<15} {waf_status:<20}")
    print()

    print("  💡 Fungsi WAF Detection:")
    print("     • Tahu jenis WAF sebelum exploit → sesuaikan payload")
    print("     • Beberapa WAF bisa di-bypass dengan teknik tertentu")
    print()

    print(f"  {'WAF':<20} {'Provider':<30} {'Susah Di-bypass':<20}")
    print(f"  {'─' * 70}")
    wafs = [
        ("Cloudflare",        "Cloudflare Inc.",        "⭐⭐⭐⭐⭐"),
        ("ModSecurity",       "Open Source / Apache",   "⭐⭐⭐"),
        ("AWS WAF",           "Amazon Web Services",    "⭐⭐⭐⭐"),
        ("Sucuri",            "GoDaddy / Sucuri",       "⭐⭐⭐⭐"),
        ("F5 BIG-IP ASM",     "F5 Networks",            "⭐⭐⭐⭐⭐"),
        ("Akamai Kona",       "Akamai",                 "⭐⭐⭐⭐⭐"),
        ("Imperva",           "Imperva Inc.",           "⭐⭐⭐⭐"),
        ("Barracuda WAF",     "Barracuda Networks",     "⭐⭐⭐"),
    ]
    for waf, prov, diff in wafs:
        print(f"  {waf:<20} {prov:<30} {diff:<20}")
    print()

    print("  🔥 Contoh bypass WAF dasar:")
    print("     • Case variation: <sCrIpT> vs <script>")
    print("     • Encoding: %3Cscript%3E vs <script>")
    print("     • Comment injection: <scr<!-->ipt>")
    print("     • Unicode: ＜script＞ (full-width)")
    print("     • Parameter pollution: ?id=1&id=2")
    print()


# ── [6] Directory Brute Force ──
def directory_bruteforce():
    print("  💡 DIRECTORY BRUTE FORCE — Finding Hidden Paths:\\n")

    tools = ["gobuster", "dirb", "feroxbuster", "ffuf", "dirsearch"]
    print(f"  {'Tool':<15} {'Status':<20} {'Metode':<30}")
    print(f"  {'─' * 65}")
    for tool in tools:
        status = check_tool(tool)
        print(f"  {tool:<15} {status:<20} {'Wordlist-based brute force':<30}")
    print()

    print("  🔥 Konsep Directory Brute Force:")
    print("     • Menggunakan wordlist (common.txt, directory-list-2.3-medium.txt)")
    print("     • Mencoba ribuan path: /admin, /backup, /config, /wp-admin")
    print("     • Filter response: 200 (OK) vs 404 (Not Found)")
    print()

    print("  💡 Contoh cara kerja gobuster:")
    print("""
    $ gobuster dir -u https://target.com \\
      -w /usr/share/wordlists/dirb/common.txt \\
      -t 50 -x php,txt,html
    """)
    print()

    print(f"  {'Status Code':<15} {'Arti':<35} {'Contoh Path':<30}")
    print(f"  {'─' * 80}")
    status_codes = [
        ("200 OK",       "File/directory ditemukan",    "/admin, /login.php"),
        ("301/302",      "Redirect (sering ke login)",  "/admin → /admin/login"),
        ("403 Forbidden", "Ada tapi dilarang akses",    "/private, /config"),
        ("401 Unauthorized", "Butuh autentikasi",       "/admin/, /cpanel"),
        ("500 Server Error", "Server error (exploit?)", "/test, /debug"),
        ("404 Not Found",   "Tidak ada",                "/nonexistent_path"),
    ]
    for code, arti, contoh in status_codes:
        print(f"  {code:<15} {arti:<35} {contoh:<30}")
    print()


# ── [7] Shodan Concept ──
def shodan_concept():
    print("  💡 SHODAN — Search Engine untuk Perangkat IoT/Infrastruktur:\\n")

    print("""
   ╔═══════════════════════════════════════════════════════╗
   ║  🔍 SHODAN = Google-nya perangkat yang terhubung     ║
   ║     internet. Bisa cari webcam, router, server,      ║
   ║     PLC industri, traffic lights, dan lainnya.       ║
   ╚═══════════════════════════════════════════════════════╝
    """)

    print(f"  {'Query Shodan':<40} {'Hasil':<40}")
    print(f"  {'─' * 80}")
    queries = [
        ("port:21 Anonymous",            "FTP anonymous login terbuka"),
        ("port:3306 root@",              "MySQL tanpa password (terkena!)"),
        ("port:8080 \"tomcat\"",          "Apache Tomcat default"),
        ("port:5900 VNC",                "VNC tanpa password"),
        ("org:\"Target Corp\"",           "Semua perangkat perusahaan target"),
        ("country:ID port:3389",         "RDP terbuka di Indonesia"),
        ("webcam 7.0",                   "Webcam publik (tanpa login)"),
        ("\"default password\" port:22",  "SSH dengan password default"),
    ]
    for q, hasil in queries:
        print(f"  {q:<40} {hasil:<40}")
    print()

    print("  🔥 Shodan Filters penting:")
    print("     • city:, country:, org:, hostname:")
    print("     • port:, before:, after:")
    print("     • title:, html:, http.title:")
    print("     • net: (CIDR range search)")
    print()


# ── [8] robots.txt Checker ──
def robots_checker():
    print("  💡 ROBOTS.TXT — Disallowed Paths Disclosure:\\n")

    print("""
  Konsep:
     robots.txt memberi tahu web crawler (Google Bot) halaman mana
     yang BOLEH dan TIDAK BOLEH di-index.

     Masalah: Hacker juga baca robots.txt!
     Disallowed path = 'Please don't crawl here' = 'Interesting stuff here!'
    """)

    print(f"  {'Directive':<20} {'Contoh':<40} {'Arti':<30}")
    print(f"  {'─' * 90}")
    examples = [
        ("User-agent:",      "User-agent: *",          "Berlaku untuk semua crawler"),
        ("Disallow:",        "Disallow: /admin",       "Jangan index /admin"),
        ("Disallow:",        "Disallow: /backup/",     "Backup folder (sering bocor)"),
        ("Disallow:",        "Disallow: /config/",     "Config file (sensitive)"),
        ("Disallow:",        "Disallow: /wp-admin",    "WP admin (sering disallow)"),
        ("Allow:",           "Allow: /public/",        "Allow specific path"),
        ("Sitemap:",         "Sitemap: https://...",   "Lokasi sitemap XML"),
    ]
    for directive, contoh, arti in examples:
        print(f"  {directive:<20} {contoh:<40} {arti:<30}")
    print()

    print("""
  🔥 Cara manual cek robots.txt:
     $ curl https://target.com/robots.txt

  🔥 Sering ditemukan di robots.txt:
     • /admin, /administrator, /backup, /config
     • /tmp, /log, /test, /dev, /api, /internal
    """)


# ── [9] Tech Stack Detection ──
def tech_detection():
    print("  💡 TECH STACK DETECTION — Identifikasi Teknologi Website:\\n")

    tools = ["whatweb", "wappalyzer", "builtwith"]
    print(f"  {'Tool':<15} {'Status':<20} {'Cara Kerja':<40}")
    print(f"  {'─' * 75}")
    for tool in tools:
        status = check_tool(tool)
        desc = {
            "whatweb": "Fingerprint via HTTP headers + HTML (CLI)",
            "wappalyzer": "Browser extension (deteksi JS)",
            "builtwith": "API-based tech profiler (berbayar)",
        }.get(tool, "")
        print(f"  {tool:<15} {status:<20} {desc:<40}")
    print()

    print("  💡 Informasi yang bisa didapat:")
    print(f"  {'Info':<25} {'Contoh':<40} {'Guna Buat Hacker':<35}")
    print(f"  {'─' * 100}")
    infos = [
        ("Web Server",       "Apache 2.4.49",          "CVE-2021-41773 (Path Traversal)"),
        ("CMS",              "WordPress 5.8",          "CVE-2021-29447 (XXE)"),
        ("Framework",        "Laravel 8.x",            "Env file exposure, debug mode"),
        ("JS Framework",     "React / Angular",         "API endpoints buried in JS"),
        ("Cloud Provider",   "Cloudflare / AWS",       "Origin IP bypass, WAF bypass"),
        ("CDN",              "Cloudflare, Akamai",      "True server IP discovery"),
        ("SSL/TLS",          "Let's Encrypt / CloudSSL","SSL certificate info (Org, Loc)"),
    ]
    for info, contoh, guna in infos:
        print(f"  {info:<25} {contoh:<40} {guna:<35}")
    print()

    print("  🔥 HTTP Headers yang berguna:")
    print("     • Server → Apache/Nginx/IIS version")
    print("     • X-Powered-By → PHP/ASP.NET version")
    print("     • X-AspNet-Version → .NET version")
    print("     • Set-Cookie → PHPSESSID (PHP), ASPSESSIONID (ASP)")
    print()


# ── [10] Analogi ──
def analogi():
    print("""
   ╔══════════════════════════════════════════════════════════╗
   ║   🔍 JADI DETEKTIF                                      ║
   ║                                                        ║
   ║   Seperti detektif yang mengamati rumah target:        ║
   ║                                                        ║
   ║   1. Cari profil rumah (WHOIS)                         ║
   ║      → Siapa pemiliknya? Alamatnya?                    ║
   ║                                                        ║
   ║   2. Google info tetangga (Google Dorking)             ║
   ║      → Apa kata orang tentang rumah ini?               ║
   ║                                                        ║
   ║   3. Cek pagar rumah (WAF Detection)                   ║
   ║      → Apakah ada alarm? Seberapa canggih?             ║
   ║                                                        ║
   ║   4. Ejek pintu dan jendela (Directory Brute Force)    ║
   ║      → Pintu samping terkunci? Jendela belakang?       ║
   ║                                                        ║
   ║   5. Cek teknologi pintu (Tech Stack Detection)        ║
   ║      → Kunci digital macam apa yang dipakai?           ║
   ╚══════════════════════════════════════════════════════════╝
    """)


def main():
    banner()

    # ── [1] Konsep Recon ──
    section(1, "KONSEP INFORMATION GATHERING")
    konsep_recon()

    # ── [2] WHOIS ──
    section(2, "WHOIS — DOMAIN LOOKUP")
    whois_concept()

    # ── [3] Google Dorking ──
    section(3, "GOOGLE DORKING / SEARCH ENGINE HACKING")
    google_dorking()

    # ── [4] Subdomain Enumeration ──
    section(4, "SUBDOMAIN ENUMERATION")
    subdomain_enum()

    # ── [5] WAF Detection ──
    section(5, "WAF DETECTION (Web Application Firewall)")
    waf_detection()

    # ── [6] Directory Brute Force ──
    section(6, "DIRECTORY BRUTE FORCE")
    directory_bruteforce()

    # ── [7] Shodan ──
    section(7, "SHODAN — IOT SEARCH ENGINE")
    shodan_concept()

    # ── [8] robots.txt ──
    section(8, "ROBOTS.TXT CHECKER")
    robots_checker()

    # ── [9] Tech Stack ──
    section(9, "TECH STACK DETECTION")
    tech_detection()

    # ── [10] Analogi ──
    section(10, "ANALOGI")
    analogi()

    # ── Summary ──
    print("=" * 60)
    print("  ✅ SESI 11 SELESAI!")
    print("=" * 60)
    print("  👉 Recap:")
    print("    • Information Gathering: Passive + Active Recon")
    print("    • WHOIS: Dapatkan info domain (owner, email, registrar)")
    print("    • Google Dorking: Google Hacking Database (GHDB)")
    print("    • Subdomain: subfinder, amass untuk temukan subdomain")
    print("    • WAF Detection: wafw00f untuk identifikasi firewall")
    print("    • Directory Brute Force: gobuster, dirb, ffuf")
    print("    • Shodan: Search engine untuk perangkat internet")
    print("    • robots.txt: Disallowed paths = hidden gems")
    print("    • Tech Stack: whatweb untuk fingerprint teknologi")
    print()
    print("  📌 LATIHAN LANJUTAN:")
    print("    1. Install whois dan cek domain target sesungguhnya")
    print("    2. Coba Google Dorking: site:example.com filetype:xls password")
    print("    3. Install subfinder/subfinder dan scan subdomain")
    print("    4. Coba wafw00f https://example.com")
    print("    5. Install gobuster dan scan direktori")
    print("    6. Cek Shodan: port:21 anonymous country:ID")
    print("    7. Cek robots.txt curl https://example.com/robots.txt")
    print("    8. Install whatweb: whatweb https://example.com")
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
