"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
"""

#mport folium 
import config as cf
import sys
import controller
import threading
from prettytable import PrettyTable
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import graph 
from DISClib.ADT import list as lt
assert cf


def printData(Catalogo):

    print("Total de aeropuertos del grafo dirigido: "+ str( Catalogo["aeropuertos1"]))
    print("Total de aeropuertos del grafo no dirigido: " + str(Catalogo["aeropuertos2"]))
    print("Total de ciudades: "  + str(Catalogo["ciudades"]))
    print("\nInformación primer aeropuerto dígrafo:")

    printTable = PrettyTable("Name,City,Country,Latitude,Longitude".split(","))
    row = [Catalogo["primero2"][i] for i in printTable.field_names]
    printTable.add_row(row)

    print(printTable)

    print("\nInformación primer aeropuerto grafo no dirigido:")
    printTable2 = PrettyTable("Name,City,Country,Latitude,Longitude".split(","))
    row = [Catalogo["primero2"][i] for i in printTable2.field_names]
    printTable2.add_row(row)

    print(printTable2)

    print("\nInformacíon de la ultima ciudad cargada")
    printTable3 = PrettyTable(["city_ascii","lat","lng","population"])
    row = [Catalogo["ciudad"][i] for i in printTable3.field_names]
    printTable3.add_row(row)

    print(printTable3)

def printReq1(catalog,rta):
 
    TableDi = PrettyTable("IATA,Name,City,Country,Bonds".split(","))
    
    for i in range(1,lt.size(rta)+1):
        if i <= 5:
            airportT=lt.getElement(rta,i)
            airport=me.getValue(mp.get(catalog['MapHelp'],airportT[0]))
            TableDi.add_row([airport['IATA'],airport['Name'],airport['City'],airport['Country'],airportT[1]])   
        
    print(TableDi)


def printReq2(rta):

    print('Hay',rta[0],'clústeres presentes en la red de transporte aéreo')

    if rta[1] == True:
        print('Los dos aeropuertos están en el mismo clúster')
    else:
        print('Los dos aeropuertos no están en el mismo clúster')

def ChooseCity(catalog,city):

    Table = PrettyTable("N,Name,Country,SubRegion,Latitud,Longitud".split(","))
    
    city_Hom=me.getValue(mp.get(catalog['City'],city))

    for i in range(1,lt.size(city_Hom)+1):    
        eachCity=lt.getElement(city_Hom,i) 
        Table.add_row([i,eachCity['city'],eachCity['country'],eachCity['admin_name'],
        eachCity['lat'],eachCity['lng']])    

    print(Table)

    poscity=int(input('Del 1 al '+str(lt.size(city_Hom))+' escoja una ciudad: '))
          
    return lt.getElement(city_Hom,poscity)
def printReq3(catalog,rta):

    print('\nEl Aeropuerto de Origen es: ',rta[2]['Name'],'('+rta[2]['IATA']+')')
    print('El Aeropuerto de Destino es: ',rta[3]['Name'],'('+rta[3]['IATA']+')')

    Table_route = PrettyTable("N°,Departure,Destination,distance_km".split(","))

    path=rta[1]
    for i in range(1,lt.size(path)+1):
        route = lt.getElement(path,i)
        airport1=me.getValue(mp.get(catalog['MapHelp'],route['vertexA']))['Name']
        airport2=me.getValue(mp.get(catalog['MapHelp'],route['vertexB']))['Name']
        Table_route.add_row([i,airport1+':('+route['vertexA']+')',airport2+':('+route['vertexB']+')',route['weight']])
    print(Table_route)

    print('La Distancia total de la ruta es: ',round(rta[0],4),'(Km)')


def printMenu():
    print("------------------------------------------------------")
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Encontrar puntos de interconexión aérea")
    print("3- Encontrar clústeres de tráfico aéreo")
    print("4- Encontrar la ruta más corta entre ciudades")
    print("5- Utilizar las millas de viajero")
    print("6- Cuantificar el efecto de un aeropuerto cerrado")
    print("7- Comparar con servicio WEB externo")



catalog = None

"""
Menu principal
"""
def thread_cycle():
    while True:
        printMenu()
        inputs = input('Seleccione una opción para continuar\n')

        if int(inputs[0]) == 1:

            print("Cargando información de los archivos ....")
            catalog = controller.NewCatalog()
            controller.loadData(catalog)
            catalogo = controller.getData(catalog)
            printData(catalogo)

            #print(graph.degree(catalog['routesDirigido'],'AER'))
            
        elif int(inputs[0]) == 2:

            rta=controller.Interconection(catalog)
            printReq1(catalog,rta)
            pass

        elif int(inputs[0]) == 3:

            IATA1=input('Ingrese el Código IATA del aeropuerto 1: ')
            IATA2=input('Ingrese el Código IATA del aeropuerto 2: ')

            rta=controller.findclust(catalog, IATA1, IATA2)
            printReq2(rta)

            pass
        
        elif int(inputs[0]) == 4:

            Dp_City=input('Ciudad origen: ')
            Dp_City=ChooseCity(catalog,Dp_City)
            Dt_city=input('Ciudad detino: ')
            Dt_city=ChooseCity(catalog,Dt_city)

            rta=controller.Shortroute(catalog,Dp_City,Dt_city)
            printReq3(catalog,rta)

            pass
        
        elif int(inputs[0]) == 5:
            pass

        elif int(inputs[0]) == 6:
            pass
        
        elif int(inputs[0]) == 7:
            pass

        elif int(inputs[0]) == 8:
            pass

        elif int(inputs[0]) == 9:
            pass

        else:
            sys.exit(0)
    sys.exit(0)

if __name__ == "__main__":
    threading.stack_size(67108864)  # 64MB stack
    sys.setrecursionlimit(2 ** 20)
    thread = threading.Thread(target=thread_cycle)
    thread.start()