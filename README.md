🚫 Website Blocker

A lightweight Python script that blocks distracting websites by editing the system hosts file, automatically switching blocking on and off according to a daily time window.

Coded by Mr Sabaz Ali Khan — Ethical Hacker, Pakistan

✨ Features
Blocks websites by redirecting them to 127.0.0.1 in the hosts file
Time-based scheduling (default: block from 09:00 to 17:00)
Cross-platform: Windows, Linux and macOS
Skips entries that are already blocked (no duplicates)
Automatically unblocks all sites when you stop the script with Ctrl+C
Zero dependencies — uses only the Python standard library

📋 Requirements
Python 3.6 or newer

Administrator / root privileges (needed to edit the hosts file)

🚀 Installation
bash

git clone https://github.com/whoami592/Website-Blocker

cd website-blocker

▶️ Usage

Linux / macOS

bash

sudo python3 website_blocker.py

Windows — open Command Prompt or PowerShell as Administrator, then run:

powershell

python website_blocker.py

The script checks the time every 60 seconds:

Time of day	Action
Between start and end hour	Websites in the list are blocked
Outside that window	Websites are unblocked

Press Ctrl+C to stop. All blocked sites are removed from the hosts file on exit.

⚙️ Configuration

Edit the constants at the top of website_blocker.py:

python
# Websites to block (include the www. variant too)
WEBSITES = ["facebook.com", "www.facebook.com", "twitter.com", "www.twitter.com"]

# Blocking window, 24-hour format
BLOCK_START_HOUR = 9    # 9 AM
BLOCK_END_HOUR = 17     # 5 PM

# IP that blocked domains are redirected to
REDIRECT_IP = "127.0.0.1"
🗂️ Hosts File Locations
OS	Path
Windows	C:\Windows\System32\drivers\etc\hosts
Linux / macOS	/etc/hosts
🔍 How It Works
The script detects your operating system and picks the correct hosts file path.
It confirms it is running with elevated privileges.
Inside the blocking window it appends 127.0.0.1 <website> lines for every site in WEBSITES.
Outside the window it rewrites the file, removing every line that mentions a listed site.
This repeats every minute until you stop the script.
⚠️ Known Limitations
Back up your hosts file before first use.
Unblocking removes any line containing a listed domain, including lines you added yourself.
On Windows, the admin check always passes, so if you forget to run as Administrator you will see a permission error instead of a warning.
Browsers may cache DNS; restart the browser or flush DNS (ipconfig /flushdns on Windows) if a change doesn't apply immediately.
Blocking via the hosts file can be bypassed by anyone with admin rights, DNS-over-HTTPS or a VPN. It is a productivity aid, not a security control.
🛡️ Disclaimer

This tool is intended for ethical and authorized use only — such as personal productivity and parental controls. Only use it on devices you own or have explicit permission to manage. Unauthorized use may be illegal. The author is not responsible for any misuse or damage.

📄 License

Released under the MIT License. (Add a LICENSE file to your repository.)

👤 Author

Mr Sabaz Ali Khan — Ethical Hacker, Pakistan

⭐ If you find this project useful, consider giving it a star on GitHub!
