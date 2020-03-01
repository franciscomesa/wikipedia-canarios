import pickle

nacimientos = 0

with open("canarios.pkl","rb") as fp:
    canarios = pickle.load(fp)

print(len(canarios))
for idcanarios in canarios:
    canario = canarios[idcanarios]
    datos = canario['vcard']
    print(canario['title'] + ' ' + str(len(datos)))
    if (datos != None and len(datos)>0 and 'Nacimiento' in datos):
        print('\tNacimiento' + datos['Nacimiento'])
        nacimientos = nacimientos + 1

print('Total: ' + str(len(canarios)))
print('Nacimientos ' + str(nacimientos) )