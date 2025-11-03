import requests

PRINTER_IP = "192.168.10.184"   # <-- your Qidi's IP
url = f"http://{PRINTER_IP}:7125/printer/objects/query?toolhead=position"

def get_z_height():
    r = requests.get(url).json()
    return r["result"]["status"]["toolhead"]["position"][2]

