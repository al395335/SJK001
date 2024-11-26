import GUI
import HAL
import utm


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
    while not (pos[0] == x and pos[1] == y):
        HAL.set_cmd_pos(x, y, height, 0.5)
        GUI.showImage(HAL.get_frontal_image())
        GUI.showLeftImage(HAL.get_ventral_image())
        pos = HAL.get_position()


pos_x, pos_y = compute_pos(boat_n, boat_w, victims_n, victims_w)
HAL.takeoff(height)
move(pos_x, pos_y)


while True:
    pass
