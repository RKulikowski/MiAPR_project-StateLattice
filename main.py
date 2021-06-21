import cv2
import numpy as np
import math
import matplotlib.pyplot as plt
from time import time

from StateLatticeClass import *
from DoStuff import *

# definicja zmiennych potrzebnych do generacji punktow i sciezek
pixels_p_m = 10
angle_st = 5
lines_number = 5
list_of_points = generate_sl_points(pixels_p_m, angle_st, lines_number)
array_of_paths = generate_sl_paths(pixels_p_m, angle_st, lines_number)
array_of_collision = generate_sl_collision_paths(pixels_p_m, angle_st, lines_number)
# wyswietlenie jako wykresu wygenerowanych punktow
for name in array_of_collision:
    path = np.asarray(array_of_collision[name])
    plt.plot(path[:, 0], path[:, 1], 'r*')
plt.show()

# definicja pozycji koncowych
local_end_pos = (260, 240, 270)
global_end_pos = (40, 3660, 90)

# wczytanie mapy
# map, width, height, start_pos, end_pos, start = read_map(7)
map, width, height, start_pos, start = read_ultimate_map()
# ustalenie okienka startowego
y = start_pos[1]
current_map_frame = map[:, y:y+250]
current_map_frame = current_map_frame.copy()

# preprowadzenie szukania sciezki dla calej mapy od razu
# points = [start]
# queue = [start]
# end_found = False

# end_found = point_finder(queue, end_found, list_of_points, height, width, points, array_of_collision, end_pos, map)
# create_path(points, array_of_paths, map)
# map = draw_path(map, points, end_found, end_pos, array_of_paths)

# map = cv2.resize(map, (750,1000), interpolation=cv2.INTER_AREA)
# cv2.imshow('map', map)

# definicja flag
end_found = False
end_frame = False
while True:
    # stworzenie listy punktow i kolejki
    points = [start]
    queue = [start]
    # zmierzenie czasu
    start_time = time()
    # wywolanie funkcji tworzacej drzewo
    end_found = point_finder(queue, end_found, list_of_points, height, width, points, array_of_collision, local_end_pos, current_map_frame, end_frame)
    # wyrysowanie drzewa
    create_path(points, array_of_paths, current_map_frame)
    end_time = time()
    # print(end_time - start_time)
    # wyrysowanie wybranej sciezki
    current_map_frame, next_point = draw_path(current_map_frame, points, end_found, local_end_pos, array_of_paths)
    current_map_frame = cv2.resize(current_map_frame, (750, 900), interpolation=cv2.INTER_AREA)
    # wyswietlenie mapy
    cv2.imshow('map', current_map_frame)
    cv2.waitKey(100)
    # wyliczenie zmiany w osi y i przesuniecia okienka
    y_change = next_point.y - start.y
    if not end_found:
        y += y_change

    if y + 250 >= 4000:
        break
    # sprawdzenie czy punkt koncowy jest na okienku i zmiana lokalnego punktu koncowego na globalny
    if y > 3500:
        local_end_pos = (40, 3660 - y, 90)
        end_frame = True
    start = Point((next_point.x, next_point.y - y_change), None, next_point.orientation, 0)
    if end_found:
        start = Point((next_point.x, next_point.y), None, next_point.orientation, 0)
    # przesuniecie okienka
    current_map_frame = map[:, y:y+250]
    current_map_frame = current_map_frame.copy()
cv2.destroyAllWindows()