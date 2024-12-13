from .quardTreeNode import QuardTreeNode
from .boundingBox import BoundingBox

import matplotlib.pyplot as plt



class QuardTree(object):
    def __init__(self):
        self.root = None
        self.deleted_count = 0
        self.points = []
        self.total_points = 0
    
    def build(self, points):

        x_coords = [point.x for point in points]
        y_coords = [point.y for point in points]

        boundary = BoundingBox(
                x_min=min(x_coords),
                y_min=min(y_coords),
                x_max=max(x_coords),
                y_max=max(y_coords)
            )
        
        self.root = QuardTreeNode(boundary=
                                  boundary, representative=None)
        self.points = points
        self.total_points = len(self.points)

        self._subdivide(self.root, self.points)
    
    def _subdivide(self, node, points):
        if node is None:
            return ValueError("Build QuardTree it first")
        
        x_mid = (node.boundary.x_max - node.boundary.x_min)/2 + node.boundary.x_min
        y_mid = (node.boundary.y_max - node.boundary.y_min)/2 + node.boundary.y_min

        quards = [
            BoundingBox(node.boundary.x_min, node.boundary.y_min, x_mid, y_mid),
            BoundingBox(x_mid, node.boundary.y_min, node.boundary.x_max, y_mid),
            BoundingBox(node.boundary.x_min, y_mid, x_mid, node.boundary.y_max),
            BoundingBox(x_mid, y_mid, node.boundary.x_max, node.boundary.y_max)
        ]

        quard_points = {quard : [] for quard in quards}

        for point in points:
            for quard in quards:
                if quard.contains_point(point):
                    quard_points[quard].append(point)
                    break

        for quard, q_points in quard_points.items():
            if points:
                child = QuardTreeNode(boundary=quard, representative=None)
                node.children.append(child)
                if len(q_points) > 1:
                    self._subdivide(child, q_points) 
                else:
                    child.representative = q_points[0]
        
        if node.representative is None:
            node.representative = node._cal_representative()
    
    def searchANN(self, query_pt, epsilon):
        S = [self.root]

        curr_point = self.root.representative
        curr_distance = query_pt.cal_distance(curr_point)

        while S:
            node = S.pop(0)
            if node.representative is None:
                continue

            node_distance = query_pt.cal_distance(node.representative)
            
            if node_distance < curr_distance:
                curr_distance = node_distance
                curr_point = node.representative

            if (node_distance - node.boundary.diameter()) < ((1 - epsilon / 2) * curr_distance):
                S.extend([child for child in node.children])

        return curr_point

    def visualize(self):
        fig, ax = plt.subplots(figsize=(10, 10))
        self._draw_node(self.root, ax)
        ax.set_aspect('equal', adjustable='box')
        plt.show()


    def _draw_node(self, node, ax):
        if node is None:
            return

        node.boundary.draw(ax)
        if node.representative:
            ax.plot(node.representative.x, node.representative.y, 'o', markersize=3)

        for child in node.children:
            self._draw_node(child, ax)
    

    def delete(self, point):
        def _delete(node):
            if node.is_leaf():
                node.remove_point(point)
                return 

            for child in node.children:
                if child.boundary.contains_point(point):
                    _delete(child)
                    break
            node.representative = node._cal_representative()

        _delete(self.root)
        self.deleted_count += 1

        self.points.remove(point)

        if self.deleted_count > self.total_points // 2:
            self.rebuild(self.root.points)
            self.deleted_count = 0

    def rebuild(self, points):
        self.build(points)