import time
from pyModbusTCP.client import ModbusClient
client = ModbusClient("192.168.0.124", 502, timeout=1)
print("open:", client.open())
while True:
    adr = int