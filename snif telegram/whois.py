import sys

# ---------------------------------------------------------
# Color system
# ---------------------------------------------------------
try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    print("\033[91m[ERROR] Missing library 'colorama'. Install: pip install colorama\033[0m")
    sys.exit(1)


# ---------------------------------------------------------
# Library Checker Function
# ---------------------------------------------------------
def check_library(lib_name, install_cmd):
    try:
        __import__(lib_name)
    except ImportError:
        print(Fore.YELLOW + f"[WARNING] Missing library: {lib_name}")
        print(Fore.YELLOW + f"→ Install it using: {install_cmd}\n")
        sys.exit(1)


# ---------------------------------------------------------
# Check required libraries BEFORE argparse runs
# ---------------------------------------------------------
check_library("fuzzywuzzy", "pip install fuzzywuzzy")
check_library("Levenshtein", "pip install python-Levenshtein")
check_library("requests", "pip install requests")
check_library("bs4", "pip install beautifulsoup4")

# ---------------------------------------------------------
# Now safe to import
# ---------------------------------------------------------
from fuzzywuzzy import fuzz
import argparse

from module.redfish import run_redfish_scanner
from module.whois_module import module_whois
from module.reverse import module_reverse
from module.proxy import module_proxy
from module.blacklist import module_blacklist
from module.scanner import module_scan
from module.geo import module_location


# ---------------------------------------------------------
# Argument parser
# ---------------------------------------------------------
parser = argparse.ArgumentParser(
    description=Fore.CYAN + "IP Intelligence Toolkit - Multi Tool",
)

parser.add_argument("-I", "--ip", help="Target IP address")

parser.add_argument(
    "--module",
    type=lambda s: s.lower(),
    choices=[
        "redfish",
        "location",
        "whois",
        "reverse",
        "proxy",
        "blacklist",
        "scan"
    ],
    help="Module to run"
)

parser.add_argument("--ports", help="Port range for scan: start-end")
parser.add_argument("--api-whoisfreaks", help="API key for WhoisFreaks")
parser.add_argument("--api-neutrino", help="API key for Neutrino API")
parser.add_argument("--api-blackbox", help="API key for Blackbox")
parser.add_argument("--api-apivoid", help="API key for APIVoid")

args = parser.parse_args()


# ---------------------------------------------------------
# Execute module
# ---------------------------------------------------------
if args.module == "redfish":
    run_redfish_scanner()

elif args.module == "location":
    if not args.ip:
        print(Fore.RED + "[ERROR] You must provide --ip for location module")
        sys.exit(1)
    module_location(args.ip)

elif args.module == "whois":
    if not args.api_whoisfreaks:
        print(Fore.YELLOW + "[WARNING] Missing API key: --api-whoisfreaks")
        print(Fore.YELLOW + "→ Register: https://whoisfreaks.com\n")
        sys.exit(1)
    module_whois(args.ip, args.api_whoisfreaks)

elif args.module == "reverse":
    if not args.api_neutrino:
        print(Fore.YELLOW + "[WARNING] Missing API key: --api-neutrino")
        print(Fore.YELLOW + "→ Register: https://neutrinoapi.com\n")
        sys.exit(1)
    module_reverse(args.ip, args.api_neutrino)

elif args.module == "proxy":
    if not args.api_blackbox:
        print(Fore.YELLOW + "[WARNING] Missing API key: --api-blackbox")
        print(Fore.YELLOW + "→ Register: https://blackbox.ai\n")
        sys.exit(1)
    module_proxy(args.ip, args.api_blackbox)

elif args.module == "blacklist":
    if not args.api_apivoid:
        print(Fore.YELLOW + "[WARNING] Missing API key: --api-apivoid")
        print(Fore.YELLOW + "→ Register: https://apivoid.com\n")
        sys.exit(1)
    module_blacklist(args.ip, args.api_apivoid)

elif args.module == "scan":
    if not args.ports:
        print(Fore.RED + "[ERROR] For scanning you must set --ports start-end")
        sys.exit(1)

    try:
        start, end = map(int, args.ports.split("-"))
    except:
        print(Fore.RED + "[ERROR] Invalid --ports format. Example: --ports 1-1000")
        sys.exit(1)

    module_scan(args.ip, start, end)
