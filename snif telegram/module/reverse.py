import requests
import sys

def check_api_key(api_key, service, signup, arg_name):
    if not api_key:
        print(f"[ERROR] Missing API Key for {service}")
        print("Signup:", signup)
        print("Use:", arg_name)
        sys.exit(1)


def module_reverse(ip, api_key):
    check_api_key(api_key,
                  "Neutrino API",
                  "https://www.neutrinoapi.com/register/",
                  "--api-neutrino")

    url = "https://neutrinoapi.net/ip-lookup"
    params = {"api-key": api_key, "ip": ip}

    r = requests.get(url, params=params)

    if r.status_code != 200:
        print("[ERROR] Reverse DNS failed:", r.text)
    else:
        print("PTR:", r.json().get("hostname", "N/A"))
