#!/usr/bin/env python3
"""Sesi 23: PTES - Penetration Testing Execution Standard"""
import subprocess
def banner():
    print("="*60)
    print("  SESI 23: PTES STANDARD")
    print("  Analogi: RESEP MASAK standar internasional")
    print("  Referensi: X-Code Ethical Elite Hacker v11")
    print("="*60)
def ptes_phases():
    print("\n[1] 7 FASE PTES")
    phases = [
        ("1", "Pre-Engagement", "Proposal, NDA, kontrak, rules of engagement",
         "DASAR: Sepak aturan main sebelum mulai"),
        ("2", "Intel Gathering", "OSINT, Shodan, Whois, DNS recon",
         "CARI: Kumpulin informasi target"),
        ("3", "Threat Modeling", "Identifikasi aset, vektor serangan, dampak bisnis",
         "PETA: Aset mana yang paling berharga?"),
        ("4", "Vulnerability Analysis", "Scan + verifikasi manual, false positive check",
         "CEK: Beneran celah apa cuma salah konfig?"),
        ("5", "Exploitation", "Proof of Concept - buktikan celah bisa dieksploitasi",
         "BUKTI: Tembus! Dapet akses!"),
        ("6", "Post-Exploitation", "Privilege Escalation, persistence, data exfil",
         "DAMPAK: Apa yang bisa dilakukan setelah masuk?"),
        ("7", "Reporting", "Laporan teknis (IT) + eksekutif (CEO)",
         "LAPOR: Surat ke CEO pake bahasa bisnis"),
    ]
    for n, name, desc, analogi in phases:
        print(f"  [{n}] {name:25} | {desc}")
        print(f"      💡 {analogi}")
def cvss():
    print("\n[2] CVSS SCORE (Common Vulnerability Scoring System)")
    print("  10 = Paling kritis, 0 = Tidak berbahaya")
    items = [
        ("0.1-3.9", "Low", "Info disclosure minor"),
        ("4.0-6.9", "Medium", "Bisa akses data terbatas"),
        ("7.0-8.9", "High", "Remote code execution possible"),
        ("9.0-10.0", "Critical", "Remote code execution tanpa auth"),
    ]
    print(f"  {'Score':<12} {'Level':<10} {'Contoh'}")
    print(f"  {'-'*45}")
    for s, l, c in items:
        print(f"  {s:<12} {l:<10} {c}")
def reporting():
    print("\n[3] STRUKTUR LAPORAN PTES")
    print("  📋 EXECUTIVE SUMMARY (untuk CEO/Manajemen)")
    print("     - Bahasa non-teknis")
    print("     - Dampak bisnis (duit, reputasi, legal)")
    print("     - Timeline & scope")
    print()
    print("  📋 TECHNICAL REPORT (untuk IT/Teknis)")
    print("     - Detail temuan per host")
    print("     - Screenshot & log")
    print("     - Steps to reproduce")
    print("     - Fix recommendation")
    print()
    print("  📋 APPENDIX")
    print("     - CVSS scores")
    print("     - Wordlist/scripts used")
    print("     - Tool versions")
    print("     - Scope & exclusions")
def tools_ptes():
    print("\n[4] TOOLS PER FASE")
    phase_tools = [
        ("Intel", "theHarvester, Maltego, Shodan, Recon-ng"),
        ("Scan", "Nmap, Nessus, OpenVAS, Nuclei"),
        ("Exploit", "Metasploit, Burp Suite, SQLmap"),
        ("Post-Exploit", "Mimikatz, BloodHound, Impacket"),
        ("Report", "Dradis, Faraday, Serpico"),
    ]
    for phase, tools in phase_tools:
        print(f"  📌 {phase:15} → {tools}")
def main():
    banner(); ptes_phases(); cvss(); reporting(); tools_ptes()
    print("\n"+"="*60)
    print("  ✅ SESI 23: PTES STANDARD SELESAI!")
    print("  👉 7 fase: Pre-engagement → Reporting")
    print("  👉 CVSS scoring: 0-10")
    print("  👉 Laporan: Eksekutif + Teknis")
    print("  📌 LATIHAN: 1. Buat NDA & RoE template")
    print("  📌 LATIHAN: 2. Hitung CVSS temuan sendiri")
    print("  📌 LATIHAN: 3. Praktek 1 full pentest cycle")
    print("="*60)
if __name__ == "__main__": main()
