import cv2
import numpy as np
import math
import matplotlib.pyplot as plt

from StateLatticeClass import *
from DoStuff import *

pixels_p_m = 10
angle_st = 15
list_of_points = generate_sl_points(pixels_p_m, angle_st)
array_of_paths = generate_sl_paths(pixels_p_m, angle_st)
array_of_collision = generate_sl_collision_paths(pixels_p_m, angle_st)

# for name in array_of_collision:
#     path = np.asarray(array_of_collision[name])
#     plt.plot(path[:, 0], path[:, 1], '*')
# plt.show()

start = []
start_pos = (0, 0)
end_pos = (0, 0, 0)
map, width, height, start_pos, end_pos, start = read_map(6)
points = [start]
queue = [start]
end_found = False

end_found = point_finder(queue, end_found, list_of_points, height, width, points, array_of_collision, end_pos, map)
create_path(points, array_of_paths, map)
map = draw_path(map, points, end_found, end_pos, array_of_paths)

# map = cv2.resize(map, (750,1000), interpolation=cv2.INTER_AREA)
cv2.imshow('map', map)
cv2.waitKey(0)
cv2.destroyAllWindows()