import shapefile as sf

with sf.Writer('shapefiles/test', shapeType=1) as w:
    w.field('name', 'C')
    w.point(120,13)
    w.record('point1')
with sf.Reader('shapefiles/test') as r:
    for x in r.iterShapes():
        print(x.points)

