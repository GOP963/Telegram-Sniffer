import requests
import sys

def check_api_key(api_key, service, signup, arg_name):
    if not api_key:
        print(f"\n[ERROR] Missing API Key for {service}")
        print("Signup:", signup)
        print("Pass API key using:", arg_name)
        sys.exit(1)


def module_whois(ip, api_key):
    check_api_key(api_key,
                  "WhoisFreaks API",
                  "https://whoisfreaks.com",
                  "--api-whoisfreaks")

    url = f"https://whoisfreaks.com/api?ip={ip}&key={api_key}"

    r = requests.get(url)
    if r.status_code != 200:
        print("[ERROR] Whois API failed:", r.text)
    else:
        print(r.json())
