import threading
import requests
import socket
from queue import Queue, Empty
from colorama import Fore, Style, init
import re

init(autoreset=True)

def wayback_subdomains(domain):
    print(f"{Fore.CYAN}[*] Fetching URLs from Wayback Machine for {domain} ...{Style.RESET_ALL}")
    url = f"https://web.archive.org/cdx/search/cdx?url=*.{domain}/*&output=json&fl=original&collapse=urlkey"
    try:
        resp = requests.get(url, timeout=60)
        if resp.status_code != 200:
            print(f"{Fore.RED}[-] Wayback Machine request failed.{Style.RESET_ALL}")
            return []
        data = resp.json()
        urls = [row[0] for row in data[1:]]
        subdomains = set()
        pattern = re.compile(r"https?://([a-zA-Z0-9_\-\.]+)\." + re.escape(domain))
        for u in urls:
            match = pattern.search(u)
            if match:
                subdomains.add(match.group(1) + "." + domain)
        print(f"{Fore.GREEN}[+] Wayback Machine found {len(subdomains)} unique subdomains.{Style.RESET_ALL}")
        return sorted(subdomains)
    except Exception as e:
        print(f"{Fore.RED}[-] Error fetching from Wayback Machine: {e}{Style.RESET_ALL}")
        return []

def is_dns_resolvable(subdomain):
    try:
        socket.gethostbyname(subdomain)
        return True
    except socket.gaierror:
        return False

def check_subdomain():
    while True:
        try:
            fqdn = queue.get(block=False)
        except Empty:
            break

        dns_ok = is_dns_resolvable(fqdn)
        if not dns_ok:
            print(f"{Fore.RED}[DNS] Not resolved: {fqdn}{Style.RESET_ALL}")
            queue.task_done()
            return

        url = f"http://{fqdn}".lower()
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, timeout=2, headers=headers)
            status = response.status_code

            color = (
                Fore.GREEN if status == 200 else
                Fore.YELLOW if 300 <= status < 400 else
                Fore.RED
            )

            print(f"{color}[{status}] {url}{Style.RESET_ALL}")

            if status < 400:
                with lock:
                    discovered_subdomains.append(fqdn)
        except (requests.ConnectionError, requests.Timeout):
            print(f"{Fore.MAGENTA}[X] Connection error: {url}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.MAGENTA}Unexpected error for {url}: {e}{Style.RESET_ALL}")
        finally:
            queue.task_done()

# --- Main ---
domain = input("Enter Your Domain Here: ").strip().lower()
if not domain:
    print("Error: Domain cannot be empty.")
    exit(1)

discovered_subdomains = []
lock = threading.Lock()
queue = Queue()

wayback_subs = wayback_subdomains(domain)
if not wayback_subs:
    print(f"{Fore.YELLOW}No subdomains found in Wayback Machine for this domain.{Style.RESET_ALL}")
    exit(0)

for fqdn in wayback_subs:
    queue.put(fqdn)

print(f"{Fore.YELLOW}[i] Total unique subdomains to check: {len(wayback_subs)}{Style.RESET_ALL}")

thread_count = 10
threads = []
for _ in range(thread_count):
    t = threading.Thread(target=check_subdomain)
    t.start()
    threads.append(t)

queue.join()
for t in threads:
    t.join()

with open("discovered_subdomains.txt", "w") as f:
    f.write("\n".join(discovered_subdomains))

print(f"{Fore.CYAN}Scan complete. Results saved to discovered_subdomains.txt{Style.RESET_ALL}")
print(f"{Fore.GREEN}Total discovered subdomains: {len(discovered_subdomains)}{Style.RESET_ALL}")
print("Exiting...")
# --- End of Script ---