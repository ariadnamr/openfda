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
      <input type="submit" value="Buscar contraindicaciones">
        Límite: <input type="text" name="limit" value="">
    </form>
    <p>Si desea acceder a la página principal de FDA<a href='https://open.fda.gov/'> Pinche aquí </a>
    <img src='http://i53.tinypic.com/2hcp2mb.gif:' width= "400" height="280" style = "float: right" />
    <BR>
    </BR>
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
               <p>Nombre medicamentos:</p>\n"""

    #Gracias al bucle for, podemos ir imprimiendo cada valor del diccionario que nos interese.
    for medicamento in range(len(repos["results"])):
        if repos["results"][medicamento]["openfda"]:
            nombre = repos["results"][medicamento]['openfda']['substance_name'][0]
            message += "<li>"+ nombre + "</li>"
        else:
            nombre = "Desconocido"
            message += "<li>"+ nombre + "</li>"


    message += "</body>" + "</html>"
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
                <p>Nombre empresas:</p>\n"""


     for medicamento in range(len(repos["results"])):
         # Nombre del componente principal: drugs.openfda.substance_name[0]
         if repos["results"][medicamento]["openfda"]:
             nombre = repos["results"][medicamento]['openfda']['manufacturer_name'][0]
             message += "<li>"+ nombre + "</li>"
         else:
             nombre = "Desconocido"
             message += "<li>"+ nombre + "</li>"
     message += "</body>" + "</html>"
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
                   <p>No se obtiene información al respecto. Aseguresé de que la empresa existe.</p>"""
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
                   <p>Nombre medicamentos:</p>\n"""


        for medicamento in range(len(repos["results"])):
            # Nombre del componente principal: drugs.openfda.substance_name[0]
            if repos["results"][medicamento]["openfda"]:
                nombre = repos["results"][medicamento]['openfda']['generic_name'][0]
                message += "<li>"+ nombre + "</li>"
            else:
                nombre = "Desconocido"
                message += "<li>"+ nombre + "</li>"

        message += "</body>" + "</html>"
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
                   <p>No se obtiene información al respecto. Aseguresé de que el ingediente activo es correcto.</p>
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
                   <p>Nombre medicamentos con ese ingrediente activo</p>"""
        for medicamento in range(len(repos["results"])):
            # Nombre del componente principal: drugs.openfda.substance_name[0]
            if repos["results"][medicamento]["openfda"]:
                nombre = repos["results"][medicamento]['openfda']['generic_name'][0]
                message += "<li>"+ nombre + "</li>"
            else:
                nombre = "Desconocido"
                message += "<li>"+ nombre + "</li>"



        message += "</body>" + "</html>"
        return message

@app.route('/listWarnings',methods=['GET']) #Ruta de las contraindicaciones.
def get_warnings():
    limite = request.args.get('limit')


    headers = {'User-Agent': 'http-client'}

    conn = http.client.HTTPSConnection("api.fda.gov")
    conn.request("GET", "/drug/label.json?limit=" + str(limite) , None, headers) #&skip=" + str(n)
    r1 = conn.getresponse()
    print(r1.status, r1.reason)
    if r1.status != 200:
        message = """ <!DOCTYPE html>
                   <html
                   <head>
                   </head>
                   <body style='background-color: #D8BFD8'>
                   <p>No se obtiene información al respecto. Aseguresé de que el medicamento existe.</p>
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
               <p>Contraindicaciones:</p>"""
        for medicamento in range(len(repos["results"])):
            # Nombre del componente principal: drugs.openfda.substance_name[0]
            if "warnings" in repos["results"][medicamento]:
                nombre = repos["results"][medicamento]["warnings"][0]
                message += "<li>"+ nombre + "</li>"
            else:
                nombre = "Desconocido"
                message += "<li>"+ nombre + "</li>"

        message += "</body>" + "</html>"
        return(message)

@app.route('/secret',methods=['GET']) #Ruta de la url restringida (no autorizada).
def abortar():
        abort(401)

@app.route("/redirect") #Ruta para redirigir a la página inicial.
def redirigir():
    return redirect(url_for('get_principal'), code = 302)

if __name__ == '__main__':
 app.run("127.0.0.1", 8000)
