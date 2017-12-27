import arcpy
import pythonaddins
import numpy
import networkx as nx


option = "shortest"
class ButtonClass14(object):
    """Implementation for Rysuj_Droge_addin.button_1 (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        print("wybrales opcje trasa najkrotsza")
        global option
        option = "shortest"
        print(option)

class ButtonClass15(object):
    """Implementation for Rysuj_Droge_addin.button_2 (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        print("wybrales opcje trasa najszybsza")
        global option
        option = "fastest"
        print(option)

class ButtonClass3(object):
    """Implementation for Rysuj_Droge_addin.button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        print("wybrales opcje z tnij najwyzsza warstwe")

class ToolClass2(object):
    """Implementation for Rysuj_Droge_addin.tool (Tool)"""

    def __init__(self):
        self.enabled = True
        self.shape = "Line"  # Can set to "Line", "Circle" or "Rectangle" for interactive shape drawing and to activate the onLine/Polygon/Circle event sinks.
        self.cursor = 3

    def onLine(self, line_geometry):

        mxd = arcpy.mapping.MapDocument("Current")
        punkty = arcpy.mapping.ListLayers(mxd)

        # if arcpy.Exists(polyline_path + "\droga.shp"):
        #   arcpy.Delete_management(polyline_path + "\droga.shp")

        # arcpy.CreateFeatureclass_management(polyline_path, "droga", "POLYLINE")


        points = []
        edges = []

        i = 0
        pkt = []

        # A: Autostrady 120
        # S: Ekspresowe 120
        # GP: Glowne ruchu [rzyspieszonego 70
        # G: Glowne 60
        # Z: Zbiorcze 60
        # L: Lokalne 40
        # I: Dojazdowe 30
        odl = []
        odlk = []
        with arcpy.da.SearchCursor(punkty[0], ["FID", "SHAPE@", "SHAPE@LENGTH", "klasaDrogi"]) as street_data:
            for s in street_data:
                id_part = str(s[1].firstPoint.X)
                id_part_ = str(s[1].firstPoint.Y)
                id = id_part[0:7] + id_part_[0:7]
                p = (id, (s[1].firstPoint.X, s[1].firstPoint.Y))
                if p not in pkt:
                    pkt.append(p)

                id_part = str(s[1].lastPoint.X)
                id_part_ = str(s[1].lastPoint.Y)
                idk = id_part[0:7] + id_part_[0:7]
                p = (id, (s[1].lastPoint.X, s[1].lastPoint.Y))
                V = 0
                if p not in pkt:
                    pkt.append(p)
                if s[3] == 'A':
                    V = 120
                elif s[3] == 'S':
                    V = 90
                elif s[3] == 'GP':
                    V = 70
                elif s[3] == 'G':
                    V = 60
                elif s[3] == 'Z':
                    V = 60
                elif s[3] == 'L':
                    V = 40
                elif s[3] == 'I':
                    V = 35
                else:
                    V = 45
                edges.append([s[0], id, idk, s[2], V])

        for pt in pkt:
            odlp = numpy.sqrt(
                (pt[1][0] - line_geometry.firstPoint.X) ** 2 + (pt[1][1] - line_geometry.firstPoint.Y) ** 2)
            odl_k = numpy.sqrt(
                (pt[1][0] - line_geometry.lastPoint.X) ** 2 + (pt[1][1] - line_geometry.lastPoint.Y) ** 2)
            odl.append(odlp)
            odlk.append(odl_k)

        n_odl = numpy.min(odl)
        n_odlk = numpy.min(odlk)
        n_odl_i = odl.index(n_odl)
        n_odl_ik = odlk.index(n_odlk)
        ok = pkt[n_odl_i]
        pkt_P = ok[0]
        okk = pkt[n_odl_ik]
        pkt_K = okk[0]

        def Create_Graph(start, end, node, edge, name, type=option):
            G = nx.Graph()
            for p in node:
                G.add_node(p[0], pos=(p[1][0], p[1][1]))
            if type == 'shortest':
                for e in edge:
                    G.add_edge(e[1], e[2], weight=e[3], id=e[0])
            elif type == 'fastest':
                for e in edge:
                    G.add_edge(e[1], e[2], weight=(e[3] / 1000) / e[4], id=e[0])

            def dist(a, b):
                if type == 'shortest':
                    x1 = 0
                    y1 = 0
                    x2 = 0
                    y2 = 0
                    for e in node:
                        if e[0] == a:
                            x1 = e[1][0]
                            y1 = e[1][1]
                        if e[0] == b:
                            x2 = e[1][0]
                            y2 = e[1][1]
                    cost = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
                elif type == 'fastest':
                    cost = 50 / 1000
                return cost



            path = nx.astar_path(G, start, end, dist, weight='weight')
            length_path = nx.astar_path_length(G, start, end, dist, weight='weight')
            print("dlugosc trasy " + name + ": " + str(length_path))
            tab = []
            for i in range(0, len(path) - 1):
                tab.append(G[path[i]][path[i + 1]]['id'])
            query = '"FID" IN ('
            for i in tab:
                query = query + str(i) + ', '
            query = query[:-2]
            query += ')'
            if arcpy.Exists(name):
                arcpy.Delete_management(name)
            arcpy.MakeFeatureLayer_management(punkty[0], name, query)
            time = 0
            for t in tab:
                for e in edge:
                    if t == e[0]:
                        e[3] *= 1.3
                        time += ((e[3] / 1000) / e[4]) * 60
            print("czas " + name + ": " + str(time) + " min")
            return edge


        if option == "shortest":
            Create_Graph(pkt_P, pkt_K, pkt, edges, 'droga_najkrotsza', "shortest")
            for i in (1, 2):
                Create_Graph(pkt_P, pkt_K, pkt, edges, "droga_alternatywna" + str(i), "shortest")
        elif option == "fastest":
            Create_Graph(pkt_P, pkt_K, pkt, edges, 'droga_najszybsza', "fastest")
            for i in (1, 2):
                Create_Graph(pkt_P, pkt_K, pkt, edges, "droga_alternatywna" + str(i), "fastest")

