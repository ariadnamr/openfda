import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov") #Establecemos la conexión con el servidor HTTP que queremos.
conn.request("GET", "/drug/label.json?limit=10", None, headers) #Enviamos nuestra petición al servidor.
r1 = conn.getresponse()
print(r1.status, r1.reason)
data_dictionary = r1.read().decode("utf-8")
conn.close()

repos = json.loads(data_dictionary)

for i in range(0,10): #Como queremos la información de 10 medicamentos, creamos un bucle for que se repite 10 veces.
    print("El identicador del medicamento es:", repos["results"][i]["id"])
    if "purpose" in repos["results"][i]: #Como no todos los medicamentos contienen información sobre el propósito o del nombre del fabricante, lo controlamos mediante sentencias condicionales.
        print("El propósito del medicamento es:", repos["results"][i]["purpose"][0])
    else:
        print("No se encuentra información al respecto. Comprueba si existe el propósito en la página oficial FDA.")

    if "manufacturer_name" in repos["results"][i]["openfda"]:
        print("El nombre del fabricante es:", repos["results"][i]["openfda"]["manufacturer_name"][0])
    else:
        print("No se encuentra información al respecto. Comprueba si existe el nombre del fabricante en la página oficial FDA.")
    print("")
