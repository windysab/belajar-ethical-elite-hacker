#!/usr/bin/env python3
"""
Sesi 22: Wireless Hacking
Mendalami keamanan jaringan nirkabel: enkripsi, serangan, dan pertahanan
Referensi: X-Code Ethical Elite Hacker v11
"""

import subprocess
import os
import sys
import socket
import struct
import re
from collections import defaultdict

# ============================================================
# BANNER
# ============================================================
def banner():
    print("=" * 60)
    print("  ETHICAL ELITE HACKER v11 — SESI 22")
    print("  Topik: Wireless Hacking & Keamanan Nirkabel")
    print("=" * 60)
    print()


# ============================================================
# [1] CEK WIRELESS TOOLS
# ============================================================
def cek_wireless_tools():
    """Memeriksa ketersediaan tool wireless hacking di sistem."""
    print("[1] CEK TOOL WIRELESS HACKING")
    print("-" * 60)

    tools = {
        'aircrack-ng': 'Aircrack-ng — WEP/WPA cracking suite',
        'airmon-ng':   'Airmon-ng — monitor mode controller',
        'airodump-ng': 'Airodump-ng — packet capture WiFi',
        'aireplay-ng': 'Aireplay-ng — packet injection',
        'airbase-ng':  'Airbase-ng — fake AP (Evil Twin)',
        'macchanger':  'Macchanger — MAC address manipulation',
        'reaver':      'Reaver — WPS brute force attack',
        'wash':        'Wash — WPS scan tool',
        'mdk3':        'MDK3 — deauth & beacon flooding',
        'mdk4':        'MDK4 — improved deauth & DoS',
        'hostapd':     'Hostapd — Access Point daemon',
        'dnsmasq':     'Dnsmasq — DHCP/DNS server ringan',
        'hashcat':     'Hashcat — GPU-accelerated password cracker',
        'hcxdumptool': 'Hcxdumptool — PMKID capture tool',
        'hcxpcapngtool': 'Hcxpcapngtool — convert pcapng to hashcat',
    }

    print(f"{'TOOL':<20} {'STATUS':<10} DESKRIPSI")
    print("-" * 60)
    tersedia = 0
    tidak_tersedia = []

    for tool, desc in tools.items():
        ret = subprocess.run(
            ['which', tool],
            capture_output=True, text=True
        )
        if ret.returncode == 0:
            # Coba dapatkan versi
            versi_ret = subprocess.run(
                [tool, '--version'] if tool != 'hashcat' else [tool, '--version'],
                capture_output=True, text=True, timeout=5
            )
            versi = versi_ret.stdout.strip().split('\n')[0][:30] if versi_ret.stdout else 'OK'
            print(f"{tool:<20} {'✅ ADA':<10} {versi}")
            tersedia += 1
        else:
            print(f"{tool:<20} {'❌ TIDAK':<10} {desc}")
            tidak_tersedia.append(tool)

    print()
    print(f"  ✅ {tersedia}/{len(tools)} tools tersedia")
    if tidak_tersedia:
        print(f"  ❌ Tidak tersedia: {', '.join(tidak_tersedia)}")
        print(f"  💡 Install: sudo apt install aircrack-ng reaver mdk3 mdk4 hostapd dnsmasq macchanger hashcat hcxtools")
    print()


# ============================================================
# [2] BAND FREKUENSI WiFi
# ============================================================
def bahas_band_frekuensi():
    """Penjelasan tentang band WiFi: 2.4GHz, 5GHz, 6GHz."""
    print("[2] BAND FREKUENSI WiFi")
    print("-" * 60)

    bands = [
        ("2.4 GHz", "802.11b/g/n/ax", "2400-2483 MHz",
         "Jangkauan jauh, tembus dinding", "Rawan interferensi (Bluetooth, microwave)",
         "1-11 (14)"),
        ("5 GHz", "802.11a/n/ac/ax", "5150-5850 MHz",
         "Kecepatan tinggi, kurang interferensi", "Jangkauan pendek, kurang tembus",
         "36-165"),
        ("6 GHz", "802.11ax (WiFi 6E)", "5925-7125 MHz",
         "Sangat cepat, sangat bersih", "Jangkauan sangat pendek",
         "1-233"),
    ]

    print(f"{'BAND':<12} {'STANDAR':<18} {'FREKUENSI':<20} {'KELEBIHAN':<30} {'KEKURANGAN':<30} {'CHANNEL':<12}")
    print("-" * 122)
    for band, std, freq, plus, minus, ch in bands:
        print(f"{band:<12} {std:<18} {freq:<20} {plus:<30} {minus:<30} {ch:<12}")

    print()
    print("  💡 WiFi 6E (6 GHz) adalah yang paling aman dari serangan deauth")
    print("  💡 2.4 GHz paling rentan karena banyak perangkat IoT using it")
    print()
    print("  🔥 Analogi: SINYAL RADIO")
    print("     AM (2.4 GHz) — jangkauan jauh, kualitas buruk, banyak noise")
    print("     FM (5 GHz)  — lebih jernih, jarak terbatas")
    print("     Digital (6 GHz) — kualitas tertinggi, jangkauan paling pendek")
    print()


# ============================================================
# [3] EVOLUSI ENKRIPSI WiFi
# ============================================================
def bahas_enkripsi_wifi():
    """Penjelasan evolusi enkripsi dari WEP ke WPA3."""
    print("[3] EVOLUSI ENKRIPSI WiFi")
    print("-" * 60)

    print("  Dari WEP → WPA → WPA2 → WPA3 — Evolusi Keamanan Nirkabel\n")

    enkripsi = [
        ("WEP",  "1997", "RC4", "64/128 bit", "Statis",
         "❌ SANGAT RENTAN", "Crack < 5 menit"),
        ("WPA",  "2003", "TKIP/RC4", "256 bit", "Dinamis (PTK)",
         "❌ RENTAN", "Crack via dictionary"),
        ("WPA2", "2004", "CCMP/AES", "128-256 bit", "4-Way Handshake (PSK/802.1X)",
         "⚠️ AMAN (dengan password kuat)", "Rentan brute force"),
        ("WPA3", "2018", "GCMP-256/AES", "256 bit", "SAE (Simultaneous Auth of Equals)",
         "✅ SANGAT AMAN", "Belum ada crack publik"),
    ]

    print(f"{'METODE':<8} {'TAHUN':<8} {'ALGORITMA':<15} {'PANJANG KUNCI':<18} {'AUTH PROTOCOL':<30} {'KEAMANAN':<30} {'KERENTANAN':<25}")
    print("-" * 134)
    for nama, tahun, algo, panjang, auth, aman, rentan in enkripsi:
        print(f"{nama:<8} {tahun:<8} {algo:<15} {panjang:<18} {auth:<30} {aman:<30} {rentan:<25}")

    print()
    print("  🔥 Detail Kerentanan per Metode:\n")

    print("  ┌─ WEP — GEMBOK PLASTIK")
    print("  │  • Initialization Vector (IV) 24-bit — habis dalam 5 menit")
    print("  │  • RC4 + CRC32 — bisa dimanipulasi (bit-flip attack)")
    print("  │  • IV collision → reveal keystream → dapat kunci")
    print("  │  • Aircrack-ng: kumpulkan ~5000-20000 IV → crack dalam detik")
    print("  │  • Tools: aircrack-ng, aircrack-ptw, chopchop attack")
    print()
    print("  ┌─ WPA — GEMBOK BESI (berkarat)")
    print("  │  • TKIP masih pake RC4 — diperbaiki dengan per-message key mixing")
    print("  │  • 4-Way Handshake: 4 frame kritis yang bisa dicapture")
    print("  │  • Michael MIC: bisa di-bypass dengan fragmentation attack")
    print("  │  • Crack: tangkap handshake → dictionary attack")
    print()
    print("  ┌─ WPA2 — GEMBOK BESI (masih kuat)")
    print("  │  • AES-CCMP — standar enkripsi militer")
    print("  │  • Kerentanan utama: PSK dictionary attack via handshake capture")
    print("  │  • PMKID attack: tanpa client, langsung dari AP")
    print("  │  • KRACK Attack (2017): bypass WPA2 via nonce reuse")
    print()
    print("  ┌─ WPA3 — GEMBOK BIOMETRIK")
    print("  │  • SAE (Simultaneous Authentication of Equals) — Dragonfly handshake")
    print("  │  • Forward secrecy: kunci baru setiap sesi")
    print("  │  • Protected Management Frames (802.11w) — anti deauth")
    print("  │  • Dragonblood (2019): timing attack, downgrade attack — sudah di-patch")
    print()


# ============================================================
# [4] 4-WAY HANDSHAKE DETAIL
# ============================================================
def bahas_4way_handshake():
    """Penjelasan detail 4-Way Handshake WPA/WPA2."""
    print("[4] 4-WAY HANDSHAKE — WPA/WPA2 Authentication")
    print("-" * 60)

    print("  Langkah-langkah:\n")
    handshake = [
        ("1", "AP → Client", "Nonce AP (ANonce)",
         "AP mengirimkan nonce-nya (angka acak)"),
        ("2", "Client → AP", "Nonce Client (SNonce) + MIC",
         "Client membalas: SNonce + Message Integrity Code (MIC)"),
        ("3", "AP → Client", "GTK + MIC (dengan ANonce+SNonce)",
         "AP mengirim kunci grup (GTK) untuk broadcast/multicast"),
        ("4", "Client → AP", "ACK (confirm)",
         "Client konfirmasi: \"Saya sudah punya kunci!\""),
    ]

    print(f"{'LANGKAH':<10} {'ARAH':<18} {'ISI':<30} {'PENJELASAN':<50}")
    print("-" * 108)
    for langkah, arah, isi, penjelasan in handshake:
        print(f"{langkah:<10} {arah:<18} {isi:<30} {penjelasan:<50}")

    print()
    print("  🔥 Kenapa ini penting?")
    print("     • Jika kita capture ke-4 frame ini → PSK bisa di-brute force")
    print("     • MIC di frame-2 bisa diverifikasi secara offline")
    print("     • Tools: airodump-ng -c <ch> --bssid <MAC> -w capture wlan0mon")
    print("     • Deauth attack: paksa client reconnect → capture handshake")
    print()
    print("  💡 PMKID Attack (hashcat -m 16800):")
    print("     • Tidak perlu menunggu handshake lengkap")
    print("     • Cukup frame pertama dari AP ke client")
    print("     • Disimpan dalam RSN IE (Robust Security Network IE)")
    print("     • Tools: hcxdumptool + hcxpcapngtool + hashcat")
    print()


# ============================================================
# [5] WPS ATTACK (PIXIE DUST & PIN BRUTE FORCE)
# ============================================================
def bahas_wps_attack():
    """Penjelasan tentang WPS dan kerentanannya."""
    print("[5] WPS — WiFi Protected Setup (Pintu Belakang)")
    print("-" * 60)

    print("  WPS = Fitur \"mudah\" konek — LANGSUNG MASALAH!\n")
    print("  ╔═══════════════════════════════════════════════════════════════╗")
    print("  ║  WPS PIN: 8 digit (sebenarnya 7 digit + 1 digit checksum)    ║")
    print("  ║  Total kombinasi: 10^7 = 10 JUTA (bukan 10^8)               ║")
    print("  ║  Tapi dibagi 2 sesi (3 digit pertama + 4 digit kedua)        ║")
    print("  ║  Maka: 10^3 + 10^4 = 11.000 percobaan MAX                   ║")
    print("  ║  Waktu: 11.000 × ~1 detik ≈ 3 jam                           ║")
    print("  ║  Dengan Pixie Dust: hitungan DETIK!                          ║")
    print("  ╚═══════════════════════════════════════════════════════════════╝\n")

    print("  ┌─ PIXIE DUST ATTACK")
    print("  │  • Eksploitasi kelemahan random number generator (RNG)")
    print("  │  • Beberapa AP menggunakan RNG lemah → ES/SK bisa ditebak")
    print("  │  • ES = Enrollee Nonce, SK = Session Key")
    print("  │  • Tools: reaver -K 1 (Pixie Dust)")
    print("  │  • Berhasil dalam < 60 detik pada AP rentan")
    print()
    print("  ┌─ PIN BRUTE FORCE (standard)")
    print("  │  • reaver -i wlan0mon -b <BSSID> -vv")
    print("  │  • Butuh 3-10 jam tergantung kecepatan AP")
    print("  │  • Bisa diakselerasi: -l 5 (delay antar percobaan)")
    print("  │  • WPS lockout: 5 gagal → AP lock 5 menit")
    print()
    print("  ┌─ PENCEGAHAN WPS")
    print("  │  • 🔥 MATIKAN WPS di router! (bukan hanya disable via web)")
    print("  │  • Gunakan flash firmware alternatif (OpenWrt, DD-WRT, Tomato)")
    print("  │  • AP modern: WPS lockout setelah 3 gagal percobaan")
    print("  │  • WPA3: WPS sudah dihapus dari standar")
    print("  │  • Cek dengan: wash -i wlan0mon")
    print()


# ============================================================
# [6] EVIL TWIN ATTACK
# ============================================================
def bahas_evil_twin():
    """Penjelasan tentang Evil Twin attack."""
    print("[6] EVIL TWIN — Kembaran Jahat")
    print("-" * 60)

    print("  Evil Twin: Access Point palsu yang meniru AP asli\n")
    print("  ┌─ LANGKAH-LANGKAH:")
    print("  │  1. Scan AP target (airodump-ng)")
    print("  │  2. Matikan interface dari network manager")
    print("  │  3. Buat AP palsu (airbase-ng atau hostapd)")
    print("  │  4. Set DNS spoofing (dnsmasq)")
    print("  │  5. Deauth client dari AP asli")
    print("  │  6. Client otomatis connect ke Evil Twin")
    print("  │  7. Tangkap semua traffic (MITM)")
    print()
    print("  ┌─ ALAT UNTUK EVIL TWIN:")
    print("  │  airbase-ng:")
    print("  │    airbase-ng -e \"WiFi_Gratis\" -c 1 wlan0mon")
    print("  │")
    print("  │  hostapd (lebih stabil):")
    print("  │    # /etc/hostapd/hostapd.conf")
    print("  │    interface=wlan0")
    print("  │    driver=nl80211")
    print("  │    ssid=EvilTwin_WiFi")
    print("  │    hw_mode=g")
    print("  │    channel=6")
    print("  │    macaddr_acl=0")
    print("  │    auth_algs=1")
    print("  │    ignore_broadcast_ssid=0")
    print()
    print("  ┌─ DNS SPOOFING (dnsmasq):")
    print("  │  Semua DNS request dialihkan ke IP attacker")
    print("  │  → Halaman phishing banking, email, social media")
    print("  │  → Capture credentials (mitmproxy, ettercap)")
    print()
    print("  💡 Pencegahan: verifikasi sertifikat SSL/TLS!")
    print("  💡 Evil Twin tidak bisa spoof HTTPS dengan valid cert")
    print("  💡 Gunakan VPN jika menggunakan WiFi publik")
    print()


# ============================================================
# [7] MAC FILTER BYPASS
# ============================================================
def bahas_mac_filter():
    """Penjelasan bypass MAC filter."""
    print("[7] MAC FILTER BYPASS")
    print("-" * 60)

    print("  ╔═══════════════════════════════════════════════════════════════╗")
    print("  ║  MAC Filter = ILUSI KEAMANAN — bukan perlindungan!           ║")
    print("  ╚═══════════════════════════════════════════════════════════════╝\n")

    print("  ┌─ CARA BYPASS:")
    print("  │  1. Monitor mode: airodump-ng wlan0mon")
    print("  │  2. Catat MAC client yang terhubung (STATION)")
    print("  │  3. Deauth client tersebut")
    print("  │  4. Ganti MAC kita ke MAC client: macchanger -m <MAC> wlan0")
    print("  │  5. Connect ke AP — seolah-olah client asli")
    print("  │  6. Ulangi untuk setiap client yang terdaftar")
    print()
    print("  ┌─ COMMAND:")
    print("  │  # Matikan interface")
    print("  │  sudo ip link set wlan0 down")
    print("  │  # Ganti MAC")
    print("  │  sudo macchanger -m 00:11:22:33:44:55 wlan0")
    print("  │  # Hidupkan kembali")
    print("  │  sudo ip link set wlan0 up")
    print("  │  # Verifikasi")
    print("  │  macchanger -s wlan0")
    print()
    print("  ┌─ DETEKSI MAC SPOOFING (dari sisi defender):")
    print("  │  • Sequence number anomaly — MAC asli punya pola seq number")
    print("  │  • Ap scanning — 2 perangkat dengan MAC sama ≠ normal")
    print("  │  • OUI database — vendor tidak cocok dengan device")
    print()
    print("  💡 MAC filtering hanya menghambat user pemula")
    print("  💡 Gunakan WPA3-Enterprise + 802.1X sebagai gantinya")
    print()


# ============================================================
# [8] DEAUTH ATTACK
# ============================================================
def bahas_deauth():
    """Penjelasan tentang deauthentication attack."""
    print("[8] DEAUTH ATTACK — Pemutus Koneksi")
    print("-" * 60)

    print("  Deauth attack: mengirim frame deauthentication palsu ke client\n")
    print("  ┌─ BAGAIMANA CARA KERJANYA:")
    print("  │  • WiFi management frames TIDAK dienkripsi (pre-802.11w)")
    print("  │  • Attacker bisa memalsukan MAC AP → kirim deauth ke client")
    print("  │  • Client yang terima: \"oh, AP suruh disconnect...\"")
    print("  │  → Client reconnect → kita capture handshake")
    print()
    print("  ┌─ TOOLS:")
    print("  │  # aireplay-ng — deauth satu client (targeted)")
    print("  │  aireplay-ng -0 5 -a <AP_MAC> -c <CLIENT_MAC> wlan0mon")
    print("  │  # -0 = deauth count, -a = AP BSSID, -c = client MAC")
    print("  │")
    print("  │  # mdk3 / mdk4 — deauth massal (all clients)")
    print("  │  mdk3 wlan0mon d -b blacklist.txt")
    print("  │  mdk4 wlan0mon d -b blacklist.txt")
    print("  │")
    print("  │  # MDK4 Beacon Flood — buat 1000+ AP palsu")
    print("  │  mdk4 wlan0mon b -a -t 00:11:22:33:44:55")
    print()
    print("  ┌─ PENCEGAHAN:")
    print("  │  • 802.11w (Protected Management Frames) — WAJIB diaktifkan")
    print("  │  • WPA3 mewajibkan PMF — anti deauth")
    print("  │  • Monitor: tcpdump / wireshark untuk deteksi deauth flood")
    print("  │  • IDS Signatures: deauth rate > 10/s dalam 1 menit = serangan")
    print()


# ============================================================
# [9] CEK WIRELESS INTERFACE
# ============================================================
def cek_wireless_interface():
    """Memeriksa interface wireless dan mode monitoring."""
    print("[9] CEK WIRELESS INTERFACE & MODE")
    print("-" * 60)

    # Cek interface via /sys/class/net
    interfaces = []
    try:
        for iface in os.listdir('/sys/class/net/'):
            path = f'/sys/class/net/{iface}'
            if os.path.isdir(path):
                # Cek apakah wireless
                wlan_path = f'{path}/wireless'
                if os.path.isdir(wlan_path):
                    interfaces.append(iface)
    except FileNotFoundError:
        pass

    if not interfaces:
        # Fallback: cari dengan iwconfig
        ret = subprocess.run(['iwconfig'], capture_output=True, text=True)
        if ret.stdout:
            for line in ret.stdout.split('\n'):
                if 'IEEE 802.11' in line:
                    iface = line.split()[0]
                    interfaces.append(iface)

    if interfaces:
        print(f"  ✅ Ditemukan {len(interfaces)} interface wireless:\n")
        for iface in interfaces:
            print(f"  ┌─ Interface: {iface}")
            # Info dari /sys/class/net
            addr_path = f'/sys/class/net/{iface}/address'
            if os.path.exists(addr_path):
                with open(addr_path) as f:
                    mac = f.read().strip()
                print(f"  │  MAC Address: {mac}")
            # Cek operstate
            state_path = f'/sys/class/net/{iface}/operstate'
            if os.path.exists(state_path):
                with open(state_path) as f:
                    state = f.read().strip()
                print(f"  │  Status: {state}")
            # Coba airmon-ng
            ret = subprocess.run(
                ['airmon-ng', 'check'],
                capture_output=True, text=True
            )
            if ret.returncode == 0:
                lines = [l for l in ret.stdout.split('\n') if iface in l]
                for l in lines:
                    print(f"  │  Airmon: {l.strip()}")
            print()
    else:
        print("  ❌ Tidak ada interface wireless terdeteksi")
        print("  💡 Pasang USB WiFi adapter + driver yang compatible")
        print()

    print("  ┌─ KOMPATIBILITAS CHIPSET WIRELESS:")
    print("  │  ✅ Recommended untuk hacking:")
    print("  │     • Atheros AR9271 (USB) — monitor mode + injection ✅")
    print("  │     • Ralink RT3070 (USB) — monitor mode + injection ✅")
    print("  │     • Realtek RTL8812AU (USB) — 5GHz + monitor ✅")
    print("  │     • Intel AX200/AX210 — monitor mode terbatas ⚠️")
    print("  │")
    print("  │  ❌ Tidak recommended:")
    print("  │     • Broadcom BCM43xx — driver proprietary, susah injection")
    print("  │     • Realtek RTL8821CE — driver bermasalah")
    print("  │     • Qualcomm QCA9377 — monitor mode terbatas")
    print()


# ============================================================
# [10] SISTEM PENCEGAHAN WIRELESS
# ============================================================
def bahas_pencegahan():
    """Rekomendasi pencegahan serangan wireless."""
    print("[10] PENCEGAHAN & HARDENING WIRELESS")
    print("-" * 60)

    print("  ╔═══════════════════════════════════════════════════════════════╗")
    print("  ║  BUKAN \"APAKAH BISA DIHACK?\" TAPI \"SEBERAPA SULIT?\"           ║")
    print("  ╚═══════════════════════════════════════════════════════════════╝\n")

    print("  ┌─ REKOMENDASI KEAMANAN:")
    print("  │")
    print("  │  1. Gunakan WPA3 jika perangkat mendukung")
    print("  │     • SAE handshake — anti dictionary attack")
    print("  │     • Forward secrecy — decrypt 1 sesi tidak reveal lainnya")
    print("  │     • PMF (Protected Management Frames) wajib — anti deauth")
    print("  │")
    print("  │  2. Jika harus WPA2, gunakan password STRONG:")
    print("  │     • Minimal 16 karakter")
    print("  │     • Campuran: huruf besar, kecil, angka, simbol")
    print("  │     • BUKAN: tanggal lahir, nama, qwerty12345")
    print("  │     • Contoh: G7k#mP9$xL2@vR!q")
    print("  │")
    print("  │  3. MATIKAN WPS")
    print("  │     • Cek via: wash -i wlan0mon")
    print("  │     • Jika nyala: matikan dari web interface AP")
    print("  │     • Flash firmware alternatif jika WPS tidak bisa dimatikan")
    print("  │")
    print("  │  4. Aktifkan 802.11w (Protected Management Frames)")
    print("  │     • Di router: Wireless → Security → PMF = Required")
    print("  │     • Blokir semua management frame yang tidak terautentikasi")
    print("  │")
    print("  │  5. Nonaktifkan SSID Broadcast?")
    print("  │     • Percuma: SSID tetap terlihat di probe request")
    print("  │     • Tools tetap bisa menemukan SSID tersembunyi")
    print("  │")
    print("  │  6. MAC Filter?")
    print("  │     • Hanya menghambat — bypass dalam 2 menit")
    print("  │     • Cocok untuk parental control, bukan security")
    print("  │")
    print("  │  7. Update firmware router secara rutin")
    print("  │     • Cek situs vendor: TP-Link, Asus, MikroTik, Ubiquiti")
    print("  │     • Atau install OpenWrt untuk update berkelanjutan")
    print("  │")
    print("  │  8. Gunakan Enterprise (802.1X) jika memungkinkan")
    print("  │     • Radius server — tiap user punya kredensial sendiri")
    print("  │     • LEAP ❌ (deprecated), EAP-TLS ✅, EAP-PEAP ✅")
    print()

    print("  ┌─ PERBANDINGAN TINGKAT KEAMANAN:")
    print(f"{'METODE':<22} {'KEAMANAN':<20} {'WAKTU CRACK':<25} {'KETERANGAN':<30}")
    print("-" * 97)
    print(f"{'WEP 64-bit':<22} {'❌ SANGAT RENDAH':<20} {'< 1 menit':<25} {'IV collision attack':<30}")
    print(f"{'WEP 128-bit':<22} {'❌ SANGAT RENDAH':<20} {'< 5 menit':<25} {'Lebih banyak IV needed':<30}")
    print(f"{'WPA TKIP':<22} {'❌ RENDAH':<20} {'Jam-hari':<25} {'Dictionary attack':<30}")
    print(f"{'WPA2 AES':<22} {'⚠️ SEDANG':<20} {'Hari-bulan':<25} {'Tergantung password':<30}")
    print(f"{'WPA2 + PMF':<22} {'✅ AMAN':<20} {'Hari-bulan':<25} {'Anti deauth, masih PSK':<30}")
    print(f"{'WPA3 SAE':<22} {'✅ SANGAT AMAN':<20} {'? - unknown':<25} {'Belum ada crack publik':<30}")
    print(f"{'WPA3-Ent 192bit':<22} {'✅✅ MILITER':<20} {'Tidak praktis':<25} {'Suite B cryptography':<30}")
    print()


# ============================================================
# [11] WIRELESS ATTACK FLOWCHART
# ============================================================
def bahas_attack_flow():
    """Diagram alur serangan wireless."""
    print("[11] FLOWCHART SERANGAN WIRELESS")
    print("-" * 60)

    print("""
  ┌──────────────────────────┐
  │  TARGET IDENTIFICATION   │
  │  airodump-ng wlan0mon    │
  └─────────┬────────────────┘
            │
            ▼
  ┌──────────────────────────┐
  │  ENCRYPTION ANALYSIS     │
  │  WEP? WPA? WPA2? WPA3?   │
  └──┬───────┬───────┬───────┘
     │       │       │
     ▼       ▼       ▼
  ┌────┐ ┌──────┐ ┌──────┐
  │WEP │ │WPA2  │ │WPA3  │
  │IV  │ │Hand- │ │???   │
  │Cap │ │shake │ │(sulit)│
  └─┬──┘ └──┬───┘ └──┬───┘
    │       │        │
    ▼       ▼        │
  ┌────┐ ┌──────┐    │
  │Arc-│ │Word- │    │
  │rack│ │list  │    │
  └────┘ └──────┘    │
    │       │        │
    ▼       ▼        ▼
  ┌──────────────────────────┐
  │  ACCESS GAINED!          │
  │  ↓                       │
  │  Post-Exploitation       │
  │  MITM / Spoofing / Data  │
  └──────────────────────────┘
  """)


# ============================================================
# [12] Cek sistem untuk info wireless
# ============================================================
def cek_sistem_wireless():
    """Mengumpulkan info tentang sistem yang berkaitan dengan wireless."""
    print("[12] INFO SISTEM TERKAIT WIRELESS")
    print("-" * 60)

    # Cek /proc/version
    try:
        with open('/proc/version', 'r') as f:
            version = f.read().strip()
            print(f"  🖥  Kernel: {version[:80]}")
    except Exception as e:
        print(f"  ❌ Gagal baca /proc/version: {e}")

    # Cek OS
    try:
        with open('/etc/os-release', 'r') as f:
            for line in f:
                if line.startswith('PRETTY_NAME='):
                    os_name = line.split('=')[1].strip().strip('"')
                    print(f"  💻 OS: {os_name}")
                    break
    except Exception as e:
        print(f"  ❌ Gagal baca OS: {e}")

    # Cek modul kernel wireless
    print()
    ret = subprocess.run(
        ['lsmod'], capture_output=True, text=True
    )
    wireless_modules = [
        'mac80211', 'cfg80211', 'ath9k', 'ath9k_htc', 'rt2800usb',
        'rtl88x2ce', 'rtl8xxxu', 'iwlwifi', 'iwldvm', 'iwlmvm',
        'brcmfmac', 'wl'
    ]
    print("  📡 Modul Kernel Wireless:")
    for mod in wireless_modules:
        if mod in ret.stdout:
            print(f"     ✅ {mod} — terdeteksi (loaded)")
    print("     💡 lsmod | grep -E 'wifi|wireless|802' untuk detail")


# ============================================================
# MAIN
# ============================================================
def main():
    banner()

    try:
        cek_wireless_tools()
    except Exception as e:
        print(f"  ❌ Error cek tools: {e}")

    print()
    try:
        cek_wireless_interface()
    except Exception as e:
        print(f"  ❌ Error cek interface: {e}")

    print()
    try:
        cek_sistem_wireless()
    except Exception as e:
        print(f"  ❌ Error sistem: {e}")

    print()
    bahas_band_frekuensi()
    bahas_enkripsi_wifi()
    bahas_4way_handshake()
    bahas_wps_attack()
    bahas_evil_twin()
    bahas_mac_filter()
    bahas_deauth()
    bahas_pencegahan()
    bahas_attack_flow()

    # ============================================================
    # RECAP & LATIHAN
    # ============================================================
    print("=" * 60)
    print("  ✅ SESI 22 SELESAI!")
    print("=" * 60)
    print()
    print("  👉 RECAP:")
    print("     • Band WiFi: 2.4 GHz (jauh, padat) vs 5 GHz (cepat, pendek) vs 6 GHz")
    print("     • Enkripsi: WEP ❌ → WPA ⚠️ → WPA2 ✅ → WPA3 ✅✅")
    print("     • 4-Way Handshake: 4 frame untuk autentikasi WPA/WPA2")
    print("     • WPS: backdoor — Pixie Dust crack dalam detik")
    print("     • Evil Twin: AP palsu untuk MITM + credential harvesting")
    print("     • MAC Filter: ilusi keamanan — bypass dengan macchanger")
    print("     • Deauth: management frame tidak dienkripsi → flood")
    print("     • Pencegahan utama: WPA3 + PMF + password kuat + matikan WPS")
    print()
    print("  📌 LATIHAN LANJUTAN:")
    print("     1. Install aircrack-ng dan cek mode monitor di USB WiFi")
    print("     2. Scan jaringan WiFi sekitar: airodump-ng wlan0mon")
    print("     3. Capture WPA handshake: deauth + capture + crack dengan wordlist")
    print("     4. Uji WPS: wash -i wlan0mon, lalu reaver jika AP rentan")
    print("     5. Simulasi Evil Twin: hostapd + dnsmasq + deauth")
    print("     6. Bypass MAC filter: deauth client, spoof MAC, reconnect")
    print("     7. Cek PMF di AP sekitar: airodump-ng --wps --pmk")
    print("     8. Upgrade router ke OpenWrt jika firmware vendor usang")
    print()

    print("  🔥 Analogi Akhir: Jaringan Wireless = POS RONDA")
    print("     • WEP = satpam tidur (gampang dilewati)")
    print("     • WPA = satpam bangun tapi bawa pentungan bambu")
    print("     • WPA2 = satpam bawa pistol + CCTV")
    print("     • WPA3 = satpam + 3 kali pengecekan + anjing pelacak + AI")
    print("     • Anda mau jadi penjaga yang mana? 🛡️")
    print()


if __name__ == '__main__':
    main()
