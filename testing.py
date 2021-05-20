import cv2

Cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    #ret, frame = Cap.read()
    frame = cv2.imread("c3po.png")
    blur = cv2.GaussianBlur(frame, (19, 19), 10)
    cv2.imshow("frame", frame)
    cv2.imshow("blur", blur)
    key = cv2.waitKey(1)
    if key == 27:
        break