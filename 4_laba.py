
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# будую куб
def define_cube(center, size, rotation_angles):

    half_size = size / 2
    vertices = np.array([
        [-half_size, -half_size, -half_size],  # 1
        [half_size, -half_size, -half_size],   # 2
        [half_size, half_size, -half_size],    # 3
        [-half_size, half_size, -half_size],   # 4
        [-half_size, -half_size, half_size],   # 5
        [half_size, -half_size, half_size],    # 6
        [half_size, half_size, half_size],     # 7
        [-half_size, half_size, half_size]     # 8
    ])
    
    rx, ry, rz = rotation_angles
#матриці обертання
    Rx = np.array([
        [1, 0, 0],
        [0, np.cos(rx), -np.sin(rx)],
        [0, np.sin(rx), np.cos(rx)]
    ])
    
    Ry = np.array([
        [np.cos(ry), 0, np.sin(ry)],
        [0, 1, 0],
        [-np.sin(ry), 0, np.cos(ry)]
    ])
    
    Rz = np.array([
        [np.cos(rz), -np.sin(rz), 0],
        [np.sin(rz), np.cos(rz), 0],
        [0, 0, 1]
    ])
    
    R = np.dot(Rz, np.dot(Ry, Rx))

    rotated_vertices = np.dot(vertices, R.T)
    translated_vertices = rotated_vertices + center
# ребра
    edges = [
        [0, 1], [1, 2], [2, 3], [3, 0],  
        [4, 5], [5, 6], [6, 7], [7, 4], 
        [0, 4], [1, 5], [2, 6], [3, 7]   
    ]
    
    return translated_vertices, edges

# проєкції точки на площину
def project_point(point_3d, projection_center, projection_plane_z):
 
    ray = point_3d - projection_center
    # час променя щоб дійти до Z площини
    t = (projection_plane_z - projection_center[2]) / ray[2]  if ray[2] != 0 else float('inf')
    
    if t <= 0:
        return None

    intersec = projection_center + t * ray

    return intersec[0], intersec[1]

def plot_3d_scene(cubes_data):

    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111, projection='3d')
    
    colors = ['b', 'r']
    # будую кожен куб
    for i, (vertices, edges) in enumerate(cubes_data):
        for edge in edges:
            x = [vertices[edge[0]][0], vertices[edge[1]][0]]
            y = [vertices[edge[0]][1], vertices[edge[1]][1]]
            z = [vertices[edge[0]][2], vertices[edge[1]][2]]
            ax.plot(x, y, z, colors[i], linewidth=2)
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('одноточкова та двоточкова центральна проєкція')
    # маштабую сцену, щоб все вмістилося
    max_range = np.array([
        np.max([vertices[:, 0].max() for vertices, _ in cubes_data]) - np.min([vertices[:, 0].min() for vertices, _ in cubes_data]),
        np.max([vertices[:, 1].max() for vertices, _ in cubes_data]) - np.min([vertices[:, 1].min() for vertices, _ in cubes_data]),
        np.max([vertices[:, 2].max() for vertices, _ in cubes_data]) - np.min([vertices[:, 2].min() for vertices, _ in cubes_data])
    ]).max() / 2.0
    # центрую сцену
    mid_x = np.mean([np.mean(vertices[:, 0]) for vertices, _ in cubes_data])
    mid_y = np.mean([np.mean(vertices[:, 1]) for vertices, _ in cubes_data])
    mid_z = np.mean([np.mean(vertices[:, 2]) for vertices, _ in cubes_data])
    # задаю межі осей
    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    ax.set_zlim(mid_z - max_range, mid_z + max_range)
    
    return fig, ax


cube1_center = np.array([-2, 0, 5])
cube1_size = 2.0
cube1_rotation = (0, 0, 0) 
    
cube2_center = np.array([2, 1, 7])
cube2_size = 1.5
cube2_rotation = (np.pi/6, np.pi/4, np.pi/6) 
    
cube1_vertices, cube1_edges = define_cube(cube1_center, cube1_size, cube1_rotation)
cube2_vertices, cube2_edges = define_cube(cube2_center, cube2_size, cube2_rotation)
# об'єдную куби
cubes_data = [(cube1_vertices, cube1_edges), (cube2_vertices, cube2_edges)]
fig_3d, ax_3d = plot_3d_scene(cubes_data)
    
plt.tight_layout()
plt.show()
