from matplotlib import pyplot as plt
import shapefile
import numpy as np

sf = shapefile.Reader("shapefiles/tester")
for shape in list(sf.iterShapes()):
    npoints=len(shape.points) # total points
    nparts = len(shape.parts) # total parts
    if nparts == 1:
        x_lon = np.zeros((len(shape.points),1))
        y_lat = np.zeros((len(shape.points),1))
        for ip in range(len(shape.points)):
            x_lon[ip] = shape.points[ip][0]
            y_lat[ip] = shape.points[ip][1]
print(x_lon, y_lat)
x_min = x_lon.min()
x_max = x_lon.max()
y_min = y_lat.min()
y_max = y_lat.max()

print(x_max, x_min)
print(y_max, y_min)

x_range = np.arange(x_min, x_max, 0.0001)
y_range = np.arange(y_min, y_max, 0.0001)
for i in range(0, len(x_range)):
    for j in range(0, len(y_range)):
        lat = [x_range[i], x_range[i]]
        lag = [y_range[j], y_range[j]]
        plt.scatter(lat, lag)
plt.show()
