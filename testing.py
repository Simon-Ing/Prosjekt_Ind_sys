import cv2


def nothing(x):
    pass


trackbars_window_name = "hsv settings"
cv2.namedWindow(trackbars_window_name, cv2.WINDOW_NORMAL)

# HSV Lower Bound
h_min_trackbar = cv2.createTrackbar("H min", trackbars_window_name, 0, 255, nothing)
s_min_trackbar = cv2.createTrackbar("S min", trackbars_window_name, 0, 255, nothing)
v_min_trackbar = cv2.createTrackbar("V min", trackbars_window_name, 0, 255, nothing)

# HSV Upper Bound
h_max_trackbar = cv2.createTrackbar("H max", trackbars_window_name, 255, 255, nothing)
s_max_trackbar = cv2.createTrackbar("S max", trackbars_window_name, 255, 255, nothing)
v_max_trackbar = cv2.createTrackbar("V max", trackbars_window_name, 255, 255, nothing)

# Kernel for morphology
kernel_x = cv2.createTrackbar("kernel x", trackbars_window_name, 0, 30, nothing)
kernel_y = cv2.createTrackbar("kernel y", trackbars_window_name, 0, 30, nothing)
    #
    # self._trackbars = [h_min_trackbar, s_min_trackbar, v_min_trackbar, h_max_trackbar, s_max_trackbar,
    #                    v_max_trackbar, kernel_x, kernel_y]

while True:
    pass
