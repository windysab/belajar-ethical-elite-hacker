#!/usr/bin/env python3
"""Sesi 3: VirtualBox, Docker & Linux Dasar"""
import subprocess, os, sys, shutil

def banner():
    print("="*60)
    print("  SESI 3: VIRTUALISASI, DOCKER & LINUX DASAR")
    print("  Analogi: Rumah Boneka (VM) | Kontrakan Instan (Docker)")
    print("  Analogi: Ilmu Sihir (Linux Terminal)")
    print("  Referensi: X-Code Ethical Elite Hacker v11")
    print("="*60)

def cek_virtualbox():
    print("\n[1] CEK VIRTUALBOX (Rumah Boneka)")
    vbox = shutil.which("VirtualBox") or shutil.which("vboxmanage")
    if vbox:
        r = subprocess.run(["vboxmanage", "--version"], capture_output=True, text=True, timeout=5)
        ver = r.stdout.strip() or "terinstall"
        print(f"  ✅ VirtualBox terdeteksi: {ver}")
    else:
        print("  ❌ VirtualBox TIDAK terinstall")
    print("  💡 VM = RUMAH BONEKA — komputer virtual di dalam komputer fisik")
    print("  💡 Hypervisor = Oracle VM VirtualBox, VMware, KVM, Hyper-V")
    print("  💡 Roda Gigi (VirtIO) = driver khusus biar VM lebih kencang\n")

    print("  📋 Perintah VirtualBox umum:")
    print("     vboxmanage list vms              → daftar VM")
    print("     vboxmanage startvm <nama> --type headless → jalanin VM tanpa GUI")
    print("     vboxmanage controlvm <nama> poweroff → matiin VM")
    print("     VBoxManage list bridgedifs       → lihat interface bridging")

def cek_docker():
    print("\n[2] CEK DOCKER (Kontrakan Instan)")
    docker = shutil.which("docker")
    if docker:
        r = subprocess.run(["docker", "--version"], capture_output=True, text=True, timeout=5)
        print(f"  ✅ Docker terdeteksi: {r.stdout.strip()}")

        print("\n  [2a] Docker Images (katalog OS/software siap pakai):")
        r2 = subprocess.run(["docker", "images"], capture_output=True, text=True, timeout=10)
        if r2.stdout.strip():
            for line in r2.stdout.strip().splitlines():
                print(f"     {line}")
        else:
            print("     (belum ada image yang di-pull)")

        print("\n  [2b] Docker Container (instansi yang berjalan):")
        r3 = subprocess.run(["docker", "ps", "-a"], capture_output=True, text=True, timeout=10)
        if r3.stdout.strip():
            for line in r3.stdout.strip().splitlines():
                print(f"     {line}")
        else:
            print("     (tidak ada container)")
    else:
        print("  ❌ Docker TIDAK terinstall")
        print("  💡 Install: sudo apt install docker.io && sudo systemctl enable --now docker")

    print("\n  📋 Perintah Docker penting:")
    print("     docker ps              → container aktif")
    print("     docker ps -a           → semua container (termasuk mati)")
    print("     docker images          → daftar image")
    print("     docker pull <image>    → download image (contoh: dwvalabs/dvwa)")
    print("     docker run -d -p 80:80 <image> → jalankan container")
    print("     docker stop <id>       → hentikan container")
    print("     docker rm <id>         → hapus container")

def cek_dvwa():
    print("\n[3] DVWA — DAMN VULNERABLE WEB APPLICATION")
    print("  💡 DVWA = aplikasi web sengaja dibuat RENTAN buat latihan")
    print("  💡 Target utama belajar OWASP Top 10 & Web Hacking")

    docker = shutil.which("docker")
    if docker:
        r = subprocess.run(["docker", "ps", "--format", "{{.Image}}"], capture_output=True, text=True, timeout=10)
        if "dvwa" in r.stdout.lower():
            print("  ✅ DVWA container sudah berjalan!")
        else:
            print("  ❌ DVWA belum jalan. Cara jalankan:")
            print("     docker pull vulnerables/web-dvwa")
            print("     docker run -d -p 80:80 vulnerables/web-dvwa")
            print("     Buka http://localhost → login admin:password")
    else:
        print("  ❌ Docker tidak ada — install dulu docker.io")

    print("\n  🔥 Alternatif lab rentan lainnya:")
    print("     • dvwalabs/dvwa        — DVWA official")
    print("     • bkimminich/juice-shop — OWASP Juice Shop (Node.js)")
    print("     • webgoat/goatandwolf  — OWASP WebGoat")
    print("     • vulnerables/web-dvwa — DVWA versi lain")

def linux_dasar():
    print("\n[4] LINUX DASAR (Ilmu Sihir)")
    print("  💡 Terminal = kunci utama Ethical Hacker. Hafalkan perintah dasar!\n")

    commands = [
        ("ls -la",          "Lihat isi folder (termasuk file tersembunyi)"),
        ("cd /tmp",         "Pindah direktori"),
        ("pwd",             "Cetak posisi folder saat ini"),
        ("whoami",          "Siapa user login sekarang"),
        ("id",              "Lihat UID/GID user"),
        ("uname -a",        "Info kernel & sistem operasi"),
        ("cat /etc/os-release", "Info distro Linux"),
        ("free -h",         "Cek RAM tersisa"),
        ("df -h",           "Cek kapasitas disk"),
        ("ps aux",          "Lihat proses berjalan"),
        ("netstat -tulpn",  "Lihat port listening (butuh sudo)"),
        ("ip a",            "Lihat IP address tiap interface"),
        ("ifconfig",        "Alternatif ip a (butuh net-tools)"),
        ("ping -c 3 google.com", "Tes koneksi internet"),
    ]

    print(f"  {'Perintah':<30} {'Fungsi'}")
    print(f"  {'-'*68}")
    for cmd, desc in commands:
        print(f"  {cmd:<30} {desc}")

    print()

    # Run a few safe commands to show real output
    print("  ▶ Demo real output perintah dasar:")
    for cmd in ["whoami", "pwd", "hostname"]:
        try:
            r = subprocess.run(cmd.split(), capture_output=True, text=True, timeout=5)
            out = r.stdout.strip().splitlines()[0] if r.stdout.strip() else "(kosong)"
            print(f"     $ {cmd} → {out}")
        except:
            print(f"     $ {cmd} → GAGAL")

def cek_tools_terinstall():
    print("\n[5] CEK TOOLS PENTING UNTUK HACKER")
    tools = {
        "nmap":    "Network Mapper — scan port & jaringan",
        "netcat":  "Swiss Army Knife jaringan (nc/ncat)",
        "tcpdump": "Packet analyzer berbasis CLI",
        "wireshark":"Packet analyzer GUI",
        "nslookup":"DNS lookup tool",
        "dig":     "DNS query tool (lebih detail)",
        "curl":    "HTTP client dari terminal",
        "wget":    "Download file dari terminal",
        "git":     "Version control — download tools dari GitHub",
    }

    print(f"  {'Tool':<12} {'Status':<10} {'Keterangan'}")
    print(f"  {'-'*60}")
    for tool, desc in tools.items():
        ada = shutil.which(tool)
        status = "✅ ADA" if ada else "❌ TIDAK"
        print(f"  {tool:<12} {status:<10} {desc}")

def analogi():
    print("\n[6] ANALOGI VIRTUALISASI & LINUX")
    data = [
        ("VirtualBox/VM",  "RUMAH BONEKA",     "Satu komputer fisik punya banyak komputer virtual. Setiap VM punya OS sendiri, kayak punya rumah boneka dengan perabot mini sendiri-sendiri."),
        ("Docker",         "KONTRAKAN INSTAN",  "Docker cuma bagi kernel host, nggak perlu install OS penuh. Cepat & ringan — kayak kontrakan yang tinggal bawa koper, langsung huni."),
        ("Linux Terminal", "ILMU SIHIR",        "Hanya dengan teks, kamu bisa kontrol penuh komputer. Mirip mantra sihir — perintah singkat tapi efeknya dahsyat."),
        ("Hypervisor",     "TUKANG KOST",       "Dia yang ngatur pembagian resource (CPU, RAM, disk) antar VM. Kayak tukang kost yang atur kamar & listrik."),
    ]
    print(f"  {'Konsep':<18} {'Analogi':<20} {'Penjelasan'}")
    print(f"  {'-'*70}")
    for konsep, an, penjelasan in data:
        print(f"  {konsep:<18} {an:<20} {penjelasan}")
    print()

def main():
    banner()
    cek_virtualbox()
    cek_docker()
    cek_dvwa()
    linux_dasar()
    cek_tools_terinstall()
    analogi()
    print("\n" + "="*60)
    print("  ✅ SESI 3 SELESAI!")
    print("  👉 Virtualisasi: VM butuh OS penuh, Docker lebih ringan")
    print("  👉 Linux adalah bahasa ibu Ethical Hacker — kuasai terminal!")
    print("  👉 DVWA = lab latihan web hacking pertama kamu")
    print("  👉 Hafalkan: ls, cd, pwd, cat, ps, netstat, ip a, nmap")
    print()
    print("  📌 LATIHAN LANJUTAN:")
    print("  1. Install VirtualBox & buat VM Kali Linux")
    print("  2. Install Docker & pull image Ubuntu:latest")
    print("  3. Jalankan container DVWA & login ke aplikasi")
    print("  4. Praktek ls -la, cd, cat, ps aux di terminal Linux")
    print("  5. Eksplorasi Docker Compose untuk lab multi-container")
    print("="*60)

if __name__ == "__main__":
    main()
