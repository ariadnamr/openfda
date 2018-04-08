import requests
n=0 #Contador mediante el cual controlaremos el parámetro "skip".

#Bucle que controla la conexión a las distintas variantes de la url(la cual es controlada por el valor n).
while True:
    url = requests.get("https://api.fda.gov/drug/label.json?search=active_ingredient:acetylsalicylic&limit=100&skip="+str(n))
    url.close()

    data_dictionary = url.json() #Diccionario que contiene toda la información proveniente de la url
                                 #cuyo archivo es un json.

    #Gracias al bucle for, podemos ir imprimiendo cada valor del diccionario que nos interese.
    for medicamento in range(len(data_dictionary["results"])):
        if "manufacturer_name" in  data_dictionary["results"][medicamento]["openfda"]:
            print("El medicamento cuyo identificador es:")
            print(data_dictionary["results"][medicamento]["id"],"")
            print("ha sido fabricado por:")
            print(data_dictionary["results"][medicamento]["openfda"]["manufacturer_name"][0], "\n\n")
        else:
            print("No se encuentra información sobre el fabricante del medicamento con id:")
            print(data_dictionary["results"][medicamento]["id"],"\n\n")
    if len(data_dictionary["results"]) < 100: #En el momento en el la longitud del diccionario sea menor que 100,
        break                                 #pararemos el bucle, pues eso significa que ya no hay más medicamentos para analizar.
    n= n +100 #Modificación del contador, sumamos 100 para más tarde introducirlo en la url
              #de forma que el parámetro skip se saltará cierta cantidad de medicamentos.
