import requests
n=0 #Contador mediante el cual controlaremos el argumento "skip".
while True: #Bucle que controla la conexión a las distintas variantes de la url(la cual es controlada por el valor n).
    url = requests.get("https://api.fda.gov/drug/label.json?limit=100&skip=" + str(n) + "&search=substance_name:ASPIRIN")
    url.close()

    data_dictionary = url.json() #Diccionario que contiene toda la información proveniente de la url cuyo archivo es un json.

    for medicamento in range(len(data_dictionary["results"])): #Gracias al bucle for, podemos ir imprimiendo cada valor del diccionario que nos interese.
        print("El medicamento cuyo identificador es: ", data_dictionary["results"][medicamento]["id"], "\nha sido fabricado por: ", data_dictionary["results"][medicamento]["openfda"]["manufacturer_name"][0])

    if len(data_dictionary["results"]) < 100: #En el momento en el la longitud del diccionario sea menor que 100, pararemos el bucle, pues eso significa que ya no hay más medicamentos para analizar.
        break
    n= n +100 #Modificación del contador, sumamos 100 para más tarde introducirlo en la url de forma que el parámetro skip se saltará cierta cantidad de medicamentos.

