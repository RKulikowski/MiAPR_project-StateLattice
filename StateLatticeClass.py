import cv2
import numpy as np
import math

class Point:
    def __init__(self, position, parent, orientation, distance, name='0f', parent_orient=None, parent_distance=None, reverse=False):
        self.position = position
        self.x = position[0]
        self.y = position[1]
        self.parent = parent
        self.parent_orient = parent_orient
        self.orientation = orientation
        if parent_distance:
            self.distance = parent_distance + distance
        else:
            self.distance = distance
        self.heuristics = self.calculate_heuristics() + self.distance + 3*abs(260 - self.x)
        self.name = name
        self.reverse = reverse

    def __str__(self):
        return f'Class Point:\nPosition: {self.position}\nParent: {self.parent}\n' \
               f'Orientation: {self.orientation}\nHeuristics: {self.heuristics}\nDistance: {self.distance}'

    def calculate_heuristics(self):
        # obliczana jest heurystyka, po fakcie widze ze nie dodalismy tutaj flagi zeby liczylo ja od globalnego punktu
        # jesli jest on osiagalny na obecnym okienku
        return math.sqrt(abs(self.position[0] - 240) * abs(self.position[0] - 240) + abs(self.position[1] - 60) *
                         abs(self.position[1] - 60))

    @staticmethod
    def do_rotate(angle, x, y):
        # funkcja obracajaca punkt o kat, w sumie powinna znalezc sie poza klasa
        rad = np.radians(angle)
        x_prim = x * np.cos(-rad) - y * np.sin(-rad)
        y_prim = x * np.sin(-rad) + y * np.cos(-rad)
        return x_prim, y_prim

    def get_state_lattice(self, points_list):
        # Obrot i przesuniecie predefiniowanych punktow na podstawie obecnego punktu
        sl_points = []
        for point_x, point_y, orientation, name, cost in points_list:
            # ograniczenie maksymalnej zmiany kata skretu kol do 15 stopni na jeden przejechany odcinek
            if abs(int(self.name[:-1]) - orientation) <= 15:
                x, y = self.do_rotate(self.orientation, point_x, point_y)
                orient = orientation + self.orientation
                sl_points.append(Point((int(x) + self.x, int(y) + self.y), self.position, orient, cost, name, self.name,
                                       self.distance, False))
        return sl_points

    def return_path(self, paths_list):
        # zwrocenie odpowiedniego wektora punktow z listy predefiniowanych sciezek na podstawie danych o poprzednim
        # punkcie
        path_points = []
        if self.parent:
            path = paths_list[self.name]
            for point_from_list in path:
                if abs(int(self.name[:-1]) - int(self.parent_orient[:-1])) <= 15:
                    orient = self.orientation - int(self.name[:-1])
                    x, y = self.do_rotate(orient, point_from_list[0], point_from_list[1])
                    path_points.append((self.parent[0] + int(x), self.parent[1] + int(y)))
        return path_points
