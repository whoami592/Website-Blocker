#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Website Blocker / Unblocker
Coded by: Cyber Security Engineer Mr Sabaz Ali Khan

Hosts file ke zariye apne system par websites block aur unblock karta hai.
Windows, Linux aur macOS par chalta hai. Administrator / root zaroori hai.
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

REDIRECT_IP = "127.0.0.1"
MARK_START = "# --- WEBSITE BLOCKER START ---"
MARK_END = "# --- WEBSITE BLOCKER END ---"


def hosts_path():
    if platform.system() == "Windows":
        root = os.environ.get("SystemRoot", r"C:\Windows")
        return os.path.join(root, "System32", "drivers", "etc", "hosts")
    return "/etc/hosts"


HOSTS = hosts_path()


def is_admin():
    try:
        if platform.system() == "Windows":
            import ctypes
            return bool(ctypes.windll.shell32.IsUserAnAdmin())
        return os.geteuid() == 0
    except Exception:
        return False


def clean_domain(text):
    d = text.strip().lower()
    for prefix in ("https://", "http://"):
        if d.startswith(prefix):
            d = d[len(prefix):]
    d = d.split("/")[0].strip()
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
    """Hosts file ko (pehle, blocked domains, baad) mein baantta hai."""
    before, blocked, after = [], [], []
    state = 0
    for line in lines:
        if line.strip() == MARK_START:
            state = 1
            continue
        if line.strip() == MARK_END:
            state = 2
            continue
        if state == 0:
            before.append(line)
        elif state == 1:
            parts = line.split()
            if len(parts) >= 2 and parts[1] != "www." + parts[1]:
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
            out.append(f"{REDIRECT_IP} {d}")
            out.append(f"{REDIRECT_IP} www.{d}")
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


def block(domains):
    before, blocked, after = split_sections(read_hosts())
    for raw in domains:
        d = clean_domain(raw)
        if not d:
            continue
        if d in blocked:
            print(f"  [=] Pehle se blocked hai: {d}")
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
            print(f"  [!] Blocked list mein nahi mili: {d}")
    save(before, blocked, after)


def unblock_all():
    before, blocked, after = split_sections(read_hosts())
    save(before, [], after)
    print(f"  [-] Sab websites unblock ho gayin ({len(blocked)}).")


def show_list():
    _, blocked, _ = split_sections(read_hosts())
    if not blocked:
        print("  Koi website blocked nahi hai.")
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
        print("  ===== Website Blocker =====")
        print("  1. Website block karein")
        print("  2. Website unblock karein")
        print("  3. Blocked list dekhein")
        print("  4. Sab unblock karein")
        print("  5. Exit")
        choice = input("\n  Option chunein (1-5): ").strip()
        try:
            if choice == "1":
                d = ask_domains("  Website(s) likhein (space/comma se alag): ")
                block(d)
            elif choice == "2":
                d = ask_domains("  Unblock karne wali website(s): ")
                unblock(d)
            elif choice == "3":
                show_list()
            elif choice == "4":
                if input("  Pakka sab unblock karni hain? (y/n): ").lower() == "y":
                    unblock_all()
            elif choice == "5":
                print("  Allah Hafiz!")
                break
            else:
                print("  Galat option.")
        except PermissionError:
            print("  [!] Permission denied. Administrator/root se chalayein.")
            break


def main():
    print(BANNER)
    print(AUTHOR.center(60))
    print("=" * 60)

    if not is_admin():
        print("\n[!] Administrator/root access chahiye.")
        if platform.system() == "Windows":
            print("    CMD/PowerShell ko 'Run as administrator' se kholein.")
        else:
            print("    Is tarah chalayein: sudo python3 website_blocker.py")
        sys.exit(1)

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
        else:
            print("Usage: website_blocker.py [block|unblock <sites...>|list|unblockall]")
        return

    menu()


if __name__ == "__main__":
    main()
