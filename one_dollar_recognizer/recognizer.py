'''
This module is an implementation of Wobbrock et al's One Dollar Recognizer.
It is based on the JavaScript implementation.
'''
from scipy.signal import resample
import config
import xml.etree.ElementTree as ET
import os
import numpy as np
import math


class Recognizer:
    def __init__(self):
        self.templates = []
        self.phi = 0.5 * (-1.0 + math.sqrt(5.0))
        self.angle_range = math.radians(45.0)
        self.angle_precision = math.radians(2.0)
        self.square_size = 250

        self.create_templates()

    def create_templates(self):
        for root, subdirs, files in os.walk('one_dollar_recognizer/templates'):
            if len(files) > 0:
                for f in files:
                    if '.xml' in f:
                        fname = f.split('.')[0]
                        label = fname[:-2]

                        xml_root = ET.parse(f'{root}/{f}').getroot()

                        points = []
                        for element in xml_root.findall('Point'):
                            x = element.get('X')
                            y = element.get('Y')
                            points.append([float(x), float(y)])

                        points = np.array(points, dtype=float)

                        transformed = self.transform(points)

                        self.templates.append((label, transformed))

    def transform(self, points):
        points = resample(points, config.NUM_POINTS)

        radians = self.indicative_angle(points)

        points = self.rotate_by(points=points, radians=-radians)

        points = self.scale_to(points)

        points = self.translate_to_origin(points)

        return points

    def indicative_angle(self, points):
        c = self.centroid(points)
        return math.atan2(c[1] - points[0][1], c[0] - points[0][0])

    def scale_to(self, points):
        b = self.bounding_box(points)
        new_points = []
        for point in points:
            qx = point[0] * (self.square_size / b[2])
            qy = point[1] * (self.square_size / b[3])
            new_points.append([qx, qy])
        return new_points

    def bounding_box(self, points):
        min_x = math.inf
        max_x = -math.inf
        min_y = math.inf
        max_y = -math.inf

        for point in points:
            min_x = min(min_x, point[0])
            min_y = min(min_y, point[1])
            max_x = max(max_x, point[0])
            max_y = max(max_y, point[1])

        return [min_x, min_y, max_x - min_x, max_y - min_y]

    def translate_to_origin(self, points):
        c = self.centroid(points=points)
        new_points = []
        for point in points:
            qx = point[0] - c[0]
            qy = point[1] - c[1]
            new_points.append([qx, qy])

        return new_points

    def recognize(self, candidate_points):
        candidate_points = self.transform(candidate_points)
        b = math.inf
        best_index = 0
        for i, template in enumerate(self.templates):
            d = self.distance_at_best_angle(
                candidate_points=candidate_points, template=template, a=-self.angle_range, b=self.angle_range)
            print(
                f'Distance at best angle for template {i} ({template[0]}): {d}')
            if d < b:
                b = d
                best_index = i
        label = self.templates[best_index][0]
        return label

    def distance_at_best_angle(self, candidate_points, template, a, b):
        x1 = self.phi * a + (1 - self.phi) * b
        f1 = self.distance_at_angle(candidate_points, template, x1)
        x2 = (1.0 - self.phi) * a + self.phi * b
        f2 = self.distance_at_angle(candidate_points, template, x2)

        while (abs(b - a) > self.angle_precision):
            # print('Fitting angle')
            if (f1 < f2):
                b = x2
                x2 = x1
                f2 = f1
                x1 = self.phi * a + (1.0 - self.phi) * b
                f1 = self.distance_at_angle(
                    candidate_points=candidate_points, template=template, radians=x1)
            else:
                a = x1
                x1 = x2
                f1 = f2
                x2 = (1.0 - self.phi) * a + self.phi * b
                f2 = self.distance_at_angle(
                    candidate_points=candidate_points, template=template, radians=x2)
        return min(f1, f2)

    def distance_at_angle(self, candidate_points, template, radians):
        new_points = self.rotate_by(candidate_points, radians)
        return self.path_distance(new_points, template[1])

    def rotate_by(self, points, radians):
        c = self.centroid(points)
        cos = math.cos(radians)
        sin = math.sin(radians)
        new_points = []
        for point in points:
            qx = (point[0] - c[0]) * cos - (point[1] - c[1]) * sin + c[0]
            qy = (point[0] - c[0]) * sin + (point[1] - c[1]) * cos + c[1]
            new_points.append([qx, qy])
        return new_points

    def centroid(self, points):
        x = 0.0
        y = 0.0
        for point in points:
            x += point[0]
            y += point[1]

        x /= len(points)
        y /= len(points)

        return [x, y]

    def path_distance(self, pts1, pts2):
        d = 0.0
        for i, point in enumerate(pts1):
            d += self.distance(point, pts2[i])
        # print(f'Path distance {d}')
        return d

    def distance(self, p1, p2):
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        return math.sqrt(dx * dx + dy * dy)
