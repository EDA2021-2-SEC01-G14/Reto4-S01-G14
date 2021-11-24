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


import config as cf
import sys
import controller
from prettytable import PrettyTable
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


def printMenu():
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
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')

    if int(inputs[0]) == 1:

        print("Cargando información de los archivos ....")
        catalog = controller.NewCatalog()
        controller.loadData(catalog)
        catalogo = controller.getData(catalog)
        printData(catalogo)
        
    elif int(inputs[0]) == 2:
        pass

    elif int(inputs[0]) == 3:
        pass
    
    elif int(inputs[0]) == 4:
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