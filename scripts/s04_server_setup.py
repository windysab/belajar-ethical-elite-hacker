#!/usr/bin/env python3
"""Sesi 4: Linux/BSD Server Setup — Apache, Nginx, MySQL, UFW"""
import subprocess, os, shutil, socket

def banner():
    print("="*60)
    print("  SESI 4: LINUX/BSD SERVER SETUP")
    print("  Analogi: Toyota vs BMW vs Tank")
    print("  — Apache = Toyota (sederhana, stabil)")
    print("  — Nginx  = BMW (cepat, modern)")
    print("  — BSD    = Tank (stabil, aman)")
    print("  Referensi: X-Code Ethical Elite Hacker v11")
    print("="*60)

def cek_web_server():
    print("\n[1] CEK WEB SERVER (Apache vs Nginx)")
    apache = shutil.which("apache2") or shutil.which("httpd")
    nginx  = shutil.which("nginx")

    if apache:
        r = subprocess.run([apache, "-v"], capture_output=True, text=True, timeout=5)
        ver = r.stdout.strip().splitlines()[0] if r.stdout.strip() else "(terinstall)"
        print(f"  ✅ Apache terdeteksi: {ver}")
        print(f"     💡 Apache = TOYOTA — andalan web server klasik, stabil, banyak modul")
    else:
        print("  ❌ Apache TIDAK terinstall (sudo apt install apache2)")

    if nginx:
        r = subprocess.run([nginx, "-v"], capture_output=True, text=True, timeout=5)
        ver = r.stderr.strip() if r.stderr.strip() else "(terinstall)"
        print(f"  ✅ Nginx terdeteksi: {ver}")
        print(f"     💡 Nginx = BMW — ringan, event-driven, cocok reverse proxy & load balancer")
    else:
        print("  ❌ Nginx TIDAK terinstall (sudo apt install nginx)")

    if not apache and not nginx:
        print("  ⚠️  Belum ada web server terinstall. Pilih salah satu:")
        print("     sudo apt install apache2   → Toyota (mudah, plugin banyak)")
        print("     sudo apt install nginx     → BMW (cepat, modern)")
    print()

    print("  📋 Perbedaan Apache vs Nginx:")
    print(f"  {'Aspek':<20} {'Apache':<25} {'Nginx'}")
    print(f"  {'-'*65}")
    print(f"  {'Arsitektur':<20} {'Process-driven':<25} {'Event-driven'}")
    print(f"  {'Konfigurasi':<20} {'.htaccess (per folder)':<25} {'Tidak support .htaccess'}")
    print(f"  {'Modul':<20} {'Dynamic loading':<25} {'Static (compile)'}")
    print(f"  {'Kinerja Statis':<20} {'Standar':<25} {'🏆 Lebih cepat'}")
    print(f"  {'Kinerja Dinamis':<20} {'🏆 Lebih stabil':<25} {'PHP via FastCGI'}")
    print(f"  {'Cocok Untuk':<20} {'Shared hosting, cPanel':<25} {'Reverse proxy, high traffic'}")

def cek_port_listening():
    print("\n[2] CEK PORT LISTENING (Web Server & Services)")
    port_name = {
        80: "HTTP (Apache/Nginx)", 443: "HTTPS", 8080: "HTTP-Alt",
        3306: "MySQL/MariaDB", 5432: "PostgreSQL", 27017: "MongoDB",
        22: "SSH", 21: "FTP", 25: "SMTP", 53: "DNS",
        6379: "Redis", 11211: "Memcached", 8443: "HTTPS-Alt",
    }
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
                if state == "0A":  # LISTEN
                    ports.append(port)
        if ports:
            print(f"  {'Port':<8} {'Service':<25} {'Status'}")
            print(f"  {'-'*45}")
            for p in sorted(ports):
                nama = port_name.get(p, "Unknown")
                print(f"  {p:<8} {nama:<25} ✅ LISTEN")
        else:
            print("  (tidak ada port listening)")
    except Exception:
        print("  (tidak bisa membaca /proc/net/tcp — butuh akses root?)")

def cek_database():
    print("\n[3] CEK DATABASE SERVER")
    mysql = shutil.which("mysql") or shutil.which("mariadb")
    psql  = shutil.which("psql")
    mongo = shutil.which("mongod") or shutil.which("mongosh")

    if mysql:
        r = subprocess.run([mysql, "--version"], capture_output=True, text=True, timeout=5)
        print(f"  ✅ MySQL/MariaDB: {r.stdout.strip() or '(terinstall)'}")
    else:
        print("  ❌ MySQL/MariaDB TIDAK terinstall (sudo apt install mariadb-server)")
        print("     💡 MySQL = penyimpan data utama untuk web app")

    if psql:
        r = subprocess.run([psql, "--version"], capture_output=True, text=True, timeout=5)
        print(f"  ✅ PostgreSQL: {r.stdout.strip()}")
        print("     💡 PostgreSQL = database canggih, support JSON, GIS, ACID compliant")
    else:
        print("  ❌ PostgreSQL TIDAK terinstall")

    if mongo:
        print(f"  ✅ MongoDB terdeteksi")
    else:
        print("  ❌ MongoDB TIDAK terinstall")

    print()
    print("  📋 Perintah dasar database:")
    print("     sudo systemctl status mariadb  → cek status MySQL")
    print("     sudo mysql -u root              → masuk ke MySQL")
    print("     SHOW DATABASES;                 → lihat database")
    print("     USE <db>; SHOW TABLES;          → lihat tabel")

def cek_firewall():
    print("\n[4] CEK FIREWALL & KEAMANAN")
    ufw = shutil.which("ufw")
    ipt = shutil.which("iptables")
    nft = shutil.which("nft")

    if ufw:
        r = subprocess.run(["sudo", "ufw", "status"], capture_output=True, text=True, timeout=5)
        status = r.stdout.strip() if r.stdout.strip() else r.stderr.strip()
        print(f"  ✅ UFW (Uncomplicated Firewall):")
        for line in status.splitlines():
            print(f"     {line}")
        print("     💡 UFW = firewall sederhana khas Ubuntu/Debian")
        print("     💡 Aturan: sudo ufw allow 22/tcp, sudo ufw deny 23")
    else:
        print("  ❌ UFW TIDAK terinstall (sudo apt install ufw)")

    if ipt:
        print("  ✅ iptables tersedia (firewall klasik Linux)")
    if nft:
        print("  ✅ nftables tersedia (firewall modern, pengganti iptables)")

    print()
    print("  📋 Aturan firewall dasar:")
    print("     sudo ufw enable              → aktifkan firewall")
    print("     sudo ufw allow 80/tcp        → buka port web")
    print("     sudo ufw deny 23             → tutup port telnet")
    print("     sudo ufw status numbered     → lihat aturan + nomor")
    print("     sudo ufw delete <number>     → hapus aturan")
    print("     sudo iptables -L -n -v       → lihat aturan iptables (lebih detail)")

def virtual_host():
    print("\n[5] KONSEP VIRTUAL HOST")
    print("  💡 Satu server bisa host BANYAK website sekaligus!")
    print()
    print("  📋 Contoh VirtualHost Apache (/etc/apache2/sites-available/):")
    print("     <VirtualHost *:80>")
    print("         ServerName tokoku.com")
    print("         DocumentRoot /var/www/tokoku")
    print("         ErrorLog ${APACHE_LOG_DIR}/tokoku_error.log")
    print("         CustomLog ${APACHE_LOG_DIR}/tokoku_access.log combined")
    print("     </VirtualHost>")
    print()
    print("  📋 Contoh Server Block Nginx (/etc/nginx/sites-available/):")
    print("     server {")
    print("         listen 80;")
    print("         server_name tokoku.com;")
    print("         root /var/www/tokoku;")
    print("         access_log /var/log/nginx/tokoku_access.log;")
    print("         error_log /var/log/nginx/tokoku_error.log;")
    print("     }")
    print()
    print("  💡 Dengan Virtual Host, 1 server bisa host: tokoku.com,")
    print("     sekolah.com, belajarhacking.com — semuanya di IP yang sama!")

def cek_bsd():
    print("\n[6] BSD — SI TANK")
    print("  💡 BSD (FreeBSD/OpenBSD) = sistem mirip Linux TAPI BUKAN Linux")
    print()
    print(f"  {'Aspek':<20} {'Linux':<25} {'BSD'}")
    print(f"  {'-'*65}")
    print(f"  {'Kernel':<20} {'Monolitik (Linux)':<25} {'Monolitik (BSD)'}")
    print(f"  {'Lisensi':<20} {'GPL':<25} {'BSD License'}")
    print(f"  {'Package':<20} {'apt/dnf/pacman':<25} {'pkg / ports'}")
    print(f"  {'Init System':<20} {'systemd':<25} {'init (RC)'}")
    print(f"  {'Firewall':<20} {'iptables/nftables':<25} {'pf (packet filter)'}")
    print(f"  {'Kelebihan':<20} {'Driver luas, kompatibel':<25} {'Stabil, aman, dokumentasi lengkap'}")
    print(f"  {'Analogi':<20} {'Toyota — serba bisa':<25} {'Tank — kuat, berat, tahan banting'}")

def cek_systemd():
    print("\n[7] CEK SERVICE STATUS (systemctl)")
    services = ["apache2", "nginx", "mariadb", "mysql", "ufw", "ssh", "docker"]
    print(f"  {'Service':<15} {'Status'}")
    print(f"  {'-'*30}")
    for svc in services:
        r = subprocess.run(["systemctl", "is-active", svc], capture_output=True, text=True, timeout=5)
        status = r.stdout.strip()
        if status == "active":
            status_fmt = "✅ RUNNING"
        elif status == "inactive":
            status_fmt = "⏹️  STOPPED"
        elif status == "failed":
            status_fmt = "❌ FAILED"
        else:
            status_fmt = f"❓ {status}" if status else "❓ TIDAK ADA"
        print(f"  {svc:<15} {status_fmt}")

def main():
    banner()
    cek_web_server()
    cek_port_listening()
    cek_database()
    cek_firewall()
    virtual_host()
    cek_bsd()
    cek_systemd()
    print("\n" + "="*60)
    print("  ✅ SESI 4 SELESAI!")
    print("  👉 Apache = Toyota (stabil, klasik, .htaccess)")
    print("  👉 Nginx  = BMW (cepat, modern, event-driven)")
    print("  👉 BSD    = Tank (stabil, aman, pf firewall)")
    print("  👉 Virtual Host = 1 server, banyak website")
    print("  👉 Firewall = UFW (mudah) / iptables (detail) / pf (BSD)")
    print()
    print("  📌 LATIHAN LANJUTAN:")
    print("  1. Install Apache2 & Nginx bersamaan, ganti port salah satunya")
    print("  2. Buat virtual host untuk domain tokoku.com di /etc/hosts")
    print("  3. Setting UFW: buka port 80/443, tutup semua port lain")
    print("  4. Install MariaDB & buat database + user baru")
    print("  5. Setup Nginx sebagai reverse proxy ke aplikasi Python (localhost:5000)")
    print("="*60)

if __name__ == "__main__":
    main()
