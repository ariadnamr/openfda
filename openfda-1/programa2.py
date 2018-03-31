import urllib.request, json #Importamos los módulos necesarios.

with urllib.request.urlopen("https://api.fda.gov/drug/label.json?limit=10") as url: #Abrimos la url gracias al módulo urllib.
    data_dictionary = json.loads(url.read().decode()) #Guardamos la información obtenida (en forma de diccionario) en una variable.


for i in range(0,10): #Como queremos la información de 10 medicamentos, creamos un bucle for que se repite 10 veces.
    print("El identicador del medicamento es:", data_dictionary["results"][i]["id"])
    if "purpose" in data_dictionary["results"][i]: #Como no todos los medicamentos contienen información sobre el propósito o del nombre del fabricante, lo controlamos mediante sentencias condicionales.
        print("El propósito del medicamento es:", data_dictionary["results"][i]["purpose"][0])
    else:
        print("No se encuentra información al respecto. Comprueba si existe el propósito en la página oficial FDA.")

    if "manufacturer_name" in data_dictionary["results"][i]["openfda"]:
        print("El nombre del fabricante s:", data_dictionary["results"][i]["openfda"]["manufacturer_name"][0])
    else:
        print("No se encuentra información al respecto. Comprueba si existe el nombre del fabricante en la página oficial FDA.")
    print("")
