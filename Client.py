import time
from pyModbusTCP.client import ModbusClient
client = ModbusClient("192.168.1.192", 502, timeout=1)
print("open:", client.open())
while True:
    action = input("action: ")
    try:
        adr = int(input("adress: "))
        if action == "rr":
            print(f"value at {adr}: {client.read_input_registers(adr)}")
        if action == "rc":
            print(f"value at {adr}: {client.read_coils(adr)}")
        if action == "wr":
            val = int(input("value: "))
            print(f"old value at {adr}: {client.read_input_registers(adr)}")
            client.write_single_register(adr, val)
            time.sleep(0.1)
            print(f"new value at {adr}: {client.read_input_registers(adr)}")
        if action == "wc":
            val = input("value: ")
            print(f"old value at {adr}: {client.read_coils(adr)}")
            if val == "t":
                client.write_single_coil(adr, True)
                time.sleep(0.1)
                print(f"new value at {adr}: {client.read_coils(adr)}")
            else:
                client.write_single_coil(adr, False)
                time.sleep(0.1)
                print(f"new value at {adr}: {client.read_coils(adr)}")
    except:
        print("Try again")
