import cv2
import numpy as np
import serial

from util import (
    get_limits,
    calculate_mean_color,
    write_serial,
    transform_string,
    find_mean_color
)

TARGET_COLOR = (0, 0, 0)
HUE_TARGET = 60

# Inputs
rectangles = [
    (257, 256, 307, 278),  # top
    (357, 308, 418, 278),  # left
    (262, 337, 323, 375),  # bot
    (171, 308, 227, 278),  # right
    (359, 321, 410, 350)   # 
]

esp32 = serial.Serial(port="/dev/ttyUSB0", baudrate=115200, timeout=0.1)
uart_string = ""

### ------------------------------------------------------ ###

if __name__ == "__main__":
    line_color = (255, 0, 0)
    thickness = 3

    vid = cv2.VideoCapture(0)

    while True:
        ret, image = vid.read()
        image = cv2.flip(image, 1)

        ### ------------------ Hardcode 6 rectangles --------------------- ###
        # Draw rectangles on the image and find dominant colors
        modified_image = image.copy()
        for i, (x1, y1, x2, y2) in enumerate(rectangles):
            cv2.rectangle(modified_image, (x1, y1), (x2, y2), (0, 0, 255), -1)  # Draw filled red rectangles
            roi = image[y1:y2, x1:x2]  # Extract region of interest
            # dominant_color = find_mean_color(image, rectangles)
            # print(f"Mean color in rectangle {i+1}: {dominant_color}")

        cv2.imshow("FRAME", modified_image)
        k = cv2.waitKey(1)
        if k % 256 == 113:
            break
        ### ------------------ Hardcode 6 rectangles --------------------- ###

        ### ------------------- Showing Original Box ---------------------- ###
        # image = cv2.imread("./images/opencv_frame_0.png", cv2.IMREAD_COLOR)
        # cv2.line(image, top_left, top_right, line_color, thickness)
        # cv2.line(image, top_right, bot_right, line_color, thickness)
        # cv2.line(image, bot_right, bot_left, line_color, thickness)
        # cv2.line(image, bot_left, top_left, line_color, thickness)

        # cv2.imshow("Original Box", image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        ### ---------------------------------------------------------------- ###

        ### ------------------- Showing the Triangles ----------------------- ###
        # image = cv2.imread("./images/edited_black.png", cv2.IMREAD_COLOR)
        # for i in range(len(vertices)):
        #     if i != 5:
        #         cv2.line(image, vertices[i], vertices[i + 1], line_color, thickness)
        #     else:
        #         cv2.line(image, vertices[i], vertices[0], line_color, thickness)

        #     cv2.line(image, vertices[i], center, line_color, thickness)

        # cv2.imshow("FRAME", image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        ### ---------------------------------------------------------------- ###

        ### ---------- Calculating Average Color within Triangles ---------- ###
        lower_limit, upper_limit = get_limits(color=TARGET_COLOR)

        # image = cv2.imread("./images/edited_black.png", cv2.IMREAD_COLOR)
        hsvImage = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsvImage, lower_limit, upper_limit)
        cv2.imshow("Mask", mask)
        mean_colors = find_mean_color(mask, rectangles)

        # If threshold is met, send a string of 1's and 0's as a proxy for a list
        prev_string = uart_string
        uart_string = ""
        for mean_color in mean_colors:
            uart_string += "1" if mean_color[0] > HUE_TARGET else "0"

        # uart_string = transform_string(uart_string)

        if prev_string == uart_string:
            write_serial(esp32, uart_string)
            print(uart_string)

        k = cv2.waitKey(1)
        if k % 256 == 113:
            break
        # elif k % 256 == 32:
        #     # SPACE pressed
        #     img_name = "./images/opencv_frame_{}.png".format(img_counter)
        #     cv2.imwrite(img_name, frame)
        #     print("{} written!".format(img_name))
        #     img_counter += 1

    ### -------------------------------------------------------------------- ###
    vid.release()
    cv2.destroyAllWindows()
