#!/usr/bin/env python3
"""Sesi 12: OWASP Top 10 — A1 s.d. A5"""

import subprocess
import sys
import os
from datetime import datetime


def banner():
    print("=" * 60)
    print("  ETHICAL ELITE HACKER v11 — Sesi 12")
    print("  OWASP Top 10 — A1 sampai A5")
    print("=" * 60)
    print("  Referensi: X-Code Ethical Elite Hacker v11")
    print("=" * 60)


def check_tool(name):
    try:
        subprocess.check_output([name, "--version"], stderr=subprocess.STDOUT, timeout=5)
        return "✅ TERINSTAL"
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return "❌ TIDAK TERINSTAL"


def section(num, title):
    print(f"\n{'─' * 50}")
    print(f"  [{num}] {title}")
    print(f"{'─' * 50}")


# ── [1] OWASP Overview ──
def owasp_overview():
    print("""
  💡 OWASP = Open Web Application Security Project
     Organisasi nonprofit yang menerbitkan "OWASP Top 10" —
     daftar 10 risiko keamanan web paling kritis.

   ╔═══════════════════════════════════════════════════════╗
   ║  OWASP TOP 10 (2021):                                ║
   ║                                                      ║
   ║  A1 — Broken Access Control                          ║
   ║  A2 — Cryptographic Failures                         ║
   ║  A3 — Injection                                      ║
   ║  A4 — Insecure Design                                ║
   ║  A5 — Security Misconfiguration                      ║
   ║  A6 — Vulnerable & Outdated Components               ║
   ║  A7 — Identification & Auth Failures                 ║
   ║  A8 — Software & Data Integrity Failures             ║
   ║  A9 — Security Logging & Monitoring Failures         ║
   ║  A10 — Server-Side Request Forgery (SSRF)            ║
   ╚═══════════════════════════════════════════════════════╝
    """)


# ── [2] A1 — Broken Access Control (IDOR) ──
def a1_broken_access():
    print("  💡 A1 — BROKEN ACCESS CONTROL / IDOR:\\n")

    print("""
   ╔═══════════════════════════════════════════════════════╗
   ║  🔑 KUNCI KAMAR SALAH                                ║
   ║     Bayangkan: Kamu nemu kunci kamar hotel. Dengan   ║
   ║     kunci itu kamu bisa buka SEMUA kamar lain!       ║
   ║     Itulah Broken Access Control.                    ║
   ╚═══════════════════════════════════════════════════════╝
    """)

    print("  IDOR = Insecure Direct Object Reference\\n")

    print("  Contoh IDOR: URL dengan ID user bisa diubah manual:")
    print("""
    https://bank.com/account/1234     ← punya kamu
    https://bank.com/account/1235     ← coba ganti angka → lihat akun orang lain!
    """)

    print(f"  {'Jenis':<25} {'Contoh':<45} {'Dampak':<30}")
    print(f"  {'─' * 100}")
    idors = [
        ("URL Tampering",       "/user/101 → /user/102",           "Lihat data user lain"),
        ("API IDOR",            "/api/v1/order/500 → /501",        "Lihat order orang"),
        ("UUID Predictable",    "/invoice/USER001 → USER002",      "Invoice orang lain"),
        ("Method Bypass",       "GET /admin (403) → X-HTTP-Method-Override: PUT", "Bypass akses"),
        ("Mass Assignment",     "{\"role\":\"user\"} → {\"role\":\"admin\"}",      "Jadi admin"),
        ("Referer Bypass",      "Referer: /admin → bisa akses /api/admin",         "Bypass CSRF"),
    ]
    for jenis, contoh, dampak in idors:
        print(f"  {jenis:<25} {contoh:<45} {dampak:<30}")
    print()

    print("  ✅ Pencegahan Broken Access Control:")
    print("     • Gunakan access control matrix (siapa boleh akses apa)")
    print("     • Jangan percaya user input untuk referensi objek")
    print("     • Gunakan UUID random, bukan increment ID")
    print("     • Server-side authorization check setiap request")
    print()


# ── [3] A2 — Cryptographic Failures ──
def a2_crypto_failure():
    print("  💡 A2 — CRYPTOGRAPHIC FAILURES (Dulu: Sensitive Data Exposure):\\n")

    print("""
   ╔═══════════════════════════════════════════════════════╗
   ║  🏷️ STIKER PASSWORD                                  ║
   ║     Bayangkan: Kamu nulis password di stiker dan     ║
   ║     nempel di monitor. Atau nyimpen password di      ║
   ║     file TXT di desktop. Sama bahayanya dengan       ║
   ║     menyimpan password dalam bentuk plaintext!       ║
   ╚═══════════════════════════════════════════════════════╝
    """)

    print("  Demo: Password Storage — Plaintext vs Hash vs Bcrypt\\n")

    # Demo password hashing
    demo_password = "P@ssw0rd123!"

    # Plaintext
    print(f"  {'Metode':<25} {'Password':<30} {'Panjang':<10}")
    print(f"  {'─' * 65}")
    print(f"  {'Plaintext':<25} {demo_password:<30} {len(demo_password):<10}")

    # Simple MD5 (hashlib)
    import hashlib
    md5_hash = hashlib.md5(demo_password.encode()).hexdigest()
    print(f"  {'MD5 (lemah!)':<25} {md5_hash:<30} {len(md5_hash):<10}")

    sha1_hash = hashlib.sha1(demo_password.encode()).hexdigest()
    print(f"  {'SHA-1 (lemah!)':<25} {sha1_hash:<30} {len(sha1_hash):<10}")

    sha256_hash = hashlib.sha256(demo_password.encode()).hexdigest()
    print(f"  {'SHA-256':<25} {sha256_hash:<30} {len(sha256_hash):<10}")

    # Simulate bcrypt-like concept (bcrypt is external lib, we demo the concept)
    import base64
    salt = os.urandom(16)
    # Simple key derivation simulation
    key = hashlib.pbkdf2_hmac('sha256', demo_password.encode(), salt, 100000)
    key_b64 = base64.b64encode(salt + key).decode()
    print(f"  {'PBKDF2-HMAC-SHA256':<25} {key_b64[:30]:<30} {len(key_b64):<10}")
    print()

    print("  💡 Kenapa bcrypt/argon2 lebih baik dari MD5/SHA?")
    print("     • MD5: Collision attack — beda input bisa hasil hash sama")
    print("     • SHA-1: Collision ditemukan (SHAttered attack)")
    print("     • SHA-256: Masih aman tapi CEPAT → brute force mudah")
    print("     • bcrypt: Lambat secara design + cost factor bisa ditingkatkan")
    print("     • Argon2: Pemenang Password Hashing Competition (2015)")
    print()

    print(f"  {'Jenis Serangan Crypto':<30} {'Cara Kerja':<40} {'Waktu Estimasi':<25}")
    print(f"  {'─' * 95}")
    attacks = [
        ("Rainbow Table",      "Precomputed hash lookup",           "Detik"),
        ("Brute Force MD5",    "Coba semua kombinasi (MD5)",        "Hari/Minggu"),
        ("Brute Force bcrypt", "Coba semua kombinasi (bcrypt)",     "Tahun/Abad"),
        ("Hash Collision",     "Cari input beda → hash sama",       "Bervariasi"),
        ("Dictionary Attack",  "Coba password umum",                "Menit"),
    ]
    for attack, cara, waktu in attacks:
        print(f"  {attack:<30} {cara:<40} {waktu:<25}")
    print()

    print("  ✅ Pencegahan Crypto Failure:")
    print("     • Gunakan bcrypt, argon2, atau scrypt untuk password")
    print("     • Jangan gunakan MD5 atau SHA-1 untuk password hashing")
    print("     • Enkripsi data sensitif di database (AES-256)")
    print("     • Gunakan HTTPS (TLS 1.2+) — jangan HTTP!")
    print("     • Jangan simpan credit card/SSN tanpa enkripsi")
    print()


# ── [4] A3 — Injection ──
def a3_injection():
    print("  💡 A3 — INJECTION (SQL, NoSQL, OS Command, LDAP):\\n")

    print("""
  Konsep: Attacker menyuntikkan kode/code ke dalam input yang
  kemudian dieksekusi oleh interpreter (SQL DB, shell OS, dll).
    """)

    print("  Demo SQL Injection — Login Bypass:\\n")
    print("  Query normal:")
    print("    SELECT * FROM users WHERE username='admin' AND password='s3cret'")
    print()
    print("  Query dengan injeksi:")
    sql_payload = "' OR '1'='1"
    print(f"    SELECT * FROM users WHERE username='{sql_payload}' AND password='anything'")
    print("    → WHERE '1'='1' selalu TRUE → login BERHASIL!")
    print()

    print(f"  {'Jenis Injection':<25} {'Contoh':<40} {'Dampak':<30}")
    print(f"  {'─' * 95}")
    injections = [
        ("SQL Injection",         "' OR 1=1 --",                 "Bypass login, dump DB"),
        ("Blind SQLi",            "' AND SLEEP(5) --",           "Time-based extraction"),
        ("NoSQL Injection",       "{\"$gt\":\"\"}",              "Bypass MongoDB auth"),
        ("OS Command",            "; ls -la /etc/passwd",        "RCE di server"),
        ("LDAP Injection",        "*)(uid=*",                    "Bypass LDAP auth"),
        ("XPath Injection",       "' or '1'='1",                 "Extract XML data"),
        ("Template Injection",    "{{7*7}}",                     "SSTI → RCE"),
        ("HTTP Header Injection", "%0d%0aX-Custom:header",       "Response splitting"),
    ]
    for jenis, contoh, dampak in injections:
        print(f"  {jenis:<25} {contoh:<40} {dampak:<30}")
    print()

    print("  ✅ Pencegahan Injection:")
    print("     • Prepared Statement / Parameterized Query (WAJIB!)")
    print("     • ORM (Object Relational Mapping) — bikin query aman")
    print("     • Input validation + whitelist (bukan blacklist)")
    print("     • Escape special characters sesuai konteks")
    print("     • Least privilege: DB user cuma bisa SELECT yang diperlukan")
    print()


# ── [5] A4 — Insecure Design ──
def a4_insecure_design():
    print("  💡 A4 — INSECURE DESIGN:\\n")

    print("""
   ╔═══════════════════════════════════════════════════════╗
   ║  Insecure Design = Cacat di ARSITEKTUR aplikasi,     ║
   ║  bukan di implementasi kode.                         ║
   ║                                                      ║
   ║  Contoh: Aplikasi yang percaya SEPENUHNYA pada       ║
   ║  client-side validation (JavaScript). Jika JS         ║
   ║  dimatikan, semua validasi hilang.                   ║
   ╚═══════════════════════════════════════════════════════╝
    """)

    print(f"  {'Cacat Design':<30} {'Contoh':<40} {'Kenapa Berbahaya':<30}")
    print(f"  {'─' * 100}")
    designs = [
        ("Client-side validation only",  "Harga di JS, backend terima aja",    "User bisa beli Rp1"),
        ("Rate limiting tidak ada",      "Login tanpa limit percobaan",        "Brute force unlimited"),
        ("No account lockout",           "Berapa kali salah password tetap",   "Dictionary attack"),
        ("Trust user-supplied role",     "Role dari cookie/user input",       "User jadi admin"),
        ("No CSRF token",                "Setiap request dipercaya asli",      "CSRF attack"),
        ("Predictable reset token",      "Token reset = timestamp+userid",     "Reset password siapa aja"),
        ("Missing MFA",                  "Hanya username + password",          "Credential stuffing"),
    ]
    for cacat, contoh, why in designs:
        print(f"  {cacat:<30} {contoh:<40} {why:<30}")
    print()

    print("  ✅ Pencegahan Insecure Design:")
    print("     • Threat modeling di awal development (STRIDE, PASTA)")
    print("     • Security by design — bukan security as an afterthought")
    print("     • Rate limiting + account lockout dari awal")
    print("     • Jangan pernah percaya client-side data")
    print("     • Prinsip: Never trust user input, always validate server-side")
    print()


# ── [6] A5 — Security Misconfiguration ──
def a5_security_misconfig():
    print("  💡 A5 — SECURITY MISCONFIGURATION:\\n")

    print("""
   ╔═══════════════════════════════════════════════════════╗
   ║  Contoh paling klasik:                               ║
   ║                                                        ║
   ║  • Directory listing ON → semua file bisa dilihat      ║
   ║  • Default credentials → admin:admin                   ║
   ║  • Debug mode ON di production → stack trace bocor     ║
   ║  • CORS terlalu longgar → http://evil.com bisa akses   ║
   ╚═══════════════════════════════════════════════════════╝
    """)

    print("  Demo: Directory Listing Check\\n")
    demo_dir = "/tmp/test_web"
    os.makedirs(f"{demo_dir}/secret", exist_ok=True)
    for fname in ["index.html", "secret/config.php", "secret/passwords.txt", "backup.sql"]:
        fpath = os.path.join(demo_dir, fname)
        if not os.path.exists(fpath):
            with open(fpath, "w") as f:
                f.write(f"# dummy file: {fname}\n")

    # Show directory listing concept
    print(f"  {'Path':<40} {'Ada':<15} {'Rentan?':<15}")
    print(f"  {'─' * 70}")
    paths = [
        (demo_dir,                "index.html, backup.sql visible",     "✅ YA (jika index tidak ada)"),
        (f"{demo_dir}/secret",    "config.php, passwords.txt",          "✅ YA (jika tidak dilindungi)"),
    ]
    for pth, content, rentan in paths:
        print(f"  {pth:<40} {content:<15} {rentan:<15}")
    print()

    # Cleanup
    import shutil
    shutil.rmtree(demo_dir, ignore_errors=True)

    print("  💡 Default Credentials Table:\\n")
    print(f"  {'Product':<25} {'Username':<20} {'Password':<20} {'Port':<10}")
    print(f"  {'─' * 75}")
    defaults = [
        ("Tomcat",        "admin",       "admin",          "8080"),
        ("Jenkins",       "admin",       "password",       "8080"),
        ("MySQL",         "root",        "(blank/none)",   "3306"),
        ("PostgreSQL",    "postgres",    "postgres",       "5432"),
        ("MongoDB",       "(none)",      "(none)",         "27017"),
        ("WordPress",     "admin",       "admin",          "80/443"),
        ("phpMyAdmin",    "root",        "(blank)",        "80/443"),
        ("Raspbian",      "pi",          "raspberry",      "22"),
    ]
    for prod, usr, pwd, port in defaults:
        print(f"  {prod:<25} {usr:<20} {pwd:<20} {port:<10}")
    print()

    print("  ✅ Pencegahan Security Misconfiguration:")
    print("     • Hapus/tidak menggunakan default credentials")
    print("     • Matikan directory listing di web server")
    print("     • Nonaktifkan debug/error reporting di production")
    print("     • Konfigurasi CORS secara ketat")
    print("     • Gunakan security headers (HSTS, X-Frame-Options, CSP)")
    print("     • Lakukan hardening checklist (CIS Benchmarks)")
    print()


# ── [7] Analogi ──
def analogi():
    print("""
   ╔══════════════════════════════════════════════════════════╗
   ║   🔑 KUNCI KAMAR SALAH (A1 — Broken Access Control)    ║
   ║      • Kunci hotel bisa buka kamar lain → IDOR          ║
   ║                                                        ║
   ║   🏷️ STIKER PASSWORD (A2 — Crypto Failure)              ║
   ║      • Password di stiker → plaintext storage           ║
   ║                                                        ║
   ║   💉 INJECTION (A3 — Injection)                        ║
   ║      • Nyuntikkan racun ke minuman → SQL injection     ║
   ║                                                        ║
   ║   🏗️ PONDASI RAPUH (A4 — Insecure Design)              ║
   ║      • Rumah dengan fondasi dari kardus — gampang roboh ║
   ║                                                        ║
   ║   🚪 PINTU TANPA KUNCI (A5 — Misconfiguration)         ║
   ║      • Pintu rumah tanpa kunci — siapa pun bisa masuk  ║
   ╚══════════════════════════════════════════════════════════╝
    """)


def main():
    banner()

    # ── [1] OWASP Overview ──
    section(1, "APA ITU OWASP TOP 10?")
    owasp_overview()

    # ── [2] A1 Broken Access Control ──
    section(2, "A1 — BROKEN ACCESS CONTROL / IDOR")
    a1_broken_access()

    # ── [3] A2 Crypto Failure ──
    section(3, "A2 — CRYPTOGRAPHIC FAILURES")
    a2_crypto_failure()

    # ── [4] A3 Injection ──
    section(4, "A3 — INJECTION")
    a3_injection()

    # ── [5] A4 Insecure Design ──
    section(5, "A4 — INSECURE DESIGN")
    a4_insecure_design()

    # ── [6] A5 Security Misconfiguration ──
    section(6, "A5 — SECURITY MISCONFIGURATION")
    a5_security_misconfig()

    # ── [7] Analogi ──
    section(7, "ANALOGI LENGKAP")
    analogi()

    # ── Summary ──
    print("=" * 60)
    print("  ✅ SESI 12 SELESAI!")
    print("=" * 60)
    print("  👉 Recap:")
    print("    • A1 Broken Access Control: IDOR — akses data orang lain via ID")
    print("    • A2 Crypto Failure: Jangan simpan password plaintext!")
    print("    • A3 Injection: Prepared statement = tameng utama")
    print("    • A4 Insecure Design: Security harus dari arsitektur")
    print("    • A5 Misconfiguration: Default creds, directory listing")
    print()
    print("  📌 LATIHAN LANJUTAN:")
    print("    1. Coba IDOR di DVWA: ubah parameter ID di URL")
    print("    2. Hash password sendiri: echo -n 'pass' | md5sum vs bcrypt")
    print("    3. SQL Injection di DVWA: ' OR '1'='1' --  ")
    print("    4. Cek CORS misconfig: curl -H 'Origin: evil.com' -I https://target.com")
    print("    5. Cari default credentials di Google: 'default password list'")
    print("    6. Test directory listing: curl https://target.com/backup/")
    print("    7. Baca OWASP Top 10 documentation resmi di owasp.org")
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
