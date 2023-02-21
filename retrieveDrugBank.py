import requests
import json


def getDrugList():

    response = requests.get("https://dgidb.org/api/v2/drugs?page=3")

    #print(response.status_code)

    #print(response.text)

    loaded = json.loads(response.text)

    print(loaded["records"])

    for drug in loaded["records"]:
        print(drug["name"])
