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

x_min = x_lon.min()
x_max = x_lon.max()
y_min = y_lat.min()
y_max = y_lat.max()

bitmap = []
row = []
x_range = np.arange(x_min, x_max, 0.0001)
y_range = np.arange(y_min, y_max, 0.0001)
for i in range(0, len(x_range)):
    row.clear()
    for j in range(0, len(y_range)):
        point = None
        if polygon.contains(Point(x_range[i], y_range[j])):
            plt.scatter(x_range[i], y_range[j], s =.5, c='b')
            point = node.Node(x_range[i], y_range[j], True)
        else:
            plt.scatter(x_range[i], y_range[j], s=.5, c='r')
            point = node.Node(x_range[i], y_range[j], False)
        row.append(point)
    bitmap.append(row)
plt.show()

data = np.array(bitmap)
print(data.shape )