from tree.points import Point
import csv
import math

def read_csv(file_path):
    with open(file_path, 'r') as file:
        dim = int(file.readline().split(',')[0])
        reader = csv.reader(file)
        points = [Point(*map(float, row)) for row in reader]
    return dim, points


def calculate_height(node):
    if node.is_leaf():
        return 1
    return 1 + max(calculate_height(child) for child in node.children)
    
def calculate_spread(points):
    if not points:
        return 0

    max_pair_distance = _find_max_pair_distance(points)
    min_pair_distance = _find_min_pair_distance(points)
    return max_pair_distance / min_pair_distance if min_pair_distance != 0 else float('inf')

def _find_max_pair_distance(points):
    max_distance = 0
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            distance = math.sqrt((points[i].x - points[j].x)**2 + (points[i].y - points[j].y)**2)
            max_distance = max(max_distance, distance)
    return max_distance

def _find_min_pair_distance(points):
    min_distance = float('inf')
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            distance = math.sqrt((points[i].x - points[j].x)**2 + (points[i].y - points[j].y)**2)
            min_distance = min(min_distance, distance)
    return min_distance if min_distance != float('inf') else 0


def filter_points(points, bounding_box):
    return list(filter(bounding_box.contains_point, points))


