
import requests
import json

# gets the total_count of drugs in the database
def getNumDrugs():
    response = requests.get("https://dgidb.org/api/v2/drugs")
    loaded = json.loads(response.text)
    return loaded["_meta"]["total_count"]

# gets a list of drugs in the DGIdb database
def getDrugList():
    drug_list = []
    total_count = getNumDrugs()
    response = requests.get("https://dgidb.org/api/v2/drugs?count=" + str(total_count))
    loaded = json.loads(response.text)
    for drug in loaded["records"]:
        drug_list.append(drug["name"].lower())
    return drug_list

def getInteractions():
    response = requests.get("https://dgidb.org/api/v2/interactions")
    loaded = json.loads(response.text)

    # print(loaded["records"][])

