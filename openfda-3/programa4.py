import socket

IP = "127.0.0.1"
PORT = 9000
MAX_OPEN_REQUESTS = 5


def process_client(clientsocket):
    datos=[] #Creamos una lista vacía donde iremos añadiendo los datos.

    mensaje_solicitud = clientsocket.recv(1024)

    import urllib.request, json

    with urllib.request.urlopen("https://api.fda.gov/drug/label.json?limit=10") as url: #Como en ocasiones anteriores, abrimos la url.
        data_dictionary = json.loads(url.read().decode())

        for i in range(0,10): #Obtenemos la información gracias al bucle for. La información obtenida la guardamos en la lista "datos".
            if "generic_name" in data_dictionary["results"][i]["openfda"]:
                print("El nombre genérico del medicamento es:", data_dictionary["results"][i]["openfda"]["generic_name"][0], "\n")
                datos.append(data_dictionary["results"][i]["openfda"]["generic_name"][0])
            else:
                print("El medicamento con id:", data_dictionary["results"][i]["id"], "no presenta 'nombre genérico'.\n")
                datos.append('El medicamento con id: "'+ data_dictionary["results"][i]["id"]+ '" no presenta "nombre genérico".')
                continue


    def crear_html(elementos): #Función que crea el contenido html.
        html = """<html>
    <head>
    <meta charset="utf-8">
    <title>10 MEDICAMENTOS</title>
    </head>
    <style>
    table, th, td {
    border: 1px solid black;
    border-collapse: collapse;
    }
    th, td {
    padding: 9px;
    }
    div {
        height: 700px;
        background: linear-gradient(to bottom, #33ccff 0%, #ff99cc 100%)
    }
    </style>
    <body>
    <div>
    <h1 style="border:2px solid DodgerBlue;">¡Bienvenido!</h2>
    <p style='font-size:20px;'>A continuación se le muestra una tabla con los 10 medicamentos pedidos:</p>
    <table style='width:60%'>
    <tr>\n <th><p style="color:pink;"style="font-size:50px;">NOMBRE DEL MEDICAMENTO</p>\n"""
        for s in elementos:
            html += "  <tr>\n   <th><p style='font-size:12px'>" + str(s) + '</p></th>\n  </tr>\n'
        html += "</table>\n<p>Para más información, acceda a la url de origen donde encontrarás toda la información actualizada--> <a href='https://api.fda.gov/drug/label.json?limit=10'>Enlace</a>\n"
        html += "<p>Si desea acceder a la página principal de FDA<a href='https://open.fda.gov/'> Pinche aquí </a>\n</div>\n</body>\n</html></p>"
        return html


    contenido= crear_html(datos)
    linea_inicial = "HTTP/1.1 200 OK\n"
    cabecera = "Content-Type: text/html\n"
    cabecera += "Content-Length: {}\n".format(len(str.encode(contenido)))

    mensaje_respuesta = str.encode(linea_inicial + cabecera + "\n" + contenido)
    clientsocket.send(mensaje_respuesta)
    clientsocket.close()


serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    serversocket.bind((IP, PORT))
    serversocket.listen(MAX_OPEN_REQUESTS)

    while True:
        print("Esperando clientes en IP: {}, Puerto: {}".format(IP, PORT))
        (clientsocket, address) = serversocket.accept()

        print("  Peticion de cliente recibida. IP: {}".format(address))
        process_client(clientsocket)

except socket.error:
    print("Problemas usando el puerto {}".format(PORT))
    print("Lanzalo en otro puerto (y verifica la IP)")

