#!/usr/bin/env python3
"""Sesi 9: Linux Server & Router Advanced — ARP, DoS, GDB, ROP"""

import subprocess
import sys
import os
import socket
import struct
import time


def banner():
    print("=" * 60)
    print("  ETHICAL ELITE HACKER v11 — Sesi 9")
    print("  Linux Server & Router Advanced")
    print("=" * 60)
    print("  Referensi: X-Code Ethical Elite Hacker v11")
    print("=" * 60)


def check_tool(name, cmd_flag=None):
    cmd = name if cmd_flag is None else cmd_flag
    try:
        subprocess.check_output([cmd, "--version"] if cmd != "which" else [cmd, name],
                                stderr=subprocess.STDOUT, timeout=5)
        return "✅ TERINSTAL"
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return "❌ TIDAK TERINSTAL"


def section(num, title):
    print(f"\n{'─' * 50}")
    print(f"  [{num}] {title}")
    print(f"{'─' * 50}")


def read_proc_net_tcp():
    """Baca koneksi TCP aktif dari /proc/net/tcp."""
    path = "/proc/net/tcp"
    print("  💡 Membaca koneksi TCP aktif dari sistem:\n")
    try:
        with open(path, "r") as f:
            lines = f.readlines()
        print(f"  {'Proto':<8} {'Local Address':<25} {'Remote Address':<25} {'Status':<12}")
        print(f"  {'─' * 70}")
        for line in lines[1:6]:  # first 5 connections
            parts = line.strip().split()
            if len(parts) < 4:
                continue
            local_ip_port = parts[1]
            rem_ip_port = parts[2]
            state_hex = parts[3]
            state_map = {
                "01": "ESTABLISHED", "02": "SYN_SENT", "03": "SYN_RECV",
                "04": "FIN_WAIT1",   "05": "FIN_WAIT2", "06": "TIME_WAIT",
                "07": "CLOSE",       "08": "CLOSE_WAIT", "09": "LAST_ACK",
                "0A": "LISTEN",      "0B": "CLOSING",
            }
            state = state_map.get(state_hex, f"0x{state_hex}")

            # Parse hex IP:port
            try:
                local_bytes = local_ip_port.split(":")[0]
                local_port = int(local_ip_port.split(":")[1], 16)
                local_ip = socket.inet_ntoa(bytes.fromhex(local_bytes.zfill(8))[::-1])
                local_str = f"{local_ip}:{local_port}"

                rem_bytes = rem_ip_port.split(":")[0]
                rem_port = int(rem_ip_port.split(":")[1], 16)
                if rem_bytes == "00000000":
                    rem_str = "0.0.0.0:0"
                else:
                    rem_ip = socket.inet_ntoa(bytes.fromhex(rem_bytes.zfill(8))[::-1])
                    rem_str = f"{rem_ip}:{rem_port}"
            except Exception:
                local_str = local_ip_port
                rem_str = rem_ip_port

            print(f"  {'TCP':<8} {local_str:<25} {rem_str:<25} {state:<12}")
        if len(lines) > 6:
            print(f"  ... dan {len(lines) - 6} koneksi lainnya (total: {len(lines) - 1})")
        print()
    except FileNotFoundError:
        print("  ⚠️  /proc/net/tcp tidak tersedia (bukan Linux)\n")
    except Exception as e:
        print(f"  ⚠️  Error membaca /proc/net/tcp: {e}\n")


def read_network_interfaces():
    """Baca interface network dari /sys/class/net/."""
    print("  💡 Interface jaringan tersedia:\n")
    try:
        ifaces = os.listdir("/sys/class/net/")
        print(f"  {'Interface':<15} {'Type':<20}")
        print(f"  {'─' * 35}")
        for iface in sorted(ifaces):
            try:
                with open(f"/sys/class/net/{iface}/type") as f:
                    iftype = f.read().strip()
                type_map = {"1": "Ethernet", "772": "Loopback", "512": "PPP", "65534": "Tunnel"}
                desc = type_map.get(iftype, f"Type {iftype}")
                print(f"  {iface:<15} {desc:<20}")
            except Exception:
                print(f"  {iface:<15} {'unknown':<20}")
        print()
    except FileNotFoundError:
        print("  ⚠️  /sys/class/net/ tidak tersedia\n")


def arp_spoofing_concept():
    """Konsep ARP Spoofing."""
    print("""
  💡 ARP Spoofing / ARP Poisoning:

  👉 ARP (Address Resolution Protocol): IP → MAC address
  👉 Attacker mengirim ARP reply palsu ke korban & gateway
  👉 Trafik korban lewat attacker (MITM)

  Alur:
    [Attacker]        [Gateway]         [Korban]
       |                  |                |
       |  ARP: 192.168.1.1 = MAC_Att     |  ← Atk ke Gateway
       |                  |  ARP: 192.168.1.2 = MAC_Att  → Korban
       |                  |                |
       |<══════ MITM: Semua trafik ══════>|

  Perintah aktual:
    echo 1 > /proc/sys/net/ipv4/ip_forward
    arpspoof -i eth0 -t 192.168.1.2 192.168.1.1
    arpspoof -i eth0 -t 192.168.1.1 192.168.1.2
    # Lalu jalankan Wireshark atau ettercap untuk capture
    """)


def dos_simulation():
    """Simulasi konsep DoS dengan socket."""
    print("  💡 Simulasi DoS/Socket Flood (konsep saja):\n")
    print(f"  {'Tipe DoS':<25} {'Cara':<40} {'Dampak':<30}")
    print(f"  {'─' * 95}")
    attacks = [
        ("SYN Flood",      "Kirim SYN terus-menerus",              "Backlog penuh"),
        ("ICMP Flood",     "Kirim ping flood",                     "Bandwidth habis"),
        ("HTTP Flood",     "Request GET/POST terus",                "CPU/Load tinggi"),
        ("UDP Flood",      "Kirim UDP random port",                "Resource habis"),
        ("Slowloris",      "Kirim HTTP partial",                   "Koneksi hung"),
    ]
    for name, method, impact in attacks:
        print(f"  {name:<25} {method:<40} {impact:<30}")
    print()

    # Simulasi socket send (non-blocking, konsep)
    print("  🔥 Contoh kode konsep SYN flood (jangan jalankan tanpa izin!):")
    print("""
    import socket, struct
    # Raw socket
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
    s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    # Kirim SYN paket terus-menerus ke target
    while True:
        packet = build_syn_packet(target_ip, spoofed_ip)
        s.sendto(packet, (target_ip, 0))
    """)


def gdb_demo():
    """GDB debugging concept."""
    print("  💡 GDB (GNU Debugger) untuk analisis exploit:\n")

    print(f"  {'Command GDB':<25} {'Fungsi':<45}")
    print(f"  {'─' * 70}")
    gdb_cmds = [
        ("gdb ./binary",      "Load binary di GDB"),
        ("run [args]",        "Jalankan program"),
        ("r < pattern.txt",   "Run dengan input pattern"),
        ("info registers",    "Lihat isi register (EIP, ESP, EAX..)"),
        ("x/10x $esp",        "Hex dump stack dari ESP"),
        ("x/s $esp",          "Lihat string di stack"),
        ("disas main",        "Disassemble fungsi main"),
        ("break *0x8048400",  "Set breakpoint di address"),
        ("continue",          "Lanjutkan eksekusi"),
        ("quit",              "Keluar GDB"),
    ]
    for cmd, desc in gdb_cmds:
        print(f"  {cmd:<25} {desc:<45}")
    print()

    print("  🔥 Pattern offset dengan GDB:")
    print("     $ gdb ./vuln")
    print("     (gdb) run <<< $(python3 -c 'print(\"A\"*72 + \"BBBB\")')")
    print("     (gdb) info registers  → EIP: 0x42424242 ('BBBB')")
    print()


def linux_exploit_concepts():
    """Linux exploit concepts."""
    print("""
  👉 Linux Exploit Concepts:

  ├── Stack Overflow  → Overwrite buffer di stack, kontrol EIP
  ├── Heap Overflow   → Overwrite chunk metadata di heap
  ├── Format String   → %x, %n untuk baca/tulis memory
  ├── Use-After-Free  → Akses memory setelah di-free
  ├── Integer Overflow→ Integer wraparound → alokasi kecil
  └── Race Condition  → Timing window antara check & use
    """)

    print(f"  {'Kerentanan':<20} {'Contoh':<30} {'Tool':<25}")
    print(f"  {'─' * 75}")
    vulns = [
        ("Stack Overflow",   "Buffer di stack",       "GDB, pwntools"),
        ("Heap Overflow",    "Fungsi malloc",          "libheap, pwntools"),
        ("Format String",    "printf(user_input)",     "GDB, fmtstr_payload"),
        ("UAF",              "Dangling pointer",       "pwntools, heapinfo"),
    ]
    for v, example, tools in vulns:
        print(f"  {v:<20} {example:<30} {tools:<25}")
    print()


def rop_bypass_demo():
    """ROP chain bypass concept."""
    print("  🔥 ROP Chain Bypass — Lanjutan dari Sesi 8\n")
    print("  ROP (Return-Oriented Programming):")
    print("  Menggunakan gadget 'ret' dari binary/libc untuk membangun chain.\n")

    print(f"  {'Tahap':<20} {'Deskripsi':<55}")
    print(f"  {'─' * 75}")
    stages = [
        ("Find Gadgets",   "Cari 'pop rdi; ret', 'system', '/bin/sh' dengan ROPgadget/objdump"),
        ("Leak libc",      "Panggil puts@plt(puts@got) → dapat base address libc"),
        ("Calc Addresses",  "system = base + offset_system, /bin/sh = base + offset_sh"),
        ("Build Chain",    "pop_rdi → addr_binsh → system → exit"),
        ("Exploit",        "Kirim chain → trigger overflow → shell"),
    ]
    for stage, desc in stages:
        print(f"  {stage:<20} {desc:<55}")
    print()

    print("  Chain layout di stack:")
    print("  ┌─────────────────────────────────────┐")
    print("  │ [padding: 72 bytes]                 │ ← buffer")
    print("  │ [EIP: pop_rdi_addr]                 │ ← kontrol EIP")
    print("  │ [arg: addr_binsh]                   │ ← arg untuk pop rdi")
    print("  │ [ret: system_addr]                  │ ← panggil system()")
    print("  │ [exit_addr]                         │ ← cleanup")
    print("  └─────────────────────────────────────┘")
    print()


def read_os_info():
    """Baca info OS."""
    try:
        with open("/etc/os-release") as f:
            data = f.read()
        for line in data.splitlines():
            if line.startswith("PRETTY_NAME="):
                os_name = line.split("=")[1].strip('"')
                print(f"  💡 OS: {os_name}")
                break
    except FileNotFoundError:
        print("  ⚠️  /etc/os-release tidak ditemukan")
    print()


def analogi():
    print("""
  ╔══════════════════════════════════════════════════════════╗
  ║   👮 MAMPERIN SATPAM (ARP Spoofing)                    ║
  ║      → Satpam diarahkan ke pintu palsu                 ║
  ║      → Attacker拦截 semua kiriman                       ║
  ║                                                        ║
  ║   📞 NELPON TERUS-TERUSAN (DoS)                       ║
  ║      → Telepon rumah diangkat terus tanpa bicara       ║
  ║      → Orang lain tidak bisa nelpon masuk              ║
  ║                                                        ║
  ║   🔧 BONGKAR MESIN (GDB)                              ║
  ║      → Buka mesin, lihat komponen dalamnya             ║
  ║      → Cari bagian yang bisa dimodifikasi              ║
  ╚══════════════════════════════════════════════════════════╝
    """)


def main():
    banner()

    # ── [1] Tool Check ──
    section(1, "PENGECEKAN TOOL")
    tools = {
        "gdb (debugger)": check_tool("gdb"),
        "arpspoof": check_tool("arpspoof", "arpspoof"),
        "tcpdump": check_tool("tcpdump", "tcpdump"),
        "hping3": check_tool("hping3", "hping3"),
        "nmap": check_tool("nmap", "nmap"),
        "python3": check_tool("python3", "python3"),
    }
    print(f"  {'Tool':<20} {'Status':<20}")
    print(f"  {'─' * 40}")
    for tool, status in tools.items():
        print(f"  {tool:<20} {status:<20}")
    print()

    # ── [2] System Info ──
    section(2, "INFO SISTEM")
    read_os_info()
    read_network_interfaces()

    # ── [3] Active TCP Connections ──
    section(3, "KONEKSI TCP AKTIF")
    read_proc_net_tcp()

    # ── [4] ARP Spoofing ──
    section(4, "ARP SPOOFING — MITM ATTACK")
    arp_spoofing_concept()

    # ── [5] DoS Simulation ──
    section(5, "DOS / DDOS — DENIAL OF SERVICE")
    dos_simulation()

    # ── [6] GDB Debugging ──
    section(6, "GDB DEBUGGING — ANALISIS EXPLOIT")
    gdb_demo()

    # ── [7] Linux Exploit Concepts ──
    section(7, "KONSEP EXPLOIT LINUX")
    linux_exploit_concepts()

    # ── [8] ROP Chain Bypass ──
    section(8, "ROP CHAIN BYPASS")
    rop_bypass_demo()

    # ── [9] Analogi ──
    section(9, "ANALOGI")
    analogi()

    # ── Summary ──
    print("=" * 60)
    print("  ✅ SESI 9 SELESAI!")
    print("=" * 60)
    print("  👉 Recap:")
    print("    • ARP Spoofing: MITM dengan memalsukan ARP")
    print("    • DoS: SYN flood, ICMP flood, HTTP flood")
    print("    • GDB: Debug binary, cari offset, kontrol EIP")
    print("    • Linux Exploit: Stack/Heap/Format String/UAF")
    print("    • ROP Chain: Bypass ASLR/DEP dengan gadget")
    print()
    print("  📌 LATIHAN LANJUTAN:")
    print("    1. Praktik ARP spoof dengan arpspoof + Wireshark di lab")
    print("    2. Coba hping3 untuk SYN flood (hanya di lab sendiri)")
    print("    3. Debug binary vulnerable dengan GDB + pwntools")
    print("    4. Buat ROP chain sederhana (ret2libc) di binary 32-bit")
    print("    5. Eksplorasi format string vulnerability di Linux")
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
