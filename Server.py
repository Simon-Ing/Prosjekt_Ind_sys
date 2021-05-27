from pyModbusTCP.server import ModbusServer

# This script is used during debugging to set up a modbus server
server = ModbusServer("192.168.68.113", 502)
print(server.host)

try:
    server.start()
    while True:
        pass

except:
    print("Shutdown server ...")
    server.stop()
    print("Server is offline")