#!/usr/bin/env python3
"""Sesi 22: Wireless Hacking - WEP/WPA, Evil Twin"""
import subprocess
def banner():
    print("="*60)
    print("  SESI 22: WIRELESS HACKING")
    print("  Analogi: SINYAL RADIO - siapa pun bisa dengar")
    print("  Referensi: X-Code Ethical Elite Hacker v11")
    print("="*60)
def wifi_concept():
    print("\n[1] KONSEP DASAR WiFi")
    print("  📡 WiFi = Radio frequency (2.4GHz / 5GHz)")
    print("  🔑 Enkripsi: WEP -> WPA -> WPA2 -> WPA3 (semakin baru semakin aman)")
    print("  💡 WiFi = SINYAL RADIO. Siapa pun bisa mendengar.")
    print("     Bedanya: data dienkripsi (WPA2). Tapi bisa di-crack.")
def enkripsi():
    print("\n[2] JENIS ENKRIPSI WiFi")
    items = [
        ("WEP", "40/104 bit", "GEMBOK PLASTIK", "5 menit"),
        ("WPA", "TKIP", "GEMBOK BESI LAMA", "Jam - hari"),
        ("WPA2", "AES-CCMP", "GEMBOK BESI BARU", "Hari - minggu"),
        ("WPA3", "SAE (Dragonfly)", "GEMBOK BIOMETRIK", "Belum bisa crack"),
    ]
    print(f"  {'Tipe':<8} {'Enkripsi':<15} {'Analogi':<25} {'Waktu Crack'}")
    print(f"  {'-'*60}")
    for t, e, a, c in items:
        print(f"  {t:<8} {e:<15} {a:<25} {c}")
def tools_check():
    print("\n[3] CEK TOOLS")
    tools = ["aircrack-ng","airmon-ng","airodump-ng","aireplay-ng",
             "reaver","hashcat","mdk3","macchanger"]
    for t in tools:
        r = subprocess.run(["which",t], capture_output=True, text=True)
        print(f"  {t:15} → {'✅ Terinstall' if r.stdout.strip() else '❌ Tidak ada'}")
def attack_methods():
    print("\n[4] METODE SERANGAN")
    attacks = [
        ("WEP Cracking", "Aircrack: tangkep IV, crack dalam 5-10 menit", "aircrack-ng -b BSSID capture.cap"),
        ("WPA Handshake", "Tangkep 4-way handshake + deauth", "aireplay-ng -0 5 -a BSSID wlan0mon"),
        ("WPA Crack", "Wordlist attack pake aircrack/hashcat", "aircrack-ng -w wordlist.txt capture.cap"),
        ("WPS Pixie Dust", "Brute force WPS PIN (reaver)", "reaver -i wlan0mon -b BSSID"),
        ("Evil Twin", "Buat AP palsu nama sama", "airbase-ng -e 'WiFi_Nama' -c 1 wlan0mon"),
        ("Deauth Attack", "Putuskan koneksi client", "aireplay-ng -0 5 -a BSSID -c CLIENT_MAC wlan0mon"),
    ]
    for name, desc, cmd in attacks:
        print(f"  ⚡ {name:20} | {desc}")
def prevention():
    print("\n[5] PERTAHANAN")
    tips = [
        ("Gunakan WPA2/WPA3", "WEP = gembok plastik, hindari!"),
        ("Password 12+ karakter", "Campur huruf besar, kecil, angka, simbol"),
        ("Matikan WPS", "Celah terbesar! WPS PIN bisa di-brute"),
        ("MAC Filter (mitigasi)", "Bukan tameng, tapi bikin ribet attacker"),
        ("Hide SSID (mitigasi)", "Tidak menyembunyikan, cuma bikin tidak kelihatan"),
        ("Update firmware router", "Patch celah keamanan"),
    ]
    for t, d in tips:
        print(f"  🔒 {t:30} → {d}")
def main():
    banner(); wifi_concept(); enkripsi(); tools_check(); attack_methods(); prevention()
    print("\n"+"="*60)
    print("  ✅ SESI 22: WIRELESS HACKING SELESAI!")
    print("  👉 Pahami perbedaan WEP/WPA/WPA2/WPA3")
    print("  👉 Cek tools wireless testing")
    print("  📌 LATIHAN: 1. airmon-ng start wlan0 2. airodump-ng wlan0mon")
    print("  📌 LATIHAN: 3. Tangkep WPA handshake 4. hashcat crack")
    print("="*60)
if __name__ == "__main__": main()
