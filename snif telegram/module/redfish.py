from colorama import Fore as color
from time import sleep
from requests import get
try:
    from bs4 import BeautifulSoup
except:
    print("run Command :"+color.GREEN+"pip install bs4")
try:
    from fuzzywuzzy import fuzz
except:
    print("run Command :"+color.GREEN+"pip install fuzzywuzzy")
bold = "\033[1m"
enbold = "\033[0m"


def banner():
    print(color.RED+r"""
          /¸...¸`:·
      ¸.·´  ¸   `·.¸.·´)
     : © ):´;      ¸  {
      `·.¸ `·  ¸.·´\`·¸)
          `\\´´\¸.·´  """)
    sleep(0.3)

print("for fating and best working fuzzywuzzy"+color.GREEN+"please (pip install python-Levenshtein)")
def banner2():
    print(color.RED+"""

 ██▀███  ▓█████ ▓█████▄   █████▒ ██▓  ██████  ██░ ██
▓██ ▒ ██▒▓█   ▀ ▒██▀ ██▌▓██   ▒ ▓██▒▒██    ▒ ▓██░ ██▒
▓██ ░▄█ ▒▒███   ░██   █▌▒████ ░ ▒██▒░ ▓██▄   ▒██▀▀██░
▒██▀▀█▄  ▒▓█  ▄ ░▓█▄   ▌░▓█▒  ░ ░██░  ▒   ██▒░▓█ ░██
░██▓ ▒██▒░▒████▒░▒████▓ ░▒█░    ░██░▒██████▒▒░▓█▒░██▓
░ ▒▓ ░▒▓░░░ ▒░ ░ ▒▒▓  ▒  ▒ ░    ░▓  ▒ ▒▓▒ ▒ ░ ▒ ░░▒░▒
  ░▒ ░ ▒░ ░ ░  ░ ░ ▒  ▒  ░       ▒ ░░ ░▒  ░ ░ ▒ ░▒░ ░
  ░░   ░    ░    ░ ░  ░  ░ ░     ▒ ░░  ░  ░   ░  ░░ ░
                     <<<CHARON>>>         """)
    sleep(0.3)


def run_redfish_scanner():
    banner()
    banner2()
    print(bold+color.LIGHTBLUE_EX+"""
    -------------------------
    | coder : CHARON        |
    | ID : @CHARON369       |
    | channel : @Norach369  |
    ------------------------- """+enbold)
    sleep(0.2)

    hostname = input(color.BLACK + color.RED + 'HOSTNAME (http/https): ' + color.RESET)

    print(color.GREEN + f"[*] Scanning {hostname} ...")

    try:
        text = get(hostname, timeout=3).text
    except Exception as e:
        print(color.RED + f"[!] Cannot connect: {e}")
        return

    soup = BeautifulSoup(text, "html.parser")
    links_detected = []

    # -- Title --
    try:
        print(color.MAGENTA + '[?] Title: ' + soup.title.text.strip())
    except:
        print(color.RED + '[?] Title: NULL')

    print(color.CYAN + "\n[+] Extracting internal links...")

    # -- Extract all <a href> --
    for link in soup.find_all("a"):
        href = link.get("href")

        if not href:
            continue

        # Normalize relative URLs
        if href.startswith("/"):
            href = hostname.rstrip("/") + href

        # Only HTTP links
        if not href.startswith("http"):
            continue

        # Skip duplicates
        if href in links_detected:
            continue

        # Internal domain detection
        try:
            if hostname.split("/")[2] in href:
                print(color.GREEN + f"--- Internal link found: {href}")
                links_detected.append(href)
                continue
        except:
            pass

        # Fuzzy match based on anchor text
        anchor = link.text.strip()
        if anchor and fuzz.ratio(anchor.lower(), href.lower()) >= 60:
            print(color.GREEN + f"--- Fuzzy match: {href}")
            links_detected.append(href)

    if links_detected == []:
        print(color.RED + "--- No useful internal links found.")
