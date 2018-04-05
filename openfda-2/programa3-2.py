#Otra forma de realizar el ejercicio, la base sigue siendo la misma, sin embargo, 
#esta vez se utiliza la biblioteca http.client.

import http.client
import json

n=0
while True: #Bucle que controla la conexión a las distintas variantes de la url(la cual es controlada por el valor n).
    headers = {'User-Agent': 'http-client'}

    conn = http.client.HTTPSConnection("api.fda.gov")
    conn.request("GET", "/drug/label.json?limit=100&skip=" + str(n) + "&search=substance_name:ASPIRIN", None, headers)
    r1 = conn.getresponse()
    print(r1.status, r1.reason)
    data_dictionary = r1.read().decode("utf-8")
    conn.close()

    repos = json.loads(data_dictionary)

    for medicamento in range(len(repos["results"])): #Gracias al bucle for, podemos ir imprimiendo cada valor del diccionario que nos interese.
        print("El medicamento cuyo identificador es: ", repos["results"][medicamento]["id"], "\nha sido fabricado por: ", repos["results"][medicamento]["openfda"]["manufacturer_name"][0])

    if len(repos["results"]) < 100: #En el momento en el la longitud del diccionario sea menor que 100, pararemos el bucle, pues eso significa que ya no hay más medicamentos para analizar.
        break
    n= n +100 #Modificación del contador, sumamos 100 para más tarde introducirlo en la url de forma que el parámetro skip se saltará cierta cantidad de medicamentos.
