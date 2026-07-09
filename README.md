# 🛡️ Ethical Elite Hacker v11 — Panduan Lengkap

**24 Sesi Belajar Ethical Hacking dari NOL sampai MAHIR**  
Dibuat oleh **X-Code Training** 🇮🇩

---

## 📋 Deskripsi

Ethical Elite Hacker v11 adalah kurikulum belajar **ethical hacking** komprehensif dalam 24 sesi. Setiap sesi berisi **skrip Python interaktif** yang bisa langsung dijalankan, lengkap dengan:

- 📖 **Materi teori** — Analogi & penjelasan sederhana
- 🛠️ **Praktik langsung** — Command & tools real
- 🩺 **Keamanan & mitigasi** — Cara melindungi sistem

Dari dasar jaringan, kriptografi, scanning, eksploitasi web, wireless, sampai karir profesional — semuanya **gratis, open source, bahasa Indonesia**.

---

## 📁 Struktur Folder

```
ethical_elite_hacker_v11/
├── 📜 README.md              ← File ini — panduan utama
├── 📦 sesi_data.json         ← Data 24 sesi (materi, praktik, mitigasi)
├── 📁 scripts/               ← Skrip Python siap jalan (22 file, ~11.006 baris)
│   ├── s01_networking_dasar.py
│   ├── s02_kriptografi.py
│   ├── s03_virtualisasi.py
│   ├── s03_linux_dasar.py
│   ├── s04_server_setup.py
│   ├── s05_scanning.py
│   ├── s06_network_hacking.py
│   ├── s07_nessus_metasploit.py
│   ├── s08_buffer_overflow.py
│   ├── s09_linux_advanced.py
│   ├── s10_wazuh_siem.py
│   ├── s11_web_gathering.py
│   ├── s12_owasp_part1.py
│   ├── s13_owasp_part2.py
│   ├── s14_xss_demo.py
│   ├── s15_file_inclusion.py
│   ├── s16_idor_upload_cmdi.py
│   ├── s17_sqli_manual.py
│   ├── s18_sqlmap_waf.py
│   ├── s19_api_pentesting.py
│   ├── s20_node_php_hardening.py
│   ├── s21_privesc.py
│   ├── s22_wireless_hacking.py
│   ├── s23_ptes_standard.py
│   └── s24_career_portfolio.py
└── 📁 panduan/               ← (opsional) Materi tambahan
```

> **Total:** 22 file skrip Python | **~11.006 baris kode**

---

## 📊 Tabel 24 Sesi

| # | Nama Sesi | 📄 Baris | 🎯 Level |
|:-:|:----------|:--------:|:--------:|
| 1 | Pengantar Cyber Security & Networking | 169 | 🟢 |
| 2 | Kriptografi & TOR | 167 | 🟢 |
| 3 | VirtualBox, Docker & Linux Dasar | 188 | 🟢 |
| 3b | Linux Dasar — Command Line | 188 | 🟢 |
| 4 | Linux/BSD Server Setup | 228 | 🟢 |
| 5 | Kali Linux & Tools — Scanning | 222 | 🟢 |
| 6 | Network Hacking — SMB, EternalBlue, MikroTik | 296 | 🟡 |
| 7 | Nessus & Metasploit Framework | 170 | 🟡 |
| 8 | Buffer Overflow Exploit | 283 | 🟡 |
| 9 | Linux Server Advanced — ARP, DoS, GDB, ROP | 363 | 🟡 |
| 10 | Wazuh SIEM — Security Information & Event Mgmt | 368 | 🟡 |
| 11 | Web Information Gathering — OSINT, Shodan | 457 | 🟡 |
| 12 | OWASP Top 10 Bagian 1 (A1–A5) | 406 | 🔴 |
| 13 | OWASP Top 10 Bagian 2 (A6–A10) | 465 | 🔴 |
| 14 | XSS Cross-Site Scripting | 490 | 🔴 |
| 15 | File Inclusion — LFI & RFI | 410 | 🔴 |
| 16 | IDOR, Upload & Command Injection | 392 | 🔴 |
| 17 | SQL Injection Manual | 556 | 🔴 |
| 18 | SQLMAP & WAF Bypass | 512 | 🔴 |
| 19 | API Pentesting | 666 | ⚫ |
| 20 | Node.js & PHP Hardening | 789 | ⚫ |
| 21 | Privilege Escalation & Incident Response | 1.059 | ⚫ |
| 22 | Wireless Hacking — WiFi, WPA, Evil Twin | 673 | ⚫ |
| 23 | PTES Standard — 7 Fase Pentest Profesional | 751 | ⚫ |
| 24 | Career & Portfolio — Red/Blue/Purple Team | 738 | ⚫ |

### 🎯 Legend Level

| Level | Rentang Sesi | Emoji | Deskripsi |
|:-----:|:------------:|:-----:|:----------|
| **Pemula** | 1–6 | 🟢 | Dasar jaringan, Linux, tools, setup |
| **Menengah** | 7–13 | 🟡 | Vulnerability scanning, exploit, SIEM, OSINT |
| **Advance** | 14–19 | 🔴 | Web security: XSS, SQLi, API, WAF bypass |
| **Expert** | 20–24 | ⚫ | Hardening, privesc, wireless, pentest metodologi |

---

## 🚀 Cara Pakai

### 1. Clone atau Download Project

```bash
git clone https://github.com/x-code/ethical-elite-hacker-v11.git
cd ethical-elite-hacker-v11
```

### 2. Jalankan Skrip Secara Berurutan

Setiap skrip berdiri sendiri — jalankan dengan Python 3:

```bash
# Contoh: Sesi 1 — Networking Dasar
python3 scripts/s01_networking_dasar.py

# Sesi 2 — Kriptografi
python3 scripts/s02_kriptografi.py

# Sesi 5 — Scanning Tools
python3 scripts/s05_scanning.py

# Sesi 14 — XSS Demo
python3 scripts/s14_xss_demo.py

# Sesi 23 — PTES Standard (7 Fase Pentest)
python3 scripts/s23_ptes_standard.py

# Sesi 24 — Career & Portfolio
python3 scripts/s24_career_portfolio.py
```

### 3. Rekomendasi Belajar

| Langkah | Aktivitas |
|:-------:|:----------|
| 1️⃣ | Pelajari **Sesi 1–6** (Pemula) — Networking, Linux, Tools |
| 2️⃣ | Lanjut ke **Sesi 7–13** (Menengah) — Scanning, Exploit, SIEM |
| 3️⃣ | Kuasai **Sesi 14–19** (Advance) — Web Security & API |
| 4️⃣ | Taklukkan **Sesi 20–24** (Expert) — Hardening, Wireless, Karir |

> 💡 **Tips:** Buat lab virtual (VirtualBox/Docker) untuk praktik aman. Jangan pernah scan/exploit server tanpa izin!

---

## 🏗️ Progres Level

### 🟢 Level Pemula (Sesi 1–6)
**Dasar-dasar yang wajib dikuasai:**
- IP, MAC, Port, DNS, OSI Layer
- Encoding, Enkripsi, Hash, RSA, TOR
- VirtualBox, Docker, Linux Command Line
- Setup Server (Apache, Nginx, MySQL, DNS)
- Kali Linux, Nmap, Metasploit, Searchsploit
- Network Hacking (SMB, EternalBlue, FTP, MikroTik)

### 🟡 Level Menengah (Sesi 7–13)
**Exploitasi & pemahaman sistem:**
- Nessus/OpenVAS Vulnerability Scanning
- Metasploit Architecture & msfvenom Payload
- Buffer Overflow — Fuzzing, EIP, ROP Chain
- ARP Spoofing, DoS, GDB Debugging
- Wazuh SIEM — Log Analysis, Detection Rules
- Web Information Gathering — OSINT, Shodan, Google Dorking
- OWASP Top 10 (A1–A10) Lengkap

### 🔴 Level Advance (Sesi 14–19)
**Keamanan web & aplikasi:**
- XSS — Reflected, Stored, DOM, CSP
- LFI & RFI — Path Traversal, Log Poisoning
- IDOR, File Upload Webshell, Command Injection
- SQL Injection Manual — Tautology, UNION, Blind
- SQLMAP & WAF Bypass — ModSecurity, Tamper
- API Pentesting — JWT, CORS, Rate Limiting

### ⚫ Level Expert (Sesi 20–24)
**Hardening, metodologi & karir:**
- Node.js & PHP Hardening — Disable Functions, Bypass
- Privilege Escalation — SUID, Kernel Exploit, Windows
- Wireless Hacking — WPA, Evil Twin, PMKID
- PTES Standard — 7 Fase Pentest Profesional
- Career & Portfolio — Red/Blue/Purple Team, Sertifikasi

---

## 🧪 Contoh Output Skrip

Jalankan sesi pertama untuk melihat gambaran materi:

```bash
$ python3 scripts/s01_networking_dasar.py

============================================================
  SESI 1: PENGANTAR CYBER SECURITY & NETWORKING
  Analogi: Jaringan = SISTEM POS
  IP = alamat rumah, Port = pintu rumah
  Referensi: X-Code Ethical Elite Hacker v11
============================================================

[1] IP ADDRESS
  IP #1: 192.168.1.10
  💡 IP = alamat rumah di jaringan

[2] MAC ADDRESS (Hardware ID)
  eth0: 00:1a:2b:3c:4d:5e
  💡 MAC = ID unik kartu jaringan (seperti NIK perangkat)

[3] PORT TERBUKA (LISTEN)
  Port 22 (SSH)    → LISTEN
  Port 80 (HTTP)   → LISTEN
  💡 Port = pintu rumah. Semakin banyak terbuka, semakin besar risiko!
```

---

## 🧠 Metodologi Pembelajaran

Setiap skrip mengikuti format standar:

```
┌─────────────────────────────────────────────┐
│  BANNER — Judul & Analogi                   │
├─────────────────────────────────────────────┤
│  📖 MATERI — Penjelasan konsep & analogi    │
│  🔧 PRAKTIK — Command & tools real          │
│  🩺 MITIGASI — Cara melindungi sistem       │
├─────────────────────────────────────────────┤
│  💬 PESAN — Kesimpulan & motivasi           │
└─────────────────────────────────────────────┘
```

---

## ⚠️ Disclaimer

> **Materi ini ditujukan untuk PEMBELAJARAN & EDUKASI SAH.**
>
> 🚫 **Jangan pernah** menggunakan teknik di sini untuk:
> - Meretas sistem tanpa izin tertulis
> - Mencuri data atau merusak infrastruktur
> - Melakukan aktivitas ilegal & melanggar hukum
>
> ✅ **Gunakan untuk:**
> - Belajar & riset keamanan siber
> - Bug bounty & pentest resmi (dengan izin)
> - Melindungi sistem & jaringan sendiri
>
> **Pelanggaran hukum adalah tanggung jawab pribadi Anda.**
> Penulis & kontributor tidak bertanggung jawab atas penyalahgunaan.

---

## 🛠️ Tools yang Digunakan

| Kategori | Tools |
|:---------|:------|
| 📡 Networking | `nmap`, `netcat`, `tcpdump`, `hping3` |
| 🔐 Kriptografi | `openssl`, `base64`, `hashlib` |
| 🐧 Linux | `bash`, `gdb`, `arpspoof` |
| 🌐 Web | `curl`, `sqlmap`, `gobuster`, `ffuf`, `wafw00f` |
| 💥 Exploit | `Metasploit`, `msfvenom`, `searchsploit` |
| 🛡️ Defense | `Wazuh`, `ModSecurity`, `UFW`, `CSP` |
| 📶 Wireless | `aircrack-ng`, `reaver`, `hcxdumptool` |

---

## 🎓 Sertifikasi Terkait

Siap uji kemampuan? Sertifikasi ini relevan:

| Level | Sertifikasi | Fokus |
|:-----:|:------------|:------|
| 🟢 | **eJPT**, **CEH** | Entry-level penetration testing |
| 🟡 | **PNPT**, **OSCP** | Practical pentest & exploit |
| 🔴 | **OSEP**, **CRTO** | Advanced evasion & adversary simulation |
| ⚫ | **CISSP**, **GCIA**, **GCIH** | Blue team, defense, management |

---

## 👏 Credits

```
╔══════════════════════════════════════════════════════╗
║  ETHICAL ELITE HACKER v11                            ║
║  Created by X-Code Training 🇮🇩                      ║
║  Kurikulum & Skrip oleh Tim X-Code                   ║
║                                                      ║
║  "Keep Learning, Keep Hacking — Use It Wisely!"      ║
╚══════════════════════════════════════════════════════╝
```

---

## 📬 Kontak & Komunitas

- 🌐 **Website:** https://x-code.dev
- 💬 **Telegram:** @XCodeCommunity
- 🐙 **GitHub:** https://github.com/x-code
- 📧 **Email:** training@x-code.dev

---

⭐ **Bintang di GitHub kalau bermanfaat!**  
🐛 **Laporkan issue atau pull request untuk kontribusi!**

---
*© 2025 X-Code Training — Ethical Elite Hacker v11*
