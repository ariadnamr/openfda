#Otra forma de realizar el ejercicio(con biblioteca http.client)
import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json", None, headers)
r1 = conn.getresponse()
print(r1.status, r1.reason)
data_dictionary = r1.read().decode("utf-8")
conn.close()

repos = json.loads(data_dictionary)

print("El identificador del medicamento es:", repos["results"][0]["id"])
