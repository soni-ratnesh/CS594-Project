from tree.points import Point
import csv
import math
import random
import time
import numpy as np

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

def cal_nn_distance(points, epsilons, tree):
    distances = {}

    for p in points:
        distances[(p.x, p.y)] = {}
        for eps in epsilons:
            nearest_point = tree.searchANN(p, eps)
            distance = p.cal_distance(nearest_point) 
            distances[(p.x, p.y)][eps] = distance
    return distances

def generate_random_queries(x_min, x_max, y_min, y_max, num_queries=1000):
    return [Point(random.uniform(x_min, x_max), random.uniform(y_min, y_max)) for _ in range(num_queries)]

def run_queries(region_min, region_max, ep, tree, num_queries=1000):
    distances = []
    query_times = []

    queries = generate_random_queries(region_min[0], region_max[0], region_min[1], region_max[1], num_queries)

    for query in queries:
        start_time = time.time()

        nearest_point = tree.searchANN(query, ep)

        query_time = time.time() - start_time
        query_times.append(query_time)

        distance = query.cal_distance(nearest_point)
        distances.append(distance)

    avg_distance = np.mean(distances)
    avg_query_time = np.mean(query_times)

    return avg_distance, avg_query_time

def sample_n_points(data_points, n, ignore_bbox=[], ignore_pts = []):
    random_points = []
    while len(random_points)!=n:
        s = random.choice(data_points)
        if s in random_points:
            continue
        if s in ignore_pts:
            continue
        for bbox in ignore_bbox:
            if bbox.contains_point(s):
                break
        else:
            random_points.append(s)
    return random_points