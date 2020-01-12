import matplotlib.pyplot as plt
import numpy as np
import shapefile

plt.figure()
ax = plt.axes() # add the axes
ax.set_aspect('equal')

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
            print(x_lon[ip], y_lat[ip])
        plt.plot(x_lon,y_lat)
        # loop over parts of each shape, plot separately
    else:
        for ip in range(nparts): # loop over parts, plot separately
            i0=shape.parts[ip]
            print(i0)
            if ip < nparts-1:
                i1 = shape.parts[ip+1]-1
            else:
                i1 = npoints
            seg=shape.points[i0:i1+1]
            x_lon = np.zeros((len(seg),1))
            y_lat = np.zeros((len(seg),1))
            for ip in range(len(seg)):
                x_lon[ip] = seg[ip][0]
                y_lat[ip] = seg[ip][1]
            plt.plot(x_lon,y_lat)

plt.show()