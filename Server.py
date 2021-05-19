from pyModbusTCP.server import ModbusServer, DataBank
from time import sleep

server = ModbusServer("192.168.1.192", 502)

print(server.host)


try:
    print("Start server...")
    server.start()
    print("Server is online")
    state = [0]
    while True:
        #DataBank.set_words(0, [int(uniform(0, 100))])
        if state != DataBank.get_words(1):
            state = DataBank.get_words(1)
            print("Value of Register 1 has changed to " +str(state))
        sleep(0.5)

except:
    print("Shutdown server ...")
    server.stop()
    print("Server is offline")