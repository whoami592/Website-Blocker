#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Website Blocker / Unblocker (Windows browsers: Chrome, Edge, Firefox, Brave)
Coded by: Cyber Security Engineer Mr Sabaz Ali Khan

Blocks and unblocks websites on your own system using the hosts file.
Also turns off "Secure DNS" in Chrome / Edge / Firefox, because that
feature lets browsers bypass the hosts file.
Also works on Linux/macOS (hosts file only). Needs Administrator / root.
"""

import os
import sys
import platform
import subprocess

BANNER = r"""
⠀⠀⠀⢀⣴⣾⣿⣿⣿⡶⢦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⠴⢾⣿⣿⣿⣷⣦⡀⠀⠀⠀
⠀⠀⣰⣿⣿⣿⣿⣿⣿⣿⣷⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣡⣴⣾⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀
⠀⠀⠉⠀⠀⠀⠀⠈⠙⠻⣿⣿⣿⣷⡄⠀⠀⠀⠀⠀⣰⣿⣿⣿⡿⠛⠉⠁⠀⠀⠀⠈⠉⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣯⠁⠀⠀⠀⠀⠀⢈⣿⠟⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢀⡴⢖⣛⣧⣴⣶⣤⣄⠹⡆⡀⠀⠀⠀⠀⡼⢃⣤⣴⣶⣧⣽⣛⡲⣤⠀⠀⠀⠀⠀
⠀⢱⣄⣴⣟⠾⣿⣿⣿⣿⣿⣿⣿⡇⠀⡇⠀⠀⠀⡇⠀⣿⣿⣿⣿⣿⣿⣿⣿⣞⣷⣄⣴⠃⠀
⢠⠟⠉⠉⠉⠛⠓⠿⠏⠸⠟⠛⠉⠀⢠⡇⠀⠀⠀⣿⠀⠀⠉⠛⠻⠇⠿⠟⠛⠋⠉⠉⠙⠻⡀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⡇⠀⠀⠀⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡾⢿⡇⠀⠀⠀⢿⠿⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⡄⠀⠀⠀⠀⠀⠀⠀⣀⣤⢴⠏⠀⣸⠁⠀⠀⠀⢸⡆⠈⢳⡀⣤⡀⠀⠀⠀⠀⠀⠀⠀⡄⠀
⠀⢹⣶⢤⣤⡤⠴⠶⠛⠉⠀⠸⠀⣄⢻⣄⠀⠀⢀⣸⢃⣀⠰⠃⠈⠙⠓⠶⠤⣤⣤⢤⣾⠃⠀
⠀⠈⢿⣆⠻⣿⣄⠀⠀⠀⠀⠀⠀⠉⣱⣬⣍⣉⣯⣥⡉⠁⠀⠀⠀⠀⠀⠀⣴⣿⢃⣾⡏⠀⠀
⠀⠀⠈⢿⣆⠹⣿⣧⣀⣀⣀⣀⣤⣴⣿⣿⠟⠙⢿⣿⣿⣦⣄⣀⣀⣀⣠⣾⡿⠁⣼⠟⠀⠀⠀
⠀⠀⠀⠈⢿⣦⡈⠻⠿⠿⠿⠿⢿⣿⣿⣋⣀⣀⣀⣻⣿⣿⠿⠿⠿⠿⠿⠛⣠⣾⠏⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠻⣎⠓⢤⣀⠀⠀⠀⠉⠉⠉⠉⠉⠉⠉⠉⠁⠀⠀⠀⣀⠴⢊⡿⠋⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠘⢧⠀⠀⠀⠀⠀⠀⠀⢤⣄⣀⣠⡄⠀⠀⠀⠀⠀⠀⢠⠞⠁⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠱⣄⠀⠀⠀⠀⠀⠀⣿⣿⡏⠀⠀⠀⠀⠀⠀⡠⠃⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⣿⣿⣷⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""

AUTHOR = "Coded by Cyber Security Engineer Mr Sabaz Ali Khan"

IS_WINDOWS = platform.system() == "Windows"
REDIRECT_IP = "127.0.0.1"
REDIRECT_IP6 = "::1"
MARK_START = "# --- WEBSITE BLOCKER START ---"
MARK_END = "# --- WEBSITE BLOCKER END ---"


def hosts_path():
    if IS_WINDOWS:
        root = os.environ.get("SystemRoot", r"C:\Windows")
        return os.path.join(root, "System32", "drivers", "etc", "hosts")
    return "/etc/hosts"


HOSTS = hosts_path()


# ---------------------------------------------------------------- admin ----
def is_admin():
    try:
        if IS_WINDOWS:
            import ctypes
            return bool(ctypes.windll.shell32.IsUserAnAdmin())
        return os.geteuid() == 0
    except Exception:
        return False


def relaunch_as_admin():
    """On Windows, re-open this script with the 'Run as administrator' prompt."""
    import ctypes
    params = " ".join(f'"{a}"' for a in sys.argv)
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, params, None, 1
    )


# ---------------------------------------------------------------- hosts ----
def clean_domain(text):
    d = text.strip().lower()
    for prefix in ("https://", "http://"):
        if d.startswith(prefix):
            d = d[len(prefix):]
    d = d.split("/")[0].split(":")[0].strip()
    if d.startswith("www."):
        d = d[4:]
    return d


def read_hosts():
    with open(HOSTS, "r", encoding="utf-8", errors="ignore") as f:
        return f.read().splitlines()


def write_hosts(lines):
    with open(HOSTS, "w", encoding="utf-8") as f:
        f.write("\n".join(lines).rstrip("\n") + "\n")


def split_sections(lines):
    """Split the hosts file into (before, blocked domains, after)."""
    before, blocked, after = [], [], []
    state = 0
    for line in lines:
        s = line.strip()
        if s == MARK_START:
            state = 1
            continue
        if s == MARK_END:
            state = 2
            continue
        if state == 0:
            before.append(line)
        elif state == 1:
            parts = s.split()
            if len(parts) >= 2:
                d = parts[1]
                if not d.startswith("www.") and d not in blocked:
                    blocked.append(d)
        else:
            after.append(line)
    return before, blocked, after


def save(before, blocked, after):
    out = list(before)
    while out and out[-1].strip() == "":
        out.pop()
    if blocked:
        out.append("")
        out.append(MARK_START)
        for d in blocked:
            for host in (d, "www." + d):
                out.append(f"{REDIRECT_IP} {host}")
                out.append(f"{REDIRECT_IP6} {host}")
        out.append(MARK_END)
    out.extend(after)
    write_hosts(out)
    flush_dns()


def flush_dns():
    try:
        system = platform.system()
        if system == "Windows":
            subprocess.run(["ipconfig", "/flushdns"], capture_output=True)
        elif system == "Darwin":
            subprocess.run(["dscacheutil", "-flushcache"], capture_output=True)
            subprocess.run(["killall", "-HUP", "mDNSResponder"], capture_output=True)
        else:
            subprocess.run(["resolvectl", "flush-caches"], capture_output=True)
    except Exception:
        pass


# -------------------------------------------------- browser Secure DNS ----
BROWSER_POLICIES = [
    # (registry path, value name, value to disable DoH)
    (r"SOFTWARE\Policies\Google\Chrome", "DnsOverHttpsMode", "off"),
    (r"SOFTWARE\Policies\Microsoft\Edge", "DnsOverHttpsMode", "off"),
    (r"SOFTWARE\Policies\BraveSoftware\Brave", "DnsOverHttpsMode", "off"),
]


def disable_secure_dns():
    """Turn off DNS-over-HTTPS in Chrome, Edge, Brave and Firefox (Windows)."""
    if not IS_WINDOWS:
        print("  [!] This option is for Windows only.")
        return
    import winreg
    for path, name, value in BROWSER_POLICIES:
        try:
            key = winreg.CreateKeyEx(
                winreg.HKEY_LOCAL_MACHINE, path, 0, winreg.KEY_SET_VALUE
            )
            winreg.SetValueEx(key, name, 0, winreg.REG_SZ, value)
            winreg.CloseKey(key)
            print(f"  [+] Secure DNS disabled: {path.split(chr(92))[-1]}")
        except OSError as e:
            print(f"  [!] Could not set {path}: {e}")
    # Firefox uses a different mechanism: policies.json next to firefox.exe
    try:
        import json
        for base in (os.environ.get("ProgramFiles", r"C:\Program Files"),
                     os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")):
            ff = os.path.join(base, "Mozilla Firefox")
            if os.path.isdir(ff):
                d = os.path.join(ff, "distribution")
                os.makedirs(d, exist_ok=True)
                p = os.path.join(d, "policies.json")
                data = {"policies": {"DNSOverHTTPS": {"Enabled": False, "Locked": True}}}
                with open(p, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2)
                print("  [+] Secure DNS disabled: Firefox")
                break
    except Exception as e:
        print(f"  [!] Firefox policy failed: {e}")
    print("  Restart your browsers for the change to take effect.")


def close_browsers():
    """Close all browsers so the new block list is picked up immediately."""
    if not IS_WINDOWS:
        return
    for exe in ("chrome.exe", "msedge.exe", "firefox.exe", "brave.exe", "opera.exe"):
        subprocess.run(["taskkill", "/F", "/IM", exe], capture_output=True)
    print("  [i] Browsers were closed. Open them again.")


# -------------------------------------------------------------- actions ----
def block(domains):
    before, blocked, after = split_sections(read_hosts())
    for raw in domains:
        d = clean_domain(raw)
        if not d:
            continue
        if d in blocked:
            print(f"  [=] Already blocked: {d}")
        else:
            blocked.append(d)
            print(f"  [+] Blocked: {d}")
    save(before, blocked, after)


def unblock(domains):
    before, blocked, after = split_sections(read_hosts())
    for raw in domains:
        d = clean_domain(raw)
        if d in blocked:
            blocked.remove(d)
            print(f"  [-] Unblocked: {d}")
        else:
            print(f"  [!] Not in the blocked list: {d}")
    save(before, blocked, after)


def unblock_all():
    before, blocked, after = split_sections(read_hosts())
    save(before, [], after)
    print(f"  [-] All websites unblocked ({len(blocked)}).")


def show_list():
    _, blocked, _ = split_sections(read_hosts())
    if not blocked:
        print("  No websites are blocked.")
        return
    print("  Blocked websites:")
    for i, d in enumerate(blocked, 1):
        print(f"   {i}. {d}")


def ask_domains(prompt):
    text = input(prompt).replace(",", " ")
    return [x for x in text.split() if x]


def menu():
    while True:
        print()
        print("  ========== Website Blocker ==========")
        print("  1. Block website(s)")
        print("  2. Unblock website(s)")
        print("  3. Show blocked list")
        print("  4. Unblock all")
        print("  5. Disable browser Secure DNS (Windows)")
        print("  6. Close all browsers (apply changes now)")
        print("  7. Exit")
        choice = input("\n  Choose an option (1-7): ").strip()
        try:
            if choice == "1":
                block(ask_domains("  Enter website(s), e.g. facebook.com youtube.com: "))
                print("  Tip: use option 5 once, then option 6 if the site still opens.")
            elif choice == "2":
                unblock(ask_domains("  Enter website(s) to unblock: "))
            elif choice == "3":
                show_list()
            elif choice == "4":
                if input("  Unblock everything? (y/n): ").lower() == "y":
                    unblock_all()
            elif choice == "5":
                disable_secure_dns()
            elif choice == "6":
                if input("  Unsaved browser work will be lost. Continue? (y/n): ").lower() == "y":
                    close_browsers()
            elif choice == "7":
                print("  Goodbye!")
                break
            else:
                print("  Invalid option.")
        except PermissionError:
            print("  [!] Permission denied. Run as Administrator / root.")
            break


def main():
    if IS_WINDOWS:
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
    print(BANNER)
    print(AUTHOR.center(60))
    print("=" * 60)

    if not is_admin():
        if IS_WINDOWS:
            print("\n[i] Administrator access is required. Requesting it now...")
            relaunch_as_admin()
        else:
            print("\n[!] Root access required. Run: sudo python3 website_blocker.py")
        sys.exit(0 if IS_WINDOWS else 1)

    # Command line: python website_blocker.py block site1 site2
    if len(sys.argv) >= 2:
        cmd = sys.argv[1].lower()
        args = sys.argv[2:]
        if cmd == "block" and args:
            block(args)
        elif cmd == "unblock" and args:
            unblock(args)
        elif cmd == "list":
            show_list()
        elif cmd == "unblockall":
            unblock_all()
        elif cmd == "securedns":
            disable_secure_dns()
        else:
            print("Usage: website_blocker.py [block|unblock <sites...>|list|unblockall|securedns]")
        return

    menu()


if __name__ == "__main__":
    main()
