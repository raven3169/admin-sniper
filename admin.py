import requests
from time import sleep
import argparse
from urllib.parse import urljoin
from colorama import Fore, Style, init

init(autoreset=True)

# ASCII Banner
banner = f"""{Fore.RED}{Style.BRIGHT}
   AdminSniper
{Style.RESET_ALL}"""

print(banner)
print(f"{Fore.CYAN}{Style.BRIGHT}{' '*20}Coded By Raven\n")
print(f"{Fore.YELLOW} Admin Panel Scriptime Hoşgeldin Dostum :D")


# Argümanlar
parser = argparse.ArgumentParser(description="Admin Panel Finder v2")
parser.add_argument("-u", "--url", required=True, help="Hedef site (http:// ile)")
parser.add_argument("-w", "--wordlist", default="admin.txt", help="Wordlist dosyası")
parser.add_argument("-o", "--output", help="Sonuçları yazacağın dosya")
parser.add_argument("-p", "--proxy", help="Proxy örn: http://127.0.0.1:8080")
args = parser.parse_args()

# Wordlist Yükle
try:
    with open(args.wordlist, "r") as f:
        paths = [line.strip() for line in f if line.strip()]
except FileNotFoundError:
    print(f"{Fore.RED}[!] Wordlist bulunamadı: {args.wordlist}")
    exit()

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/113.0"
}
proxies = {
    "http": args.proxy,
    "https": args.proxy
} if args.proxy else None

found = []

print(f"{Fore.GREEN}\n[+] Tarama başlatılıyor: {args.url}")
print(f"[+] Wordlist: {args.wordlist}\n")

for path in paths:
    full_url = urljoin(args.url.rstrip("/") + "/", path)
    try:
        res = requests.get(full_url, headers=headers, timeout=5, proxies=proxies)
        if res.status_code == 200:
            print(f"{Fore.GREEN}[✓] Bulundu: {full_url}")
            found.append(full_url)
        elif res.status_code == 403:
            print(f"{Fore.YELLOW}[×] Engellendi (403): {full_url}")
        elif res.status_code == 404:
            pass  # Sessiz geç
        else:
            print(f"{Fore.WHITE}[ ] {res.status_code} - {full_url}")
    except Exception as e:
        print(f"{Fore.RED}[!] Hata: {full_url} -> {e}")
    sleep(0.2)

if args.output:
    with open(args.output, "w") as out:
        for url in found:
            out.write(url + "\n")
    print(f"{Fore.CYAN}\n[+] Sonuçlar kaydedildi: {args.output}")
else:
    print(f"{Fore.CYAN}\n[+] Tarama tamamlandı.")