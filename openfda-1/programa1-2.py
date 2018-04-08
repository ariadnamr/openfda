#Otra forma de realizar el ejercicio(con biblioteca http.client)

import json
import http.client #Importamos la biblioteca HTTP.client la cual nos permite implementar clientes web de manera muy sencilla.

headers = {'User-Agent': 'http-client'} #Definimos el tipo de cliente que va a hacer la peticion 
                                        #(integrado en python).

conn = http.client.HTTPSConnection("api.fda.gov") #Permite la consexión con el recurso determinado.
conn.request("GET", "/drug/label.json", None, headers) #Realizamos una petición para obtener el archivo específico.
r1 = conn.getresponse() #Obtenemos el json
print(r1.status, r1.reason) #Imprimimos el estado y la razón de nuestra conexión.
data_dictionary = r1.read().decode("utf-8") #Decodificamos el json a utf-8, 
                                            # estándar que abarcaba todos los caracteres de las ortografías del mundo.
                                            # (el contenido sigue siendo json)
conn.close() #Cerramos la conexión.

repos = json.loads(data_dictionary) #Loads hace que ese json se convierta en string en python 
                                    #en forma de diccionario.

print("El identificador del medicamento es:", repos["results"][0]["id"])
print("El propósito del medicamento es:", repos["results"][0]["purpose"][0])
print("El nombre del fabricante es:", repos["results"][0]["openfda"]["manufacturer_name"][0])

