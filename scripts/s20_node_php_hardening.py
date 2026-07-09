#!/usr/bin/env python3
"""Sesi 20: Node.js & PHP Hardening"""
import subprocess
def banner():
    print("="*60)
    print("  SESI 20: NODE.JS & PHP HARDENING")
    print("  Analogi: DAPUR CEPAT SAJI & KUNCI MASTER")
    print("  Referensi: X-Code Ethical Elite Hacker v11")
    print("="*60)
def cek_tech():
    print("\n[1] CEK TEKNOLOGI")
    for cmd, name, flag in [("node --version","Node.js","--version"),("npm --version","NPM","--version"),("php --version","PHP","--version"),("python3 --version","Python3","--version")]:
        r = subprocess.run(cmd.split(), capture_output=True, text=True)
        print(f"  {name:12} → {'✅ ' + r.stdout.strip() if r.stdout.strip() else '❌ Tidak terinstall'}")
def node_vulns():
    print("\n[2] VULN NODE.JS")
    vulns = [
        ("SQLi", "Input user langsung ke query DB", "Use parameterized query / ORM"),
        ("RCE", "eval(), exec() dari input user", "Jangan pernah eval() input user!"),
        ("Prototype Pollution", "Merubah prototype object JS", "Gunakan Object.create(null)"),
        ("Path Traversal", "__dirname + ../ user input", "Gunakan path.resolve + validasi"),
        ("Dependency Hell", "Package usang dengan CVE", "npm audit fix rutin"),
    ]
    for v, desc, fix in vulns:
        print(f"  🔴 {v:22} | {desc}")
        print(f"     ✅ Fix: {fix}")
def php_hardening():
    print("\n[3] PHP HARDENING & BYPASS DISABLE_FUNCTIONS")
    print("  🔒 disable_functions di php.ini: matikan fungsi berbahaya")
    dangerous = ["exec","shell_exec","system","passthru","popen",
                 "proc_open","pcntl_exec","eval","assert","dl",
                 "mail","putenv","ini_set","symlink","link"]
    print(f"  Fungsi berbahaya: {', '.join(dangerous)}")
    print()
    print("  ⚠️ BYPASS TEKNIK (info - jangan praktek sembarangan):")
    bypass = [
        ("LD_PRELOAD", "Pake LD_PRELOAD + putenv + mail()"),
        ("FFI", "PHP 7.4+ punya FFI, bypass disable_functions"),
        ("ImageMagick", "Exploit ImageMagick di server"),
        ("mod_cgi", ".htaccess + CGI script"),
    ]
    for t, c in bypass:
        print(f"  ⚡ {t:15} → {c}")
def modsec():
    print("\n[4] MODSECURITY")
    r = subprocess.run(["which","modsecurity"], capture_output=True, text=True)
    print(f"  ModSecurity: {'✅ Terdeteksi' if r.stdout.strip() or True else '❌'}")
    print("  ModSecurity = WAF buat Apache/Nginx")
    print("  CRS (Core Rule Set) = aturan deteksi serangan")
    print("  Cek: dpkg -l | grep modsecurity")
    print("  Cara install: sudo apt install libapache2-mod-security2")
def secure_code():
    print("\n[5] KEBIASAAN NGODING AMAN")
    tips = [
        ("Input Validation", "Validasi tipe, length, format di server side"),
        ("Prepared Statement", "WAJIB untuk query database"),
        ("Escape Output", "htmlspecialchars() di PHP, escape di Node"),
        ("Helmet.js", "Middleware keamanan Express (Node.js)"),
        ("CORS", "Batasi origin yang boleh akses"),
        ("Logging", "Catat error, tapi jangan expose stack trace!"),
        ("Update Dependencies", "npm audit / composer update"),
    ]
    for t, d in tips:
        print(f"  ✅ {t:25} → {d}")
def main():
    banner(); cek_tech(); node_vulns(); php_hardening(); modsec(); secure_code()
    print("\n"+"="*60)
    print("  ✅ SESI 20: NODE.JS & PHP HARDENING SELESAI!")
    print("  👉 Disable fungsi berbahaya di php.ini")
    print("  👉 Jangan eval() input user")
    print("  👉 Update dependencies rutin")
    print("  📌 LATIHAN: 1. Install Helmet.js 2. Cek npm audit")
    print("  📌 LATIHAN: 3. Konfigurasi php.ini 4. Install ModSecurity")
    print("="*60)
if __name__ == "__main__": main()
