#!/usr/bin/env python3
"""Sesi 1: Networking Dasar - Cek jaringan & port"""
import socket, subprocess, sys

def banner():
    print("="*60)
    print("  SESI 1: CEK JARINGAN & PORT")
    print("  Analogi: Jaringan = SISTEM POS")
    print("  IP = alamat rumah, Port = pintu rumah")
    print("="*60)

def cek_ip():
    print("\n[1] CEK IP ADDRESS")
    import subprocess
    try:
        r = subprocess.run(["hostname", "-I"], capture_output=True, text=True)
        ip = r.stdout.strip().split()[0] if r.stdout.strip() else "N/A"
        print(f"  IP lokal: {ip}")
    except:
        print("  IP lokal: N/A")
    print(f"  Loopback: 127.0.0.1")
    print(f"  DNS Google: 8.8.8.8")

def scan_port(host, port):
    """Cek apakah port terbuka"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    result = s.connect_ex((host, port))
    s.close()
    return result == 0

def cek_port_umum():
    print("\n[2] CEK PORT UMUM DI localhost")
    ports = {22: "SSH", 80: "HTTP", 443: "HTTPS", 3306: "MySQL", 8080: "HTTP-Alt"}
    for port, name in ports.items():
        status = "TERBUKA" if scan_port("127.0.0.1", port) else "Tertutup"
        print(f"  Port {port} ({name}): {status}")

def cek_protokol():
    print("\n[3] PROTOKOL & FUNGSINYA")
    protos = [
        ("HTTP/80", "Web biasa", "Browsing internet"),
        ("HTTPS/443", "Web aman", "Browsing terenkripsi"),
        ("FTP/21", "Transfer file", "Upload/download file"),
        ("SSH/22", "Remote aman", "Akses server dari jauh"),
        ("DNS/53", "Domain ke IP", "Nerjemahin google.com ke IP"),
        ("SMB/445", "File sharing", "Berbagi file di jaringan"),
    ]
    print(f"  {'Protocol':<15} {'Port':<8} {'Fungsi'}")
    print(f"  {'-'*40}")
    for p, port, desc in protos:
        print(f"  {p:<15} {port:<8} {desc}")

def main():
    banner()
    cek_ip()
    cek_port_umum()
    cek_protokol()
    print("\n" + "="*60)
    print("  LATIHAN:")
    print("  1. Ganti '127.0.0.1' dengan IP target lain")
    print("  2. Tambah port lain untuk dicek")
    print("  3. Coba ping google.com dari terminal")
    print("="*60)

if __name__ == "__main__":
    main()
