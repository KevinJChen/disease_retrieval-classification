
import requests
import json

# gets the total_count of drugs in the database
def getNumDrugs():
    response = requests.get("https://dgidb.org/api/v2/drugs")
    loaded = json.loads(response.text)
    return loaded["_meta"]["total_count"]

def getNumInteractionsPages():
    response = requests.get("https://dgidb.org/api/v2/interactions")
    loaded = json.loads(response.text)
    return loaded["_meta"]["total_pages"]

def getNumInteractions():
    response = requests.get("https://dgidb.org/api/v2/interactions")
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
    print("Retrieved " + str(total_count) + " drugs from DGIdb.")
    return drug_list

def getInteractions():
    drug_gene_interaction = []
    total_count = getNumInteractionsPages()
    counter = 1
    for i in range(1, total_count+1):
        response = requests.get("https://dgidb.org/api/v2/interactions?count=25&page=" + str(i))
        loaded = json.loads(response.text)
        for interaction in loaded["records"]:
            drug_gene_interaction.append([interaction["drug_name"],
                                          interaction["interaction_types"],
                                          interaction["gene_name"]])
        print("Querying page " + str(i) + " of " + str(total_count) + " (drug gene interactions).")
    print("Retrieved " + str(getNumInteractions()) + " drug-gene interactions from DGIdb.")
    return drug_gene_interaction
