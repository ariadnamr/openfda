import requests
url = requests.get("https://api.fda.gov/drug/label.json") #Nos "conectamos" a la url.
data_dictionary= url.json() #Obtenemos la información procedente de esa url (que se guarda en forma de diccionario)
                            # y le damos un nombre.
#Mediante busquedas e el diccionario y en las listas que contiene, obtenemos la información que queremos.
print("El identificador del medicamento es:", data_dictionary["results"][0]["id"])
print("El propósito del medicamento es:", data_dictionary["results"][0]["purpose"][0])
print("El nombre del fabricante es:", data_dictionary["results"][0]["openfda"]["manufacturer_name"][0])
