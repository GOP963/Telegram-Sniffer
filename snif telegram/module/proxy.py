import requests
import sys

def check_api_key(api_key, service, signup, arg_name):
    if not api_key:
        print(f"[ERROR] Missing API Key for {service}")
        print("Signup:", signup)
        print("Use:", arg_name)
        sys.exit(1)


def module_proxy(ip, api_key):
    check_api_key(api_key,
                  "Blackbox Proxy API",
                  "https://blackbox.com",
                  "--api-blackbox")

    url = f"https://blackbox.com/api/proxy?ip={ip}&key={api_key}"

    r = requests.get(url)
    if r.status_code != 200:
        print("[ERROR] Proxy check failed:", r.text)
    else:
        print(r.json())
