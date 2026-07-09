#!/usr/bin/env python3
"""Sesi 2: Kriptografi - Encode, Hash, Enkripsi"""
import hashlib, base64, os

def banner():
    print("="*60)
    print("  SESI 2: KRIPTOGRAFI DASAR")
    print("  Analogi: Encode=BAHASA SANDI, Hash=SIDIK JARI")
    print("="*60)

def demo_base64():
    print("\n[1] BASE64 ENCODE/DECODE")
    pesan = "Rahasia: Saya suka belajar hacking etis!"
    encoded = base64.b64encode(pesan.encode()).decode()
    decoded = base64.b64decode(encoded).decode()
    print(f"  Pesan asli : {pesan}")
    print(f"  Encode     : {encoded}")
    print(f"  Decode     : {decoded}")
    print("  INGAT: Base64 BUKAN enkripsi! Gampang dibalikin.")

def demo_hash():
    print("\n[2] FUNGSI HASH")
    pesan = "password123"
    md5 = hashlib.md5(pesan.encode()).hexdigest()
    sha1 = hashlib.sha1(pesan.encode()).hexdigest()
    sha256 = hashlib.sha256(pesan.encode()).hexdigest()
    print(f"  Pesan : {pesan}")
    print(f"  MD5   : {md5}  (JANGAN DIPAKAI)")
    print(f"  SHA1  : {sha1}  (JANGAN DIPAKAI)")
    print(f"  SHA256: {sha256} (AMAN)")
    print("  Hash itu SATU ARAH. Gak bisa dibalik jadi password asli.")
    print("  Kalo mau crack, kamu harus coba tebak passwordnya.")

def demo_xor():
    print("\n[3] ENKRIPSI XOR SEDERHANA")
    def xor_encrypt(plain, key):
        return ''.join(chr(ord(p) ^ ord(key[i % len(key)])) for i, p in enumerate(plain))
    
    key = "kunci123"
    pesan = "Data Rahasia"
    encrypted = xor_encrypt(pesan, key)
    decrypted = xor_encrypt(encrypted, key)
    print(f"  Key   : {key}")
    print(f"  Pesan : {pesan}")
    print(f"  Encrypt: {encrypted.encode('utf-8')}")
    print(f"  Decrypt: {decrypted}")

def demo_password_hashing():
    print("\n[4] SIMULASI HASH PASSWORD (Seperti di database)")
    passwords = ["admin", "password123", "qwerty", "123456", "rahasia"]
    for pwd in passwords:
        h = hashlib.sha256(pwd.encode()).hexdigest()
        print(f"  {pwd:15} -> SHA256: {h[:20]}...")

def main():
    banner()
    demo_base64()
    demo_hash()
    demo_xor()
    demo_password_hashing()
    print("\n" + "="*60)
    print("  LATIHAN:")
    print("  1. Ganti pesan rahasia di Base64")
    print("  2. Coba hash file: python3 -c \"import hashlib; print(hashlib.md5(open('file','rb').read()).hexdigest())\"")
    print("  3. Buat XOR key yang lebih panjang")
    print("="*60)

if __name__ == "__main__":
    main()
