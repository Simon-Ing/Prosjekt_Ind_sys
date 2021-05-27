import cv2
import numpy as np
import PySimpleGUI as sg


def aruco(img, object_corners=[0, 1, 2, 3]):
    marker_corners = []
    coordinates = []
    marker_active = [False, False, False, False]
    for i in range(0, 35):
        marker_corners.append((1, 1, 1, 1))
        coordinates.append((1, 1))

    all_markers_active = False

    # Load AruCo markers, in this case we are using the 50 first 6x6 AruCo Markers.
    aruco_dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_50)
    aruco_parameters = cv2.aruco.DetectorParameters_create()
    (corners, ids, rejected) = cv2.aruco.detectMarkers(img, aruco_dictionary, parameters=aruco_parameters)

    # Check if any markers have been detected. If not, return unaltered image.
    if len(corners) > 0:
        ids = ids.flatten()
        for (markerCorner, markerID) in zip(corners, ids):

            # Mark the detected markerID's in object corner  as active.
            if markerID in object_corners:
                marker_active[markerID] = True

            corners = markerCorner.reshape((4, 2))
            (topLeft, topRight, bottomRight, bottomLeft) = corners

            topRight = (int(topRight[0]), int(topRight[1]))
            bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
            bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
            topLeft = (int(topLeft[0]), int(topLeft[1]))

            cX = int((topLeft[0] + bottomRight[0]) / 2.0)
            cY = int((topLeft[1] + bottomRight[1]) / 2.0)

            coordinates[markerID] = (cX, cY)
            marker_corners[markerID] = (topLeft, topRight, bottomLeft, bottomRight)

        # If all corners are detected and warp is enabled, warp the frame and marker coordinates.
        if all(marker_active):
            all_markers_active = True

            marker_active[object_corners[0]] = False
            marker_active[object_corners[1]] = False
            marker_active[object_corners[2]] = False
            marker_active[object_corners[3]] = False

            # Dimensions of the frame.
            dimensions = (img.shape[1], img.shape[0])

            # Declare
            pts1 = np.float32(
                [marker_corners[object_corners[0]][0], marker_corners[object_corners[1]][1],
                 marker_corners[object_corners[2]][2], marker_corners[object_corners[3]][3]])
            pts2 = np.float32([[0, 0], [dimensions[0], 0], [0, dimensions[1]], [dimensions[0], dimensions[1]]])

            # Calculate the perspective transform.
            matrix = cv2.getPerspectiveTransform(pts1, pts2)

            return True, matrix
    return False, None


def init_GUI():
    layout = [[sg.Button('Start', key='start', enable_events=True), sg.Button('Quit', key='quit', )],
              [sg.Text('YELLOW', text_color='Black', background_color='yellow', font=('helvetica', 15))],
              [sg.Text('hue'),
               sg.Slider((0, 179), 13, key='yhl', enable_events=True),
               sg.Slider((0, 179), 32, key='yhu', enable_events=True),
               sg.Text('sat'),
               sg.Slider((0, 255), 111, key='ysl', enable_events=True),
               sg.Slider((0, 255), 228, key='ysu', enable_events=True),
               sg.Text('val'),
               sg.Slider((0, 255), 96, key='yvl', enable_events=True),
               sg.Slider((0, 255), 148, key='yvu', enable_events=True)],

              [sg.Text('GREEN', text_color='Black', background_color='green', font=('helvetica', 15))],
              [sg.Text('hue'),
               sg.Slider((0, 179), 59, key='ghl', enable_events=True),
               sg.Slider((0, 179), 88, key='ghu', enable_events=True),
               sg.Text('sat'),
               sg.Slider((0, 255), 8, key='gsl', enable_events=True),
               sg.Slider((0, 255), 50, key='gsu', enable_events=True),
               sg.Text('val'),
               sg.Slider((0, 255), 84, key='gvl', enable_events=True),
               sg.Slider((0, 255), 138, key='gvu', enable_events=True)],

              [sg.Text('RED', text_color='Black', background_color='red', font=('helvetica', 15))],
              [sg.Text('hue'),
               sg.Slider((0, 179), 0, key='rhl', enable_events=True),
               sg.Slider((0, 179), 10, key='rhu', enable_events=True),
               sg.Text('sat'),
               sg.Slider((0, 255), 120, key='rsl', enable_events=True),
               sg.Slider((0, 255), 230, key='rsu', enable_events=True),
               sg.Text('val'),
               sg.Slider((0, 255), 84, key='rvl', enable_events=True),
               sg.Slider((0, 255), 138, key='rvu', enable_events=True)],

              [sg.Text('BLUE', text_color='Black', background_color='blue', font=('helvetica', 15))],
              [sg.Text('hue'),
               sg.Slider((0, 179), 119, key='bhl', enable_events=True),
               sg.Slider((0, 179), 132, key='bhu', enable_events=True),
               sg.Text('sat'),
               sg.Slider((0, 255), 4, key='bsl', enable_events=True),
               sg.Slider((0, 255), 29, key='bsu', enable_events=True),
               sg.Text('val'),
               sg.Slider((0, 255), 119, key='bvl', enable_events=True),
               sg.Slider((0, 255), 159, key='bvu', enable_events=True)]
              ]

    window = sg.Window('Title', layout)
    return window


def calibrate(window):

    event, values = window.read()
    if event in ('quit', sg.WIN_CLOSED ):
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



def find(mask):
    x = y = 0
    contours, h = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 100:
            x, y, w, h = cv2.boundingRect(contour)
            return True, x + w//2, y + h//2
    return False, x, y
