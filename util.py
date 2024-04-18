import cv2
import numpy as np
import time
from sklearn.cluster import KMeans


def transform_string(s):
    index_order = [0, 5, 4, 1, 2, 3]  # Order of precedence for indices
    for index in index_order:
        if s[index] == "1":
            return "0" * index + "1" + "0" * (len(s) - index - 1)
    return s


# Function to find the dominant color in an image
def find_dominant_color(image):
    pixels = image.reshape((-1, 3))
    kmeans = KMeans(n_clusters=1)
    kmeans.fit(pixels)
    dominant_color = kmeans.cluster_centers_[0]
    return dominant_color.astype(int)


def find_mean_color(image, rectangles):
    """Returns the mean BGR value for the rectangles"""
    mean_colors = []

    # Iterate over each rectangle and calculate the mean color
    for rect in rectangles:
        # Extract rectangle coordinates
        x1, y1, x2, y2 = rect

        # Create a mask for the rectangle
        mask = np.zeros(image.shape[:2], dtype=np.uint8)
        cv2.rectangle(mask, (x1, y1), (x2, y2), 255, -1)  # Draw filled rectangle

        # Compute the mean color within the rectangle
        mean_color = cv2.mean(image, mask=mask)[:3]
        mean_colors.append(mean_color)

    return mean_colors


def write_serial(esp32, text):
    esp32.write(bytes(text, "utf-8"))


def calculate_mean_color(image, vertices, center) -> list[tuple]:
    """Returns the mean HSV value for the 6 triangles"""
    mean_colors = []

    # Iterate over each vertex and calculate the mean color in the triangle formed by the vertex, center, and adjacent vertex
    for i in range(len(vertices)):
        # Define the vertices of the triangle
        vertex1 = vertices[i]
        vertex2 = vertices[(i + 1) % len(vertices)]  # Next vertex in the list
        triangle = np.array([vertex1, vertex2, center], np.int32)

        # Create a mask for the triangle
        mask = np.zeros(
            image.shape[:2], dtype=np.uint8
        )  # Create a mask with the same dimensions as the image
        cv2.fillPoly(mask, [triangle], 255)  # Fill the triangle area with white (255)

        # Compute the mean color within the triangle
        mean_color = cv2.mean(image, mask=mask)[:3]
        mean_colors.append(mean_color)

    return mean_colors


def get_limits(color):
    c = np.uint8([[color]])  # BGR values
    hsvC = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)

    hue = hsvC[0][0][0]  # Get the hue value
    value = hsvC[0][0][2]  # Get the value (brightness) component

    # If the brightness is very low, consider it as black
    if value < 50:
        lowerLimit = np.array([0, 0, 0], dtype=np.uint8)
        upperLimit = np.array(
            [180, 255, 50], dtype=np.uint8
        )  # Set a threshold for brightness
    else:
        lowerLimit = np.array([hue - 40, 0, 0], dtype=np.uint8)
        upperLimit = np.array([hue + 40, 255, 255], dtype=np.uint8)

    return lowerLimit, upperLimit
