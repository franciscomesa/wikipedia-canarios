import wikipedia
#import mediawiki as pw
import urllib
import json
import wikipediaapi

# https://es.wikipedia.org/w/api.php?action=query&list=categorymembers&cmpageid=132668&format=json&cmlimit=500
# https://www.mediawiki.org/wiki/API:Categorymembers

def print_categorymembers(categorymembers, level=0, max_level=10):
        for c in categorymembers.values():
            print("%s: %s (ns: %d)" % ("*" * (level + 1), c.title, c.ns))
            if c.ns == wikipediaapi.Namespace.CATEGORY and level < max_level:
                print_categorymembers(c.categorymembers, level=level + 1, max_level=max_level)



def listaPaginasporID(pageid):
#Páginas enlazadas directamente en una categoría    
    listaPaginas = []
    pages = urllib.request.urlopen("https://es.wikipedia.org/w/api.php?action=query&list=categorymembers&cmpageid=" + str(pageid) + "&format=json&cmlimit=500")
    print("https://es.wikipedia.org/w/api.php?action=query&list=categorymembers&cmpageid=" + str(pageid) + "&format=json&cmlimit=500")
    data = json.load(pages)
    query = data['query']
    category = query['categorymembers']
    for x in category:
        print (str(x['pageid']) + ' > ' + x['title'].replace("Categoría", "Category"))
        listaPaginas.append(x['pageid'])
    return listaPaginas


def listaCategoriasporID(pageid):
#Subcategorías por ID
    listaCategorias = []
    pages = urllib.request.urlopen("https://es.wikipedia.org/w/api.php?action=query&list=categorymembers&cmpageid=" + str(pageid) + "&format=json&cmlimit=500&cmtype=subcat")
    data = json.load(pages)
    query = data['query']
    category = query['categorymembers']
    for x in category:
        print (str(x['pageid']) + ' > ' + x['title'].replace("Categoría", "Category"))
        listaCategorias.append(x['pageid'])
    return listaCategorias



#
# Valores por defecto para el script
#
LANG = "es"
CATEGORIAORIGEN = "Category:Canarios"
IDCATEGORIAORIGEN = 132668

###CATEGORIAORIGEN   = "Category:Naturales_de_la_provincia_de_Las_Palmas"
###IDCATEGORIAORIGEN = 4343370


wikipedia.set_lang(LANG)  

#print(wikipedia.search("Bill"))

canarios = wikipedia.page(CATEGORIAORIGEN)

print(canarios)
print(canarios.links)

# Library wikipedia-api
wiki_wiki = wikipediaapi.Wikipedia('es')




print("\n\n\nMétodo alternativo\n\n\n")

# Páginas enlazadas?
#pages = urllib.request.urlopen("https://es.wikipedia.org/w/api.php?action=query&list=categorymembers&cmtitle=" + CATEGORIAORIGEN + "&format=json&cmlimit=5000")
#Subcategorías por nombre
#pages = urllib.request.urlopen("https://es.wikipedia.org/w/api.php?action=query&list=categorymembers&cmtitle=" + CATEGORIAORIGEN + "&format=json&cmlimit=5000&cmtype=subcat")
#Subcategorías por ID
#pages = urllib.request.urlopen("https://es.wikipedia.org/w/api.php?action=query&list=categorymembers&cmpageid=" + str(IDCATEGORIAORIGEN) + "&format=json&cmlimit=5000&cmtype=subcat")
print("https://es.wikipedia.org/w/api.php?action=query&list=categorymembers&cmtitle=" + CATEGORIAORIGEN + "&format=json&cmlimit=5000&cmtype=subcat")


print ("Obtenemos subcategorías")
subcategorias = listaCategoriasporID(IDCATEGORIAORIGEN)
print(subcategorias)
print ("Obtenemos páginas")
paginas = listaPaginasporID(IDCATEGORIAORIGEN)
print("paginas")
print(paginas)

# Copiado de https://pypi.org/project/Wikipedia-API/
cat = wiki_wiki.page(CATEGORIAORIGEN)
print("Category members: "+CATEGORIAORIGEN)
print_categorymembers(cat.categorymembers)

for p in paginas:
    pagina = wikipedia.page(None,p)
    print(pagina)
    page_py = wiki_wiki.page(p)
    print(page_py)