#!/usr/bin/env python3
"""Sesi 20: Node.js & PHP Hardening"""

import subprocess
import sys
import os
import stat
import pwd
import grp
from datetime import datetime


def banner():
    print("=" * 60)
    print("  ETHICAL ELITE HACKER v11 — Sesi 20")
    print("  Node.js & PHP Hardening")
    print("=" * 60)
    print("  Referensi: X-Code Ethical Elite Hacker v11")
    print("=" * 60)


def check_tool(name):
    try:
        subprocess.check_output([name, "--version"], stderr=subprocess.STDOUT, timeout=5)
        return "✅ TERINSTAL"
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        try:
            subprocess.check_output(["which", name], stderr=subprocess.STDOUT, timeout=5)
            return "✅ TERINSTAL"
        except (subprocess.CalledProcessError, FileNotFoundError, OSError):
            return "❌ TIDAK TERINSTAL"


def section(num, title):
    print(f"\n{'─' * 50}")
    print(f"  [{num}] {title}")
    print(f"{'─' * 50}")


# ── [1] Check Environment ──
def check_environment():
    section(1, "CEK LINGKUNGAN SERVER")

    print("""
  💡 Sebelum hardening, kita harus tahu environment apa yang terinstall.
    """)

    # Cek OS
    print("  👉 CEK OS:")
    os_files = ["/etc/os-release", "/etc/lsb-release"]
    for f in os_files:
        if os.path.exists(f):
            try:
                with open(f) as fh:
                    for line in fh:
                        if line.startswith("PRETTY_NAME") or line.startswith("DISTRIB_DESCRIPTION"):
                            print(f"     {line.strip()}")
            except Exception:
                pass

    print()
    print("  👉 CEK PHP:")
    php_status = check_tool("php")
    print(f"     PHP: {php_status}")
    if php_status == "✅ TERINSTAL":
        try:
            result = subprocess.check_output(["php", "--version"],
                                             stderr=subprocess.STDOUT, timeout=5).decode().strip()
            first_line = result.split("\n")[0]
            print(f"     {first_line}")
        except Exception:
            pass

    print()
    print("  👉 CEK NODE.JS:")
    node_status = check_tool("node")
    npm_status = check_tool("npm")
    print(f"     Node.js: {node_status}")
    print(f"     npm:     {npm_status}")
    if node_status == "✅ TERINSTAL":
        try:
            result = subprocess.check_output(["node", "--version"],
                                             stderr=subprocess.STDOUT, timeout=5).decode().strip()
            print(f"     Node.js version: {result}")
        except Exception:
            pass

    print()
    print("  👉 CEK APACHE / NGINX:")
    for svc in ["apache2", "nginx", "httpd"]:
        res = check_tool(svc)
        if res == "✅ TERINSTAL":
            print(f"     {svc}: {res}")
    print()

    # Cek PHP extensions dangerous
    print("  👉 CEK PHP EXTENSION BERBAHAYA:")
    if php_status == "✅ TERINSTAL":
        dangerous_exts = [
            "exec", "system", "passthru", "shell_exec", "popen",
            "proc_open", "eval", "assert", "create_function",
            "dl", "putenv", "mail", "FFI"
        ]
        print(f"     {'Extension':<25} {'Status':<15} {'Keterangan':<40}")
        print(f"     {'─' * 80}")
        for ext in dangerous_exts:
            try:
                check = subprocess.run(
                    ["php", "-r", f"echo function_exists('{ext}') ? 'ADA' : 'TIDAK';"],
                    capture_output=True, text=True, timeout=5
                )
                status_ext = "✅ ADA" if check.stdout.strip() == "ADA" else "❌ TIDAK"
                keterangan = "⚠️ Bisa RCE!" if check.stdout.strip() == "ADA" else "Aman"
                print(f"     {ext:<25} {status_ext:<15} {keterangan:<40}")
            except Exception:
                print(f"     {ext:<25} {'❌ ERROR':<15} {'Gagal cek':<40}")
    else:
        print("     PHP tidak terinstall — skip pengecekan extension.")
    print()


# ── [2] Node.js Vulnerabilities ──
def nodejs_vulns():
    section(2, "NODE.JS VULNERABILITIES & MITIGASI")

    print("""
  💡 Node.js rentan terhadap beberapa jenis serangan serius.
     Ini dia yang paling sering ditemukan:
    """)

    print(f"  {'#':<3} {'Vulnerability':<30} {'Dampak':<45} {'Mitigasi':<45}")
    print(f"  {'─' * 123}")
    vulns = [
        ("1", "SQL Injection",          "Database compromise, data bocor",         "Prepared statements (parameterized queries)"),
        ("2", "RCE via eval()",         "Attacker execute code di server",         "JANGAN pakai eval() — gunakan Function() atau JSON.parse"),
        ("3", "Prototype Pollution",    "Modify Object.prototype → RCE/DoS",       "Use Object.create(null), sanitize JSON input"),
        ("4", "Path Traversal",         "Baca file di luar direktori",             "Gunakan path.resolve + validasi.relative"),
        ("5", "Dependency Hell",        "Supply chain attack via npm package",     "Audit dependency (npm audit), lockfile"),
        ("6", "Command Injection",      "Execute OS command via input",            "Gunakan child_process.execFile, jangan exec()"),
        ("7", "NoSQL Injection",        "Bypass auth via MongoDB operators",       "Sanitize $gt, $ne, $regex di input JSON"),
        ("8", "XSS via SSR",            "Inject script via server-side rendering", "Escape output, gunakan Helmet.js"),
        ("9", "Insecure Deserialization","RCE via malicious serialized object",    "Jangan gunakan JSON.parse pada input langsung"),
        ("10","Directory Listing",       "List semua file di folder",              "Nonaktifkan directory listing di Express"),
    ]
    for v in vulns:
        print(f"  {v[0]:<3} {v[1]:<30} {v[2]:<45} {v[3]:<45}")

    print()

    # Prototype Pollution Demo
    print("  🔥 PROTOTYPE POLLUTION DEMO:")
    print()
    print("""
     // Code vulnerable:
     const merge = (target, source) => {
       for (let key in source) {
         if (source.hasOwnProperty(key)) {
           target[key] = source[key];
         }
       }
     };

     // Attacker kirim payload:
     const payload = JSON.parse('{"__proto__": {"isAdmin": true}}');
     merge({}, payload);

     // Sekarang SEMUA object punya isAdmin = true!
     console.log({}.isAdmin); // true

     💡 Solusi: Object.create(null) atau gunakan lodash defaultsDeep
    """)

    print("  🔥 HELMET.JS — SECURITY MIDDLEWARE:")
    print("""
     const helmet = require('helmet');
     app.use(helmet());  // Otomatis set security headers!

     Apa yang dilakukan Helmet.js:
     • X-Content-Type-Options: nosniff
     • Strict-Transport-Security (HSTS)
     • X-Frame-Options: DENY (cegah clickjacking)
     • X-XSS-Protection: 0 (nonaktifkan legacy XSS filter)
     • Content-Security-Policy (CSP)
     • Referrer-Policy: no-referrer
    """)

    print("  📌 NPM AUDIT:")
    npm_status = check_tool("npm")
    print(f"     npm status: {npm_status}")
    if npm_status == "✅ TERINSTAL":
        print("     Jalankan: npm audit (cek vulnerability di dependencies)")
        print("     Jalankan: npm audit fix (auto-fix kalau ada patch)")
    else:
        print("     npm tidak terinstall — skip.")
    print()


# ── [3] PHP disable_functions ──
def php_disable_functions():
    section(3, "PHP DISABLE_FUNCTIONS")

    print("""
  💡 disable_functions di php.ini adalah DAFTAR HITAM:
     Fungsi PHP yang tidak boleh dijalankan.
     Ibarat KUNCI MASTER yang ngelock fungsi berbahaya.
    """)

    php_status = check_tool("php")
    if php_status == "✅ TERINSTAL":
        print("  🔧 Cek disable_functions di sistem ini:")
        print()
        try:
            result = subprocess.run(
                ["php", "-i"],
                capture_output=True, text=True, timeout=10
            )
            output = result.stdout
            for line in output.split("\n"):
                if "disable_functions" in line.lower() and "=>" in line:
                    print(f"     {line.strip()}")
                    break
            else:
                print("     (tidak ditemukan baris disable_functions)")
        except Exception as e:
            print(f"     Error: {e}")
        print()
    else:
        print("  PHP tidak terinstall — skip.")
        print()

    print(f"  {'Fungsi':<25} {'Dampak Keamanan':<50} {'Sebaiknya':<35}")
    print(f"  {'─' * 110}")
    funcs = [
        ("exec()",           "Execute shell command via PHP",              "DISABLE — ganti dengan non-RCE alternatif"),
        ("system()",         "Execute + output langsung",                  "DISABLE — attacker bisa RCE"),
        ("passthru()",       "Execute + raw binary output",               "DISABLE — berbahaya"),
        ("shell_exec()",     "Execute return string",                      "DISABLE — backdoor klasik"),
        ("popen()",          "Buka pipe ke command",                       "DISABLE — bisa RCE"),
        ("proc_open()",      "Eksekusi command kompleks",                  "DISABLE — alternatif: exec dengan whitelist"),
        ("eval()",           "Eksekusi string sebagai PHP code",           "DISABLE — backdoor favorit attacker!"),
        ("assert()",         "Evaluasi assertion string",                  "DISABLE — mirip eval, bisa RCE"),
        ("create_function()","Buat function dinamis",                      "DISABLE — deprecated di PHP 7.2, hapus di 8.0"),
        ("dl()",             "Load extension dinamis",                     "DISABLE — loading arbitrary .so berbahaya"),
        ("putenv()",         "Set environment variable",                   "⚠️ Hati-hati — dipakai untuk LD_PRELOAD bypass"),
        ("mail()",           "Send mail (digunakan bypass disable_functions)", "⚠️ Hati-hati — dipakai di LD_PRELOAD exploit"),
        ("fopen()",          "Buka file",                                 "✅ Relatif aman — jaga permission"),
        ("file_get_contents()","Baca file ke string",                      "✅ Relatif aman — jaga path traversal"),
    ]
    for f in funcs:
        print(f"  {f[0]:<25} {f[1]:<50} {f[2]:<35}")

    print()

    print("""
  🔥 Config php.ini yang aman:
    """)
    print(f"  {'Directive':<45} {'Nilai Aman':<30} {'Keterangan':<40}")
    print(f"  {'─' * 115}")
    configs = [
        ("disable_functions",            "exec,system,passthru,shell_exec,popen,...", "Matikan fungsi berbahaya"),
        ("allow_url_fopen",              "Off",                                       "Cegah RFI/LFI"),
        ("allow_url_include",            "Off",                                       "Cegah remote file inclusion"),
        ("display_errors",               "Off",                                       "Cegah verbose error"),
        ("expose_php",                   "Off",                                       "Sembunyikan versi PHP"),
        ("file_uploads",                 "On (jika perlu)",                           "Batasi ukuran & tipe file"),
        ("open_basedir",                 "/var/www/html:/tmp",                         "Batasi akses filesystem"),
        ("session.cookie_httponly",      "1",                                         "Cegah XSS akses session cookie"),
        ("session.cookie_secure",        "1",                                         "Cookie hanya via HTTPS"),
        ("session.cookie_samesite",      "Strict",                                    "Cegah CSRF"),
        ("upload_max_filesize",          "2M",                                        "Batasi ukuran upload"),
        ("post_max_size",                "8M",                                        "Batasi ukuran POST"),
        ("max_execution_time",           "30",                                        "Batasi waktu eksekusi"),
        ("memory_limit",                 "128M",                                      "Batasi memory"),
    ]
    for c in configs:
        print(f"  {c[0]:<45} {c[1]:<30} {c[2]:<40}")
    print()


# ── [4] Bypass Techniques ──
def bypass_techniques():
    section(4, "BYPASS DISABLE_FUNCTIONS — TEKNIK UMUM")

    print("""
  💡 Ini adalah teknik yang digunakan attacker untuk bypass
     disable_functions. PENTING diketahui agar bisa di-mitigasi!
    """)

    print(f"  {'#':<3} {'Teknik':<30} {'Cara Kerja':<55} {'Mitigasi':<40}")
    print(f"  {'─' * 128}")
    bypasses = [
        ("1", "LD_PRELOAD + mail()",   "Load shared object berbahaya via putenv + mail() trigger", "Disable putenv + mail(), atau gunakan AppArmor"),
        ("2", "FFI (PHP 7.4+)",        "Foreign Function Interface — panggil C function langsung", "Disable FFI extension (extension=ffi)"),
        ("3", "ImageMagick (imagick)", "Gunakan ImageMagick untuk execute command via MVG",        "Disable imagick, gunakan policy.xml"),
        ("4", "mod_cgi (Apache)",      "Upload .cgi script dan execute via CGI handler",           "Disable mod_cgi, gunakan mod_cgid dengan restriksi"),
        ("5", "PCNTL extension",       "Process Control — fork, exec via PHP",                     "Disable pcntl extension"),
        ("6", "SplFileObject",         "Baca file sistem via SPL class",                           "Gunakan open_basedir restriction"),
        ("7", "GD/Imagick + payload",  "Eksploitasi bug di image processing",                     "Update library, disable Imagick jika tidak perlu"),
        ("8", "PHP-GG Bypasser",       "Tool otomatis bypass disable_functions",                   "Hardening total + WAF + RASP"),
    ]
    for b in bypasses:
        print(f"  {b[0]:<3} {b[1]:<30} {b[2]:<55} {b[3]:<40}")

    print()

    print("  🔥 LD_PRELOAD + mail() BYPASS DETAIL:")
    print("""
     Langkah-langkah bypass (classic):
     1. Attacker upload file .so berbahaya (evil.so)
     2. Set LD_PRELOAD via putenv('LD_PRELOAD=/tmp/evil.so')
     3. Panggil mail() — yang trigger sendmail binary
     4. sendmail load evil.so via LD_PRELOAD
     5. Code di evil.so jalan dengan full privilege!

     💡 Mitigasi:
     • Disable putenv() dan mail() di disable_functions
     • Gunakan AppArmor/SELinux untuk restrict process
     • Set open_basedir ketat
     • Gunakan PHP-FPM dengan user berbeda per site
     • Install RASP (Runtime Application Self-Protection)

     🔥 ALTERNATIF: FFI (PHP 7.4+)
     $ffi = FFI::cdef("int system(const char *command);");
     $ffi->system("id");
     // System call langsung — bypass PHP function restrictions!

     💡 Mitigasi FFI:
     • Jangan install extension FFI di production
     • Jika terlanjur, disable di php.ini: extension=ffi
    """)
    print()


# ── [5] ModSecurity ──
def modsecurity_check():
    section(5, "MODSECURITY — WEB APPLICATION FIREWALL")

    print("""
  💡 ModSecurity adalah WAF (Web Application Firewall) open-source
     yang melindungi aplikasi web dari serangan umum.
    """)

    print("  🔧 CEK MODSECURITY DI SISTEM:")
    print()

    modsec_check = check_tool("modsecurity")
    modsec2_check = check_tool("mod_security2")

    # Check apache mod
    apache_status = check_tool("apache2")
    if apache_status == "✅ TERINSTAL":
        try:
            result = subprocess.run(
                ["apache2ctl", "-M"],
                capture_output=True, text=True, timeout=10
            )
            if "security2" in result.stdout.lower():
                print("     ✅ ModSecurity (security2_module) terdeteksi di Apache!")
            else:
                print("     ⚠️ ModSecurity TIDAK terdeteksi di Apache modules.")
        except Exception:
            print("     ❌ Tidak bisa cek Apache modules (apache2ctl -M gagal)")
    else:
        print("     Apache tidak terinstall — ModSecurity mungkin via Nginx or lainnya.")

    print()
    print(f"  {'Komponen':<25} {'Deskripsi':<60}")
    print(f"  {'─' * 85}")
    mos = [
        ("ModSecurity Engine",     "Core WAF engine — filter HTTP traffic"),
        ("CRS (Core Rule Set)",    "OWASP CRS — ruleset untuk SQLi, XSS, LFI, RCE dll"),
        ("SecRuleEngine",          "On/DetectionOnly/Off — mode operasi"),
        ("SecDefaultAction",       "Action default: deny, log, pass, redirect"),
        ("SecRequestBodyAccess",   "Akses body request untuk filtering POST"),
        ("SecResponseBodyAccess",  "Akses response body untuk filtering output"),
        ("SecAuditEngine",         "Audit log — rekam semua request/response"),
        ("SecDataDir",            "Direktori penyimpanan data persistent"),
    ]
    for m in mos:
        print(f"  {m[0]:<25} {m[1]:<60}")
    print()

    print("  🔥 OWASP CRS RULES (contoh):")
    print()
    print(f"  {'Rule ID':<12} {'Deskripsi':<60}")
    print(f"  {'─' * 72}")
    rules = [
        ("942100", "SQL Injection — tautology ' OR '1'='1 detected"),
        ("942130", "SQL Injection — comment injection --, # detected"),
        ("941100", "XSS — script tag <script> detected"),
        ("931100", "Path Traversal — ../ detected"),
        ("932100", "RCE — Unix command injection"),
        ("933100", "PHP Injection — eval() detected"),
        ("934100", "Node.js Injection — prototype pollution attempt"),
    ]
    for r in rules:
        print(f"  {r[0]:<12} {r[1]:<60}")
    print()


# ── [6] Secure Coding — Node.js ──
def secure_coding_node():
    section(6, "SECURE CODING: NODE.JS BEST PRACTICES")

    print("""
  💡 Prinsip secure coding untuk Node.js:
    """)

    print("  ❌ VULNERABLE CODE:")
    print("""
     // 1. SQL Injection
     const query = `SELECT * FROM users WHERE id = ${req.params.id}`;
     db.query(query);

     // 2. RCE via eval
     const result = eval(req.body.expression);

     // 3. Command Injection
     const output = execSync('ping ' + req.body.ip);

     // 4. Path Traversal
     const data = fs.readFileSync(req.params.path);
    """)

    print("  ✅ SECURE CODE:")
    print("""
     // 1. Prepared Statements
     const query = 'SELECT * FROM users WHERE id = $1';
     db.query(query, [req.params.id]);

     // 2. No eval — gunakan Function constructor
     const fn = new Function('return ' + sanitizedInput);

     // 3. execFile dengan parameter terpisah
     const { execFile } = require('child_process');
     execFile('ping', ['-c', '1', sanitizedIp]);

     // 4. Path validation
     const path = require('path');
     const safePath = path.resolve('/app/data/', req.params.path);
     if (!safePath.startsWith('/app/data/')) throw new Error('Invalid path');
    """)

    print("  📌 DEPENDENCY CHECK — NPM AUDIT:")
    npm_status = check_tool("npm")
    if npm_status == "✅ TERINSTAL":
        try:
            result = subprocess.run(
                ["npm", "audit", "--version"],
                capture_output=True, text=True, timeout=5
            )
            print(f"     npm audit tersedia (versi: {result.stdout.strip()})")
            print()
            print("     Command:  npm audit")
            print("     Fix:      npm audit fix")
            print("     Dry run:  npm audit fix --dry-run")
        except Exception:
            print("     npm audit tidak bisa dijalankan.")
    else:
        print("     npm tidak terinstall — skip.")
    print()

    print("  📌 OWASP DEPENDENCY CHECK:")
    print("""
     • Tool: OWASP Dependency-Check
     • Install: sudo apt install dependency-check-cli
     • Jalankan: dependency-check --project MyApp --scan .
     • Output: HTML report berisi CVE untuk tiap dependency
     """)
    print()


# ── [7] Secure Coding — PHP ──
def secure_coding_php():
    section(7, "SECURE CODING: PHP BEST PRACTICES")

    print("""
  💡 Prinsip secure coding untuk PHP:
    """)

    print("  ❌ VULNERABLE CODE:")
    print("""
     // 1. SQL Injection
     $query = "SELECT * FROM users WHERE id = " . $_GET['id'];
     mysqli_query($conn, $query);

     // 2. RCE via system
     system('ping -c 1 ' . $_POST['ip']);

     // 3. File Inclusion
     include($_GET['page'] . '.php');

     // 4. Unsafe unserialize
     $data = unserialize($_POST['data']);
    """)

    print("  ✅ SECURE CODE:")
    print("""
     // 1. Prepared Statements (MySQLi)
     $stmt = $conn->prepare(\"SELECT * FROM users WHERE id = ?\");
     $stmt->bind_param(\"i\", $_GET['id']);
     $stmt->execute();

     // 2. No system/exec — gunakan filter_var + escapeshellarg
     $ip = filter_var($_POST['ip'], FILTER_VALIDATE_IP);
     if ($ip) {
       $output = shell_exec('ping -c 1 ' . escapeshellarg($ip));
     }

     // 3. Whitelist-based inclusion
     $allowed = ['home', 'about', 'contact'];
     $page = in_array($_GET['page'], $allowed) ? $_GET['page'] : 'home';
     include($page . '.php');

     // 4. JSON instead of serialize (lebih aman)
     $data = json_decode($_POST['data'], true);
    """)

    print("  🔥 INPUT VALIDATION CHECKLIST:")
    print()
    checklists = [
        "✅ Validate tipe data (int, string, email, URL)",
        "✅ Sanitize input (strip_tags, htmlspecialchars, filter_var)",
        "✅ Gunakan prepared statements untuk SQL",
        "✅ Whitelist path untuk file inclusion",
        "✅ Jangan trust user input — validate EVERYTHING",
        "✅ Gunakan CSRF token untuk form submission",
        "✅ Set proper Content-Type headers",
        "✅ Log semua request mencurigakan",
    ]
    for item in checklists:
        print(f"     {item}")
    print()


# ── [8] File Permissions & Ownership ──
def file_permissions():
    section(8, "FILE PERMISSIONS & OWNERSHIP")

    print("""
  💡 Salah satu aspek hardening paling BASIC tapi paling sering diabaikan!
    """)

    print(f"  {'Item':<30} {'Recommended':<35} {'Penjelasan':<45}")
    print(f"  {'─' * 110}")
    perms = [
        ("Web Root (/var/www/html)",  "755 root:www-data",        "Owner root, group www-data, other hanya read+exec"),
        ("Config files (.env, .ini)", "640 root:www-data",        "Hanya root bisa write, www-data bisa read"),
        ("Log files",                 "640 www-data:adm",         "Log bisa dibaca admin, ditulis web server"),
        ("Upload directory",          "750 www-data:www-data",    "Hanya web server yang akses"),
        ("Session files (/tmp)",      "733 root:root",            "Sticky bit — tiap user punya file sendiri"),
        ("Backup files",             "600 root:root",             "Backup harus super-private"),
        ("SSL Certificates",         "600 root:root",             "Private key — SANGAT SENSITIF"),
        ("PHP files (.php)",         "644 root:www-data",         "Owner bisa write, group & other only read"),
    ]
    for p in perms:
        print(f"  {p[0]:<30} {p[1]:<35} {p[2]:<45}")

    print()
    print("  🔥 Cek permission di direktori ini:")
    try:
        stat_info = os.stat("/home/ubuntu/.hermes/home/belajar_ethical_elite/scripts/")
        perm_oct = oct(stat.S_IMODE(stat_info.st_mode))
        owner = pwd.getpwuid(stat_info.st_uid).pw_name
        group = grp.getgrgid(stat_info.st_gid).gr_name
        print(f"     /home/ubuntu/.hermes/home/belajar_ethical_elite/scripts/")
        print(f"     Permission: {perm_oct}, Owner: {owner}:{group}")
    except Exception as e:
        print(f"     Error: {e}")

    print()
    print("  📌 COMMANDS UNTUK SET PERMISSION:")
    print("     chown -R root:www-data /var/www/html")
    print("     chmod -R 755 /var/www/html")
    print("     chmod 640 /var/www/html/.env")
    print("     find /var/www/html -type f -name '*.php' -exec chmod 644 {} \\;")
    print()


# ── [9] Server Hardening Tips ──
def server_hardening():
    section(9, "SERVER HARDENING TIPS")

    print("""
  💡 Checklist hardening untuk production server:
    """)

    print(f"  {'#':<3} {'Area':<25} {'Action':<55} {'Prioritas':<12}")
    print(f"  {'─' * 95}")
    tips = [
        ("1",  "PHP",        "Disable dangerous functions di disable_functions",                 "🔴 KRITIS"),
        ("2",  "PHP",        "Set expose_php = Off",                                            "🔴 KRITIS"),
        ("3",  "PHP",        "Set display_errors = Off",                                        "🔴 KRITIS"),
        ("4",  "PHP",        "Set allow_url_include = Off",                                     "🔴 KRITIS"),
        ("5",  "PHP",        "Set open_basedir ke direktori terbatas",                          "🟡 SEDANG"),
        ("6",  "PHP",        "Nonaktifkan ekstensi tidak perlu (ffi, imagick, pcntl)",          "🔴 KRITIS"),
        ("7",  "Node.js",    "Gunakan Helmet.js middleware",                                    "🔴 KRITIS"),
        ("8",  "Node.js",    "Jalankan npm audit secara rutin",                                 "🟡 SEDANG"),
        ("9",  "Node.js",    "Jangan jalankan sebagai root — gunakan user node",                "🔴 KRITIS"),
        ("10", "Node.js",    "Set NODE_ENV=production (nonaktifkan debug)",                     "🔴 KRITIS"),
        ("11", "Apache",     "Nonaktifkan directory listing (Options -Indexes)",                "🔴 KRITIS"),
        ("12", "Apache",     "Install ModSecurity + OWASP CRS",                                 "🟡 SEDANG"),
        ("13", "Apache",     "Set ServerSignature Off, ServerTokens Prod",                      "🟡 SEDANG"),
        ("14", "File",       "Permission 755/644 — tidak ada file writable by www-data",        "🔴 KRITIS"),
        ("15", "File",       "File .env, config di luar web root",                              "🔴 KRITIS"),
        ("16", "Network",    "Gunakan HTTPS (Let's Encrypt gratis)",                            "🔴 KRITIS"),
        ("17", "Network",    "Firewall: UFW/iptables — tutup port tidak perlu",                 "🔴 KRITIS"),
        ("18", "Network",    "Rate limiting dengan fail2ban",                                   "🟡 SEDANG"),
        ("19", "OS",         "Auto security update (unattended-upgrades)",                      "🟡 SEDANG"),
        ("20", "OS",         "AppArmor/SELinux — mandatory access control",                     "🟢 RENDAH"),
    ]
    for t in tips:
        print(f"  {t[0]:<3} {t[1]:<25} {t[2]:<55} {t[3]:<12}")

    print()
    print("  🔥 PRIORITAS: Lakukan KRITIS dulu, baru SEDANG, lalu RENDAH.")
    print("     Jangan kewalahan — setidaknya 5 item KRITIS harus done ASAP!")
    print()


# ── [10] PHP Composer Audit ──
def composer_audit():
    section(10, "COMPOSER AUDIT (PHP DEPENDENCY CHECK)")

    print("""
  💡 Sama seperti npm audit untuk Node.js, PHP punya
     composer audit untuk cek keamanan dependency.
    """)

    composer_status = check_tool("composer")
    print(f"  🔧 Composer status: {composer_status}")
    print()

    if composer_status == "✅ TERINSTAL":
        try:
            result = subprocess.run(
                ["composer", "--version"],
                capture_output=True, text=True, timeout=5
            )
            print(f"     {result.stdout.strip()}")
        except Exception:
            pass
    else:
        print("     Composer tidak terinstall. Install dengan:")
        print("     php -r \"copy('https://getcomposer.org/installer', 'composer-setup.php');\"")
        print("     php composer-setup.php")
        print("     php -r \"unlink('composer-setup.php');\"")
        print("     mv composer.phar /usr/local/bin/composer")
        print()

    print("  📌 COMMANDS:")
    print("     composer audit                    # Cek vulnerability di dependencies")
    print("     composer update --audit            # Update + audit sekaligus")
    print("     composer why-not <package>         # Cek kenapa package nggak bisa diupdate")
    print()

    print(f"  {'Package':<35} {'CVE':<20} {'Severity':<15} {'Patched Version':<20}")
    print(f"  {'─' * 90}")
    audit_examples = [
        ("laravel/framework", "CVE-2023-XXXX", "HIGH",   "v10.20.0"),
        ("monolog/monolog",   "CVE-2022-XXXX", "CRITICAL", "v3.3.0"),
        ("guzzlehttp/guzzle", "CVE-2023-XXXX", "MEDIUM", "v7.7.0"),
        ("phpunit/phpunit",   "CVE-2022-XXXX", "HIGH",   "v10.5.0"),
    ]
    for ae in audit_examples:
        print(f"  {ae[0]:<35} {ae[1]:<20} {ae[2]:<15} {ae[3]:<20}")
    print()

    print("""
  🔥 Konsep OWASP Dependency Check:
     • Scan semua dependency (Composer, npm, Maven, pip, etc.)
     • Cocokkan dengan database CVE (NVD)
     • Output: report HTML dengan severity HIGH/MEDIUM/LOW
     • Integrasi CI/CD untuk auto-fail jika ada CRITICAL CVE
    """)


# ── [11] Analogi ──
def analogi():
    section(11, "ANALOGI DAPUR CEPAT SAJI & KUNCI MASTER")

    print("""
   ╔══════════════════════════════════════════════════════════╗
   ║  🍳 ANALOGI DAPUR CEPAT SAJI (Node.js)                 ║
   ║                                                        ║
   ║  Node.js = DAPUR CEPAT SAJI modern                    ║
   ║     • Banyak alat (packages) dari berbagai supplier    ║
   ║     • Supplier nakal bisa kirim alat RUSAK (Dependency ║
   ║       Hell / Supply Chain Attack)                      ║
   ║     • Koki (eval()) bisa masak SEMBARANGAN (RCE)       ║
   ║     • Helm (Helmet.js) lindungi koki dari cedera       ║
   ║     • Buku resep (lockfile) pastikan semua pakai       ║
   ║       alat sama (reproducible build)                   ║
   ║                                                        ║
   ║  🔑 ANALOGI KUNCI MASTER (PHP disable_functions)      ║
   ║                                                        ║
   ║  PHP = GUDANG DENGAN BANYAK PINTU                      ║
   ║     • disable_functions = KUNCI MASTER                 ║
   ║       yang ngunci pintu berbahaya                      ║
   ║     • Tanpa disable_functions = Semua pintu terbuka    ║
   ║     • Tapi ada teknik MEMBOBOL kunci master:           ║
   ║       - LD_PRELOAD = Lewat ventilasi udara             ║
   ║       - FFI = Bikin kunci duplikat                     ║
   ║       - ImageMagick = Pakai alat tukang lain           ║
   ║       - mod_cgi = Bikin pintu baru                     ║
   ║                                                        ║
   ║  🔒 HARDENING = Pasang SEMUA kunci + alarm + CCTV!    ║
   ╚══════════════════════════════════════════════════════════╝
    """)


# ── Main ──
def main():
    banner()

    # ── [1] Check Environment ──
    check_environment()

    # ── [2] Node.js Vulnerabilities ──
    nodejs_vulns()

    # ── [3] PHP disable_functions ──
    php_disable_functions()

    # ── [4] Bypass Techniques ──
    bypass_techniques()

    # ── [5] ModSecurity ──
    modsecurity_check()

    # ── [6] Secure Coding Node.js ──
    secure_coding_node()

    # ── [7] Secure Coding PHP ──
    secure_coding_php()

    # ── [8] File Permissions ──
    file_permissions()

    # ── [9] Server Hardening ──
    server_hardening()

    # ── [10] Composer Audit ──
    composer_audit()

    # ── [11] Analogi ──
    analogi()

    # ── Summary ──
    print("=" * 60)
    print("  ✅ SESI 20 SELESAI!")
    print("=" * 60)
    print("  👉 Recap:")
    print("    • Node.js: SQLi, RCE (eval), Prototype Pollution, Path Traversal")
    print("    • Helmet.js: Security middleware untuk Express (headers aman)")
    print("    • npm audit: Cek vulnerability di dependencies Node.js")
    print("    • PHP: disable_functions = Kunci Master — matikan exec, system, eval dll")
    print("    • Bypass: LD_PRELOAD + mail(), FFI, ImageMagick, mod_cgi")
    print("    • ModSecurity: WAF open-source — OWASP CRS melindungi dari SQLi, XSS, RCE")
    print("    • Secure coding: Prepared statements, no eval, whitelist path")
    print("    • File permission: 755/644, root:www-data, .env di luar web root")
    print("    • Server hardening: 20 checklist — prioritas KRITIS dulu")
    print("    • Composer audit: Cek PHP dependency vulnerability")
    print()
    print("  📌 LATIHAN LANJUTAN:")
    print("    1. Cek versi: node --version, npm --version, php --version")
    print("    2. Cek disable_functions: php -i | grep disable_functions")
    print("    3. Coba jalankan: php -r \"echo exec('id');\" (apakah di-disable?)")
    print("    4. Buat script Node.js sederhana dengan Helmet.js")
    print("    5. Jalankan npm audit (butuh package.json dengan dependencies)")
    print("    6. Cek Apache modules: apache2ctl -M | grep security")
    print("    7. Install ModSecurity di Ubuntu: sudo apt install libapache2-mod-security2")
    print("    8. Cek file permission: ls -la /etc/php/ (perhatikan owner & group)")
    print("    9. Baca php.ini: grep -n 'disable_functions' /etc/php/*/cli/php.ini")
    print("    10. Pelajari Prototype Pollution di Node.js (contoh kode)")
    print("    11. Coba simulasi SQL injection prepared statements (PHP)")
    print("    12. Hardening checklist: cek setidaknya 5 prioritas KRITIS")
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
