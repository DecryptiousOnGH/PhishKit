# PhishKit-Builder

**Author:** Decryptious_ on Discord / Punchborn on IG  
**License:** MIT  
**Platforms:** Linux, Windows, macOS

An educational phishing awareness testing tool for authorized security training. Clones target login pages, injects a credential harvester for demonstration purposes, and generates detailed reports.

**FOR AUTHORIZED SECURITY TESTING & EDUCATIONAL PURPOSES ONLY.**

---

## ⚠️ Legal Notice

This tool is designed for:
- **Security awareness training** within your organization
- **Authorized penetration testing** with written permission
- **Educational demonstrations** in controlled environments

**Misuse of this tool is illegal.** The author assumes no liability for unauthorized use. Always obtain explicit written permission before testing any system you do not own.

---

## Features

- **Page Cloning:** Downloads and clones any login page with assets (CSS, JS, images)
- **Harvester Injection:** Injects JavaScript credential capture into forms
- **Built-in Server:** Lightweight HTTP server to serve cloned pages
- **Data Export:** Saves harvested credentials to JSON with metadata
- **Report Generation:** Statistical analysis of test results
- **Custom JavaScript:** Inject additional payloads for advanced testing
- **Redirect Control:** Configure post-harvest redirect URL

---

## Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Step 1: Download
git clone https://github.com/DecryptiousOnGH/PhishKit-Builder
cd PhishKit-Builder
pip install -r requirements.txt

## Usage 

**Clone a Target Page**
python3 phishkit.py clone -u https://target-site.com/login -o output_dir

**Clone with Custom Redirect**
python3 phishkit.py clone -u https://example.com/login --redirect https://example.com/success

**Clone with Custom JavaScript**
python3 phishkit.py clone -u https://example.com/login --custom-js payload.js

**Generate Report from Harvest**
python3 phishkit.py report -f harvested_credentials.json

**List Capabilities**
python3 phishkit.py templates

## Options

Command	    Flag	   Description
clone	  -u, --url	        Required. Target URL to clone
clone	  -o, --output	    Output directory (default: phishkit_output)
clone	  -p, --port	    Server port (default: 8080)
clone	  --redirect	    URL to redirect after credential harvest
clone	  --custom-js	    Custom JavaScript file to inject
report	  -f, --file	    Harvested credentials JSON file
templates		            List built-in capabilities

## Workflow Example

**1. Clone the Target**

python3 phishkit.py clone -u https://training-site.com/login -o training_phish

Output: 

============================================================
                    PhishKit-Builder
      Educational Phishing Awareness Testing Tool
============================================================
  Author: Decryptious_ on Discord / Punchborn on IG
  Platforms: Linux | Windows | macOS
  Modes: Clone | Harvest | Report
  FOR AUTHORIZED SECURITY TESTING & EDUCATION ONLY
============================================================

[!] WARNING: This tool is for authorized testing only
[!] Ensure you have explicit permission to test the target
[?] Do you have authorization? (yes/no): yes

[*] Cloning target: https://training-site.com/login
[+] Page cloned successfully
[+] Output: /path/to/training_phish
[*] To start harvester server:
    cd training_phish
    python3 server.py

**2. Start the Server**

cd training_phish
python3 server.py

Output: 

[*] Harvester server running on http://0.0.0.0:8080
[*] Press Ctrl+C to stop

**3. Conduct Training**
Direct trainees to your server. When they enter credentials:

[HARVEST] 2026-04-22T21:42:00 | IP: 192.168.1.50 | Data: {"username":"testuser","password":"testpass123"}

**4. Generate Report**

python3 phishkit.py report -f training_phish/harvested_credentials.json

Output:

============================================================
              PhishKit-Builder Harvest Report
============================================================
  Author: Decryptious_ on Discord / Punchborn on IG
============================================================

[*] Total harvests: 15
[*] Unique IPs: 12

[*] Harvest Timeline:
  2026-04-22T21:42:00 | 192.168.1.50 | Mozilla/5.0...
  2026-04-22T21:43:15 | 192.168.1.51 | Mozilla/5.0...

[*] Field Analysis:
  username: 15 occurrences
  password: 15 occurrences
  remember_me: 8 occurrences

[+] Report saved: phishkit_report_20260422_214200.json

## Security Features

Authorization Prompt: Requires explicit confirmation before cloning
No External Dependencies: Server uses only Python stdlib
JSON Export: Structured data for analysis
IP Logging: Tracks source of all harvests
User Agent Logging: Identifies client browsers
Timestamp Recording: Full audit trail

## Custom JavaScript Injection
Create a .js file with additional payloads:

// custom_payload.js
console.log("Custom tracking loaded");
// Add keylogger, geolocation, etc. for advanced training

Run with:

python3 phishkit.py clone -u https://example.com/login --custom-js custom_payload.js

## Disclaimer

This tool is for authorized security testing and educational purposes only.
Unauthorized access to computer systems is illegal under the Computer Fraud and Abuse Act (CFAA) and similar laws worldwide. The author explicitly condemns misuse and assumes no liability for illegal activities conducted with this tool.
By using this tool, you agree to:
Only test systems you own or have written authorization to test
Obtain explicit permission from system owners
Use findings to improve security awareness and defenses
Never use harvested credentials for unauthorized access

## Author
Decryptious_ on Discord / Punchborn on IG 

