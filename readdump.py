import pickle
from enum import Enum
#
# What's Canary?
#   Born at Canary Islands
#
# What's not canary person?
#   Born outside of Canary Islands
#
# People without vcard
#
#

class Canaryborn(Enum):
    canary = 1
    notcanary = 0
    unknown = 2


#provinces=["Álava", "Albacete", "Alicante", "Almería", "Asturias", "Ávila", "Badajoz", "Barcelona", "Burgos", "Cáceres", "Cádiz", "Cantabria", "Castellón", "Ciudad Real", "Córdoba", "Cuenca", "Gerona", "Granada", "Guadalajara", "Guipúzcoa", "Huelva", "Huesca", "Islas Baleares", "Jaén", "La Coruña", "La Rioja", "Las Palmas", "León", "Lérida", "Lugo", "Madrid", "Málaga", "Murcia", "Navarra", "Orense", "Palencia", "Pontevedra", "Salamanca", "Santa Cruz de Tenerife", "Segovia", "Sevilla", "Soria", "Tarragona", "Teruel", "Toledo", "Valencia", "Valladolid", "Vizcaya", "Zamora", "Zaragoza", "Ceuta", "Melilla"];
provinces=["Álava", "Albacete", "Alicante", "Almería", "Asturias", "Ávila", "Badajoz", "Barcelona", "Burgos", "Cáceres", "Cádiz", "Cantabria", "Castellón", "Ciudad Real", "Córdoba", "Cuenca", "Gerona", "Granada", "Guadalajara", "Guipúzcoa", "Huelva", "Huesca", "Islas Baleares", "Jaén", "La Coruña", "La Rioja", "León", "Lérida", "Lugo", "Madrid", "Málaga", "Murcia", "Navarra", "Orense", "Palencia", "Pontevedra", "Salamanca", "Segovia", "Sevilla", "Soria", "Tarragona", "Teruel", "Toledo", "Valencia", "Valladolid", "Vizcaya", "Zamora", "Zaragoza", "Ceuta", "Melilla"];
canaryplaces={
    "La Orotava" : "Tenerife", "Puerto de la Cruz" : "Tenerife", "Los Realejos" : "Tenerife", "San Cristóbal de La Laguna" : "Tenerife",
    "La Perdoma" : "Tenerife", "Santa Cruz de tenerife" : "Tenerife",
    "Garachico" : "Tenerife", "Candelaria" : "Tenerife", "Guía de Isora" : "Tenerife", "Arafo" : "Tenerife", "San Miguel de Abona" : "Tenerife",
    "Granadilla de Abona" : "Tenerife", "La Guancha" : "Tenerife", "Tacoronte" : "Tenerife",
    "Santa Cruz de La Palma" : "La Palma",
    "Tazacorte" : "La Palma", 
    "Valverde" : "El Hierro", "El Pinar" : "El Hierro", "El Hierro" : "El Hierro",
    "San Bartolomé" : "Lanzarote", "Arrecife" : "Lanzarote",
    "Hermigua" : "La Gomera",
    "Puerto del Rosario" : "Fuerteventura",
    "Vecindario" : "Gran Canaria", "Agaete" : "Gran Canaria", "Gran Canaria" : "Gran Canaria",
    "Teror" : "Gran Canaria", "Telde" : "Gran Canaria", "Santa Brígida" : "Gran Canaria",
    "Las Palmas" : "Gran Canaria", "Tenerife" : "Tenerife", "Gomera" : "La Gomera", "Lanzarote" : "Lanzarote", "Fuerteventura" : "Fuerteventura"}
nacimientos = 0
totalcanarios = 0
sindatos = 0
nocanarios = 0
nosesabe = 0

def processBorn(born):
    result = born.replace('(', ' ').replace(')', ' ')
    result = result.replace('España', '')
    return result

def isCanary(born, idwikipedia):
    if born is None or len(born) == 0:
        #print("!! canario " + born)
        return Canaryborn.desconocido
    for province in provinces:
        if (born.find(province) > -1):
            #print("No canario: " + born)
            return Canaryborn.notcanary
    #print("Es canario " + born)
    for canaryplace in canaryplaces:
        if (born.find(canaryplace) > -1):
            return Canaryborn.canary

    return Canaryborn.unknown

def testBornSite(listofpersons):
    global nacimientos
    global totalcanarios
    global nocanarios
    global sindatos
    global nosesabe
    for idwikipedia in listofpersons:
        person = listofpersons[idwikipedia]
        data = person['vcard']
        #print(person['title'] + '\t' + str(len(data)))
        #if person['categoria'].find('Obispos') == -1 \
        #and person['categoria'].find('Religiosos') == -1:
        if (data != None and len(data)>0 and 'Nacimiento' in data):
                #print('\tNacimiento: ' + processBorn(data['Nacimiento']))
                #print('\tCategoría: ' + person['categoria'])
            checkBorn = isCanary(data['Nacimiento'], idwikipedia)
            checkBornResult = "No hay dat: "
            if checkBorn == Canaryborn.canary:
                checkBornResult = "Es Canario: "
                totalcanarios += 1
            elif checkBorn == Canaryborn.notcanary:
                checkBornResult = "No Canario: "
                nocanarios += 1
            else:
                checkBornResult = "!! Canario: "
                nosesabe += 1
            nacimientos +=  1
            #totalcanarios = totalcanarios + 1
            if checkBorn == Canaryborn.unknown:
                print(checkBornResult + person['title'] + '\t' + data['Nacimiento'])

        else:
            #print("NO VCARD:   " + person['categoria'] + '\t'  +person['title'])
            sindatos += 1
            



# Load list of biographies previously fetched
with open("canarios.pkl","rb") as fp:
    canarios = pickle.load(fp)

print(len(canarios))
testBornSite(canarios)



print("---------------\nResume:\n")
print('\tTotal: ' + str(len(canarios)))
print('\tTotal canarios:   ' + str(totalcanarios))
print('\tTotal No se sabe: ' + str(nosesabe))
print('\tTotal sin vcard:  ' + str(sindatos))
print('\tNo canarios:      ' + str(nocanarios))
print('\tNacimientos       ' + str(nacimientos) )