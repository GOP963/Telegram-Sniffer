import socket
import threading

print_lock = threading.Lock()

def port_worker(ip, port):
    try:
        s = socket.socket()
        s.settimeout(0.5)
        if s.connect_ex((ip, port)) == 0:
            with print_lock:
                print(f"[OPEN] {port}")
        s.close()
    except:
        pass


def module_scan(ip, start, end):
    print(f"Scanning {ip} ports {start}-{end}")
    for port in range(start, end + 1):
        t = threading.Thread(target=port_worker, args=(ip, port))
        t.start()
