#!/usr/bin/env python3
"""Sesi 2: Kriptografi - Encode, Hash, Enkripsi, TOR, SSH Tunnel"""
import hashlib, base64, os, subprocess

def banner():
    print("="*60)
    print("  SESI 2: KRIPTOGRAFI & TOOLS KEAMANAN")
    print("  Referensi: X-Code Ethical Elite Hacker v11")
    print("="*60)

def demo_base64():
    print("\n[1] BASE64 ENCODE/DECODE")
    pesan = "Rahasia: Saya suka belajar hacking etis!"
    encoded = base64.b64encode(pesan.encode()).decode()
    decoded = base64.b64decode(encoded).decode()
    print(f"  Pesan asli : {pesan}")
    print(f"  Encode     : {encoded}")
    print(f"  Decode     : {decoded}")
    print("  💡 Base64 BUKAN enkripsi! Gampang dibalikin.")
    print("     Contoh: PHPShell sering di-base64 biar lolos filter WAF")
    print("     Cara detek: string acak huruf+angka+== di akhir")

def demo_caesar():
    print("\n[2] CAESAR CIPHER (Enkripsi Simetris)")
    def caesar(text, shift):
        result = ""
        for char in text:
            if char.isalpha():
                ascii_offset = 65 if char.isupper() else 97
                result += chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
            else:
                result += char
        return result

    pesan = "Halo ini pesan rahasia"
    geser = 3
    encrypted = caesar(pesan, geser)
    decrypted = caesar(encrypted, -geser)
    print(f"  Pesan    : {pesan}")
    print(f"  Geser {geser} : {encrypted}")
    print(f"  Kembali  : {decrypted}")
    print("  💡 Caesar = ganti huruf berdasarkan shift")
    print("     Gampang dipecah: tinggal coba 25 kemungkinan shift")

def demo_xor():
    print("\n[3] ENKRIPSI XOR")
    def xor_encrypt(plain, key):
        return ''.join(chr(ord(p) ^ ord(key[i % len(key)])) for i, p in enumerate(plain))
    
    key = "kunci123"
    pesan = "Data Rahasia"
    encrypted = xor_encrypt(pesan, key)
    decrypted = xor_encrypt(encrypted, key)
    print(f"  Key      : {key}")
    print(f"  Pesan    : {pesan}")
    print(f"  Encrypt  : {repr(encrypted)}")
    print(f"  Decrypt  : {decrypted}")
    print("  💡 XOR: kalau tau key, balikin gampang")
    print("     Banyak malware pake XOR buat obfuscate payload")

def demo_hash():
    print("\n[4] FUNGSI HASH (SIDIK JARI DIGITAL)")
    pesan = "password123"
    md5 = hashlib.md5(pesan.encode()).hexdigest()
    sha1 = hashlib.sha1(pesan.encode()).hexdigest()
    sha256 = hashlib.sha256(pesan.encode()).hexdigest()
    print(f"  Pesan    : {pesan}")
    print(f"  MD5      : {md5}  (JANGAN — udah bisa di-crack)")
    print(f"  SHA1     : {sha1}  (JANGAN — udah bisa di-crack)")
    print(f"  SHA256   : {sha256} (AMAN — masih kuat)")
    print("  💡 Hash = SATU ARAH. Gak bisa dibalik.")
    print("     Cara crack: tebak pake wordlist (hashcat)")

def demo_hash_crack():
    print("\n[5] SIMULASI CRACK HASH PAKE WORDLIST")
    # Common weak passwords + their SHA1 hash
    wordlist = ["admin", "password123", "123456", "qwerty", "rahasia", "letmein"]
    target_hash = hashlib.sha1("password123".encode()).hexdigest()
    print(f"  Target hash (SHA1): {target_hash}")
    print(f"  Wordlist: {wordlist}")
    for word in wordlist:
        h = hashlib.sha1(word.encode()).hexdigest()
        if h == target_hash:
            print(f"  ✅ KETEMU! Password = '{word}'")
            break
    print("  💡 Ini cara kerja hashcat/John — bedanya pake GPU & wordlist raksasa")

def demo_rsa():
    print("\n[6] RSA (Enkripsi Asimetris) — SEDERHANA")
    print("  Konsep: Ada PUBLIC KEY (dibagi) + PRIVATE KEY (rahasia)")
    print("  Orang kirim pesan: enkrip pake PUBLIC KEY")
    print("  Kamu baca: dekrip pake PRIVATE KEY")
    print()
    print("  🔑 Contoh sederhana pake bilangan prima:")
    p, q = 61, 53  # bilangan prima
    n = p * q      # 3233
    e = 17         # public exponent
    # d = private exponent (rumit, skip kalkulasi manual)
    print(f"  p={p}, q={q} → n={n}")
    print(f"  Public Key  = (n={n}, e={e})")
    print(f"  Private Key = (n={n}, d=...hitung pake extended Euclidean)")
    print()
    print("  💡 RSA: aman karena faktorisasi n=p*q susah banget")
    print("     Makin besar p & q makin aman (4096 bit = standar)")
    print("     HTTPS, SSH, GPG semua pake RSA/ECC")

def demo_firewall():
    print("\n[7] FIREWALL & PORT KNOCKING")
    print("  🔥 Firewall = SATPAM di pintu jaringan")
    print("     Atur: IP/port mana yang BOLEH lewat, mana yang DIBLOKIR")
    print()
    print("  🚪 PORT KNOCKING = KETUK PINTU RAHASIA")
    print("     Cara: ketuk port 1000 → 2000 → 3000 (urutan rahasia)")
    print("     Baru firewall buka port SSH (22) buat kamu")
    print("     Kalo langsung scan port 22, kelihatan TERTUTUP")
    print()
    r = subprocess.run(["which", "ufw"], capture_output=True, text=True)
    if r.stdout.strip():
        r2 = subprocess.run(["ufw", "status"], capture_output=True, text=True)
        print(f"  Status UFW di sini:\n{r2.stdout[:300]}")
    else:
        print("  UFW: tidak terinstall di sini (bisa diaktifkan kalo perlu)")
    print("  💡 Port knocking: anti-scan, cuma yang tau urutan bisa akses")

def demo_tor_ssh():
    print("\n[8] TOR & SSH TUNNEL")
    print("  🌐 TOR = SURAT BERANTAI lewat banyak pos")
    print("     Data muter lewat 3 node random (Entry → Middle → Exit)")
    print("     IP asli kamu GAK KELIATAN oleh server tujuan")
    print("     Install: sudo apt install tor")
    print("     Jalankan: tor &")
    print("     Akses: curl --socks5 127.0.0.1:9050 http://duckduckgo.com")
    print()
    print("  🚇 SSH TUNNEL = TEROWONGAN AMAN")
    print("     ssh -D 1080 user@server   (SOCKS proxy via SSH)")
    print("     ssh -L 8080:target:80 user@server  (port forwarding)")
    print("     💡 Berguna buat bypass firewall / akses internal server")
    print()
    # Check if tor is installed
    r = subprocess.run(["which", "tor"], capture_output=True, text=True)
    print(f"  TOR: {'TERINSTAL ✅' if r.stdout.strip() else 'Tidak terinstal'} di sini")

def main():
    banner()
    demo_base64()
    demo_caesar()
    demo_xor()
    demo_hash()
    demo_hash_crack()
    demo_rsa()
    demo_firewall()
    demo_tor_ssh()
    print("\n" + "="*60)
    print("  ✅ SESI 2 SELESAI!")
    print("  👉 Base64, Caesar, XOR, Hash, RSA")
    print("  👉 Hash cracking, Firewall, Port Knocking")
    print("  👉 TOR & SSH Tunnel")
    print()
    print("  📌 LATIHAN LANJUTAN:")
    print("  1. Crack hash pake hashcat: hashcat -m 0 hash.txt wordlist.txt")
    print("  2. Install TOR & coba browse anonim")
    print("  3. Bikin SSH tunnel: ssh -D 1080 user@vps")
    print("  4. Reverse engineering: baca disassembly binary")
    print("="*60)

if __name__ == "__main__":
    main()
