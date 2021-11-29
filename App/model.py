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

import numpy 
import math
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
def addtomap(map,key,object):

    if mp.contains(map,key):
    
            entry=mp.get(map,key)
            list=entry['value']
            lt.addLast(list,object)
            mp.put(map,key,list)
            #print(mp.get(catalog['BeginDate'],artist['BeginDate']))
            
    else: 
        list=lt.newList(datastructure='ARRAY_LIST')
        lt.addLast(list,object)
        mp.put(map,key,list)

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
    #mp.put(catalog["City"], name, city)
    addtomap(catalog["City"], name, city)

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
##############################

##### REQ 1 #####

def Interconection(catalog):

    digraph=catalog['routesDirigido']
    Nodigraph=catalog['routesNodirigido']

    Divertexs=graph.vertices(digraph)
    NoDivertexs=graph.vertices(Nodigraph)

    VMaxDi=lt.getElement(Divertexs,1)
    VMaxDidegree=graph.outdegree(digraph,VMaxDi) + graph.indegree(digraph,VMaxDi)

    for i in range(1,lt.size(Divertexs)+1):

        Vertice=lt.getElement(Divertexs,i)
        out=graph.outdegree(digraph,Vertice)
        indeg=graph.indegree(digraph,Vertice)
        degree=out+indeg

        if degree >= VMaxDidegree:
            VMaxDi=Vertice
            VMaxDidegree=degree

    listDi=lt.newList(datastructure='ARRAY_LIST')
    lt.addLast(listDi,VMaxDi)

    for i in range(1,lt.size(NoDivertexs)+1):
        Vertice=lt.getElement(NoDivertexs,i)
        degree=graph.degree(Nodigraph,Vertice)

        if degree == VMaxDidegree:
             lt.addLast(listDi,Vertice)

####################################################

    VMaxNoDi=lt.getElement(NoDivertexs,1)
    VMaxNoDidegree=graph.degree(Nodigraph,VMaxNoDi)

    for i in range(1,lt.size(NoDivertexs)+1):
        Vertice=lt.getElement(NoDivertexs,i)
        degree=graph.degree(Nodigraph,Vertice)

        if degree == VMaxNoDidegree:
            VMaxNoDi=Vertice
            VMaxDidegree=degree

    listNoDi=lt.newList(datastructure='ARRAY_LIST')
    lt.addLast(listNoDi,VMaxNoDi)

    for i in range(1,lt.size(NoDivertexs)+1):
        Vertice=lt.getElement(NoDivertexs,i)
        #degree=graph.degree(Nodigraph,Vertice)
        out=graph.outdegree(digraph,Vertice)
        indeg=graph.indegree(digraph,Vertice)
        degree=out+indeg

        if degree == VMaxNoDidegree:
             lt.addLast(listNoDi,Vertice)

    #print(listDi,listNoDi)

    return listDi,listNoDi

##### REQ 2 #####

def findclust(catalog, IATA1, IATA2):

    catalog['routesDirigido']

    SCC = scc.KosarajuSCC(catalog['routesDirigido'])

    Components=scc.connectedComponents(SCC)
   
    Conect=scc.stronglyConnected(SCC,IATA1,IATA2)

    return Components, Conect

    
##### REQ 3 #####

def t(catalog,milles,Departure):


    return

##### REQ 4 #####

def traveller(catalog,milles,Departure):

    kms=float(milles)*1.6/2

    mp.get(catalog['City'],Departure)
    search=djk.Dijkstra(catalog['routesNodirigido'],Departure)

    return

##### REQ 5 #####



##### REQ 6 #####

#FUNCION AUXILIARES

def distanceCord(Lat1,Lon1,Lat2,Lon2):

    r=6371 
    distanceP1 = math.sqrt(pow(math.sin((Lat2-Lat1)/2),2)  +  math.cos(Lat1)*math.cos(Lat2)*pow(math.sin((Lon2-Lon2)/2),2))
    distanceF= 2*r*math.asin(distanceP1)
    return distanceF
    
# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento