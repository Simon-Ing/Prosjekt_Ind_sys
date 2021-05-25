import cv2
import numpy as np
import PySimpleGUI as sg


def nothing(x):
    pass


def init_GUI():
    layout = [[sg.Button('Quit', key='quit', )],
              [sg.Text('YELLOW', text_color='Black', background_color='yellow', font=('helvetica', 15))],
              [sg.Text('hue'),
               sg.Slider((0, 179), 20, key='yhl', enable_events=True),
               sg.Slider((0, 179), 40, key='yhu', enable_events=True),
               sg.Text('sat'),
               sg.Slider((0, 255), 130, key='ysl', enable_events=True),
               sg.Slider((0, 255), 240, key='ysu', enable_events=True),
               sg.Text('val'),
               sg.Slider((0, 255), 130, key='yvl', enable_events=True),
               sg.Slider((0, 255), 220, key='yvu', enable_events=True)],

              [sg.Text('GREEN', text_color='Black', background_color='green', font=('helvetica', 15))],
              [sg.Text('hue'),
               sg.Slider((0, 179), 50, key='ghl', enable_events=True),
               sg.Slider((0, 179), 80, key='ghu', enable_events=True),
               sg.Text('sat'),
               sg.Slider((0, 255), 20, key='gsl', enable_events=True),
               sg.Slider((0, 255), 140, key='gsu', enable_events=True),
               sg.Text('val'),
               sg.Slider((0, 255), 20, key='gvl', enable_events=True),
               sg.Slider((0, 255), 120, key='gvu', enable_events=True)],

              [sg.Text('RED', text_color='Black', background_color='red', font=('helvetica', 15))],
              [sg.Text('hue'),
               sg.Slider((0, 179), 0, key='rhl', enable_events=True),
               sg.Slider((0, 179), 10, key='rhu', enable_events=True),
               sg.Text('sat'),
               sg.Slider((0, 255), 130, key='rsl', enable_events=True),
               sg.Slider((0, 255), 250, key='rsu', enable_events=True),
               sg.Text('val'),
               sg.Slider((0, 255), 90, key='rvl', enable_events=True),
               sg.Slider((0, 255), 170, key='rvu', enable_events=True)],

              [sg.Text('BLUE', text_color='Black', background_color='blue', font=('helvetica', 15))],
              [sg.Text('hue'),
               sg.Slider((0, 179), 80, key='bhl', enable_events=True),
               sg.Slider((0, 179), 160, key='bhu', enable_events=True),
               sg.Text('sat'),
               sg.Slider((0, 255), 0, key='bsl', enable_events=True),
               sg.Slider((0, 255), 40, key='bsu', enable_events=True),
               sg.Text('val'),
               sg.Slider((0, 255), 60, key='bvl', enable_events=True),
               sg.Slider((0, 255), 160, key='bvu', enable_events=True)]
              ]

    window = sg.Window('Title', layout)
    return window

# def init_GUI():
#     cv2.namedWindow("GUI", cv2.WINDOW_NORMAL)
#     cv2.createTrackbar("LH_YELLOW", "GUI", 25, 255, nothing)
#     cv2.createTrackbar("LS_YELLOW", "GUI", 30, 255, nothing)
#     cv2.createTrackbar("LV_YELLOW", "GUI", 100, 255, nothing)
#     cv2.createTrackbar("UH_YELLOW", "GUI", 30, 255, nothing)
#     cv2.createTrackbar("US_YELLOW", "GUI", 180, 255, nothing)
#     cv2.createTrackbar("UV_YELLOW", "GUI", 240, 255, nothing)
#
#     cv2.createTrackbar("LH_GREEN", "GUI", 50, 255, nothing)
#     cv2.createTrackbar("LS_GREEN", "GUI", 0, 255, nothing)
#     cv2.createTrackbar("LV_GREEN", "GUI", 0, 255, nothing)
#     cv2.createTrackbar("UH_GREEN", "GUI", 80, 255, nothing)
#     cv2.createTrackbar("US_GREEN", "GUI", 255, 255, nothing)
#     cv2.createTrackbar("UV_GREEN", "GUI", 255, 255, nothing)
#
#     cv2.createTrackbar("LH_RED", "GUI", 5, 255, nothing)
#     cv2.createTrackbar("LS_RED", "GUI", 50, 255, nothing)
#     cv2.createTrackbar("LV_RED", "GUI", 140, 255, nothing)
#     cv2.createTrackbar("UH_RED", "GUI", 15, 255, nothing)
#     cv2.createTrackbar("US_RED", "GUI", 215, 255, nothing)
#     cv2.createTrackbar("UV_RED", "GUI", 240, 255, nothing)
#
#     cv2.createTrackbar("LH_BLUE", "GUI", 73, 255, nothing)
#     cv2.createTrackbar("LS_BLUE", "GUI", 0, 255, nothing)
#     cv2.createTrackbar("LV_BLUE", "GUI", 0, 255, nothing)
#     cv2.createTrackbar("UH_BLUE", "GUI", 130, 255, nothing)
#     cv2.createTrackbar("US_BLUE", "GUI", 255, 255, nothing)
#     cv2.createTrackbar("UV_BLUE", "GUI", 255, 255, nothing)


def calibrate(window):

    event, values = window.read()
    if event in ('quit', None):
        window.close()

    yellow_lower = (values['yhl'], values['ysl'], values['yvl'])
    yellow_upper = (values['yhu'], values['ysu'], values['yvu'])

    green_lower = (values['ghl'], values['gsl'], values['gvl'])
    green_upper = (values['ghu'], values['gsu'], values['gvu'])

    red_lower = (values['rhl'], values['rsl'], values['rvl'])
    red_upper = (values['rhu'], values['rsu'], values['rvu'])

    blue_lower = (values['bhl'], values['bsl'], values['bvl'])
    blue_upper = (values['bhu'], values['bsu'], values['bvu'])

    return event, (yellow_lower, yellow_upper, green_lower, green_upper, red_lower, red_upper, blue_lower, blue_upper)


def show_cal_screen(hsv, frame, thresholds):
    mask_yellow = cv2.inRange(hsv, thresholds[0], thresholds[1])
    res_yellow = cv2.bitwise_and(frame, frame, mask=mask_yellow)
    cv2.putText(res_yellow, "Yellow", (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 200), 2)
    mask_green = cv2.inRange(hsv, thresholds[2], thresholds[3])
    res_green = cv2.bitwise_and(frame, frame, mask=mask_green)
    cv2.putText(res_green, "Green", (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    mask_red = cv2.inRange(hsv, thresholds[4], thresholds[5])
    res_red = cv2.bitwise_and(frame, frame, mask=mask_red)
    cv2.putText(res_red, "Red", (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    mask_blue = cv2.inRange(hsv, thresholds[6], thresholds[7])
    res_blue = cv2.bitwise_and(frame, frame, mask=mask_blue)
    cv2.putText(res_blue, "Blue", (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    top = np.hstack((res_yellow, res_green))
    bottom = np.hstack((res_red, res_blue))
    img = np.vstack((top, bottom))
    cv2.imshow("Calibration", cv2.resize(img, (0, 0), fx=0.6, fy=0.6))
#
#
# def calibrate(frame):
#     hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
#
#     l_h_y = cv2.getTrackbarPos("LH_YELLOW", "GUI")
#     l_s_y = cv2.getTrackbarPos("LS_YELLOW", "GUI")
#     l_v_y = cv2.getTrackbarPos("LV_YELLOW", "GUI")
#     u_h_y = cv2.getTrackbarPos("UH_YELLOW", "GUI")
#     u_s_y = cv2.getTrackbarPos("US_YELLOW", "GUI")
#     u_v_y = cv2.getTrackbarPos("UV_YELLOW", "GUI")
#     l_b_y = np.array([l_h_y, l_s_y, l_v_y])
#     u_b_y = np.array([u_h_y, u_s_y, u_v_y])
#     mask_yellow = cv2.inRange(hsv, l_b_y, u_b_y)
#     res_yellow = cv2.bitwise_and(frame, frame, mask=mask_yellow)
#     cv2.putText(res_yellow, "Yellow", (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 200), 2)
#
#     l_h_g = cv2.getTrackbarPos("LH_GREEN", "GUI")
#     l_s_g = cv2.getTrackbarPos("LS_GREEN", "GUI")
#     l_v_g = cv2.getTrackbarPos("LV_GREEN", "GUI")
#     u_h_g = cv2.getTrackbarPos("UH_GREEN", "GUI")
#     u_s_g = cv2.getTrackbarPos("US_GREEN", "GUI")
#     u_v_g = cv2.getTrackbarPos("UV_GREEN", "GUI")
#     l_b_g = np.array([l_h_g, l_s_g, l_v_g])
#     u_b_g = np.array([u_h_g, u_s_g, u_v_g])
#     mask_green = cv2.inRange(hsv, l_b_g, u_b_g)
#     res_green = cv2.bitwise_and(frame, frame, mask=mask_green)
#     cv2.putText(res_green, "Green", (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
#
#     l_h_r = cv2.getTrackbarPos("LH_RED", "GUI")
#     l_s_r = cv2.getTrackbarPos("LS_RED", "GUI")
#     l_v_r = cv2.getTrackbarPos("LV_RED", "GUI")
#     u_h_r = cv2.getTrackbarPos("UH_RED", "GUI")
#     u_s_r = cv2.getTrackbarPos("US_RED", "GUI")
#     u_v_r = cv2.getTrackbarPos("UV_RED", "GUI")
#     l_b_r = np.array([l_h_r, l_s_r, l_v_r])
#     u_b_r = np.array([u_h_r, u_s_r, u_v_r])
#     mask_red = cv2.inRange(hsv, l_b_r, u_b_r)
#     res_red = cv2.bitwise_and(frame, frame, mask=mask_red)
#     cv2.putText(res_red, "Red", (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
#
#     l_h_b = cv2.getTrackbarPos("LH_BLUE", "GUI")
#     l_s_b = cv2.getTrackbarPos("LS_BLUE", "GUI")
#     l_v_b = cv2.getTrackbarPos("LV_BLUE", "GUI")
#     u_h_b = cv2.getTrackbarPos("UH_BLUE", "GUI")
#     u_s_b = cv2.getTrackbarPos("US_BLUE", "GUI")
#     u_v_b = cv2.getTrackbarPos("UV_BLUE", "GUI")
#     l_b_b = np.array([l_h_b, l_s_b, l_v_b])
#     u_b_b = np.array([u_h_b, u_s_b, u_v_b])
#     mask_blue = cv2.inRange(hsv, l_b_b, u_b_b)
#     res_blue = cv2.bitwise_and(frame, frame, mask=mask_blue)
#     cv2.putText(res_blue, "Blue", (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
#     # cv2.imshow("blue", res_blue)
#
#     top = np.hstack((res_yellow, res_green))
#     bottom = np.hstack((res_red, res_blue))
#     img = np.vstack((top, bottom))
#     cv2.imshow("Calibration", cv2.resize(img, (0, 0), fx=0.6, fy=0.6))
#     return l_b_y, u_b_y, l_b_g, u_b_g, l_b_r, u_b_r, l_b_b, u_b_b
#


def find(mask):
    x = y = 0
    contours, h = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 100:
            x, y, w, h = cv2.boundingRect(contour)
            return True, x + w//2, y + h//2
    return False, x, y
