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
from prettytable import PrettyTable
import math
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import stack
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.ADT import graph 
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import mergesort as mg
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
                "MapGraph" : mp.newMap(10000,maptype="PROBING"),
                "MapAirport_bycity" : mp.newMap(10000,maptype="PROBING"),
                "MapAirport_bycountry" : mp.newMap(10000,maptype="PROBING")
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
def addtoOrdmap(map,key,object):

    if om.contains(map,key):
    
            entry=om.get(map,key)
            list=entry['value']
            lt.addLast(list,object)
            om.put(map,key,list)
            #print(mp.get(catalog['BeginDate'],artist['BeginDate']))
            
    else: 
        list=lt.newList(datastructure='ARRAY_LIST')
        lt.addLast(list,object)
        om.put(map,key,list)
def addAirport(catalog, airport):

    a = catalog["MapHelp"]
    name = airport["IATA"]
    if not mp.contains(a,name):
        mp.put(a, name, airport)

    addtomap(catalog['MapAirport_bycity'],airport['City'],airport)
    addtomap(catalog['MapAirport_bycountry'],airport['Country'],airport)

def addRoute(catalog, route):

    dp = route["Departure"]
    dt = route["Destination"]

    route1 = catalog["routesDirigido"]
    route2 = catalog["routesNodirigido"]

    routes = tuple(sorted((dp, dt)))

    if not mp.contains(catalog["MapRoutes"], (dp, dt)):
        if graph.containsVertex(route1, dp) and graph.containsVertex(route1, dt):
            graph.addEdge(route1,dp, dt, float(route["distance_km"]))
        elif not graph.containsVertex(route1, dp) and not graph.containsVertex(route1, dt):
            graph.insertVertex(route1, dp)
            graph.insertVertex(route1, dt)
            graph.addEdge(route1, dp, dt, float(route["distance_km"]))
        elif not graph.containsVertex(route1, dp):
            graph.insertVertex(route1, dp)
            graph.addEdge(route1, dp, dt, float(route["distance_km"]))
        else:
            graph.insertVertex(route1, dt)
            graph.addEdge(route1, dp, dt, float(route["distance_km"]))
        
        if catalog["AirportDirigido"] is None:
            catalog["AirportDirigido"] = dp
        mp.put(catalog["MapRoutes"], (dp, dt), None)

    if mp.contains(catalog["MapRoutes"], (dt, dp)) and not mp.contains(catalog["MapGraph"], routes):
        
        if graph.containsVertex(route2, dp) and graph.containsVertex(route2, dt):
            graph.addEdge(route2,dp, dt, float(route["distance_km"]))
        elif not graph.containsVertex(route2, dp) and not graph.containsVertex(route2, dt):
            graph.insertVertex(route2, dp)
            graph.insertVertex(route2, dt)
            graph.addEdge(route2, dp, dt, float(route["distance_km"]))
        elif not graph.containsVertex(route2, dp):
            graph.insertVertex(route2, dp)
            graph.addEdge(route2, dp, dt, float(route["distance_km"]))
        else:
            graph.insertVertex(route2, dt)
            graph.addEdge(route2, dp, dt, float(route["distance_km"]))
        
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

    Divertexs=graph.vertices(digraph)

    MapDi=om.newMap(omaptype='RBT')

    for i in range(1,lt.size(Divertexs)+1):

        Vertice=lt.getElement(Divertexs,i)
        out=graph.outdegree(digraph,Vertice)
        indeg=graph.indegree(digraph,Vertice)
        degree=out+indeg

        addtoOrdmap(MapDi,degree,(Vertice,degree))

    Top=lt.newList(datastructure='ARRAY_LIST')

    for i in range(0,5):
        Max=om.maxKey(MapDi)
        for j in range(1,lt.size(me.getValue(om.get(MapDi,Max)))+1) :
                list=me.getValue(om.get(MapDi,Max))
                lt.addLast(Top,lt.getElement(list,j))
        
        om.remove(MapDi,Max)

    return Top
    
####################################################

    
    return listDi

##### REQ 2 #####

def findclust(catalog, IATA1, IATA2):

    Digraph=catalog['routesDirigido']

    SCC = scc.KosarajuSCC(catalog['routesDirigido'])

    Components=scc.connectedComponents(SCC)
   
    if graph.getEdge(Digraph,IATA1,IATA2) != None:
        Conect=scc.stronglyConnected(SCC,IATA1,IATA2)
    else:
        Conect=False

    return Components, Conect

    
##### REQ 3 #####
def closestAirport(catalog,city):

    #AirportsCity=me.getValue(mp.get(catalog['MapAirport_bycity'],city['city_ascii']))

    AirportsCity=me.getValue(mp.get(catalog['MapAirport_bycountry'],city['country']))

    m_airport=lt.getElement(AirportsCity,1)
    m_distance=distanceCord(city['lat'],city['lng'],m_airport['Latitude'],m_airport['Longitude'])

    for i in range(1,lt.size(AirportsCity)+1):

        airport=lt.getElement(AirportsCity,i)
        distance=distanceCord(city['lat'],city['lng'],airport['Latitude'],airport['Longitude'])
        
        if distance < m_distance:
            m_distance = distance
            m_airport = airport

    return m_distance,m_airport

def Shortroute(catalog,Dp_City,Dt_city):

    airport_dp=closestAirport(catalog,Dp_City)

    airport_dt=closestAirport(catalog,Dt_city)

    search=djk.Dijkstra(catalog['routesNodirigido'],airport_dp[1]['IATA'])
    path=djk.pathTo(search,airport_dt[1]['IATA'])

    distance_aerea=0
    #print(path)
    for i in range(1,lt.size(path)+1):
        distance_aerea += lt.getElement(path,i)['weight']

    #print(path)

    distance_terrestre = airport_dp[0]+airport_dt[0]

    Tdistance=distance_aerea+distance_terrestre

    return [Tdistance, path, airport_dp[1], airport_dt[1]]



##### REQ 4 #####

def traveller(catalog,milles,Departure):

    kms=float(milles)*1.6/2

    mp.get(catalog['City'],Departure)
    search=djk.Dijkstra(catalog['routesNodirigido'],Departure)

    return

##### REQ 5 #####

def CloseAir(catalog, aeropuerto):

    a1 = catalog["routesDirigido"]
    
    origen = lt.newList("ARRAY_LIST")
    destino = lt.newList("ARRAY_LIST")
    for uno in lt.iterator(graph.vertices(a1)):
        if uno == aeropuerto:
            adj = graph.adjacents(a1, uno)
            for i in lt.iterator(adj):
                lt.addLast(origen, i)
        else:
            adj = graph.adjacents(a1,uno)
            if lt.isPresent(adj, aeropuerto):
                lt.addLast(destino, uno)

    suma = lt.size(destino)+lt.size(origen)

    return destino, origen, suma

##### REQ 6 #####

#FUNCION AUXILIARES

def distanceCord(Lat1,Lon1,Lat2,Lon2):

    Lat1=float(Lat1)
    Lon1=float(Lon1)
    Lat2=float(Lat2)
    Lon2=float(Lon2)

    c = math.pi/180 #constante para transformar grados en radianes
    r=6371 
    
    #distanceP1 = math.sqrt(pow(math.sin((Lat2-Lat1)/2),2)  +  math.cos(Lat1)*math.cos(Lat2)*pow(math.sin((Lon2-Lon1)/2),2))
    #distanceF= 2*r*math.asin(distanceP1)

    d=2*r*math.asin(math.sqrt(math.sin(c*(Lat2-Lat1)/2)**2 + math.cos(c*Lat1)*math.cos(c*Lat2)*math.sin(c*(Lon2-Lon1)/2)**2))
    return d

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento
