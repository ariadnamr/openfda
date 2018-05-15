import http.client
import json
import requests
from flask import Flask
from flask import jsonify
from flask import request
from flask import Flask, render_template
from flask import abort
from flask import render_template, url_for, redirect


app = Flask(__name__)

@app.route('/',methods=['GET']) #Ruta que nos dirige a la página inicial donde se encuentran los formularios.
def get_principal(): #Función que devuelve el html principal.
    return """<!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Mini servidor</title>
    </head>
    <body style='background: linear-gradient(to right, #33ccff, #ff99cc)'>
    <p style='font-size:24px;'> OPCIONES A ELEGIR PARA OBTENER DATOS DE OpenFDA:</p>
    <img src='http://i53.tinypic.com/2hcp2mb.gif:' width= "400" height="280" style = "float: right" />
    <form action = "listDrugs" method="get" align="left">
      <input type="submit" value="Listar fármaco">
        Limite: <input type="text" name="limit" value="">
    </form>
    <BR>
    </BR>
    <form action = "listCompanies" method="get" align="left">
      <input type="submit" value="Listar empresas">
        Limite: <input type="text" name="limit" value="">
    </form>
    <BR>
    </BR>
    <form action = "searchDrug" method="get" align="left">
      <input type="submit" value="Buscar fármaco">
        Ingrediente activo: <input type="text" name="active_ingredient" value="">
        Límite: <input type="text" name="limit" value="">
    </form>
    <BR>
    </BR>
    <form action = "searchCompany" method="get" align="left">
      <input type="submit" value="Buscar empresas">
        Empresa: <input type="text" name="company" value=""\n>
        Límite: <input type="text" name="limit" value="">
    </form>
    <BR>
    </BR>
    <form action = "listWarnings" method="get" align="left">
      <input type="submit" value="Buscar precauciones">
        Límite: <input type="text" name="limit" value="">
    </form>
    <p>Si desea acceder a la página principal de OpenFDA<a href='https://open.fda.gov/'> Pinche aquí </a>
    <img src='http://i53.tinypic.com/2hcp2mb.gif:' width= "400" height="280" style = "float: right" />
    <BR>
    </BR>
    <p>Indicaciones: Esta página solo contempla límites del 1 al 100. </p>
    <img src='https://lasaludmovil.files.wordpress.com/2014/06/openfda_logo.jpg?w=640:' width= 300" height="100" style = "float: left" />
    </body>
    </html>"""

@app.route('/listDrugs',methods=['GET']) #Ruta de la lista de fármacos.
def get_listDrugs():
    limit = request.args.get('limit', default = "1") #Recuperamos la variable "limit"
                                                    #cuyo valor asignado es el introducido por el usuario.
    headers = {'User-Agent': 'http-client'}

    conn = http.client.HTTPSConnection("api.fda.gov") #Establecemos la conexión con OpenFDA.
    conn.request("GET", "/drug/label.json?limit="+ limit , None, headers) #Realizamos una petición para obtener
                                                                          #el archivo específico.
    r1 = conn.getresponse()#Obtenemos el json.

    print(r1.status, r1.reason) #Imprimimos el estado y la razón de nuestra conexión.

    data_dictionary = r1.read().decode("utf-8") #Decodificamos el json a utf-8,
                                            # estándar que abarcaba todos los caracteres de las ortografías del mundo.
                                            # (el contenido sigue siendo json)

    conn.close() #Cerramos la conexión con OpenFDA.

    repos = json.loads(data_dictionary)#Loads hace que ese json se convierta en string en python
                                       #en forma de diccionario.

    message = """ <!DOCTYPE html>
               <html
               <head>
               </head>
               <body style='background-color: #66CDAA'>
               <p style="color:#000066;"style="font-size:50px;">NOMBRE MEDICAMENTOS:</p>\n"""

    for medicamento in range(len(repos["results"])):#Gracias al bucle for, podemos ir introduciendo en "message"
                                                    #cada valor del diccionario que nos interese.
        if repos["results"][medicamento]["openfda"]:
            nombre = repos["results"][medicamento]['openfda']['substance_name'][0]
            message += "<li>"+ nombre + "</li>"

        else:
            nombre = "Desconocido"
            message += "<li>"+ nombre + "</li>"


    message += """<p><a href='http://127.0.0.1:8000/'> Home </a>
            </body>
            </html>"""

    return message

@app.route('/listCompanies',methods=['GET'])
def get_active_ingredient():
     limit = request.args.get('limit', default = "1")

     headers = {'User-Agent': 'http-client'}
     conn = http.client.HTTPSConnection("api.fda.gov")
     conn.request("GET", "/drug/label.json?limit="+ limit , None, headers)
     r1 = conn.getresponse()
     print(r1.status, r1.reason)
     data_dictionary = r1.read().decode("utf-8")
     conn.close()
     repos = json.loads(data_dictionary)

     message = """ <!DOCTYPE html>
                <html
                <head>
                </head>
                <body style='background-color: #66CDAA'>
                <p style="color:#000066;"style="font-size:50px;">NOMBRE EMPRESAS:</p>\n"""


     for medicamento in range(len(repos["results"])):

         if repos["results"][medicamento]["openfda"]:
             nombre = repos["results"][medicamento]['openfda']['manufacturer_name'][0]
             message += "<li>"+ nombre + "</li>"

         else:
             nombre = "Desconocido"
             message += "<li>"+ nombre + "</li>"

     message += """<p><a href='http://127.0.0.1:8000/'> Home </a>
             </body>
             </html>"""

     return message


@app.route('/searchCompany',methods=['GET']) #Ruta de la lista de empresas.
def get_company():
    company = request.args.get('company')
    limit = request.args.get('limit', default = "10")

    headers = {'User-Agent': 'http-client'}
    conn = http.client.HTTPSConnection("api.fda.gov")
    conn.request("GET", "/drug/label.json?search=manufacturer_name:"+ company + "&limit="+ limit, None, headers)
    r1 = conn.getresponse()
    print(r1.status, r1.reason)

    if r1.status !=200: #Si el estado es distinto de 200, imprimimos la información expuesta a cotinuación:
        message = """ <!DOCTYPE html>
                   <html
                   <head>
                   </head>
                   <body style='background-color: #D8BFD8'>
                   <p style='font-size:24px;'> ¿HA INTRODUCIDO BIEN LOS DATOS?</p>
                   <p>No se obtiene información al respecto. Aseguresé de que la empresa existe.</p>
                   <p>Probablemente no se haya podido establecer la conexión con OpenFDA debido al recurso solicitado (error 404)</p>
                   <img src='https://i2.wp.com/www.silocreativo.com/wp-content/uploads/2017/11/error-404-web-creativa.gif?resize=600%2C323&quality=100&strip=all&ssl=1:'/>
                   <style type="text/css">
                   img {
                    width: 580px;
                    height: 390px;
                    margin-top: -195px;
                    margin-left: -290px;
                    left: 50%;
                    top: 50%;
                    position: absolute;
                   }
                   </style>
                   <p><a href='http://127.0.0.1:8000/'> Home </a>
                   </body>
                   </html>"""
        return message

    else:
        data_dictionary = r1.read().decode("utf-8")
        conn.close()
        repos = json.loads(data_dictionary)

        message = """ <!DOCTYPE html>
                   <html
                   <head>
                   </head>
                   <body style='background-color: #66CDAA'>
                   <p style="color:#000066;"style="font-size:50px;">NOMBRE MEDICAMENTOS ASOCIADOS A DICHA EMPRESA:</p>\n"""


        for medicamento in range(len(repos["results"])):

            if repos["results"][medicamento]["openfda"]:
                nombre = repos["results"][medicamento]['openfda']['generic_name'][0]
                message += "<li>"+ nombre + "</li>"

            else:
                nombre = "Desconocido"
                message += "<li>"+ nombre + "</li>"

        message += """<p><a href='http://127.0.0.1:8000/'> Home </a>\n
                </body>
                </html>"""

        return message

@app.route('/searchDrug',methods=['GET']) #Ruta de la búsqueda de fármacos.
def get_drug():
    active_ingredient = request.args.get('active_ingredient')
    limit = request.args.get('limit', default = "10")

    headers = {'User-Agent': 'http-client'}
    conn = http.client.HTTPSConnection("api.fda.gov")
    conn.request("GET", "/drug/label.json?search=active_ingredient:"+ active_ingredient+ "&limit="+ limit, None, headers)
    r1 = conn.getresponse()
    print(r1.status, r1.reason)

    if r1.status != 200:
        message = """ <!DOCTYPE html>
                   <html
                   <head>
                   </head>
                   <body style='background-color: #D8BFD8'>
                   <p style='font-size:24px;'> ¿HA INTRODUCIDO BIEN LOS DATOS?</p>
                   <p>No se obtiene información al respecto. Aseguresé de que el ingrediente activo es correcto.</p>
                   <p>Probablemente no se haya podido establecer la conexión con OpenFDA debido al recurso solicitado (error 404)</p>
                   <img src='https://i2.wp.com/www.silocreativo.com/wp-content/uploads/2017/11/error-404-web-creativa.gif?resize=600%2C323&quality=100&strip=all&ssl=1:'/>
                   <style type="text/css">
                   img {
                    width: 580px;
                    height: 390px;
                    margin-top: -195px;
                    margin-left: -290px;
                    left: 50%;
                    top: 50%;
                    position: absolute;
                   }
                   </style>
                   <p><a href='http://127.0.0.1:8000/'> Home </a>
                   </body>
                   </html>"""

        return message

    else:

        data_dictionary = r1.read().decode("utf-8")
        conn.close()

        repos = json.loads(data_dictionary)
        message = """ <!DOCTYPE html>
                   <html
                   <head>
                   </head>
                   <body style='background-color: #66CDAA'>
                   <p style="color:#000066;"style="font-size:50px;">NOMBRE MEDICAMETOS CON DICHO INGREDIENTE ACTIVO:</p>\n"""
        for medicamento in range(len(repos["results"])):

            if repos["results"][medicamento]["openfda"]:
                nombre = repos["results"][medicamento]['openfda']['generic_name'][0]
                message += "<li>"+ nombre + "</li>"

            else:
                nombre = "Desconocido"
                message += "<li>"+ nombre + "</li>"

        message += """<p><a href='http://127.0.0.1:8000/'> Home </a>
                </body>
                </html>"""

        return message

@app.route('/listWarnings',methods=['GET']) #Ruta de las contraindicaciones.
def get_warnings():
    limite = request.args.get('limit')

    headers = {'User-Agent': 'http-client'}
    conn = http.client.HTTPSConnection("api.fda.gov")
    conn.request("GET", "/drug/label.json?limit=" + str(limite) , None, headers)
    r1 = conn.getresponse()
    print(r1.status, r1.reason)

    if r1.status != 200:
        message = """ <!DOCTYPE html>
                   <html
                   <head>
                   </head>
                   <body style='background-color: #D8BFD8'>
                   <p style='font-size:24px;'> ¿HA INTRODUCIDO BIEN LOS DATOS?</p>
                   <p>No se obtiene información al respecto. Aseguresé de que el medicamento existe.</p>
                   <p>Probablemente no se haya podido establecer la conexión con OpenFDA debido al recurso solicitado (error 404)</p>
                   <img src='https://i2.wp.com/www.silocreativo.com/wp-content/uploads/2017/11/error-404-web-creativa.gif?resize=600%2C323&quality=100&strip=all&ssl=1:'/>
                   <style type="text/css">
                   img {
                    width: 580px;
                    height: 390px;
                    margin-top: -195px;
                    margin-left: -290px;
                    left: 50%;
                    top: 50%;
                    position: absolute;
                   }
                   </style>
                   <p><a href='http://127.0.0.1:8000/'> Home </a>
                   </body>
                   </html>"""

        return message

    else:

        data_dictionary = r1.read().decode("utf-8")
        conn.close()
        repos = json.loads(data_dictionary)

        message = """ <!DOCTYPE html>
               <html
               <head>
               </head>
               <body style='background-color: #66CDAA'>
               <p style="color:#000066;"style="font-size:50px;">PRECAUCIONES:</p>\n"""

        for medicamento in range(len(repos["results"])):

            if "warnings" in repos["results"][medicamento]:
                nombre = repos["results"][medicamento]["warnings"][0]
                message += "<li>"+ nombre + "</li>"

            else:
                nombre = "Desconocido"
                message += "<li>"+ nombre + "</li>"

        message += """<p><a href='http://127.0.0.1:8000/'> Home </a>
                </body>
                </html>"""

        return(message)

@app.route('/secret',methods=['GET']) #Ruta de la url restringida (no autorizada).
def abortar():
    abort(401)

@app.route("/redirect") #Ruta para redirigir a la página inicial.
def redirigir():
    return redirect(url_for('get_principal'), code = 302)

if __name__ == '__main__':
 app.run("127.0.0.1", 8000)
