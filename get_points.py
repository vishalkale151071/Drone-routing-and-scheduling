from matplotlib import pyplot as plt
from shapely.geometry import Point, Polygon
import shapefile
import numpy as np
import node

drones = 5

polygon = None
poly_points = None


def line_intersection(l1, l2):
    dx = (l1[0][0] - l1[1][0], l2[0][0] - l2[1][0])
    dy = (l1[0][1] - l1[1][1], l2[0][1] - l2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(dx, dy)
    if div == 0:
       print('lines do not intersect')

    d = (det(*l1), det(*l2))
    x = det(d, dx) / div
    y = det(d, dy) / div
    return x, y


sf = shapefile.Reader("shapefiles/dyp")
for shape in list(sf.iterShapes()):
    npoints=len(shape.points) # total points
    nparts = len(shape.parts) # total parts
    polygon = Polygon(shape.points)
    poly_points = shape.points
    if nparts == 1:
        x_lon = np.zeros((len(shape.points),1))
        y_lat = np.zeros((len(shape.points),1))
        for ip in range(len(shape.points)):
            x_lon[ip] = shape.points[ip][0]
            y_lat[ip] = shape.points[ip][1]
        #plt.plot(x_lon, y_lat)

x_min, y_min, x_max, y_max = polygon.bounds

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
            point = node.Node(x_range[i], y_range[j], "In")
        else:
            plt.scatter(x_range[i], y_range[j], s=.5, c='yellow')
            point = node.Node(x_range[i], y_range[j], "Out")
        row.append(point)
    bitmap.append(row)

shape = np.array(bitmap).shape

# for x in range(0, shape[0]):
#     for y in range(0, shape[1]):
#         if bitmap[x][y].get_state() == "Out":
#             try:
#                 if bitmap[x+1][y].get_state() == "In":
#                     if (bitmap[x+1][y-1].get_state() == "In" and bitmap[x][y-1].get_state() == "In") or (bitmap[x+1][y+1].get_state() == "In" and bitmap[x][y+1].get_state() == "In"):
#                         bitmap[x][y].set_state("Partial")
#                 elif bitmap[x-1][y].get_state():
#                     if (bitmap[x-1][y-1].get_state() == "In" and bitmap[x][y-1].get_state() == "In") or (bitmap[x-1][y+1].get_state() == "In" and bitmap[x][y+1].get_state() == "In"):
#                         bitmap[x][y].set_state("Partial")
#             except:
#                 pass

x_array = []
y_array = []
for e,x in enumerate(bitmap):
    row = []
    for y in x:
        if y.get_state() in ["In", "Partial"]:
            row.append(y)
    if e % 2 != 0:
        row.reverse()

    for i in row:
        temp = i.get_points()
        x_array.append(temp[0])
        y_array.append(temp[1])
index = len(x_array)
for i in range(0,len(poly_points)-1):
    result = filter(lambda x: (x <= poly_points[i][1] and x >= poly_points[i+1][1]) or (x >= poly_points[i][1] and x <= poly_points[i+1][1]), y_range)
    for line in result:
        pt = line_intersection((poly_points[i],poly_points[i+1]),((0,line),(x_max,line)))
        x_array.insert(index, pt[0])
        y_array.insert(index, pt[1])
lenght = len(x_array)
part = lenght//drones
start, end = 0, part

clr = ['green', 'orange', 'cyan', 'red', 'coral', 'green', 'orange', 'cyan', 'red', 'coral']
for i in range(0, drones):
    if i == drones - 1:
        x = x_array[start:-1]
        y = y_array[start:-1]
    else:
        x = x_array[start:end]
        y = y_array[start:end]

    plt.plot(x, y, color=clr[i])
    start = end - 1
    end = end + part
plt.show()