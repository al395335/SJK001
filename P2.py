import GUI
import HAL
import utm
import math
import cv2
import numpy as np
import time


boat_n = [40, 16, 48.2]
boat_w = [3, 49, 3.5]

victims_n = [40, 16, 47.23]
victims_w = [3, 49, 1.78]

height = 3


def compute_pos(init_n, init_w, end_n, end_w):
    init_coord_n = init_n[0] + init_n[1]/60 + init_n[2]/3600
    end_coord_n = end_n[0] + end_n[1]/60 + end_n[2]/3600

    init_coord_w = -(init_w[0] + init_w[1]/60 + init_w[2]/3600)
    end_coord_w = -(end_w[0] + end_w[1]/60 + end_w[2]/3600)

    init_coords_utm = utm.from_latlon(init_coord_n, init_coord_w)
    end_coords_utm = utm.from_latlon(end_coord_n, end_coord_w)

    return init_coords_utm[1] - end_coords_utm[1], init_coords_utm[0] - end_coords_utm[0]


def move(x, y):
    pos = HAL.get_position()
    dist = math.dist([pos[0], pos[1]], [x, y])
    while dist > 0.1:
        HAL.set_cmd_pos(x, y, height, 0.5)
        GUI.showImage(HAL.get_frontal_image())
        GUI.showLeftImage(HAL.get_ventral_image())
        pos = HAL.get_position()
        dist = math.dist([pos[0], pos[1]], [x, y])


def rotate_image(image, angle):
    if angle == 0: return image
    height, width = image.shape[:2]
    rot_mat = cv2.getRotationMatrix2D((width/2, height/2), angle, 0.9)
    result = cv2.warpAffine(image, rot_mat, (width, height), flags=cv2.INTER_LINEAR)
    return result


# Check rotated faces
def treat_image(face_cascade, image, faces):
    for rot in [0, 15, 30, 45, 60, 90, 120, 135, 150, 180]: 
        rotated_img = rotate_image(image, rot)
        gray_image = cv2.cvtColor(rotated_img, cv2.COLOR_BGR2GRAY)
        face = face_cascade.detectMultiScale(
            gray_image, scaleFactor=1.05, minNeighbors=3, minSize=(30, 30)
        )
        if len(face) > 0:
            pos = HAL.get_position()
            if compare_faces(pos, faces):
                print("Found!")
                faces.append(pos)
                return faces
            else:
                return faces
    return faces


# Make circles anticlockwise increasing radius when completing a circle
def move_circle(radius, angles, angles_pos):
    if angles_pos == len(angles):
        radius += 4
        angles_pos = 0
    x = -radius * math.cos(angles[angles_pos])
    y = radius * math.sin(angles[angles_pos])
    HAL.set_cmd_pos(x + pos_x, y + pos_y, height, 0.5) 
    angles_pos += 1
    return radius, angles_pos


# Similarity with position of faces. Return True if the face has not been detected yet
def compare_faces(face, faces):
    #print(face)
    for f in faces:
        dist = math.dist(face, f)
        #print(dist)
        if dist < 4.5:
            return False
    return True




pos_x, pos_y = compute_pos(boat_n, boat_w, victims_n, victims_w)
HAL.takeoff(height)
move(pos_x, pos_y)


victim_count = 0
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

radius = 7
angles = np.linspace(0, -2*np.pi, 700)
angles_pos = 0
faces = []

while len(faces) < 6:
    image = HAL.get_ventral_image()
    GUI.showLeftImage(image)
    GUI.showImage(HAL.get_frontal_image())
    faces = treat_image(face_cascade, image, faces)
    radius, angles_pos = move_circle(radius, angles, angles_pos)
    time.sleep(1/10)


move(0, 0)
HAL.land()


while True:
    pass
