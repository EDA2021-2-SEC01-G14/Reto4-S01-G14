"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import graph 
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf


# Construccion de modelos

def NewCatalog():

    catalog = { "AirportDirigido" : None,
                "Airport2" : None,
                "routesDirigido": graph.newGraph(directed=True, size=10000),
                "routesNodirigido": graph.newGraph(size=3000),
                "MapHelp" : mp.newMap(10000,maptype="PROBING"),
                "MapRoutes" : mp.newMap(50000,maptype="PROBING"),
                "City": mp.newMap(41002,maptype="PROBING"),
                "addCity" : None,
                "MapGraph" : mp.newMap(10000,maptype="PROBING")
                }

    return catalog

# Funciones para agregar informacion al catalogo

def addAirport(catalog, airport):

    a = catalog["MapHelp"]
    name = airport["IATA"]
    if not mp.contains(a,name):
        mp.put(a, name, airport)


def addRoute(catalog, route):

    dp = route["Departure"]
    dt = route["Destination"]

    route1 = catalog["routesDirigido"]
    route2 = catalog["routesNodirigido"]

    routes = tuple(sorted((dp, dt)))

    if not mp.contains(catalog["MapRoutes"], (dp, dt)):
        if graph.containsVertex(route1, dp) and graph.containsVertex(route1, dt):
            graph.addEdge(route1,dp, dt, route["distance_km"])
        elif not graph.containsVertex(route1, dp) and not graph.containsVertex(route1, dt):
            graph.insertVertex(route1, dp)
            graph.insertVertex(route1, dt)
            graph.addEdge(route1, dp, dt, route["distance_km"])
        elif not graph.containsVertex(route1, dp):
            graph.insertVertex(route1, dp)
            graph.addEdge(route1, dp, dt, route["distance_km"])
        else:
            graph.insertVertex(route1, dt)
            graph.addEdge(route1, dp, dt, route["distance_km"])
        
        if catalog["AirportDirigido"] is None:
            catalog["AirportDirigido"] = dp
        mp.put(catalog["MapRoutes"], (dp, dt), None)

    if mp.contains(catalog["MapRoutes"], (dt, dp)) and not mp.contains(catalog["MapGraph"], routes):
        
        if graph.containsVertex(route2, dp) and graph.containsVertex(route2, dt):
            graph.addEdge(route2,dp, dt, route["distance_km"])
        elif not graph.containsVertex(route2, dp) and not graph.containsVertex(route2, dt):
            graph.insertVertex(route2, dp)
            graph.insertVertex(route2, dt)
            graph.addEdge(route2, dp, dt, route["distance_km"])
        elif not graph.containsVertex(route2, dp):
            graph.insertVertex(route2, dp)
            graph.addEdge(route2, dp, dt, route["distance_km"])
        else:
            graph.insertVertex(route2, dt)
            graph.addEdge(route2, dp, dt, route["distance_km"])
        
        if catalog["Airport2"] is None:
            catalog["Airport2"] = dp
        mp.put(catalog["MapGraph"], routes, None)

def addCity(catalog, city):
    name = city["city_ascii"]
    catalog["addCity"] = city
    mp.put(catalog["City"], name, city)

# Funciones para creacion de datos

# Funciones de consulta
def getData(catalog):
    
    resultado = {}
    resultado["primero1"] = me.getValue(mp.get(catalog["MapHelp"], catalog["AirportDirigido"]))
    resultado["primero2"] = me.getValue(mp.get(catalog["MapHelp"], catalog["Airport2"]))
    resultado["aeropuertos1"] =lt.size(graph.vertices(catalog["routesDirigido"]))
    resultado["aeropuertos2"] =  lt.size(graph.vertices(catalog["routesNodirigido"]))
    resultado["ciudades"]=mp.size(catalog["City"])
    resultado["ciudad"] = catalog["addCity"]

    return resultado


##### REQ 2 #####

def findclust(catalog, IATA1, IATA2):

    catalog['routesDirigido']

    SCC = scc.KosarajuSCC(catalog['routesDirigido'])

    Components=scc.connectedComponents(SCC)
   
    Conect=scc.stronglyConnected(SCC,IATA1,IATA2)

    return Components, Conect

    
##### REQ 4 #####

def traveller(catalog,milles,Departure):


    return

##### REQ 4 #####

def traveller(catalog,milles,Departure):

    kms=float(milles)*1.6/2

    search=djk.Dijkstra(catalog['routesNodirigido'],Departure)

    return

##### REQ 5 #####



##### REQ 6 #####


# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento