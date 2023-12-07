import folium
from folium.plugins import HeatMap
import networkx as nx
import osmnx as ox
import pandas as pd
import pickle
import os
from app import database as db_helper
from shapely.geometry import LineString
from shapely.ops import unary_union
from shapely.geometry import Point
import numpy as np

'''
def get_route():
   
    map = folium.Map(location=[34.063932, -118.359229], zoom_start=13)
    return map
'''

def get_route(origin, destination):
    ox.config(use_cache=True, log_console=True)
    lat_origin, lng_origin = origin
    lat_destination, lng_destination = destination
    # 定义地点和坐标
    #place = "Los Angeles, California, USA"
    start = (lat_origin, lng_destination)
    end = (lat_destination, lng_destination)
    # 获取地区的街道网络
    script_dir = os.path.dirname(os.path.realpath(__file__))
    ###################
    # 构建文件的绝对路径
    file_path = os.path.join(script_dir, 'Los_Angeles_map.pickle')
    
    #with open('/app/Los_Angeles_map.pickle', 'rb') as file:
    with open(file_path, 'rb') as file:
        G = pickle.load(file)
    #G = ox.graph_from_place(place, network_type='drive')

    '''
        # 确保文件存在
    file_path = '/home/lsr/cs411/SafeHomeApp/app/Los_Angeles_map.pickle'
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"文件 '{file_path}' 不存在。")

    # 从文件中加载序列化的图形
    with open(file_path, 'rb') as file:
        try:
            G = pickle.load(file)
        except (pickle.UnpicklingError, EOFError) as e:
            raise ValueError(f"从 '{file_path}' 加载图形时出错：{e}")
    '''

    # 找到最近的节点
    start_node = ox.distance.nearest_nodes(G, start[1], start[0])
    end_node = ox.distance.nearest_nodes(G, end[1], end[0])

    # 存储多条路径及其经纬度信息
    paths_coords = []
    paths =[]

    for _ in range(5):  # 生成5条路径
        # 计算最短路径
        route = nx.shortest_path(G, start_node, end_node, weight='length')
        paths.append(route)

        # 提取经纬度信息
        route_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in route]
        paths_coords.append(route_coords)

        # 增加这条路径上所有边的权重
        for i in range(len(route) - 1):
            if G.has_edge(route[i], route[i + 1]):
                G[route[i]][route[i + 1]][0]['length'] *= 1.1

    # 打印每条路径的经纬度信息
    #for i, coords in enumerate(paths_coords):
    #    print(f"Path {i + 1}:")
    #    for coord in coords:
    #        print(coord)

    # 创建初始地图，以第一条路径的起点为中心
    #map = folium.Map(location=[start[0], start[1]], zoom_start=13)

    for path_coords in paths_coords:
        # 创建线段
        line = LineString(path_coords)

        # 生成缓冲区
        buffer = line.buffer(0.002)  # 100米的大致缓冲区

        # # 将缓冲区转换为Folium的Polygon格式
        # folium.Polygon(
        #     locations=[list(coord) for coord in buffer.exterior.coords],
        #     color='blue',
        #     fill_color='blue',
        #     fill_opacity=0.5
        # ).add_to(map)

    regions = []

    for path_coords in paths_coords:
        line = LineString(path_coords)
        buffer = line.buffer(0.002)  # 100米的大致缓冲区
        regions.append(buffer)

    # 获取经纬度最大最小值
    for i, region in enumerate(regions):
        # 获取边界框 (min_lon, min_lat, max_lon, max_lat)
        min_log, min_lat, max_log, max_lat = region.bounds

    data_square = db_helper.within_region(max_log, max_lat, min_log, min_lat)             # 方框
    
    # 存储每个region的犯罪事件数量
    crime_counts = []


    for region in regions:
    # 计算region内的点的数量
        #count = sum(region.contains(Point(lon, lat)) for lat, lon in data_square)
        count = 0
        for lat, lon in data_square:
            print("assadasdsa")
            print(lat, " ", lon)
            if (region.contains(Point(lon, lat))):
                count += 1

        crime_counts.append(count)

    # # 打印结果
    # for i, count in enumerate(crime_counts):
    #     print(f"Region {i + 1} has {count} crimes")
        

    # print('\n')
    # 存储每条路径的长度
    path_lengths = []

    for path in paths:
        # 计算当前路径的长度
        path_length = sum(ox.utils_graph.get_route_edge_attributes(G, path, 'length'))
        path_lengths.append(path_length)

    # # 打印每条路径的长度
    # for i, length in enumerate(path_lengths):
    #     print(f"Length of Path {i + 1}: {length} meters")

    scores = []
    for i in range(5):
        scores.append (3e6 / (path_lengths[i]*np.sqrt(crime_counts[i])))
    #print(scores)

    # 获取得分最高的路径
    highest_score_index = scores.index(max(scores))
    highest_score_path = paths[highest_score_index]

    # # 打印结果
    # print('\n' + f"Choose Path: {highest_score_index + 1}")

    map = folium.Map(location=[start[0], start[1]], zoom_start=13)

    # 为每条路径绘制一条线
    for i, route_coords in enumerate(paths_coords):
        # 为每条路径设置不同的颜色
        if i != highest_score_index:
            line = folium.PolyLine(route_coords, weight=2, color=f'blue', opacity=0.7).add_to(map)
            folium.Marker(route_coords[0], popup=f'Start Path {i+1}').add_to(map)
            folium.Marker(route_coords[-1], popup=f'End Path {i+1}').add_to(map)
        else:
            line = folium.PolyLine(route_coords, weight=5, color=f'red', opacity=0.7).add_to(map)
            folium.Marker(route_coords[0], popup=f'Start Path {i+1}').add_to(map)
            folium.Marker(route_coords[-1], popup=f'End Path {i+1}').add_to(map)





    # # 为每条路径绘制一条线
    # for i, route_coords in enumerate(paths_coords):
    #     # 为每条路径设置不同的颜色
    #     line = folium.PolyLine(route_coords, weight=2, color=f'blue', opacity=0.7).add_to(map)
    #     folium.Marker(route_coords[0], popup=f'Start Path {i+1}').add_to(map)
    #     folium.Marker(route_coords[-1], popup=f'End Path {i+1}').add_to(map)
    
    return map


def get_heat_map(data):
    # data = [(34.0407, -118.2468, 0.71),
    # (34.0928, -118.3287, 1.30),
    # (34.0242, -118.4965, 0.04),
    # (33.9850, -118.4695, 0.25),
    # (34.0736, -118.4004, 0.16),
    # (33.7701, -118.1937, 0.46)] #example

    # 将数据转换为列表的列表形式，以便进行归一化
    data_list = [[item[2], item[1], item[3]] for item in data]

    # 计算value的最大值和最小值用于归一化
    values = [item[3] for item in data]
    max_value = max(values)
    min_value = min(values)

    # 归一化处理
    normalized_data = [[item[0], item[1], (item[2] - min_value) / (max_value - min_value) if max_value > min_value else 0] for item in data_list]

    # 确定地图的初始视图中心
    center_latitude = sum(item[2] for item in data) / len(data)
    center_longitude = sum(item[1] for item in data) / len(data)
    center_latitude, center_longitude = remove_extremes(data)

    # 创建地图实例
    map = folium.Map(location=[center_latitude, center_longitude], zoom_start=10)

    # 添加热点图层
    HeatMap(normalized_data).add_to(map)

    return map


def remove_extremes(data, percentage=0.05):
    # Sort based on Latitude and Longitude
    data_sorted_by_lat = sorted(item[2] for item in data)
    data_sorted_by_lon = sorted(item[1] for item in data)

    # 计算要去除的元素数量
    n = int(len(data) * percentage)

    # 去除极端值
    filtered_by_lat = data_sorted_by_lat[n:-n]
    filtered_by_lon = data_sorted_by_lon[n:-n]

    # 计算平均纬度和经度
    center_latitude = sum(filtered_by_lat) / len(filtered_by_lat)
    center_longitude = sum(filtered_by_lon) / len(filtered_by_lon)

    return center_latitude, center_longitude