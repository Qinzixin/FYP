import numpy as np
points_i = np.array([[201,469]])
polygon_data = open('estimated_polygon.data', 'r')
for line in polygon_data:
    records = line.split()
    x = float(records[0])
    y = float(records[1])
    points_i = np.append(points_i, [[x, y]], axis=0)
polygon_data.close()

'''
from matplotlib.path import Path

tupVerts= points_i.tolist()

x, y = np.meshgrid(np.arange(878), np.arange(544)) # make a canvas with coordinates
x, y = x.flatten(), y.flatten()
points = np.vstack((x,y)).T

p = Path(tupVerts) # make a polygon
grid = p.contains_points(points)
mask = grid.reshape(878,544) # now you have a mask with points inside a polygon
print("o")
'''

from shapely.geometry import MultiPoint,Polygon,Point
vertices_p = points_i.tolist()
m = Polygon(vertices_p)
print("generated shape area: %f" % m.area)

import matplotlib.pyplot as plt
import numpy as np
list_x = [201]
list_y = [649]
for i in range(878):
    for j in range(544):
        if Point(i,j).intersects(m)== True:
            list_x.append(i)
            list_y.append(j)
xpoints = np.array(list_x)
ypoints = np.array(list_y)

plt.plot(xpoints, ypoints, 'o')
plt.show()