#!/usr/bin/env python3
"""Sesi 24: Career & Portfolio - Red/Blue Team, Sertifikasi"""
def banner():
    print("="*60)
    print("  SESI 24: KARIR & PORTFOLIO")
    print("  Analogi: STRIKER vs BEK, BAGIAN HUKUM")
    print("  Referensi: X-Code Ethical Elite Hacker v11")
    print("="*60)

def team_roles():
    print("\n[1] TIM KEAMANAN")
    roles = [
        ("🔴 Red Team", "Offensive", "Simulasi serangan, cari celah", "OSCP, GPEN"),
        ("🔵 Blue Team", "Defensive", "Monitor, deteksi, tangkis", "GCIA, CISSP"),
        ("🟣 Purple Team", "Kolaborasi", "Red+Blue kerja sama", "Semua"),
        ("🏢 SOC Analyst", "Monitor 24/7", "Pantau SIEM, respon insiden", "Security+, CySA+"),
        ("🎯 Pentester", "Ethical Hacking", "Tes penetrasi sistem", "OSCP, PNPT"),
        ("📋 GRC", "Governance", "Kebijakan, risiko, compliance", "CISA, CISM"),
        ("🔬 DFIR", "Forensik", "Investigasi setelah serangan", "GCFA, GCFE"),
    ]
    print(f"  {'Role':<16} {'Fokus':<15} {'Tugas':<25} {'Sertifikasi'}")
    print(f"  {'-'*70}")
    for r, f, t, s in roles:
        print(f"  {r:<16} {f:<15} {t:<25} {s}")

def career_path():
    print("\n[2] JALUR KARIR")
    print("  🟢 Entry Level (0-2 thn): SOC Analyst L1, Junior Pentester")
    print("     Gaji: Rp 5-15 jt/bln")
    print("  🟡 Mid Level (2-5 thn): Pentester, SOC L2, Security Engineer")
    print("     Gaji: Rp 15-30 jt/bln")
    print("  🔴 Senior (5+ thn): Lead Pentester, Security Manager, CISO")
    print("     Gaji: Rp 30-80+ jt/bln")
    print()
    print("  💡 TIPS: Jangan cuma fokus hacking!")
    print("     Networking, Linux, dan soft skill juga penting.")

def sertifikasi():
    print("\n[3] SERTIFIKASI")
    certs = [
        ("Pemula", "CompTIA Security+", "Dasar - 2-3 bulan", "$400"),
        ("Menengah", "CEH (EC-Council)", "Ethical Hacking - 3-6 bln", "$1,200"),
        ("Menengah", "OSCP (OffSec)", "Practical hacking - 6+ bln", "$1,600"),
        ("Lanjut", "PNPT (TCM)", "Full pentest - 3-6 bln", "$500"),
        ("Lanjut", "CISSP (ISC2)", "Manajemen keamanan - 6+ bln", "$700"),
        ("Expert", "OSED/OSEP", "Exploit dev/AD - 6+ bln", "$1,600"),
    ]
    print(f"  {'Level':<10} {'Sertifikasi':<20} {'Durasi':<20} {'Biaya'}")
    print(f"  {'-'*60}")
    for l, s, d, b in certs:
        print(f"  {l:<10} {s:<20} {d:<20} {b}")

def portfolio():
    print("\n[4] MEMBANGUN PORTFOLIO")
    print("  🎯 GitHub: Dokumentasi lab + writeup CTF")
    print("  🎯 LinkedIn: Connect dengan komunitas security")
    print("  🎯 CV: STAR format (Situation, Task, Action, Result)")
    print("  🎯 Blog: Tulis writeup & tutorial (Medium/GitHub Pages)")
    print("  🎯 CTF: Ikut CTF di CTFtime.org")
    print("  🎯 Bug Bounty: HackerOne, Bugcrowd, Synack")
    print()
    print("  💡 STAR INTERVIEW:")
    print("     S: Client minta tes keamanan aplikasi web")
    print("     T: Tes 20 endpoint dalam 1 minggu")
    print("     A: Scan + manual test, dapet 5 critical + 10 high")
    print("     R: Semua critical fixed dalam 3 hari")

def tips():
    print("\n[5] TIPS SUKSES")
    print("  🔥 Praktek > Teori. Lab setiap hari minimal 1 jam.")
    print("  🔥 Networking: Ikut komunitas (Discord, Telegram, Meetup)")
    print("  🔥 Soft skill: Cara jelasin temuan ke non-teknis")
    print("  🔥 Sertifikasi bagus, tapi pengalaman lebih penting")
    print("  🔥 Jangan pernah menyerah! Butuh waktu & konsistensi")

def main():
    banner(); team_roles(); career_path(); sertifikasi(); portfolio(); tips()
    print("\n"+"="*60)
    print("  ✅ SESI 24: KARIR & PORTFOLIO SELESAI!")
    print("  👉 Pilih jalur: Red/Blue/Purple/GRC/DFIR")
    print("  👉 Sertifikasi: Security+ -> OSCP -> CISSP")
    print("  👉 Bangun portfolio: GitHub + Blog + LinkedIn")
    print()
    print("  📌 ACTION PLAN:")
    print("  1. Bikin GitHub & push project ini")
    print("  2. Daftar CTFtime.org, ikut CTF pemula")
    print("  3. Daftar HackerOne/Bugcrowd cari program VDP")
    print("  4. Praktek rutin 1 jam/hari")
    print("  5. Target: Security+ (3 bulan) -> OSCP (6-12 bulan)")
    print("="*60)

if __name__ == "__main__": main()
