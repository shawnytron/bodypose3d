import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from utils import DLT
import sys

# Set Seaborn's default style
sns.set_theme()

pose_keypoints = np.array([16, 14, 12, 11, 13, 15, 24, 23, 25, 26, 27, 28])

def read_keypoints(filename):
    fin = open(filename, 'r')

    kpts = []
    while(True):
        line = fin.readline()
        if line == '': break

        line = line.split()
        line = [float(s) for s in line]

        line = np.reshape(line, (len(pose_keypoints), -1))
        kpts.append(line)

    kpts = np.array(kpts)
    return kpts

def calculate_origin_distance(kpts3d):
    # Calculate the distance between the origin and the first point
    first_point = kpts3d[0]
    origin_distance = np.linalg.norm(first_point)
    return origin_distance

def visualize_3d(p3ds):
    """Now visualize in 3D"""
    torso = [[0, 1] , [1, 7], [7, 6], [6, 0]]
    armr = [[1, 3], [3, 5]]
    arml = [[0, 2], [2, 4]]
    legr = [[6, 8], [8, 10]]
    legl = [[7, 9], [9, 11]]
    body = [torso, arml, armr, legr, legl]
    colors = ['red', 'blue', 'green', 'black', 'orange']

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for framenum, kpts3d in enumerate(p3ds):
        if framenum % 2 == 0:
            continue  # skip every 2nd frame

        # Calculate the distance between the origin and the first point
        origin_distance = calculate_origin_distance(kpts3d)

        for bodypart, part_color in zip(body, colors):
            for _c in bodypart:
                ax.plot(xs=[kpts3d[_c[0], 0], kpts3d[_c[1], 0]], 
                        ys=[kpts3d[_c[0], 1], kpts3d[_c[1], 1]], 
                        zs=[kpts3d[_c[0], 2], kpts3d[_c[1], 2]], 
                        linewidth=4, c=part_color)

        for i in range(12):
            ax.text(kpts3d[i, 0], kpts3d[i, 1], kpts3d[i, 2], str(i))
            ax.scatter(xs=kpts3d[i:i+1, 0], ys=kpts3d[i:i+1, 1], zs=kpts3d[i:i+1, 2])

        # Set axis limits based on origin distance
        limit = 30
        ax.set_xlim3d(-origin_distance - limit, origin_distance + limit)
        ax.set_xlabel('x')
        ax.set_ylim3d(-origin_distance - limit, origin_distance + limit)
        ax.set_ylabel('y')
        ax.set_zlim3d(-origin_distance - limit, origin_distance + limit)
        ax.set_zlabel('z')
        
        plt.pause(0.1)
        ax.cla()

if __name__ == '__main__':
    participant_id = None
    if len(sys.argv) == 2:
        participant_id = sys.argv[1]
    
    if participant_id:
        filename = f'kpts_3d_p{participant_id}.dat'
    else:
        filename = 'kpts_3d.dat'

    p3ds = read_keypoints(filename)
    visualize_3d(p3ds)