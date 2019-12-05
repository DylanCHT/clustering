from collections import defaultdict
from math import *
import random
import math
import csv

def point_avg(points):
    """
    Accepts a list of points, each with the same number of dimensions.
    (points can have more dimensions than 2)
    
    Returns a new point which is the center of all the points.
    """
    points_sum = [sum(x) for x in zip(*points)]
    return [col_sum /len(points) for col_sum in points_sum]


def update_centers(data_set, assignments):
    """
    Accepts a dataset and a list of assignments; the indexes 
    of both lists correspond to each other.
    Compute the center for each of the assigned groups.
    Return `k` centers in a list
    """
    newM = defaultdict(list)
    listC = []
    for assignment, point in zip(assignments, data_set):
        newM[assignment].append(point)

    for points in newM.values():
        listC.append(point_avg(points))

    return listC


def assign_points(data_points, centers):
    """
    """
    assignments = []
    for point in data_points:
        shortest = inf  # positive infinity
        shortest_index = 0
        for i in range(len(centers)):
            val = distance(point, centers[i])
            if val < shortest:
                shortest = val
                shortest_index = i
        assignments.append(shortest_index)
    return assignments


def distance(a, b):
    """
    Returns the Euclidean distance between a and b
    """
    dimention = len(a)
    sum = 0
    if len(b) == 0 or len(a) == 0:
        return 1000000
    else:
        for i in range(dimention):
            sum += (a[i] - b[i]) ** 2
        return sqrt(sum)


def generate_k(data_set, k):
    """
    Given `data_set`, which is an array of arrays,
    return a random set of k points from the data_set
    """
    kset = [data_set[random.randint(0, len(data_set) - 1)] for y in range(0, k)]
    return kset


def get_list_from_dataset_file(dataset_file):
    data_list = []
    with open(dataset_file) as csv:
        for line in csv:
            line = line.strip().split(",")
            indivi_data = [float(line[0]),float(line[1])]
            data_list.append(indivi_data)
    return data_list

def cost_function(clustering):
    total_cost = 0
    for data_set in clustering.keys():
        datas = clustering[data_set]
        centers = point_avg(datas)
        for indiv_data in datas:
            total_cost += distance(indiv_data, centers)
    return total_cost


def k_means(dataset_file, k):
    dataset = get_list_from_dataset_file(dataset_file)
    k_points = generate_k(dataset, k)
    assignments = assign_points(dataset, k_points)
    old_assignments = None
    while assignments != old_assignments:
        new_centers = update_centers(dataset, assignments)
        old_assignments = assignments
        assignments = assign_points(dataset, new_centers)
    clustering = defaultdict(list)
    for assignment, point in zip(assignments, dataset):
        clustering[assignment].append(point)
    return clustering
