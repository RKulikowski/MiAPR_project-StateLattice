import cv2
import numpy as np
import math
import matplotlib.pyplot as plt
from StateLatticeClass import *


def generate_sl_points(pixels_per_m, angle_step, lin_number):
    # Funkcja generująca punkty, podawane argumenty to liczba pixeli na metr, krok w stopniach i liczba generowanych
    # punktow
    #
    sl_points = []
    # wyliczany jest indeks srodkowego puntku, ktory zostanie ustalony jak jazda prosto na krotszy dystans niz zakret
    lin_middle = int((lin_number - 1) / 2)
    for sl_step in range(lin_number):
        # sprawdzany jest czy indeks jest indeksem jazdy prosto
        if sl_step == lin_middle:
            # metr do przodu w osi x
            sl_x = 1 * pixels_per_m
            sl_y = 0
            # Przekazanie punktu do listy z argumentami niezbędnymi do dodania go do drzewa
            # Są to odpowiednio wspolrzedne, kat skrecenia opon, nazwa i koszt
            sl_points.append((sl_x, sl_y, 0, '0f', 10))
        else:
            # w przypadku skrętu przejechany dystans w x to zawsze 2 metry
            sl_x = 2 * pixels_per_m
            # następnie w zależności od kata skretu opon (rysunek przedstawiajacy te operacje jest w readme) wyliczana
            # jest wspolrzedna w y
            sl_radius = sl_x / np.sin(abs(sl_step - lin_middle) * np.radians(angle_step))
            sl_y = -(sl_step - lin_middle) / abs(sl_step - lin_middle) \
                   * (sl_radius - np.cos(abs(sl_step - lin_middle) * np.radians(angle_step)) * sl_radius)
            # Przekazanie punktu do listy z argumentami niezbędnymi do dodania go do drzewa
            sl_points.append((sl_x, sl_y, (sl_step - lin_middle) * angle_step, str((sl_step - lin_middle) * angle_step)
                              + 'f', abs(sl_step - lin_middle) * angle_step / 2 + 20))
    # jazda w tył generowana jest analogicznie
    # for sl_step in range(lin_number):
    #     if sl_step == lin_middle:
    #         sl_x = 2.5 * pixels_per_m
    #         sl_y = 0
    #         sl_points.append((-sl_x, sl_y, 0, '0r', 50))
    #     else:
    #         sl_x = 5 * pixels_per_m
    #         sl_radius = sl_x / np.sin(abs(sl_step - lin_middle) * np.radians(angle_step))
    #         sl_y = -(sl_step - lin_middle) / abs(sl_step - lin_middle) \
    #                * (sl_radius - np.cos(abs(sl_step - lin_middle) * np.radians(angle_step)) * sl_radius)
    #         sl_points.append((-sl_x, -sl_y, (sl_step - lin_middle) * angle_step,
    #                           str((sl_step - lin_middle) * angle_step) + 'r', abs(sl_step - lin_middle)
    #                           * 2 * angle_step + 110))
    return sl_points


def generate_sl_paths(pixels_per_m, angle_step, lin_number):
    # sciezki sa generowane podobnie jak punkty, z tym ze zamiast tylko ostatniego zapisywane sa iteracyjnie wszystkie
    paths = dict()
    lin_middle = int((lin_number - 1) / 2)
    for path_step in range(lin_number):
        path_points = []
        if path_step == lin_middle:
            xs = np.linspace(0, 10, 11, dtype=np.int32)
            for xy in range(11):
                path_point = [xs[xy], 0]
                path_points.append(path_point)
        else:
            for i in range(0, 31):
                rad = i / 30 * abs(path_step - lin_middle) * np.radians(angle_step)
                radius = 2 / np.sin(abs(path_step - lin_middle) * np.radians(angle_step))
                x = (np.sin(rad) * radius) * pixels_per_m
                y = -(path_step - lin_middle) / abs(path_step - lin_middle) * (radius - np.cos(rad) * radius) \
                    * pixels_per_m
                path_point = [x, y]
                path_points.append(path_point)

        name = str((path_step - lin_middle) * angle_step) + 'f'
        paths[name] = path_points
    for path_step in range(lin_number):
        path_points = []
        if path_step == lin_middle:
            xs = np.linspace(0, -10, 11, dtype=np.int32)
            for xy in range(11):
                path_point = [xs[xy], 0]
                path_points.append(path_point)
        else:
            for i in range(0, 31):
                rad = i / 30 * abs(path_step - lin_middle) * np.radians(angle_step)
                radius = 2 / np.sin(abs(path_step - lin_middle) * np.radians(angle_step))
                x = (np.sin(rad) * radius) * pixels_per_m
                y = -(path_step - lin_middle) / abs(path_step - lin_middle) * (radius - np.cos(rad) * radius) \
                    * pixels_per_m
                path_point = [-x, -y]
                path_points.append(path_point)
        name = str((path_step - lin_middle) * angle_step) + 'r'
        paths[name] = path_points
    return paths


def generate_sl_collision_paths(pixels_per_m, angle_step, lin_number):
    # punkty kolizji generowane sa jak sciezki z mniejsza iloscia iteracji, ale oprocz tego dodawane sa boxy dookola
    # kazdego punktu z rozmiarem w pixelach zdefiniowanym w zmiennej box_size
    paths = dict()
    box_size = 10
    lin_middle = int((lin_number - 1) / 2)
    for path_step in range(lin_number):
        path_points = []
        if path_step == lin_middle:
            xs = np.linspace(0, 10, 4, dtype=np.int32)
            for xy in range(4):
                path_point = [xs[xy], 0]
                path_points.append(path_point)
                path_points.append([xs[xy] + box_size, box_size])
                path_points.append([xs[xy] + box_size, - box_size])
                path_points.append([xs[xy] - box_size, - box_size])
                path_points.append([xs[xy] - box_size, box_size])
        else:
            for i in range(0, 11):
                rad = i / 10 * abs(path_step - lin_middle) * np.radians(angle_step)
                radius = 2 / np.sin(abs(path_step - lin_middle) * np.radians(angle_step))
                x = (np.sin(rad) * radius) * pixels_per_m
                y = -(path_step - lin_middle) / abs(path_step - lin_middle) * (radius - np.cos(rad) * radius) \
                    * pixels_per_m
                path_point = [x, y]
                path_points.append(path_point)
                corner_x, corner_y = Point.do_rotate(i / 10 * (path_step - lin_middle) * angle_step, box_size, box_size)
                path_points.append([x + corner_x, y + corner_y])
                path_points.append([x + corner_y, y - corner_x])
                path_points.append([x - corner_x, y - corner_y])
                path_points.append([x - corner_y, y + corner_x])

        name = str((path_step - lin_middle) * angle_step) + 'f'
        paths[name] = path_points
    for path_step in range(lin_number):
        path_points = []
        if path_step == lin_middle:
            xs = np.linspace(0, -10, 6, dtype=np.int32)
            for xy in range(6):
                path_point = [xs[xy], 0]
                path_points.append(path_point)
                path_points.append([xs[xy] + box_size, box_size])
                path_points.append([xs[xy] + box_size, - box_size])
                path_points.append([xs[xy] - box_size, - box_size])
                path_points.append([xs[xy] - box_size, box_size])
        else:
            for i in range(0, 11):
                rad = i / 10 * abs(path_step - lin_middle) * np.radians(angle_step)
                radius = 2 / np.sin(abs(path_step - lin_middle) * np.radians(angle_step))
                x = (np.sin(rad) * radius) * pixels_per_m
                y = -(path_step - lin_middle) / abs(path_step - lin_middle) * (radius - np.cos(rad) * radius) \
                    * pixels_per_m
                path_point = [-x, -y]
                path_points.append(path_point)
                corner_x, corner_y = Point.do_rotate(i / 10 * (path_step - lin_middle) * angle_step, box_size, box_size)
                path_points.append([-x + corner_x, -y + corner_y])
                path_points.append([-x + corner_y, -y - corner_x])
                path_points.append([-x - corner_x, -y - corner_y])
                path_points.append([-x - corner_y, -y + corner_x])
        name = str((path_step - lin_middle) * angle_step) + 'r'
        paths[name] = path_points

    # for name in paths:
    #     path = np.asarray(paths[name])
    #     plt.plot(path[:, 0], path[:, 1], 'r')
    # plt.show()

    return paths


def is_in_map(checked_point, map_height, map_width):
    # finkcja sprawdzajaca czy dany punkt jest na mapie
    if 15 < checked_point.x < map_height - 15 and 15 < checked_point.y < map_width - 15:
        return True
    else:
        return False


# def read_map(map_number):
#     # funkcja wczytujaca mape
#     map_name = "data/mapa{}.png".format(map_number)
#     map = cv2.imread(map_name)
#     map = np.transpose(map, (1, 0, 2))
#     width = np.shape(map)[1]
#     height = np.shape(map)[0]
#
#     start = []
#     start_pos = (0, 0)
#     end_pos = (0, 0, 0)
#
#     if map_name == "data/mapa2.png":
#         start_pos = (70, 70)
#         end_pos = (780, 1380, 90)
#         start = Point(start_pos, None, 270, 0)
#     if map_name == "data/mapa3.png":
#         start_pos = (120, 120)
#         end_pos = (100, 1440, 270)
#         start = Point(start_pos, None, 270, 0)
#     if map_name == "data/mapa5.png":
#         start_pos = (390, 50)
#         end_pos = (290, 400, 225)
#         start = Point(start_pos, None, 270, 0)
#     if map_name == "data/mapa6.png":
#         start_pos = (25, 25)
#         end_pos = (40, 260, 0)
#         start = Point(start_pos, None, 180, 0)
#     if map_name == "data/mapa7.png":
#         start_pos = (60, 60)
#         end_pos = (750, 960, 90)
#         start = Point(start_pos, None, 270, 0)
#
#     return map, width, height, start_pos, end_pos, start


def read_ultimate_map():
    # funkcja wczytujaca ostateczna mape z miejscem na parking, zwracajaca poza sama mapa rowniez pozycje startowa,
    # koncowa a takze wymiary okienka na ktorym planowany jest ruch
    map_name = "data/ultimate_mapa.png"
    map = cv2.imread(map_name)
    map = np.transpose(map, (1, 0, 2))
    width = 250
    height = 300
    start_pos = (260, 60)
    start = Point(start_pos, None, 270, 0)
    return map, width, height, start_pos, start


def point_finder(queue, end_found, list_of_points, height, width, points, array_of_collision, end_pos, map, end_frame):
    # funkcja dodajaca nowe punkty do drzewa
    # jako argumenty podawana jest kolejka punktow jeszcze nie sprawdzonych, flaga odnosnie znalezienia konca, lista
    # wszystkich punktow, rozmiary okienka, lista z predefiniowanymi punktami i lista kolizji, pozycja koncowa, mapa
    # i flaga znalezienia okienka ze sciezka do pozycji koncowej
    while queue:
        # kolejka sortowana jest po heurystyce
        queue = sorted(queue, key=lambda e: e.heuristics)
        # pobierany jest pierwszy element kolejki
        point = queue.pop(0)
        # generowane sa punkty w odniesieniu do obecnie badanego punktu
        new_points = point.get_state_lattice(list_of_points)
        for new_point in new_points:
            # definiowana jest flaga czy punkt sie nadaje do drzewa
            is_new = True
            # sprawdzamy czy punkt jest na mapie
            if not is_in_map(new_point, height, width):
                continue
            # sprawdzamy czy nie istnieje juz punkt o zblizonej pozycji i orientacji zeby go nie dublowac
            for point in points:
                if abs(new_point.x - point.x) < 15 and abs(new_point.y - point.y) < 15 \
                        and abs(new_point.orientation - point.orientation) <= 1:
                    is_new = False
                    break
            # sprawdzane sa kolizje
            collisions = new_point.return_path(array_of_collision)
            for collision_point in collisions:
                if map[collision_point[0], collision_point[1], 0] == 0:
                    is_new = False
            # jesli faga nie zostala zmieniona, to punkt jest dodawany do list punktow i do kolejki
            if is_new:
                points.append(new_point)
                queue.append(new_point)
                # map[new_point.x, new_point.y] = [1, 1, 255]
                # cv2.imshow('map', map)
                # cv2.waitKey(0)
                # jesli punkt jest w pozycji koncowej przekazywana zmieniana jest flaga
                if abs(new_point.y - end_pos[1]) < 15 and abs(new_point.x - end_pos[0]) < 15\
                        and abs(new_point.orientation % 360 - end_pos[2]) <= 0:
                    if end_frame:
                        end_found = True
                        # print("end found!")
                    break
        # if len(queue) > 200:
        #     break
    return end_found


def create_path(points, array_of_paths, map):
    # narysowanie sciezki na podstawie predefiniowanych wektorow punktow
    for point2 in points:
        path = point2.return_path(array_of_paths)
        if path:
            for point in path:
                map[point[0], point[1]] = [255, 0, 0]


def draw_path(map, points, end_found, end_pos, array_of_paths):
    # narysowanie sciezki ktora zostala wybrana
    # w przypadku gdy nie znaleziono globalnego punktu koncowego, sciezka bedzie prowadzona do lokalnego punktu
    # znajdujacego sie na prawym pasie ruchu
    finish_points = []
    if not end_found:
        for finished_point in points:
            if finished_point.y > 200:
                finish_points.append(finished_point)
    else:
        for finished_point in points:
            if abs(finished_point.y - end_pos[1]) <= 15 and abs(finished_point.x - end_pos[0]) <= 15 \
                    and abs(finished_point.orientation % 360 - end_pos[2]) <= 0:
                finish_points.append(finished_point)
                break
    # print(end_found)
    # if end_found:
    # print(len(finish_points))
    finish_points = sorted(finish_points, key=lambda e: e.heuristics)
    path = [finish_points[0]]

    while True:
        if not len(path) == 0:
            if path[-1].distance == 0:
                break
            for point in points:
                if point.x == path[-1].parent[0] and point.y == path[-1].parent[1]:
                    path.append(point)
                    break
        else:
            break
    if not len(path) == 0:
        for point2 in path:
            path_from_point = point2.return_path(array_of_paths)
            if path_from_point:
                for point in path_from_point:
                    map[point[0], point[1]] = [0, 0, 255]
    map[end_pos[0], end_pos[1]] = [0, 255, 0]

    return map, path[-2]
