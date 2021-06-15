import cv2
import numpy as np
import math
import matplotlib.pyplot as plt

from StateLatticeClass import *
from DoStuff import *

pixels_p_m = 10
angle_st = 5
lines_number = 5
list_of_points = generate_sl_points(pixels_p_m, angle_st, lines_number)
array_of_paths = generate_sl_paths(pixels_p_m, angle_st, lines_number)
array_of_collision = generate_sl_collision_paths(pixels_p_m, angle_st, lines_number)
#
# for name in array_of_collision:
#     path = np.asarray(array_of_collision[name])
#     plt.plot(path[:, 0], path[:, 1], 'r*')
# plt.show()

end_pos = (60, 240, 270)
# map, width, height, start_pos, end_pos, start = read_map(7)
map, width, height, start_pos, start = read_ultimate_map()
y = start_pos[1]
current_map_frame = map[:, y:y+250]
current_map_frame = current_map_frame.copy()
# points = [start]
# queue = [start]
# end_found = False

# end_found = point_finder(queue, end_found, list_of_points, height, width, points, array_of_collision, end_pos, map)
# create_path(points, array_of_paths, map)
# map = draw_path(map, points, end_found, end_pos, array_of_paths)

# map = cv2.resize(map, (750,1000), interpolation=cv2.INTER_AREA)
# cv2.imshow('map', map)
while True:
    points = [start]
    queue = [start]
    end_found = False
    point_finder(queue, end_found, list_of_points, height, width, points, array_of_collision, end_pos, current_map_frame)
    end_found = create_path(points, array_of_paths, current_map_frame)
    current_map_frame, next_point = draw_path(current_map_frame, points, end_found, end_pos, array_of_paths)
    current_map_frame = cv2.resize(current_map_frame, (1000, 400), interpolation=cv2.INTER_AREA)
    cv2.imshow('map', current_map_frame)
    cv2.waitKey(100)
    y_change = next_point.y - start.y
    y += y_change
    if y + 250 >= 4000:
        break
    start = Point((next_point.x, next_point.y - y_change), None, next_point.orientation, 0)
    current_map_frame = map[:, y:y+250]
    current_map_frame = current_map_frame.copy()
cv2.destroyAllWindows()