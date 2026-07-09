#!/usr/bin/env python3
"""Sesi 1: Networking Dasar - Cek jaringan & port"""
import socket, subprocess, os, struct

def banner():
    print("="*60)
    print("  SESI 1: PENGANTAR CYBER SECURITY & NETWORKING")
    print("  Analogi: Jaringan = SISTEM POS")
    print("  IP = alamat rumah, Port = pintu rumah")
    print("  Referensi: X-Code Ethical Elite Hacker v11")
    print("="*60)

def cek_ip():
    print("\n[1] IP ADDRESS")
    r = subprocess.run(["hostname", "-I"], capture_output=True, text=True)
    ips = r.stdout.strip().split()
    for i, ip in enumerate(ips):
        print(f"  IP #{i+1}: {ip}")
    print("  💡 IP = alamat rumah di jaringan")

def cek_mac():
    print("\n[2] MAC ADDRESS (Hardware ID)")
    for iface in ["eth0", "ens5", "wlan0"]:
        try:
            with open(f"/sys/class/net/{iface}/address") as f:
                mac = f.read().strip()
                print(f"  {iface}: {mac}")
        except:
            pass
    print("  💡 MAC = ID unik kartu jaringan (seperti NIK perangkat)")

def cek_port_buka():
    print("\n[3] PORT TERBUKA (LISTEN)")
    port_name = {22: "SSH", 80: "HTTP", 443: "HTTPS", 8080: "HTTP-Alt",
                 3306: "MySQL", 21: "FTP", 25: "SMTP", 53: "DNS", 3389: "RDP"}
    try:
        with open("/proc/net/tcp") as f:
            lines = f.readlines()[1:]
        ports = []
        for line in lines:
            parts = line.split()
            if len(parts) >= 4:
                port_hex = parts[1].split(":")[1]
                port = int(port_hex, 16)
                state = parts[3]
                if state == "0A":
                    ports.append(port)
        for p in sorted(ports):
            nama = port_name.get(p, "?")
            print(f"  Port {p:5} ({nama:15}) — TERBUKA ✅")
    except:
        print("  (tidak bisa akses /proc/net/tcp)")
    print("  💡 Port = pintu rumah. Buka = layanan siap melayani")

def cek_dns():
    print("\n[4] CEK DNS (Domain → IP Address)")
    for site in ["google.com", "github.com", "xcode.or.id"]:
        r = subprocess.run(["getent", "hosts", site], capture_output=True, text=True)
        ips = [l.split()[0] for l in r.stdout.strip().splitlines() if l.strip()]
        if ips:
            print(f"  {site:15} → {', '.join(ips[:2])}")
        else:
            print(f"  {site:15} → GAGAL")
    print("  💡 DNS = buku telepon internet")

def cek_gateway():
    print("\n[5] GATEWAY (Pintu ke Internet)")
    try:
        with open("/proc/net/route") as f:
            for line in f.readlines()[1:]:
                parts = line.split()
                if parts[1] == "00000000":
                    gw_bytes = bytes.fromhex(parts[2])
                    gw_ip = socket.inet_ntoa(gw_bytes)
                    print(f"  Gateway: {gw_ip} (via {parts[0]})")
                    print(f"  💡 Gateway = pintu pos utama ke luar")
                    break
    except:
        print("  (tidak bisa baca routing)")

def osi_layer():
    print("\n[6] OSI 7 LAYER")
    print("  📦 Proses data dari aplikasi sampai kabel:")
    print(f"  {'Layer':<8} {'Nama':<16} {'Contoh':<20} {'Analogi'}")
    print(f"  {'-'*55}")
    for l, n, c, a in [
        ("7", "Application", "HTTP, FTP, DNS", "Browser"),
        ("6", "Presentation", "SSL/TLS", "Enkripsi"),
        ("5", "Session", "Session", "Login"),
        ("4", "Transport", "TCP/UDP", "TCP=ngantre, UDP=lempar"),
        ("3", "Network", "IP, Routing", "Router atur jalur"),
        ("2", "Data Link", "MAC, Switch", "Switch kirim ke MAC"),
        ("1", "Physical", "Kabel, WiFi", "Sinyal listrik"),
    ]:
        print(f"  {l:<8} {n:<16} {c:<20} {a}")

def protokol():
    print("\n[7] PROTOKOL JARINGAN & PORT")
    print(f"  {'Protokol':<18} {'Port':<10} {'Fungsi':<20} {'Analogi'}")
    print(f"  {'-'*58}")
    for p, port, fungsi, analogi in [
        ("HTTP", "80", "Web", "Browsing biasa"),
        ("HTTPS", "443", "Web Aman", "+ SSL/TLS"),
        ("FTP", "21", "Transfer File", "Upload file"),
        ("SSH", "22", "Remote Aman", "Akses server"),
        ("DNS", "53", "Domain→IP", "Buku telepon"),
        ("DHCP", "67-68", "IP Otomatis", "Dapet IP dari router"),
        ("SMB", "445", "File Sharing", "Berbagi file"),
        ("SMTP", "25", "Kirim Email", "Pos surat"),
        ("POP3", "110", "Terima Email", "Ambil surat"),
        ("Telnet", "23", "Remote (Lama)", "Tidak aman"),
        ("RDP", "3389", "Remote Windows", "Remote Dekstop"),
    ]:
        print(f"  {p:<18} {port:<10} {fungsi:<20} {analogi}")

def red_blue():
    print("\n[8] TIM KEAMANAN")
    print("  🔴 Red Team   = Hacker Etis (nyerang, cari celah)")
    print("  🔵 Blue Team  = Defender (jagain, pantau, tangkis)")
    print("  🟣 Purple Team = Kerjasama Red + Blue")
    print("  🏢 SOC Analyst = Monitor 24/7, respon insiden")
    print("  🎯 Penetration Tester = Ethical Hacker profesional")
    print()
    print("  📋 Skill Wajib: Networking, Linux, Programming, Security Tools")
    print("  📋 Metodologi: PTES (Penetration Testing Execution Standard)")
    print("  📋 Alur: Intel → Threat Model → Vuln Analysis → Exploit → Report")

def scan_port(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    r = s.connect_ex((host, port))
    s.close()
    return r == 0

def extra_scan():
    print("\n[9] SCAN PORT KE TARGET EKSTERNAL")
    targets = [("google.com", 80), ("google.com", 443), ("github.com", 443)]
    for host, port in targets:
        try:
            ip = socket.gethostbyname(host)
            status = "TERBUKA ✅" if scan_port(ip, port) else "Tertutup ❌"
            print(f"  {host:15} port {port:5} → {status}")
        except:
            print(f"  {host:15} port {port:5} → GAGAL resolve")

def main():
    banner()
    cek_ip()
    cek_mac()
    cek_port_buka()
    cek_dns()
    cek_gateway()
    osi_layer()
    protokol()
    red_blue()
    extra_scan()
    print("\n" + "="*60)
    print("  ✅ SESI 1: PENGANTAR CYBER SECURITY & NETWORKING")
    print("  👉 Materi: IP, MAC, port, DNS, gateway, OSI Layer")
    print("  👉 Tim: Red Team (nyerang), Blue Team (bertahan)")
    print("  👉 Protokol: HTTP, SSH, DNS, FTP, SMB, SMTP, dll")
    print()
    print("  📌 LANJUTAN: Subnetting (/24, /16, CIDR)")
    print("  📌 LANJUTAN: ARP, Routing (NAT), VPN, DMZ")
    print("  📌 LANJUTAN: Praktek baca hexdump & magic number file")
    print("="*60)

if __name__ == "__main__":
    main()
