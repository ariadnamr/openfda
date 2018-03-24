import urllib.request, json

with urllib.request.urlopen("https://api.fda.gov/drug/label.json?limit=10") as url:
    data_dictionary = json.loads(url.read().decode())


    for i in range(0,10):
        print("El identicador del medicamento es:", data_dictionary["results"][i]["id"])
        if "purpose" in data_dictionary["results"][i]:
            print("El propósito del medicamento es:", data_dictionary["results"][i]["purpose"][0])

        if "manufacturer_name" in data_dictionary["results"][i]["openfda"]:
            print("El nombre del fabricante s:", data_dictionary["results"][i]["openfda"]["manufacturer_name"][0])
        print("")
        
