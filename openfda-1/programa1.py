import urllib.request, json

with urllib.request.urlopen("https://api.fda.gov/drug/label.json") as url:
    data_dictionary = json.loads(url.read().decode())

print("EL identificador del medicamento es:", data_dictionary["results"][0]["id"])
print("El propósito del medicamento es:", ((str(data_dictionary["results"][0]["purpose"])).strip("[]")).strip("'"))
print("El nombre del fabricante es:", data_dictionary["results"][0]["openfda"]["manufacturer_name"][0])
