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
 """

import config as cf
import model
import csv


# Inicialización del Catálogo de libros

def NewCatalog():
    return model.NewCatalog()

# Funciones para la carga de datos

def loadData(catalog):

    file = cf.data_dir + "airports_full.csv"
    airports = csv.DictReader(open(file, encoding="utf-8"), delimiter=",")

    for airport in airports:
        model.addAirport(catalog, airport)


    file = cf.data_dir + "routes_full.csv"
    routes = csv.DictReader(open(file, encoding="utf-8"), delimiter=",")

    for route in routes:
        model.addRoute(catalog, route)

    file = cf.data_dir + "worldcities.csv"
    cities = csv.DictReader(open(file, encoding="utf-8"), delimiter=",")

    for city in cities:
        model.addCity(catalog, city)

##### REQ 2 #####

def findclust(catalog, IATA1, IATA2):
    return model.findclust(catalog, IATA1, IATA2)

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo

def getData(catalog):
    return model.getData(catalog)