#!/usr/bin/env python3
"""Sesi 3: VirtualBox, Docker & Linux Dasar"""
import subprocess, os, pwd, grp, stat

def banner():
    print("="*60)
    print("  SESI 3: VIRTUALISASI & LINUX DASAR")
    print("  Referensi: X-Code Ethical Elite Hacker v11")
    print("  💡 Virtualisasi = RUMAH BONEKA di dalam rumah")
    print("  💡 Docker = KONTRAKAN INSTAN")
    print("  💡 Linux = ILMU SIHIR command line")
    print("="*60)

def cek_system():
    print("\n[1] CEK SISTEM & KERNEL")
    r = subprocess.run(["uname", "-a"], capture_output=True, text=True)
    print(f"  Kernel: {r.stdout.strip()}")
    r = subprocess.run(["cat", "/etc/os-release"], capture_output=True, text=True)
    for line in r.stdout.splitlines():
        if line.startswith("PRETTY_NAME="):
            print(f"  OS: {line.split('=')[1].strip('\"')}")
    print(f"  User saat ini: {os.environ.get('USER', 'unknown')}")
    print(f"  Home: {os.environ.get('HOME', 'unknown')}")
    print("  💡 Di VPS ini kita pake Ubuntu, via Docker container")

def cek_users():
    print("\n[2] USER & GROUP")
    print("  Daftar user (dari /etc/passwd):")
    r = subprocess.run(["cat", "/etc/passwd"], capture_output=True, text=True)
    users = []
    for line in r.stdout.splitlines():
        parts = line.split(":")
        if int(parts[2]) >= 1000 or parts[0] in ["root", "hermes"]:
            users.append(f"    {parts[0]:15} (UID: {parts[2]})")
    for u in users[:10]:
        print(u)
    print(f"  ... dan {len(users)} total user terdaftar")
    print("  💡 User = penghuni rumah. Root = pemilik rumah.")

def cek_permissions():
    print("\n[3] FILE PERMISSION (chmod/chown)")
    print("  Cek permission file penting:")
    for path in ["/etc/passwd", "/etc/shadow", "/etc/ssh/sshd_config"]:
        try:
            st = os.stat(path)
            mode = stat.filemode(st.st_mode)
            owner = pwd.getpwuid(st.st_uid).pw_name
            group = grp.getgrgid(st.st_gid).gr_name
            print(f"  {path:40} {mode} {owner}:{group}")
        except:
            print(f"  {path:40} — tidak bisa dibaca")
    print()
    print("  💡 rwx rwx rwx = owner group others")
    print("     r=4 (baca), w=2 (tulis), x=1 (eksekusi)")
    print("     chmod 755 file = rwxr-xr-x (owner full, lainnya baca+jalan)")

def cek_storage():
    print("\n[4] STORAGE & DISK")
    r = subprocess.run(["df", "-h"], capture_output=True, text=True)
    print(r.stdout[:500])
    print("  💡 df = disk free. Lihat kapasitas & sisa space.")

def docker_concept():
    print("\n[5] DOCKER & VIRTUALISASI")
    print("  💡 VirtualBox = VM penuh (OS tamu sendiri)")
    print("  💡 Docker = container (pake kernel host)")
    print()
    print("  Perbandingan:")
    print(f"  {'':15} {'VM (VirtualBox)':25} {'Docker Container'}")
    print(f"  {'-'*55}")
    print(f"  {'Boot':15} {'Menit':25} {'Detik'}")
    print(f"  {'Ukuran':15} {'GB':25} {'MB'}")
    print(f"  {'Resource':15} {'Berat':25} {'Ringan'}")
    print(f"  {'Isolasi':15} {'Sangat aman':25} {'Cukup'}")
    print()
    # Check docker
    r = subprocess.run(["which", "docker"], capture_output=True, text=True)
    if r.stdout.strip():
        r2 = subprocess.run(["docker", "ps", "--format", "{{.Names}} {{.Image}} {{.Status}}"], capture_output=True, text=True)
        print("  Docker aktif di server ini:")
        for line in r2.stdout.strip().splitlines():
            print(f"    {line}")
    else:
        print("  Docker tidak terinstall di sini (tapi kita jalan di container!)")

    print()
    print("  Perintah Docker penting:")
    print("    docker ps           = lihat container jalan")
    print("    docker images       = lihat image tersedia")
    print("    docker run -d nginx = jalankan Nginx container")
    print("    docker exec -it ... bash = masuk ke container")
    print("    docker-compose up   = jalanin multi-container")

def bash_tips():
    print("\n[6] BASH COMMAND DASAR")
    cmds = [
        ("ls -la", "Lihat file lengkap"),
        ("cd ..", "Naik folder"),
        ("pwd", "Lokasi sekarang"),
        ("mkdir folder", "Buat folder"),
        ("touch file.txt", "Buat file kosong"),
        ("cp source dest", "Copy file"),
        ("mv source dest", "Pindah/rename file"),
        ("rm file", "Hapus file"),
        ("cat file", "Lihat isi file"),
        ("head/tail -n 10", "Lihat awal/akhir file"),
        ("grep 'kata' file", "Cari kata di file"),
        ("chmod 755 file", "Ubah permission"),
        ("chown user:group", "Ubah kepemilikan"),
        ("ps aux", "Lihat proses jalan"),
        ("kill PID", "Matikan proses"),
        ("w", "Siapa aja yang login"),
        ("whoami", "Siapa saya"),
        ("sudo command", "Jalanin sebagai root"),
        ("apt install pkg", "Install package"),
        ("systemctl status", "Cek service"),
    ]
    print(f"  {'Perintah':25} {'Fungsi'}")
    print(f"  {'-'*45}")
    for cmd, desc in cmds:
        print(f"  {cmd:25} {desc}")

def ssh_server():
    print("\n[7] SSH SERVER & SAMBA")
    print("  🔑 SSH Server = pintu remote aman")
    r = subprocess.run(["which", "sshd"], capture_output=True, text=True)
    print(f"  SSH daemon: {'TERINSTAL ✅' if r.stdout.strip() else 'Tidak terinstall'}")
    print()
    print("  📁 SAMBA = berbagi file antar OS")
    print("     Install: sudo apt install samba")
    print("     Config: /etc/samba/smb.conf")
    print("     Share folder, atur valid users, read only / writable")
    print()
    print("  🌐 Apache vs Nginx:")
    print(f"     {'Apache':20} {'Nginx'}")
    print(f"     {'-'*35}")
    print("     | Module-based | Event-driven  |")
    print("     | .htaccess    | Lebih cepat   |")
    print("     | Fleksibel    | Lebih ringan  |")
    r2 = subprocess.run(["which", "nginx"], capture_output=True, text=True)
    r3 = subprocess.run(["which", "apache2"], capture_output=True, text=True)
    print(f"     Nginx: {'TERINSTAL ✅' if r2.stdout.strip() else 'Tidak'}")
    print(f"     Apache2: {'TERINSTAL ✅' if r3.stdout.strip() else 'Tidak'}")

def keamanan():
    print("\n[8] KEAMANAN LINUX DASAR")
    print("  🔒 Matikan recovery mode GRUB (biar gak bisa reset password)")
    print("     echo 'GRUB_DISABLE_RECOVERY=true' >> /etc/default/grub")
    print()
    print("  🔥 Firewall UFW:")
    print("     sudo ufw enable              = nyalakan")
    print("     sudo ufw allow 22/tcp        = izinkan SSH")
    print("     sudo ufw deny from 1.2.3.4   = blokir IP")
    print("     sudo ufw status verbose      = cek status")
    print()
    print("  🔐 SSH Hardening:")
    print("     Port 2222           (ganti port)")
    print("     PermitRootLogin no  (larang root login)")
    print("     PasswordAuthentication no (pake key)")
    print("     AllowUsers hermes   (hanya user tertentu)")

def main():
    banner()
    cek_system()
    cek_users()
    cek_permissions()
    cek_storage()
    docker_concept()
    bash_tips()
    ssh_server()
    keamanan()
    print("\n" + "="*60)
    print("  ✅ SESI 3 SELESAI!")
    print("  👉 System info, user & permission")
    print("  👉 Docker vs VM, Bash command")
    print("  👉 SSH server, Apache/Nginx, SAMBA")
    print("  👉 Firewall UFW, SSH hardening")
    print()
    print("  📌 PRAKTIK LANJUTAN:")
    print("  1. Install VirtualBox di laptop & bikin VM Kali")
    print("  2. Coba docker: docker run -d -p 8080:80 nginx")
    print("  3. Setting IP: nano /etc/netplan/01-netcfg.yaml")
    print("  4. Bikin user baru: sudo useradd -m siswa1")
    print("  5. Coba SSH dari laptop ke VPS ini")
    print("="*60)

if __name__ == "__main__":
    main()
