#!/usr/bin/env python3
"""Sesi 5: Kali Linux & Tools — Scanning Jaringan & Eksploitasi"""
import socket, subprocess, shutil, os, struct
from datetime import datetime

def banner():
    print("="*60)
    print("  SESI 5: KALI LINUX & TOOLS SCANNING")
    print("  Analogi: KOTAK ALAT TUKANG")
    print("  — Kali Linux = kotak perkakas lengkap tukang (hacker)")
    print("  — Nmap = meteran buat ukur pintu & jendela (scan port)")
    print("  — Metasploit = bor listrik buat bobol (exploit framework)")
    print("  Referensi: X-Code Ethical Elite Hacker v11")
    print("="*60)

def cek_kali():
    print("\n[1] CEK KALI LINUX / DISTRO")
    try:
        with open("/etc/os-release") as f:
            data = f.read()
        if "kali" in data.lower():
            print("  ✅ KALI LINUX terdeteksi! 🏆")
        elif "ubuntu" in data.lower():
            print("  ℹ️  Ubuntu terdeteksi (bukan Kali, tapi tetap bisa belajar)")
        elif "debian" in data.lower():
            print("  ℹ️  Debian terdeteksi (mirip Kali, cocok untuk belajar)")
        else:
            print("  ℹ️  Distro lain terdeteksi")
    except:
        print("  ℹ️  Tidak bisa deteksi distro")
    print("  💡 Kali Linux = OS khusus penetration testing, pre-installed 600+ tools")
    print("  💡 Alternatif: Parrot OS, BlackArch, Ubuntu + tools manual")

def cek_tools_hacker():
    print("\n[2] CEK TOOLS HACKER (Nmap, Metasploit, Searchsploit, dll)")
    tools = {
        "nmap":        ("🌐 Nmap", "Network Mapper — scan port, OS detection, service version"),
        "msfconsole":  ("💀 Metasploit", "Exploit framework — cari & jalankan exploit"),
        "searchsploit":("📚 Searchsploit", "Database exploit lokal (offline Exploit-DB)"),
        "hydra":       ("🔑 Hydra", "Brute force password (SSH, FTP, HTTP, dll)"),
        "john":        ("🔐 John the Ripper", "Crack password hash offline"),
        "sqlmap":      ("🗄️ SQLmap", "Auto SQL Injection detection & exploitation"),
        "burpsuite":   ("🕷️ Burp Suite", "Web proxy buat intercept & modifikasi request"),
        "wireshark":   ("📡 Wireshark", "Packet sniffer & network traffic analyzer"),
        "aircrack-ng": ("📶 Aircrack-ng", "WiFi hacking suite (monitor, crack WPA/WEP)"),
        "whatweb":     ("🕸️ WhatWeb", "Fingerprint teknologi website (CMS, framework)"),
        "nikto":       ("🧹 Nikto", "Web server vulnerability scanner"),
        "gobuster":    ("💥 Gobuster", "Directory/file/subdomain brute force"),
        "responder":   ("🎣 Responder", "LLMNR/NBT-NS poisoning — intercept credentials"),
        "bettercap":   ("🧢 Bettercap", "MITM framework — sniff, inject, redirect"),
        "routersploit":("🔌 RouterSploit", "Exploit khusus perangkat jaringan (router, IoT)"),
    }
    print(f"  {'Tool':<20} {'Status':<30} {'Keterangan'}")
    print(f"  {'-'*75}")
    for tool, (emoji_name, desc) in sorted(tools.items()):
        ada = shutil.which(tool)
        status = "✅ SIAP" if ada else "❌ TIDAK ADA"
        marker = "✅" if ada else "⬜"
        print(f"  {marker} {emoji_name:<18} {status:<30} {desc}")

def nmap_scan_simulasi():
    print("\n[3] SIMULASI NMAP SCAN")
    nmap = shutil.which("nmap")
    if nmap:
        target = "127.0.0.1"
        print(f"  🔍 Menjalankan nmap -sS -A -T4 {target} (scan cepat localhost)...")
        r = subprocess.run(
            ["nmap", "-sS", "-A", "-T4", "-p", "22,80,443,3306,8080", target],
            capture_output=True, text=True, timeout=30
        )
        if r.stdout.strip():
            for line in r.stdout.strip().splitlines():
                print(f"     {line}")
        else:
            print(f"     (stderr) {r.stderr.strip()}")
        print("  💡 -sS = SYN scan (stealth) | -A = deteksi OS + service")
        print("  💡 -T4 = kecepatan agresif | -p = port tertentu")
    else:
        print("  ❌ Nmap tidak terinstall. Install: sudo apt install nmap")
        print("  💡 Contoh perintah nmap yang sering dipakai:")
        print("     nmap -sn 192.168.1.0/24       → ping sweep (cari host hidup)")
        print("     nmap -sS 192.168.1.1           → SYN scan port umum")
        print("     nmap -sV 192.168.1.1           → deteksi versi service")
        print("     nmap -O 192.168.1.1            → deteksi OS")
        print("     nmap -A 192.168.1.1            → agresif (OS + versi + script)")
        print("     nmap --script vuln 192.168.1.1 → scan kerentanan")
        print("     nmap -p- 192.168.1.1           → scan SEMUA port (65.535)")

def searchsploit():
    print("\n[4] SEARCHSPLOIT — DATABASE EXPLOIT")
    ss = shutil.which("searchsploit")
    if ss:
        # Search for a known vulnerability
        r = subprocess.run([ss, "eternalblue"], capture_output=True, text=True, timeout=10)
        out = r.stdout.strip() or r.stderr.strip()
        if "Exploit Title" in out:
            print("  ✅ Searchsploit berfungsi! Pencarian 'eternalblue':")
            lines = out.splitlines()
            # Show header + first few results
            for line in lines[:12]:
                print(f"     {line}")
            if len(lines) > 12:
                print(f"     ... ({len(lines) - 12} hasil lainnya)")
        else:
            print(f"  ℹ️  Searchsploit output:\n{out[:500]}")
    else:
        print("  ❌ Searchsploit tidak terinstall (paket: exploitdb)")
        print("  💡 Install: sudo apt install exploitdb")
        print("  💡 Atau buka online: https://www.exploit-db.com/")
    print("  🔥 Searchsploit = database exploit OFFLINE, bisa dipake tanpa internet!")

def metasploit_check():
    print("\n[5] METASPLOIT FRAMEWORK")
    msf = shutil.which("msfconsole")
    if msf:
        print("  ✅ Metasploit framework terinstall!")
        r = subprocess.run(["msfconsole", "--version"], capture_output=True, text=True, timeout=10)
        print(f"     {r.stdout.strip() or r.stderr.strip()}")
    else:
        print("  ❌ msfconsole tidak ditemukan")
        print("  💡 Install: curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall && chmod +x msfinstall && ./msfinstall")

    print("\n  📋 Arsitektur Metasploit:")
    print(f"  {'Komponen':<20} {'Fungsi'}")
    print(f"  {'-'*50}")
    print(f"  {'msfconsole':<20} Main CLI interface")
    print(f"  {'msfdb':<20} Database backend (PostgreSQL)")
    print(f"  {'exploit/':<20} Folder exploit (windows/, linux/, webapp/, dll)")
    print(f"  {'payload/':<20} Payload (reverse shell, bind shell, meterpreter)")
    print(f"  {'auxiliary/':<20} Scanner, fuzzer, DoS (bukan exploit)")
    print(f"  {'post/':<20} Post-exploitation module")
    print(f"  {'encoder/':<20} Encode payload biar lolos antivirus")
    print()
    print("  💡 Alur dasar Metasploit:")
    print("     use exploit/...")
    print("     set RHOSTS <target>")
    print("     set PAYLOAD ...")
    print("     exploit")

def routersploit_check():
    print("\n[6] ROUTERSPLOIT — EXPLOIT ROUTER & IoT")
    rs = shutil.which("routersploit") or shutil.which("rsf.py")
    if rs:
        print("  ✅ RouterSploit terdeteksi!")
    else:
        print("  ❌ RouterSploit tidak terinstall")
        print("  💡 Install: git clone https://github.com/threat9/routersploit.git")
        print("     cd routersploit && python3 -m pip install -r requirements.txt")
        print("     python3 rsf.py")
    print("  🔥 RouterSploit khusus buat bobol router, CCTV, perangkat IoT")
    print("  📋 Module terkenal: rce, creds, scanners, exploits")

def password_grabbing():
    print("\n[7] PASSWORD GRABBING — KONSEP & DEMO")
    print("  🔑 Teknik mengambil password (legal hanya di lab sendiri!):")

    teknik = [
        ("Sniffing HTTP",      "Tangkap password dari traffic HTTP (plain text) pakai Wireshark/tcpdump"),
        ("MITM (ARP Spoof)",   "Palsukan ARP, jadi 'orang tengah' antara korban & gateway"),
        ("Phishing",           "Buat halaman login palsu (Social Engineering Toolkit / SET)"),
        ("Keylogger",          "Rekam semua ketikan korban (hardware atau software)"),
        ("Hash Dumping",       "Ekstrak hash password dari SAM (Windows) / /etc/shadow (Linux)"),
        ("Brute Force",        "Coba jutaan kombinasi password (Hydra, John, Hashcat)"),
        ("Credential Stuffing","Gunakan username:password bocor dari breach lain"),
        ("LLMNR Poisoning",    "Responder — intercept hash NTLMv2 dari jaringan Windows"),
    ]
    print(f"  {'Teknik':<25} {'Cara Kerja'}")
    print(f"  {'-'*65}")
    for teknik, cara in teknik:
        print(f"  🔸 {teknik:<23} {cara}")

def port_scan_real():
    print("\n[8] REAL PORT SCAN (localhost)")
    services = {22:"SSH", 80:"HTTP", 443:"HTTPS", 3306:"MySQL", 8080:"HTTP-Alt",
                21:"FTP", 23:"Telnet", 25:"SMTP", 53:"DNS", 445:"SMB",
                3389:"RDP", 5900:"VNC", 6379:"Redis", 5432:"PostgreSQL"}
    target = "127.0.0.1"
    print(f"  🔍 Scanning {target} untuk port umum...")
    print(f"  {'Port':<8} {'Service':<18} {'Status'}")
    print(f"  {'-'*45}")
    for port, svc in sorted(services.items()):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            result = s.connect_ex((target, port))
            s.close()
            if result == 0:
                print(f"  🔓 {port:<5} {svc:<18} ✅ TERBUKA")
        except:
            pass
    print("  💡 TCP Connect Scan = 3-way handshake lengkap (tidak stealth)")

def main():
    banner()
    cek_kali()
    cek_tools_hacker()
    nmap_scan_simulasi()
    searchsploit()
    metasploit_check()
    routersploit_check()
    password_grabbing()
    port_scan_real()
    print("\n" + "="*60)
    print("  ✅ SESI 5 SELESAI!")
    print("  👉 Kali Linux = kotak alat lengkap ethical hacker")
    print("  👉 Nmap = tool paling fundamental untuk reconnaisance")
    print("  👉 Metasploit = framework exploit paling populer")
    print("  👉 Searchsploit = database exploit offline (Exploit-DB)")
    print("  👉 RouterSploit = exploit khusus router & IoT")
    print("  👉 Password grabbing = teknik mengambil kredensial korban")
    print()
    print("  📌 LATIHAN LANJUTAN:")
    print("  1. Scan jaringan lokal: nmap -sn 192.168.1.0/24")
    print("  2. Scan port dengan service version: nmap -sV 192.168.1.1")
    print("  3. Cari exploit: searchsploit apache 2.4.49")
    print("  4. Jalankan msfconsole & cari module: search eternalblue")
    print("  5. Clone RouterSploit & eksplorasi module-nya")
    print("  6. Praktek Hydra: hydra -l admin -P wordlist.txt ssh://target")
    print("="*60)

if __name__ == "__main__":
    main()
