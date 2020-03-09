import pickle
from enum import Enum
import pageviewapi
import wikipediaapi


# API page views Wikipedia https://wikitech.wikimedia.org/wiki/Analytics/AQS/Pageviews#Monthly_counts
# https://pypi.org/project/pageviewapi/
# R: https://cran.r-project.org/web/packages/pageviews/vignettes/Accessing_Wikimedia_pageviews.html
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

DATE_INI = '20190101'
DATE_END = '20191231'
WIKI_REP = 'es.wikipedia'

#provinces=["Álava", "Albacete", "Alicante", "Almería", "Asturias", "Ávila", "Badajoz", "Barcelona", "Burgos", "Cáceres", "Cádiz", "Cantabria", "Castellón", "Ciudad Real", "Córdoba", "Cuenca", "Gerona", "Granada", "Guadalajara", "Guipúzcoa", "Huelva", "Huesca", "Islas Baleares", "Jaén", "La Coruña", "La Rioja", "Las Palmas", "León", "Lérida", "Lugo", "Madrid", "Málaga", "Murcia", "Navarra", "Orense", "Palencia", "Pontevedra", "Salamanca", "Santa Cruz de Tenerife", "Segovia", "Sevilla", "Soria", "Tarragona", "Teruel", "Toledo", "Valencia", "Valladolid", "Vizcaya", "Zamora", "Zaragoza", "Ceuta", "Melilla"];
provinces=["Alcalá de Henares", "Palma de Mallorca", "Vitoria", "Bilbao", 
    "Reus", "Fuencalderas", "Tarancón", "Miranda de Ebro", "Jérez del Marquesado","Barbastro","Azpeitia","Suecia","Reino Unido",
    "Reus", "Calatayud","Maiquetía", "Sicilia", "Alemania","Legazpia","Marsella", "Francia","Vich","Roma", "Cuba","Estados Unidos","Alcaudete",
     "Álava", "Albacete", "Alicante", "Almería", "Asturias", "Ávila", "Badajoz", "Barcelona", "Burgos", "Cáceres", "Cádiz", "Cantabria", "Castellón", "Ciudad Real", "Córdoba", "Cuenca", "Gerona", "Granada", "Guadalajara", "Guipúzcoa", "Huelva", "Huesca", "Islas Baleares", "Jaén", "La Coruña", "La Rioja", "León", "Lérida", "Lugo", "Madrid", "Málaga", "Murcia", "Navarra", "Orense", "Palencia", "Pontevedra", "Salamanca", "Segovia", "Sevilla", "Soria", "Tarragona", "Teruel", "Toledo", "Valencia", "Valladolid", "Vizcaya", "Zamora", "Zaragoza", "Ceuta", "Melilla"]
canaryplaces={
    "La Orotava" : "Tenerife", "Puerto de la Cruz" : "Tenerife", "Los Realejos" : "Tenerife", 
    "San Cristóbal de La Laguna" : "Tenerife", "San Cristobal de La Laguna" : "Tenerife",
    "La Perdoma" : "Tenerife", "Santa Cruz de tenerife" : "Tenerife", "Icod de Los Vinos" : "Tenerife",
    "Güímar" : "Tenerife",
    "Garachico" : "Tenerife", "Candelaria" : "Tenerife", "Guía de Isora" : "Tenerife", "Arafo" : "Tenerife", "San Miguel de Abona" : "Tenerife",
    "Granadilla de Abona" : "Tenerife", "La Guancha" : "Tenerife", "Tacoronte" : "Tenerife",
    "Arico" : "Tenerife", "El Sauzal" : "Tenerife", "Icod de los Vinos" : "Tenerife", "Arona" : "Tenerife",
    "Santa Cruz de La Palma" : "La Palma", "Los Llanos de Aridane" : "La Palma",
    "Tazacorte" : "La Palma",  "El Paso" : "La Palma", "Tijarafe" : "La Palma", 
    "Garafía" : "La Palma", "La Palma" : "La Palma", "San Andrés y Sauces" : "La Palma", 
    "Valverde" : "El Hierro", "El Pinar" : "El Hierro", "El Hierro" : "El Hierro",
    "Ingenio" : "Gran Canaria", "Mogán" : "Gran Canaria", "Gáldar" : "Gran Canaria", "Arucas" : "Gran Canaria", "Agüimes" : "Gran Canaria",
    "La Aldea de San Nicolás" : "Gran Canaria",
    "San Bartolomé" : "Lanzarote", "Arrecife" : "Lanzarote", "Teguise" : "Lanzarote", "Tinajo" : "Lanzarote", 
    "Santa Lucía de Tirajana" : "Gran Canaria", "Maspalomas" : "Gran Canaria",
    "Tuineje" : "Fuerteventura",
    "Islote de Lobos" : "Fuerteventura",
    "Vega de San Mateo" : "Gran Canaria",
    "Sabinosa" : "El Hierro", 
    "Las Tricias" : "La Palma", 
    "Breña Alta" : "La Palma", "Breña Baja" : "La Palma",
    "Santa Cruz de la Palma" : "La Palma", "Villa de Mazo" : "La Palma",  
    "Agulo" : "La Gomera", "Vallehermoso" : "La Gomera", 
    "Hermigua" : "La Gomera",
    "Puerto del Rosario" : "Fuerteventura",
    "Vecindario" : "Gran Canaria", "Agaete" : "Gran Canaria", "Gran Canaria" : "Gran Canaria",
    "Teror" : "Gran Canaria", "Telde" : "Gran Canaria", "Santa Brígida" : "Gran Canaria",
    "Las Palmas" : "Gran Canaria", "Tenerife" : "Tenerife", "Gomera" : "La Gomera", "Lanzarote" : "Lanzarote", "Fuerteventura" : "Fuerteventura",
    "Islas Canarias" : "Islas Canarias"}
nacimientos = 0
totalcanarios = 0
sindatos = 0
nocanarios = 0
nosesabe = 0


def sumPageViewsWikis(page, wikis):
    resultado = sumPageViews(page)
    #print('>resultado parcial (es) : ' + str(resultado) + ' >' + page)
    if len(wikis) > 0:
#        print(' no wiki lang list')
#        resultado = sumPageViews(page)
#    else:
        for repo in wikis.keys():
            wiki = wikipediaapi.Wikipedia(repo) 
            pagelang = wiki.page(wikis[repo].title)
            titleRepo = str(wikis[repo])
            #print('pagelang:' + titleRepo+'.')
            #print(titleRepo[0:titleRepo.index(' (')])
            #print('\t\t\t.'+titleRepo[0:titleRepo.index(' (id:')] + '. ' + repo )
            resultadoParcial = sumPageViews(titleRepo[0:titleRepo.index(' (id:')], repo)
            resultado += resultadoParcial
            #print('\t\t\t-'+wikis[repo].title + '-\t' + str(resultadoParcial))
            #print('.'+titleRepo[0:titleRepo.index(' (')] +'.')
    #print('>>>>Resultado final: ' + str(resultado))
    return resultado
            

    

def sumPageViews(page, wiki_language = 'es'):
    resultado = 0
    #print('>'+wiki_language + ' .')
    #print(page)
    try:
        views = pageviewapi.per_article(wiki_language + '.wikipedia', page, DATE_INI, DATE_END,
                        access='all-access', agent='all-agents', granularity='daily')
        resultado = sum(int(item['views']) for item in views['items'])
        #print(tmp_vistas)
        #print(len(views['items']))    
        #print(sum(int(item['views']) for item in views['items']))
    except:
        print('\t\tERROR DATA:(' + wiki_language + ')' + page)
        resultado = -1
    finally:
        return resultado


def processBorn(born):
    result = born.replace('(', ' ').replace(')', ' ')
    result = result.replace('España', '')
    return result

def isCanary(born, idwikipedia):
    if  born is None or len(born) == 0:
        #print("!! canario " + born)
        return Canaryborn.unknown
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
    strFichero = ''
    bucle = 1
    for idwikipedia in listofpersons:
        person = listofpersons[idwikipedia]
        #if person['title'].find('Carla') == -1:
        #    continue
        data = person['vcard']
        strParcial = ''
        #print(person['title'] + '\t' + str(len(data)))
        #if person['categoria'].find('Obispos') == -1 \
        #and person['categoria'].find('Religiosos') == -1:
        if (data != None and len(data)>0 and 'Nacimiento' in data):
                #print('\tNacimiento: ' + processBorn(data['Nacimiento']))
                #print('\tCategoría: ' + person['categoria'])
            checkBorn = isCanary(data['Nacimiento'], idwikipedia)
            if checkBorn == Canaryborn.unknown:
                checkBorn = isCanary(data.get('Origen',''), idwikipedia)
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
            # TODOS SON CANARIOS
            allWikisViews = sumPageViewsWikis(person['title'], person['languagesdetail'])
            strParcial = str(bucle) + ' ' + checkBornResult + person['title'] + '\t' + str(person['backlinks']) + '\t' + str(sumPageViews(person['title'])) + '\t' + str(allWikisViews) + '\t' + str(person['numlanguages']) + '\t' + data['Nacimiento'] + '\t' + person['categoria'].replace('\n', ' ')
            #print(strParcial)
            #if checkBorn == Canaryborn.unknown or checkBorn == Canaryborn.canary:
                #print(str(bucle) + ' ' + checkBornResult + person['title'] + '\t' + str(person['backlinks']) + '\t' + str(sumPageViews(person['title'])) + '\t' + data['Nacimiento'] + '\t' + person['categoria'])
                #if checkBorn == Canaryborn.unknown:
                #    print('\t\t\t' + data.get('Origen', 'N/A'))
                #print('\t\t\t' + str(person['languagesdetail']))
                #sumPageViewsWikis(person['title'], person['languagesdetail'])
        else:
            #print("NO VCARD:   " + person['categoria'] + '\t'  +person['title'])
            sindatos += 1
            allWikisViews = sumPageViewsWikis(person['title'], person['languagesdetail'])
            strParcial = str(bucle) + ' ' + checkBornResult + person['title'] + '\t' + str(person['backlinks']) + '\t' + str(sumPageViews(person['title'])) + '\t' + str(allWikisViews) + '\t' + str(person['numlanguages']) + '\tSINVCARD\t' + person['categoria'].replace('\n', ' ')
            #print(strParcial)
            
        print (strParcial)
        strFichero += strParcial + '\n'    
        bucle += 1
    fp = open("wikipedia-canarios.csv","w")
    fp.write(strFichero )
    fp.close()    
            



# Load list of biographies previously fetched
with open("canarios.pkl","rb") as fp:
    canarios = pickle.load(fp)

#print('Paris         ' + str(sumPageViews('Paris'))) 
#print('Madrid        ' + str(sumPageViews('Madrid')))
#print('Madrid(en)    ' + str(sumPageViews('Madrid', 'en'))) 
#print('Tenerife      ' + str(sumPageViews('Tenerife'))) 
#print('Pedro Guerra  ' + str(sumPageViews('Pedro Guerra'))) 


print("Total canarios: " + str(len(canarios)))
print("Lugar\tNombre\tBacklinks\tPageviews(ES)\tNacimiento\tCategoria")
testBornSite(canarios)

print("---------------\nResume:\n")
print('\tTotal:            ' + str(len(canarios)))
print('\tTotal canarios:   ' + str(totalcanarios))
print('\tTotal No se sabe: ' + str(nosesabe))
print('\tTotal sin vcard:  ' + str(sindatos))
print('\tNo canarios:      ' + str(nocanarios))
print('\tNacimientos       ' + str(nacimientos) )