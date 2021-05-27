import cv2
import Kuka
from pyModbusTCP.client import ModbusClient
import threading

# This is the main python program in the project "Kuka Robot - Industrielle Styresystemer 2021"

# Declare the initial threshold values
thresholds = ((0.0, 0.0, 0.0), (179.0, 255.0, 255.0), (0.0, 0.0, 0.0), (179.0, 255.0, 255.0), (0.0, 0.0, 0.0),
              (179.0, 255.0, 255.0), (0.0, 0.0, 0.0), (179.0, 255.0, 255.0))
event = ''


# Define the calibration function that will run continuously via multithreading
def calibration():
    global event
    global thresholds
    while True:
        event, thresholds = Kuka.calibrate(window)  # Update the threshold values

# Connect to modbus
print("Connecting to Modbus...")
client = ModbusClient("192.168.0.124", 502)
client.open()
print("Connected to Modbus!")

Cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)     # Initialize camera
window = Kuka.init_GUI()                     # Initialize GUI
calibrate_thread = threading.Thread(target=calibration)  # Declare a thread to run the calibration function
calibrate_thread.start()                                 # Start the thread

# Main loop
while True:
    color, x, y, = 0, 0, 0  # Set x, y, and color variables to zero

    # read from modbus
    try:
        yellow = client.read_coils(10)[0]
        green = client.read_coils(11)[0]
        red = client.read_coils(12)[0]
        blue = client.read_coils(13)[0]
    except TypeError:
        print("Modbus Error")
        yellow, green, red, blue = False, False, False, False
        pass

    print(yellow, green, red, blue)
    ret, frame = Cap.read()                         # Read from camera
    blur = cv2.GaussianBlur(frame, (25, 25), 10)    # Blur the image
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)     # make a HSV version of the blurred image
    Kuka.show_cal_screen(hsv, frame, thresholds)    # Show the calibration screen


    # If yellow variable is True, make a mask from the threshold values and find the position of the object-
    # draw a circle on the object and write "yellow" by the circle, set color variable to 1 representing yellow
    if yellow:
        mask = cv2.inRange(hsv, thresholds[0], thresholds[1])
        found, x, y = Kuka.find(mask)
        cv2.circle(frame, (x, y), 7, (0, 0, 0), -1)
        cv2.putText(frame, "Yellow", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        if found:
            color = 1

    # If green variable is True and no yellow object was found, do the same as above for green, then red, then blue
    if green and color == 0:
        mask = cv2.inRange(hsv, thresholds[2], thresholds[3])
        found, x, y = Kuka.find(mask)
        cv2.circle(frame, (x, y), 7, (0, 0, 0), -1)
        cv2.putText(frame, "Green", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        if found:
            color = 2

    if red and color == 0:
        mask = cv2.inRange(hsv, thresholds[4], thresholds[5])
        found, x, y = Kuka.find(mask)
        cv2.circle(frame, (x, y), 7, (0, 0, 0), -1)
        cv2.putText(frame, "Red", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        if found:
            color = 3

    if blue and color == 0:
        mask = cv2.inRange(hsv, thresholds[6], thresholds[7])
        found, x, y = Kuka.find(mask)
        cv2.circle(frame, (x, y), 7, (0, 0, 0), -1)
        cv2.putText(frame, "Blue", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        if found:
            color = 4

    # write variables for x- and y-position and color to modbus
    client.write_single_register(32001, x)
    client.write_single_register(32002, y)
    client.write_single_register(32003, color)

    #show video feed
    cv2.imshow("result", frame)

    # if esc key is pressed, break the loop and end the program
    key = cv2.waitKey(5)
    if key == 27:
        break
    if event == 'quit':
        break

Cap.release()
cv2.destroyAllWindows()
