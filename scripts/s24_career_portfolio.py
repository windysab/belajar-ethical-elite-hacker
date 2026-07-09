#!/usr/bin/env python3
"""
Sesi 24: Career & Portfolio — Membangun Karir di Cyber Security
Panduan lengkap karir, sertifikasi, portfolio, dan networking
Referensi: X-Code Ethical Elite Hacker v11
"""

import subprocess
import os
import sys
import datetime
import platform

# ============================================================
# BANNER
# ============================================================
def banner():
    print("=" * 60)
    print("  ETHICAL ELITE HACKER v11 — SESI 24")
    print("  Topik: Career & Portfolio — Jadi Hacker Profesional!")
    print("=" * 60)
    print()


# ============================================================
# [1] RED TEAM vs BLUE TEAM vs LAINNYA
# ============================================================
def bahas_role_keamanan():
    """Peran-peran dalam cyber security."""
    print("[1] PERAN DALAM CYBER SECURITY")
    print("-" * 60)

    roles = [
        ("🔴 RED TEAM", "Penetration Testing",
         "Menyerang (ethical hacking)", "Striker / Penyerang",
         "OSCP, OSEP, CRTO", "Offensive Security Engineer",
         "Simulasi serangan nyata, cari celah sebelum attacker"),
        ("🔵 BLUE TEAM", "Defense & Monitoring",
         "Bertahan (detect & respond)", "Bek / Defender",
         "CISSP, GCIA, GCIH", "SOC Analyst, Incident Responder",
         "Monitor SIEM, analisis malware, incident response"),
        ("🟣 PURPLE TEAM", "Red+Blue Collaboration",
         "Red+Blue kolaborasi", "Gelandang serang-belakang",
         "OSCP + CISSP", "Purple Team Lead",
         "Bridging attacker & defender, improve deteksi"),
        ("🟢 GRC", "Governance Risk Compliance",
         "Tata kelola & kepatuhan", "Wasit / Hukum",
         "CISA, CISM, CRISC", "GRC Analyst, Compliance Officer",
         "Audit, policy, compliance (ISO 27001, PCI DSS)"),
        ("🟡 DFIR", "Digital Forensics & IR",
         "Forensik digital & respons insiden", "Detektif CSI",
         "GCFE, GCFA, GNFA", "Forensic Analyst, IR Lead",
         "Investigasi breach, recovery data, legal hold"),
        ("⚪ Threat Intel", "Threat Intelligence",
         "Analisis ancaman global", "Analis Intelijen",
         "GCTI, CTIA", "Threat Intel Analyst",
         "Track APT groups, IOC sharing, threat hunting"),
        ("🟠 Vuln Management", "Vulnerability Management",
         "Manajemen patch & risk", "Dokter / Perawat",
         "CISSP, CEH", "Vuln Mgmt Engineer",
         "Scan, prioritize, remediate vulnerabilities"),
    ]

    print(f"{'ROLE':<25} {'FOKUS':<22} {'AKSI':<22} {'ANALOGI':<22} {'SERTIF':<22} {'JABATAN':<28} {'TUGAS UTAMA':<48}")
    print("-" * 209)
    for icon_nama, fokus, aksi, analogi, sertif, jabatan, tugas in roles:
        print(f"{icon_nama:<25} {fokus:<22} {aksi:<22} {analogi:<22} {sertif:<22} {jabatan:<28} {tugas:<48}")

    print()
    print("  💡 Pilih role sesuai minat:")
    print("     • Suka nge-hack? → Red Team")
    print("     • Suka defense & analisis? → Blue Team")
    print("     • Suka dua-duanya? → Purple Team")
    print("     • Suka dokumen & audit? → GRC")
    print("     • Suka puzzle & investigasi? → DFIR")
    print()


# ============================================================
# [2] LEVEL KARIR & GAJI
# ============================================================
def bahas_level_karir():
    """Level karir dan kisaran gaji."""
    print("[2] LEVEL KARIR & KISARAN GAJI")
    print("-" * 60)

    print("  ╔═══════════════════════════════════════════════════════════════╗")
    print("  ║  Gaji = Lokasi × Sertifikasi × Tahun Pengalaman × Role       ║")
    print("  ╚═══════════════════════════════════════════════════════════════╝\n")

    levels = [
        ("Entry Level", "0-2 tahun", "Junior Pentester / SOC L1 / IT Support",
         "IDR 60-120jt/thn", "USD 50-80K/thn",
         "Security+ \nNetwork+ \nCEH (optional)",
         "- Bisa scan NMAP\n- Basic scripting (Python/Bash)\n- Paham OWASP Top 10"),
        ("Mid Level", "2-5 tahun", "Pentester / SOC L2 / Security Engineer",
         "IDR 150-300jt/thn", "USD 85-130K/thn",
         "OSCP \nCISSP (Associate) \nPNPT",
         "- Lead engagement kecil\n- Exploit development\n- Report writing mandiri"),
        ("Senior Level", "5+ tahun", "Lead Pentester / SOC Manager / Arch",
         "IDR 350-700jt+/thn", "USD 140-200K+/thn",
         "OSEP \nCISSP \nOSED \nCREST",
         "- Team lead\n- Methodologi design\n- Client management\n- Complex engagements"),
    ]

    for level, exp, role, gaji_idr, gaji_usd, sertif, skills in levels:
        print(f"  ┌─ {level} ({exp})")
        print(f"  │  📌 Role: {role}")
        print(f"  │  💰 Gaji: {gaji_idr}  |  {gaji_usd}")
        print(f"  │  🏅 Sertifikasi: {sertif.replace(chr(10), ', ')}")
        skills_formatted = skills.replace(chr(10), '\n  │            ')
        print(f"  │  🛠️  Skills: {skills_formatted}")
        print()

    print("  💡 FAKTOR YANG MEMPENGARUHI GAJI:")
    print("     • Lokasi: Jakarta/Singapura > kota kecil")
    print("     • Remote: banyak perusahaan US/UK hire remote")
    print("     • Industri: finance & tech > government")
    print("     • Sertifikasi: OSCP = rata-rata +30% gaji")
    print("     • Freelance: bisa 2-3x gaji tetap tapi tidak stabil")
    print()


# ============================================================
# [3] JALUR SERTIFIKASI
# ============================================================
def bahas_sertifikasi():
    """Jalur sertifikasi dari pemula hingga expert."""
    print("[3] JALUR SERTIFIKASI CYBER SECURITY")
    print("-" * 60)

    print("""
  ╔═══════════════════════════════════════════════════════════════╗
  ║   PEMULA → MENENGAH → MAHIR → EXPERT → MASTER                ║
  ╚═══════════════════════════════════════════════════════════════╝\n""")

    jalur = [
        ("🟢 PEMULA", "", ""),
        ("", "CompTIA Security+", "Dasar keamanan IT, prerequisite semua"),
        ("", "CompTIA Network+", "Dasar networking, sangat membantu"),
        ("", "CEH (EC-Council)", "Teori hacking, banyak kritik tapi diakui HRD"),
        ("🟡 MENENGAH", "", ""),
        ("", "OSCP (Offensive Security)", "Praktikal! 24 jam exam, lab-heavy"),
        ("", "PNPT (TCM Security)", "Lebih real-world: AD, pivoting, report"),
        ("", "eJPT (eLearnSecurity)", "Alternatif lebih murah dari OSCP"),
        ("🔴 MAHIR", "", ""),
        ("", "OSEP (Offensive Security)", "AV evasion, AD exploitation lanjut"),
        ("", "CRTP (PentesterAcademy)", "Active Directory attack & defense"),
        ("", "GPEN (SANS/GIAC)", "Penetration testing dengan metodologi SANS"),
        ("🔵 BLUE/SOC", "", ""),
        ("", "CISSP (ISC2)", "Manajemen keamanan — gold standard non-teknis"),
        ("", "GCIA (SANS/GIAC)", "Intrusion analysis — jadi SOC expert"),
        ("", "GCIH (SANS/GIAC)", "Incident handling & response"),
        ("🟢 GRC", "", ""),
        ("", "CISA (ISACA)", "IT Audit — audit keamanan sistem informasi"),
        ("", "CISM (ISACA)", "Information Security Management"),
        ("", "CRISC (ISACA)", "Risk & Control — risk management"),
        ("⚪ DFIR", "", ""),
        ("", "GCFE (SANS/GIAC)", "Forensic examiner — Windows forensik"),
        ("", "GCFA (SANS/GIAC)", "Advanced forensic analysis"),
        ("", "CHFI (EC-Council)", "Computer Hacking Forensic Investigator"),
    ]

    for item in jalur:
        if item[1] == "" and item[2] == "":
            print(f"  ┌─ {item[0]}")
        else:
            print(f"  │  ├─ {item[1]:<45} — {item[2]}")
    print()

    print("  💡 TIPS MEMILIH SERTIFIKASI:")
    print("     • Baru mulai? Ambil Security+ dulu — fondasi")
    print("     • Mau jadi pentester? OSCP adalah gold standard")
    print("     • Budget terbatas? PNPT ($399) atau eJPT ($250)")
    print("     • Manajemen? CISSP — butuh 5 tahun pengalaman")
    print("     • Jangan kejar sertifikat doang — praktek itu wajib!")
    print()


# ============================================================
# [4] PORTFOLIO BUILDING
# ============================================================
def bahas_portfolio():
    """Membangun portfolio yang menarik."""
    print("[4] PORTFOLIO BUILDING — Album Kenangan Hacker")
    print("-" * 60)

    print("""
  ╔═══════════════════════════════════════════════════════════════╗
  ║  Portfolio = Album kenangan — bukti karya & perjalanan       ║
  ╚═══════════════════════════════════════════════════════════════╝\n""")

    print("  ┌─ KOMPONEN PORTFOLIO WAJIB:\n")
    print("  │  1️⃣  GITHUB — Source code & project")
    print("  │     • Exploit scripts yang kamu buat (jangan yang merusak!)")
    print("  │     • Automation tools (scanner, parser, report generator)")
    print("  │     • CTF writeup scripts (solusi capture the flag)")
    print("  │     • README.md yang bagus untuk setiap repo")
    print("  │     • Contoh: github.com/username/recon-toolkit")
    print()
    print("  │  2️⃣  LINKEDIN — Profesional presence")
    print("  │     • Headline: Ethical Hacker | OSCP | Pentester")
    print("  │     • About: ceritakan perjalanan dan minat")
    print("  │     • Featured: post CTF writeup, certs, project")
    print("  │     • Recommendations: minta rekomendasi dari klien/rekan")
    print()
    print("  │  3️⃣  BLOG / WEBSITE — Personal brand")
    print("  │     • Medium / Hashnode / Dev.to / GitHub Pages")
    print("  │     • Post CTF writeup, tutorial, opini")
    print("  │     • Case study: \"How I hacked X and got $5K bounty\"")
    print("  │     • Minimal 1 artikel per bulan — konsistensi lebih penting")
    print()
    print("  │  4️⃣  CTF WRITEUP — Bukti kemampuan teknis")
    print("  │     • Detail: methodology, tools, commands, screenshot")
    print("  │     • Jangan: copy paste writeup orang lain")
    print("  │     • Platform: HackTheBox, TryHackMe, CTFtime")
    print("  │     • Target: 10-20 writeup yang berkualitas")
    print()
    print("  │  5️⃣  BUG BOUNTY — Validasi keahlian di dunia nyata")
    print("  │     • Mulai dari program publik (HackerOne, Bugcrowd)")
    print("  │     • Target yang realistis: scope kecil, low hanging fruit")
    print("  │     • XSS, IDOR, SQLi — masih banyak yang reward")
    print("  │     • Dokumentasi findings di portfolio")
    print()


# ============================================================
# [5] STAR INTERVIEW TECHNIQUE
# ============================================================
def bahas_star_interview():
    """Teknik wawancara STAR."""
    print("[5] STAR INTERVIEW TECHNIQUE")
    print("-" * 60)

    print("""
  STAR = Situation, Task, Action, Result
  Format standar untuk menjawab pertanyaan behavioral interview

  ╔═══════════════════════════════════════════════════════════════╗
  ║  S — Situation: Setting/kondisi                              ║
  ║  T — Task: Tanggung jawab Anda                               ║
  ║  A — Action: Langkah konkret yang Anda ambil                  ║
  ║  R — Result: Hasil (pakai angka jika bisa!)                   ║
  ╚═══════════════════════════════════════════════════════════════╝\n""")

    print("  ┌─ CONTOH PERTANYAAN: \"Ceritakan saat Anda menemukan critical vulnerability\"\n")
    print("  │  ❌ JAWABAN BURUK:")
    print("  │  \"Saya nemu SQL injection terus report ke developer.\"\n")
    print("  │  ✅ JAWABAN STAR:")
    print("  │  [S] Saat magang di PT ABC, saya melakukan penetration testing")
    print("  │      pada aplikasi e-commerce yang melayani 50K user/hari.")
    print("  │  [T] Tugas saya adalah menemukan critical vulnerability di modul")
    print("  │      checkout yang terhubung ke database payment.")
    print("  │  [A] Saya melakukan manual testing dan menemukan blind SQL injection")
    print("  │      di parameter 'order_id'. Saya mengkonfirmasi dengan sqlmap")
    print("  │      (--dbs), dan mendokumentasikan PoC + dampak + rekomendasi fix.")
    print("  │  [R] Tim developer menambal dalam 48 jam. Saya mendapat pengakuan")
    print("      dalam security newsletter perusahaan.")
    print()
    print("  ┌─ CONTOH PERTANYAAN LAIN: \"Pernah gagal di project?\"\n")
    print("  │  [S] Saya lead pentest untuk client perbankan, scope 30 IP.")
    print("  │  [T] Deadline 2 minggu, tapi tim hanya 2 orang.")
    print("  │  [A] Saya prioritaskan high-value target, gunakan automation,")
    print("  │      dan komunikasi proaktif dengan client tentang keterbatasan.")
    print("  │  [R] 80% scope selesai tepat waktu. Client paham dan extend scope")
    print("  │      untuk bulan berikutnya. Saya belajar manage ekspektasi.")
    print()
    print("  💡 Latihan: siapkan 5 cerita STAR untuk wawancara!")
    print("  💡 Gunakan angka: \"menghemat 200 jam kerja\" > \"menghemat waktu\"")
    print()


# ============================================================
# [6] BUG BOUNTY PLATFORMS
# ============================================================
def bahas_bug_bounty():
    """Platform bug bounty dan cara memulainya."""
    print("[6] PLATFORM BUG BOUNTY")
    print("-" * 60)

    platforms = [
        ("HackerOne", "hackerone.com", "Program publik & private",
         "Signal, Reputation", "Apple, Google, GitHub, Twitter"),
        ("Bugcrowd", "bugcrowd.com", "Program publik & private",
         "Points, Rank, Badges", "Tesla, Spotify, Atlassian"),
        ("Synack", "synack.com", "Private (undangan saja)",
         "SRT coins, bounty", "US Gov, Fortune 500"),
        ("Intigriti", "intigriti.com", "Eropa focused",
         "Points, Badges", "KFC, Unity, Procter & Gamble"),
        ("YesWeHack", "yeswehack.com", "Eropa & Asia focused",
         "Badges, Hall of Fame", "Orange, TotalEnergies"),
        ("Open Bug Bounty", "openbugbounty.org", "Publik tanpa reward",
         "Hall of Fame", "Siapa saja (tanpa reward)"),
        ("BugBase", "bugbase.in", "India focused",
         "Points, Bounty", "Indian startups"),
    ]

    print(f"{'PLATFORM':<15} {'URL':<25} {'TIPE':<30} {'RANK SYSTEM':<25} {'KLIEN TERKENAL':<40}")
    print("-" * 135)
    for nama, url, tipe, rank, klien in platforms:
        print(f"{nama:<15} {url:<25} {tipe:<30} {rank:<25} {klien:<40}")

    print()
    print("  ┌─ TIPS MEMULAI BUG BOUNTY:")
    print("  │  1. Mulai dari program publik dengan scope web")
    print("  │  2. Cari low hanging fruit: XSS reflected, IDOR, open redirect")
    print("  │  3. Baca writeup bounty hunter lain untuk belajar teknik")
    print("  │  4. Gunakan tools: Burp Suite, nuclei, gf (patterns)")
    print("  │  5. Jangan gunakan scanner otomatis tanpa izin!")
    print("  │  6. Konsisten: 1-2 jam per hari > 8 jam seminggu sekali")
    print()


# ============================================================
# [7] CTF PLATFORMS
# ============================================================
def bahas_ctf():
    """Platform CTF untuk belajar dan berlatih."""
    print("[7] CTF PLATFORMS — Latihan & Kompetisi")
    print("-" * 60)

    print("  ┌─ PLATFORM CTF UNTUK LATIHAN:\n")

    ctf = [
        ("HackTheBox", "hackthebox.com",
         "VM lab (retired & active machines), challenges",
         "Free tier + VIP $14/bulan", "Machine of the month, writeup"),
        ("TryHackMe", "tryhackme.com",
         "Guided learning paths, rooms, CTF",
         "Free tier + VIP $10/bulan", "Tutorial banget → cocok pemula"),
        ("CTFtime", "ctftime.org",
         "Jadwal CTF global, team ranking",
         "Free", "Cari tim, ikut kompetisi tiap akhir pekan"),
        ("VulnHub", "vulnhub.com",
         "Download VM vulnerable, local play",
         "Free", "Boot2root classics (DC-1, Kioptrix)"),
        ("picoCTF", "picoctf.com",
         "Educational CTF untuk pelajar",
         "Free", "Pemula banget, materi lengkap"),
        ("Root-Me", "root-me.org",
         "Challenge by category (Web, Crypto, Stego)",
         "Free", "Bisa latihan per tema"),
        ("OverTheWire", "overthewire.org",
         "Wargames (Bandit, Leviathan, Natas)",
         "Free", "Best untuk belajar Linux & web dasar"),
    ]

    print(f"{'PLATFORM':<18} {'URL':<28} {'FITUR':<50} {'BIAYA':<25} {'CATATAN':<40}")
    print("-" * 161)
    for nama, url, fitur, biaya, catatan in ctf:
        print(f"{nama:<18} {url:<28} {fitur:<50} {biaya:<25} {catatan:<40}")

    print()
    print("  💡 START HERE:")
    print("     1. OverTheWire Bandit — dasar Linux & command line")
    print("     2. TryHackMe — guided learning path, super pemula friendly")
    print("     3. HackTheBox — setelah paham dasar, challange nyata")
    print("     4. CTFtime — ikut kompetisi, belajar dari tim lain")
    print()


# ============================================================
# [8] SOFT SKILLS
# ============================================================
def bahas_soft_skills():
    """Soft skills yang penting dalam cyber security."""
    print("[8] SOFT SKILLS — Bukan Cuma Teknis!")
    print("-" * 60)

    print("""
  ╔═══════════════════════════════════════════════════════════════╗
  ║  Teknis dapat belajar, soft skill butuh latihan bertahun2     ║
  ╚═══════════════════════════════════════════════════════════════╝\n""")

    soft = [
        ("Komunikasi", "Tertulis & Lisan",
         "Report writing, presentasi ke management non-teknis",
         "Latihan: tulis blog post teknikal, presentasi di meetup"),
        ("Report Writing", "Dokumentasi",
         "Buat temuan jelas: problem + bukti + solusi",
         "Gunakan template, sertakan screenshot & CVSS"),
        ("Manajemen Client", "Client-facing",
         "Manage ekspektasi, handle klien sulit",
         "Empati, transparan, proaktif update progres"),
        ("Time Management", "Organisasi",
         "Banyak scope, deadline ketat, prioritaskan critical",
         "Gunakan Trello/Notion, buat daily standup notes"),
        ("Teamwork", "Kolaborasi",
         "Share findings, peer review, knowledge transfer",
         "Pair programming, war room, blameless post-mortem"),
        ("Adaptability", "Pembelajaran",
         "Teknologi baru tiap hari, harus update terus",
         "Baca blog, ikut conference, hands-on lab"),
        ("Ethics", "Integritas",
         "Jangan abuse akses, jangan jual data",
         "Patuhi RoE, ceritakan kegagalan jujur"),
    ]

    print(f"{'SKILL':<20} {'KATEGORI':<18} {'PENJELASAN':<55} {'TIPS LATIHAN':<50}")
    print("-" * 143)
    for skill, kategori, penjelasan, tips in soft:
        print(f"{skill:<20} {kategori:<18} {penjelasan:<55} {tips:<50}")

    print()
    print("  🔥 Quote: \"Technical skills get you the interview,")
    print("     soft skills get you the job — and the promotion.\"")
    print()


# ============================================================
# [9] LAB SETUP
# ============================================================
def bahas_lab_setup():
    """Setup lab dengan budget terbatas."""
    print("[9] LAB SETUP — Budget-Friendly Options")
    print("-" * 60)

    print("""
  ┌─ OPSI SETUP LAB:
  │
  │  🟢 BUDGET MINIMAL (< $100):
  │  • Laptop bekas (ThinkPad X230/X240 — $50-80)
  │  • Linux (Ubuntu/Debian) + VirtualBox
  │  • VM vuln: Metasploitable 2 & 3, DVWA, VulnHub machines
  │  • Cloud: AWS Free Tier (EC2 t2.micro) — 12 bulan gratis
  │
  │  🟡 BUDGET MENENGAH ($200-500):
  │  • Laptop + 16GB RAM (minimal untuk multi VM)
  │  • Proxmox — hypervisor untuk multiple lab VMs
  │  • Active Directory lab: Windows Server eval + Windows 10
  │  • USB WiFi adapter: Alfa AWUS036ACH ($45)
  │  • VPS: DigitalOcean/Linode $5-10/bln untuk C2 server
  │
  │  🔴 BUDGET PROFESIONAL ($1000+):
  │  • Dedicated server: Dell PowerEdge R630 (ebay ~$300-500)
  │  • ESXi/vSphere homelab
  │  • Firewall: pfSense/OPNsense
  │  • Switch managed: Cisco SG250
  │  • NAS: TrueNAS untuk storage + backup
  │
  │  ☁️  OPSI CLOUD:
  │  • TryHackMe — $10/bulan (lab sudah siap!)
  │  • HackTheBox — VIP $14/bulan
  │  • PentesterLab — $20/bulan (web focused)
  │  • AWS/Azure/GCP — free tier (setup vulnerable infra)
  │
  │  📦 TOOLS WAJIB DI LAB:
  │  • Kali Linux (attacker)
  │  • Metasploitable 2 & 3 (target Linux)
  │  • Windows Server eval (AD domain controller)
  │  • Windows 10/11 eval (client)
  │  • pfsense (firewall)
  │  • Ubuntu Server (web server target)
  │"""


# ============================================================
# [10] COMMUNITY & NETWORKING
# ============================================================
def bahas_community():
    """Komunitas dan networking."""
    print("[10] COMMUNITY & NETWORKING")
    print("-" * 60)

    print("""
  ┌─ KOMUNITAS YANG HARUS DIJOIN:
  │
  │  🎯 TELEGRAM:
  │  • @cyberlawupdate — update hukum siber Indonesia
  │  • @linux_id — komunitas Linux Indonesia
  │  • @bugbounty_id — bug bounty hunters Indonesia
  │  • @kucing_keren — komunitas hacker Indonesia (terbesar!)
  │
  │  🎯 DISCORD:
  │  • HackTheBox Discord — diskusi machines & challenges
  │  • TryHackMe Discord — bantuan untuk room
  │  • NetSecFocus — job board & mentorship
  │
  │  🎯 MEETUP & CONFERENCE (Indonesia):
  • IDSECCONF — konferensi keamanan tahunan Jakarta
  • BCC (Bali Cyber Conference) — tahunan di Bali
  • ISC2 Chapter Indonesia — networking security professional
  • OWASP Chapter Indonesia — web security focus
  )
  │
  │  🎯 KONFERENSI INTERNASIONAL:
  • DEF CON — Las Vegas, konferensi hacker terbesar
  • Black Hat — US, Europe, Asia
  • BSides — komunitas lokal di seluruh dunia
  • RSA Conference — San Francisco (enterprise focus)
  • Hack.lu — Luxembourg (CTF & talks)
  │
  │  💡 NETWORKING TIPS:
  │  • Jangan malu bertanya di grup — semua pernah pemula
  │  • Share knowledge — bantu jawab pertanyaan orang lain
  │  • Ikut CTF tim — belajar kolaborasi & komunikasi
  │  • Hadiri meetup — face to face lebih berkesan
  │  • Jaga reputasi — jangan toxic, jangan sombong
  │""")


# ============================================================
# [11] SALARY NEGOTIATION
# ============================================================
def bahas_negosiasi():
    """Tips negosiasi gaji."""
    print("[11] SALARY NEGOTIATION TIPS")
    print("-" * 60)

    print("""
  ╔═══════════════════════════════════════════════════════════════╗
  ║  Yang tidak berani negosiasi rugi 10-30% dari potensi gaji!  ║
  ╚═══════════════════════════════════════════════════════════════╝\n""")

    print("  ┌─ ATURAN EMAS NEGOSIASI:")
    print("  │  1. JANGAN sebut angka pertama!")
    print("  │     • Tanya: \"Berapa range budget untuk posisi ini?\"")
    print("  │     • Atau: \"Saya flexible, tergantung total package\"")
    print("  │")
    print("  │  2. Riset pasar sebelum negosiasi:")
    print("  │     • Glassdoor, LinkedIn Salary, Levels.fyi")
    print("  │     • Tanya teman di industri (jika ada)")
    print("  │     • Sesuaikan dengan lokasi & industri")
    print("  │")
    print("  │  3. Jual VALUE bukan KEBUTUHAN:")
    print("  │     • \"Dengan OSCP & 3 tahun pengalaman, saya bisa...\"")
    print("  │     • \"Saya menemukan critical vuln senilai $50K di...\"")
    print("  │     • BUKAN \"Saya butuh gaji naik karena sewa naik\"")
    print("  │")
    print("  │  4. Negosiasi total package, bukan cuma gaji:")
    print("  │     • Bonus tahunan (%)")
    print("  │     • Stock options / ESOP")
    print("  │     • Sertifikasi budget ($5K+ per tahun)")
    print("  │     • Conference budget (DEF CON!)")
    print("  │     • Training & course reimbursement")
    print("  │     • WFH / remote allowance")
    print("  │     • Asuransi kesehatan & gigi")
    print("  │")
    print("  │  5. Timing:")
    print("  │     • Setelah offer diterima, SEBELUM tanda tangan")
    print("  │     • Jangan negosiasi di screening/HR awal")
    print("  │     • \"Saya tertarik dengan posisi ini...\"")
    print()
    print("  💡 Contoh script:")
    print("  \"Terima kasih untuk offer-nya. Saya sangat tertarik dengan")
    print("   posisi ini dan tim yang luar biasa. Dari riset saya,")
    print("   range untuk posisi ini dengan sertifikasi OSCP saya")
    print("   adalah 150-180jt. Apakah mungkin adjust ke 165jt?\"")
    print()


# ============================================================
# [12] CONTINUOUS LEARNING
# ============================================================
def bahas_continuous_learning():
    """Sumber belajar berkelanjutan."""
    print("[12] CONTINUOUS LEARNING — Tidak Pernah Berhenti")
    print("-" * 60)

    print("""
  🎧  PODCASTS:
  • Darknet Diaries — cerita hacker & incident nyata (WAJIB!)
  • Risky Business — weekly security news
  • Security Now — deep dive teknis
  • The CyberWire — daily news briefing
  • H4x0r Podcast — komunitas cyber Indonesia

  📚  BUKU WAJIB:
  • The Web Application Hacker's Handbook (Stuttard & Pinto)
  • Penetration Testing: A Hands-On Introduction to Hacking (Weidman)
  • The Hacker Playbook 3 (Kim)
  • Red Team Field Manual (RTFM — Ben Clark)
  • Blue Team Field Manual (BTFM — Alan White)
  • Social Engineering: The Art of Human Hacking (Hadnagy)
  • Ghost in the Wires (Kevin Mitnick)
  • Tribe of Hackers (Marcus J. Carey)

  🎥  YOUTUBE CHANNELS:
  • IppSec — walkthrough HackTheBox machines (BELAJAR!)
  • John Hammond — CTF, malware, edukasi
  • NetworkChuck — pemula friendly
  • The Cyber Mentor — pentest & bug bounty
  • STÖK — bug bounty focused
  • HackerSploit — red team & blue team
  • LiveOverflow — binary exploitation & CTF
  • NahamSec — bug bounty methodology
  • David Bombal — networking, Linux, hacking
  • InsiderPhD — academic & research security

  📰  BLOG & WEBSITE:
  • PortSwigger Research — web security research
  • Google Project Zero — 0-day research
  • SANS ISC — internet storm center
  • Krebs on Security — Brian Krebs' blog
  • The DFIR Report — forensics & IR case studies
  • PentesterLab blog — hands-on exercises
  • offensive security blog — kali & exploit

  🏫  COURSE PLATFORMS:
  • TCM Security Academy — Practical Ethical Hacking ($25)
  • Offensive Security — OSCP, OSEP, OSED ($999+)
  • SANS — gold standard training ($5000+)
  • Pluralsight — library lengkap ($29/bln)
  • Cybrary — free tier available
  • Udemy — beli pas diskon ($10-15/course)
  """)


# ============================================================
# [13] CEK KESIAPAN KARIR
# ============================================================
def cek_kesiapan_karir():
    """Cek kesiapan tools dan environment."""
    print("[13] CEK KESIAPAN LINGKUNGAN")
    print("-" * 60)

    print(f"  🖥  Hostname: {platform.node()}")
    print(f"  🐍 Python: {sys.version.split()[0]}")
    print(f"  📅 Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")

    print()
    print("  📋 CEK SKILL CHECKLIST:")
    checklist = [
        ("Python scripting", True),
        ("Linux command line", True),
        ("Basic networking", True),
        ("NMAP", subprocess.run(['which', 'nmap'], capture_output=True).returncode == 0),
        ("Metasploit", subprocess.run(['which', 'msfconsole'], capture_output=True).returncode == 0),
        ("Git", subprocess.run(['which', 'git'], capture_output=True).returncode == 0),
    ]

    for skill, status in checklist:
        if status:
            print(f"     ✅ {skill}")
        else:
            print(f"     ⬜ {skill} — perlu dipelajari / diinstall")

    print()
    print("  💡 Setelah Sesi 24 ini, Anda sudah punya fondasi:")
    print("     • Session 01-10: Dasar IT & Python")
    print("     • Session 11-15: Network & Web Security")
    print("     • Session 16-21: Exploitation & Defense")
    print("     • Session 22: Wireless Hacking")
    print("     • Session 23: PTES Standard (Metodologi Pentest)")
    print("     • Session 24: Career & Portfolio (Sekarang!)")
    print()


# ============================================================
# MAIN
# ============================================================
def main():
    banner()
    bahas_role_keamanan()

    print()
    bahas_level_karir()

    print()
    bahas_sertifikasi()

    print()
    bahas_portfolio()

    print()
    bahas_star_interview()

    print()
    bahas_bug_bounty()

    print()
    bahas_ctf()

    print()
    bahas_soft_skills()

    print()
    bahas_lab_setup()

    print()
    bahas_community()

    print()
    bahas_negosiasi()

    print()
    bahas_continuous_learning()

    print()
    cek_kesiapan_karir()

    # ============================================================
    # RECAP & LATIHAN
    # ============================================================
    print("=" * 60)
    print("  ✅ SESI 24 SELESAI!")
    print("  ✅ SELURUH ETIKA ELITE HACKER v11 SELESAI!")
    print("=" * 60)
    print()
    print("  👉 RECAP KARIR:")
    print("     • Role: Red 🔴, Blue 🔵, Purple 🟣, GRC 🟢, DFIR 🟡")
    print("     • Level: Entry (0-2th) → Mid (2-5th) → Senior (5+th)")
    print("     • Sertifikasi: Security+ → OSCP → OSEP → CISSP")
    print("     • Portfolio: GitHub + LinkedIn + Blog + CTF Writeup")
    print("     • Wawancara: Gunakan STAR (Situation, Task, Action, Result)")
    print("     • Bug Bounty: HackerOne, Bugcrowd, Intigriti")
    print("     • Latihan: HTB, THM, VulnHub, CTFtime")
    print("     • Soft skill: komunikasi, report writing, client mgmt")
    print("     • Negosiasi: Jangan sebut angka pertama! Riset pasar!")
    print("     • Continuous learning: podcast, buku, YouTube, course")
    print()
    print("  📌 LATIHAN LANJUTAN (AKHIR):")
    print("     1. Buat akun LinkedIn + GitHub — isi dengan project Kamu")
    print("     2. Tulis 1 CTF writeup (TryHackMe atau HackTheBox)")
    print("     3. Buat 1 blog post tentang topik keamanan yang Kamu kuasai")
    print("     4. Daftar di 1 bug bounty platform (HackerOne/Bugcrowd)")
    print("     5. Buat GitHub Pages portfolio site")
    print("     6. Cek sertifikasi: daftar Security+ atau langsung OSCP")
    print("     7. Ikut 1 CTF kompetisi di CTFtime")
    print("     8. Gabung minimal 2 komunitas keamanan (Telegram/Discord)")
    print("     9. Siapkan 5 cerita STAR untuk wawancara")
    print("    10. Rencanakan karir 1 tahun ke depan — target, sertif, lab")
    print()
    print("  💬 PESAN TERAKHIR:")
    print("  \"Knowledge is power, but only if you use it ethically.\"")
    print("  Anda sudah memiliki tools, teknik, dan metodologi.")
    print("  Sekarang: gunakan untuk kebaikan. Jadilah pahlawan siber, bukan penjahat.")
    print("  Selamat berkarir di dunia Cyber Security! 🚀🛡️")
    print()
    print("  ╔═══════════════════════════════════════════════════════════════╗")
    print("  ║  ETHICAL ELITE HACKER v11 — SELESAI!                        ║")
    print("  ║  Created by X-Code — Keep Learning, Keep Hacking!           ║")
    print("  ╚═══════════════════════════════════════════════════════════════╝")
    print()


if __name__ == '__main__':
    main()
