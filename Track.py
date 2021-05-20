import cv2
import Kuka
from pyModbusTCP.client import ModbusClient
import time


client = ModbusClient("192.168.0.124", 502)
while not client.open():
    print("Connecting to Modbus...")
print("Connected to Modbus!")
Cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
Kuka.init_GUI()

while True:
    client.open()
    color = 0
    x = y = 0
    yellow = client.read_coils(10)[0]
    green = client.read_coils(11)[0]
    red = client.read_coils(12)[0]
    blue = client.read_coils(13)[0]

    print(yellow, green, red, blue)

    ret, frame = Cap.read()
    blur = cv2.GaussianBlur(frame, (25, 25), 10)

    lower_yellow, upper_yellow, lower_green, upper_green, lower_red, upper_red, lower_blue, upper_blue = Kuka.calibrate(blur)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    if yellow:
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
        x, y = Kuka.find(mask)
        cv2.circle(frame, (x, y), 7, (0, 0, 0), -1)
        cv2.putText(frame, "Yellow", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        color = 1

    if green and x == 0:
        mask = cv2.inRange(hsv, lower_green, upper_green)
        x, y = Kuka.find(mask)
        cv2.circle(frame, (x, y), 7, (0, 0, 0), -1)
        cv2.putText(frame, "Green", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        color = 2

    if red and x == 0:
        mask = cv2.inRange(hsv, lower_red, upper_red)
        x, y = Kuka.find(mask)
        cv2.circle(frame, (x, y), 7, (0, 0, 0), -1)
        cv2.putText(frame, "Red", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        color = 3

    if blue and x == 0:
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        x, y = Kuka.find(mask)
        cv2.circle(frame, (x, y), 7, (0, 0, 0), -1)
        cv2.putText(frame, "Blue", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        color = 4

    client.write_single_register(32001, x)
    client.write_single_register(32002, y)
    #client.write_single_register(32003, color)
    cv2.imshow("result", frame)
    key = cv2.waitKey(5)


    if key == 27:
        break

Cap.release()
cv2.destroyAllWindows()
