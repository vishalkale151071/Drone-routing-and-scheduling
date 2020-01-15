from matplotlib import pyplot as plt
from shapely.geometry import Point, Polygon
import numpy as np
import node
import geopy.distance as distance
import tkinter as tk
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import Point, Polygon
import shapefile
import node
from tkinter import filedialog


class MyFirstGUI:
    
    def filesel(self):
        filename = filedialog.askopenfilename(initialdir="E:\TE\SIH\Drone-routing-and-scheduling\shapefiles",title="Select file",filetypes=(("shape files", "*.shp"), ("all files", "*.*")))
        self.newf = filename[39:-1]

    def run(self):

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

        sf = shapefile.Reader(self.newf)
        for shape in list(sf.iterShapes()):
            npoints = len(shape.points)  # total points
            nparts = len(shape.parts)  # total parts
            polygon = Polygon(shape.points)
            poly_points = shape.points
            if nparts == 1:
                x_lon = np.zeros((len(shape.points), 1))
                y_lat = np.zeros((len(shape.points), 1))
                for ip in range(len(shape.points)):
                    x_lon[ip] = shape.points[ip][0]
                    y_lat[ip] = shape.points[ip][1]
                plt.plot(x_lon, y_lat)

        plt.savefig("boundary.png")
        plt.close()

        x_min, y_min, x_max, y_max = polygon.bounds
        print(polygon.length * 20)
        bitmap = []
        row = []
        x_range = np.arange(x_min, x_max, 0.0001)
        y_range = np.arange(y_min, y_max, 0.0001)
        for j in range(0, len(y_range)):
            row = []
            for i in range(0, len(x_range)):
                point = None
                if polygon.contains(Point(x_range[i], y_range[j])):
                    plt.scatter(x_range[i], y_range[j], s=.5, c='blue')
                    point = node.Node(x_range[i], y_range[j], "In")
                else:
                    plt.scatter(x_range[i], y_range[j], s=.5, c='red')
                    point = node.Node(x_range[i], y_range[j], "Out")
                row.append(point)
            bitmap.append(row)
        plt.plot()
        plt.savefig("dotcon.png")
        plt.close()

        shape = np.array(bitmap).shape

        x_array = []
        y_array = []
        for e, x in enumerate(bitmap):
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
        cal = []
        for i in range(0, len(poly_points) - 1):
            result = filter(lambda x: (x <= poly_points[i][1] and x >= poly_points[i + 1][1]) or (
                        x >= poly_points[i][1] and x <= poly_points[i + 1][1]), y_range)
            for line in result:
                pt = line_intersection((poly_points[i], poly_points[i + 1]), ((0, line), (x_max, line)))
                cal.append(pt)
                x_array.insert(index, pt[0])
                y_array.insert(index, pt[1])

        total_length = 0
        for i in range(0, len(x_array) - 1):
            total_length += distance.vincenty((x_array[i], y_array[i]), ((x_array[i + 1], y_array[i + 1]))).m

        part = total_length / drones
        print(part)
        clr = ['red', 'orange', 'cyan', 'green', 'coral']

        x_array.reverse()
        y_array.reverse()

        i = 0;
        path_x = [x_array[i]]
        path_y = [y_array[i]]
        td = 0
        self.max_time = 0;
        self.info = []
        clr = ['red', 'blue', 'cyan', 'coral', 'orange']
        for j in range(0, drones):
            while td <= part and i < len(x_array) - 1:
                td += distance.vincenty((x_array[i], y_array[i]), ((x_array[i + 1], y_array[i + 1]))).m
                i += 1
                path_x.append(x_array[i])
                path_y.append(y_array[i])
            plt.plot(path_x, path_y, color=clr[j])
            if td/1000 > self.max_time:
                self.max_time = td/1000
            d = dict(drone=j + 1, distance=td, time=td/1000, color=clr[j])
            path_y = [y_array[i]]
            path_x = [x_array[i]]
            self.info.append(d)
            td = 0

        plt.savefig("final.png")
        plt.close()
        self.b_img = Image.open("boundary.png")
        self.b_img = self.b_img.resize((500,300), Image.ANTIALIAS)
        self.pic = ImageTk.PhotoImage(self.b_img)

        self.lab = tk.Label(image=self.pic)
        self.lab.place(x=50,y=5)


        self.b_img1 = Image.open("dotcon.png")
        self.b_img1 = self.b_img1.resize((500,300), Image.ANTIALIAS)
        self.pic1 = ImageTk.PhotoImage(self.b_img1)

        self.lab1 = tk.Label(image=self.pic1)
        self.lab1.place(x=760,y=5)

        for e,d in enumerate(self.info):
            lable = "Drone : {}, Color : {}, Distance : {}, Time : {}.".format(d['drone'], d['color'], d['distance'], d['time'])
            tk.Label(self.lab4, text=lable).place(x=10, y=50 * (e+1), )

        tk.Label(self.lab4, text="Total Time : {}.".format("%.2f" % self.max_time)).place(x=10, y=10)
        self.lab4.place(x=760, y=330)

        
        self.b_img2 = Image.open("final.png")
        self.b_img2 = self.b_img2.resize((500,300), Image.ANTIALIAS)
        self.pic2 = ImageTk.PhotoImage(self.b_img2)

        self.lab2 = tk.Label(image=self.pic2)
        self.lab2.place(x=50,y=330)

    def __init__(self, master):
        self.master = master
        master.title("A simple GUI")
        self.b_img3 = Image.open("drone1.jpg")
        self.pic3 = ImageTk.PhotoImage(self.b_img3)

        self.lab3 = tk.Label(image=self.pic3)
        self.lab3.place(x=0,y=0)

        self.lab4 = tk.Frame(master, height=300, width=500)

        self.button2 = tk.Button(root, text="RUN", command=self.run, bg="Brown")
        self.button2.place(x=700, y=650)


        self.button4 = tk.Button(root, text="Select File", command=self.filesel, bg="Brown")
        self.button4.place(x=400, y=650)

        self.newf = ""


root = tk.Tk()
root.geometry('1920x1080+0+0')
root.resizable(height=None, width=None)
root.title("Drone Routing and Planning")
my_gui = MyFirstGUI(root)
root.mainloop()
