#!/usr/bin/python3
import tkinter
from zeroconf import IPVersion, ServiceInfo, Zeroconf
import qrcode
import socket
import uploadserver
from os import chdir, getcwd
import threading
import time
from tkinter import filedialog

print("Change Dir? (y/n)")
a = input("#")
DIRECTORY = getcwd()

if (a.lower() == 'y'):
    root = tkinter.Tk()
    root.wm_withdraw()
    DIRECTORY = filedialog.askdirectory()
    root.destroy()
dir = getcwd()
print(dir)
chdir('../')


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip = (s.getsockname()[0])
s.close()

print(f"Current IP : {ip}")

url = "http://" + ip + ":8000"


print("----- UPLOAD SERVER -----")
qr2 = qrcode.QRCode()
qr2.add_data(url + "/upload")
qr2.print_ascii()

print("----- DOWNLOAD SERVER -----")
qr = qrcode.QRCode()
qr.add_data(url)
qr.print_ascii()

print()
print(url)
print()

chdir(DIRECTORY)


website = threading.Thread(target=uploadserver.main, daemon=True)

website.start()


ip_version = IPVersion.V4Only

desc = {'URL': f'http://{ip}:8000'}

info = ServiceInfo(
    "_http._tcp.local.",
    f"{socket.gethostname()}._http._tcp.local.",
    addresses=[ip],
    port=8000,
    properties=desc,
    server="ash-2.local.",
)
zeroconf = Zeroconf(ip_version=ip_version)
print("Registration of a service, press Ctrl-C to exit...")
zeroconf.register_service(info)


try:
    while True:
        time.sleep(0.5)
except KeyboardInterrupt:
    pass
finally:
    print("Unregistering...")
    zeroconf.unregister_service(info)
    zeroconf.close()
    time.sleep(1)
