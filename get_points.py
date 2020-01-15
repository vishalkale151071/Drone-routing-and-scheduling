from matplotlib import pyplot as plt
from shapely.geometry import Point, Polygon
import shapefile
import numpy as np
import node

polygon = None
sf = shapefile.Reader("shapefiles/tester")
for shape in list(sf.iterShapes()):
    npoints=len(shape.points) # total points
    nparts = len(shape.parts) # total parts
    polygon = Polygon(shape.points)
    if nparts == 1:
        x_lon = np.zeros((len(shape.points),1))
        y_lat = np.zeros((len(shape.points),1))
        for ip in range(len(shape.points)):
            x_lon[ip] = shape.points[ip][0]
            y_lat[ip] = shape.points[ip][1]
        plt.plot(x_lon, y_lat)

x_min = x_lon.min()
x_max = x_lon.max()
y_min = y_lat.min()
y_max = y_lat.max()

bitmap = []
row = []
x_range = np.arange(x_min, x_max, 0.0001)
y_range = np.arange(y_min, y_max, 0.0001)
for j in range(0, len(y_range)):
    row = []
    for i in range(0, len(x_range)):
        point = None
        if polygon.contains(Point(x_range[i], y_range[j])):
            plt.scatter(x_range[i], y_range[j], s =.5, c='blue')
            point = node.Node(x_range[i], y_range[j], True)
        else:
            plt.scatter(x_range[i], y_range[j], s=.5, c='red')
            point = node.Node(x_range[i], y_range[j], False)
        row.append(point)
    bitmap.append(row)

for j in range(0, len(y_range)):
    for i in range(0, len(x_range)):


shape = np.array(bitmap).shape
x_array = []
y_array = []
for e,x in enumerate(bitmap):
    row = []
    for y in x:
        if y.get_state():
            row.append(y)
    if e % 2 != 0:
        row.reverse()


    for i in row:
        temp = i.get_points()
        x_array.append(temp[0])
        y_array.append(temp[1])

plt.plot(x_array, y_array, c='green')
plt.show()