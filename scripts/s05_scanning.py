#!/usr/bin/env python3
"""Sesi 5: Scanning Jaringan & Port dengan Python"""
import socket, sys
from datetime import datetime

def banner():
    print("="*60)
    print("  SESI 5: SCANNING JARINGAN")
    print("  Analogi: SATPAM keliling gedung")
    print("="*60)

def scan_port(host, port, timeout=1):
    """Cek port dengan TCP connect scan"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        result = s.connect_ex((host, port))
        s.close()
        return result == 0, "Terbuka" if result == 0 else "Tertutup"
    except:
        return False, "Error"

def scan_ports(host, ports):
    print(f"\n[1] SCAN PORT DI {host}")
    print(f"  Waktu: {datetime.now().strftime('%H:%M:%S')}")
    print(f"  {'Port':<8} {'Service':<15} {'Status'}")
    print(f"  {'-'*40}")
    
    services = {22:"SSH", 21:"FTP", 23:"Telnet", 25:"SMTP",
                53:"DNS", 80:"HTTP", 110:"POP3", 143:"IMAP",
                443:"HTTPS", 445:"SMB", 3306:"MySQL", 3389:"RDP",
                5432:"PostgreSQL", 5900:"VNC", 6379:"Redis", 8080:"HTTP-Alt",
                8443:"HTTPS-Alt", 27017:"MongoDB"}
    
    for port in ports:
        open_status, status = scan_port(host, port)
        service = services.get(port, "Unknown")
        marker = "🔓" if open_status else "  "
        print(f"  {marker} {port:<5} {service:<15} {status}")

def scan_localhost():
    print("\n[2] SCAN LOCALHOST (127.0.0.1)")
    common_ports = [22, 80, 443, 3306, 8080, 8000, 5000, 3000]
    scan_ports("127.0.0.1", common_ports)

def os_detect():
    print("\n[3] INFO SISTEM")
    import platform
    print(f"  OS: {platform.system()} {platform.release()}")
    print(f"  Hostname: {socket.gethostname()}")
    try:
        ip = socket.gethostbyname(socket.gethostname())
        print(f"  IP: {ip}")
    except:
        pass

def main():
    banner()
    os_detect()
    scan_localhost()
    print("\n" + "="*60)
    print("  LATIHAN:")
    print("  1. Ganti target IP scan (contoh: 192.168.1.1)")
    print("  2. Tambah port lain ke daftar")
    print("  3. Coba scan dengan timeout berbeda")
    print("="*60)

if __name__ == "__main__":
    main()
