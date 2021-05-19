import cv2
import numpy as np

import imutils

def nothing(x):
    pass


def init_GUI():
    cv2.namedWindow("GUI", cv2.WINDOW_KEEPRATIO)
    cv2.createTrackbar("LH_YELLOW", "GUI", 9, 255, nothing)
    cv2.createTrackbar("LS_YELLOW", "GUI", 29, 255, nothing)
    cv2.createTrackbar("LV_YELLOW", "GUI", 194, 255, nothing)
    cv2.createTrackbar("UH_YELLOW", "GUI", 33, 255, nothing)
    cv2.createTrackbar("US_YELLOW", "GUI", 151, 255, nothing)
    cv2.createTrackbar("UV_YELLOW", "GUI", 255, 255, nothing)

    cv2.createTrackbar("LH_GREEN", "GUI", 31, 255, nothing)
    cv2.createTrackbar("LS_GREEN", "GUI", 22, 255, nothing)
    cv2.createTrackbar("LV_GREEN", "GUI", 121, 255, nothing)
    cv2.createTrackbar("UH_GREEN", "GUI", 90, 255, nothing)
    cv2.createTrackbar("US_GREEN", "GUI", 81, 255, nothing)
    cv2.createTrackbar("UV_GREEN", "GUI", 217, 255, nothing)

    cv2.createTrackbar("LH_RED", "GUI", 0, 255, nothing)
    cv2.createTrackbar("LS_RED", "GUI", 53, 255, nothing)
    cv2.createTrackbar("LV_RED", "GUI", 224, 255, nothing)
    cv2.createTrackbar("UH_RED", "GUI", 8, 255, nothing)
    cv2.createTrackbar("US_RED", "GUI", 156, 255, nothing)
    cv2.createTrackbar("UV_RED", "GUI", 255, 255, nothing)

    cv2.createTrackbar("LH_BLUE", "GUI", 97, 255, nothing)
    cv2.createTrackbar("LS_BLUE", "GUI", 208, 255, nothing)
    cv2.createTrackbar("LV_BLUE", "GUI", 144, 255, nothing)
    cv2.createTrackbar("UH_BLUE", "GUI", 115, 255, nothing)
    cv2.createTrackbar("US_BLUE", "GUI", 255, 255, nothing)
    cv2.createTrackbar("UV_BLUE", "GUI", 255, 255, nothing)


def calibrate(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    l_h_y = cv2.getTrackbarPos("LH_YELLOW", "GUI")
    l_s_y = cv2.getTrackbarPos("LS_YELLOW", "GUI")
    l_v_y = cv2.getTrackbarPos("LV_YELLOW", "GUI")
    u_h_y = cv2.getTrackbarPos("UH_YELLOW", "GUI")
    u_s_y = cv2.getTrackbarPos("US_YELLOW", "GUI")
    u_v_y = cv2.getTrackbarPos("UV_YELLOW", "GUI")
    l_b_y = np.array([l_h_y, l_s_y, l_v_y])
    u_b_y = np.array([u_h_y, u_s_y, u_v_y])
    mask_yellow = cv2.inRange(hsv, l_b_y, u_b_y)
    res_yellow = cv2.bitwise_and(frame, frame, mask=mask_yellow)
    cv2.putText(res_yellow, "Yellow", (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 200), 2)

    l_h_g = cv2.getTrackbarPos("LH_GREEN", "GUI")
    l_s_g = cv2.getTrackbarPos("LS_GREEN", "GUI")
    l_v_g = cv2.getTrackbarPos("LV_GREEN", "GUI")
    u_h_g = cv2.getTrackbarPos("UH_GREEN", "GUI")
    u_s_g = cv2.getTrackbarPos("US_GREEN", "GUI")
    u_v_g = cv2.getTrackbarPos("UV_GREEN", "GUI")
    l_b_g = np.array([l_h_g, l_s_g, l_v_g])
    u_b_g = np.array([u_h_g, u_s_g, u_v_g])
    mask_green = cv2.inRange(hsv, l_b_g, u_b_g)
    res_green = cv2.bitwise_and(frame, frame, mask=mask_green)
    cv2.putText(res_green, "Green", (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    l_h_r = cv2.getTrackbarPos("LH_RED", "GUI")
    l_s_r = cv2.getTrackbarPos("LS_RED", "GUI")
    l_v_r = cv2.getTrackbarPos("LV_RED", "GUI")
    u_h_r = cv2.getTrackbarPos("UH_RED", "GUI")
    u_s_r = cv2.getTrackbarPos("US_RED", "GUI")
    u_v_r = cv2.getTrackbarPos("UV_RED", "GUI")
    l_b_r = np.array([l_h_r, l_s_r, l_v_r])
    u_b_r = np.array([u_h_r, u_s_r, u_v_r])
    mask_red = cv2.inRange(hsv, l_b_r, u_b_r)
    res_red = cv2.bitwise_and(frame, frame, mask=mask_red)
    cv2.putText(res_red, "Red", (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    l_h_b = cv2.getTrackbarPos("LH_BLUE", "GUI")
    l_s_b = cv2.getTrackbarPos("LS_BLUE", "GUI")
    l_v_b = cv2.getTrackbarPos("LV_BLUE", "GUI")
    u_h_b = cv2.getTrackbarPos("UH_BLUE", "GUI")
    u_s_b = cv2.getTrackbarPos("US_BLUE", "GUI")
    u_v_b = cv2.getTrackbarPos("UV_BLUE", "GUI")
    l_b_b = np.array([l_h_b, l_s_b, l_v_b])
    u_b_b = np.array([u_h_b, u_s_b, u_v_b])
    mask_blue = cv2.inRange(hsv, l_b_b, u_b_b)
    res_blue = cv2.bitwise_and(frame, frame, mask=mask_blue)
    cv2.putText(res_blue, "Blue", (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    # cv2.imshow("blue", res_blue)

    top = np.hstack((res_yellow, res_green))
    bottom = np.hstack((res_red, res_blue))
    img = np.vstack((top, bottom))
    cv2.imshow("Calibration", cv2.resize(img, (0, 0), fx=0.6, fy=0.6))
    return l_b_y, u_b_y, l_b_g, u_b_g, l_b_r, u_b_r, l_b_b, u_b_b


def find(mask):
    x = y = 0
    contour = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contour = imutils.grab_contours(contour)
    for c in contour:
        area = cv2.contourArea(c)
        if area > 500:
            m = cv2.moments(c)
            x = int(m["m10"] / m["m00"])
            y = int(m["m01"] / m["m00"])
            return x, y
    return x, y