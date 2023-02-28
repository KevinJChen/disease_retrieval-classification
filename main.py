import retrieveReactome
import retrieveSynthea
import retrieveDGIdb
import time
import os


'''
patientID -> disease -> medication -> gene 

-> pathway -> pathway information




patientID - disease - medication - 

RxNorm


disease -> medication -> gene -> gene information



disease -> medication
SYNTHEA data: retrieve medication from those prescribed due to disease

medication -> pathway

PharmGKB: https://www.pharmgkb.org/pathways
Drug Bank: https://go.drugbank.com

DGIdb: https://www.dgidb.org/api

pathway -> pathway information
REACTOME API: query with pathway/pathway ID
'''


def main():

    # track time of program
    start = time.time()

    # key = patient ID
    # value = disease and list of medications
    id_medication = {}

    # read txt file if exists
    if os.path.exists("id_medication.txt"):
        print("Extracting information from id_medication.txt...")

        with open('id_medication.txt', 'r') as f:
            lines = f.readlines()
            for line in lines:
                tokenized = line.split(",")
                id_medication[tokenized[0]] = tokenized[1:-1]

    else:

        print("Retrieving drug information from DGIdb and patient ID, medication, disesase from Synthea...")

        # retrieve list of drugs from DGIdb database
        drug_list = retrieveDGIdb.getDrugList()
        time1 = time.time()
        print("Drugs retrieved from DGIdb " + str(time1-start) + " sec)")

        # extract [patient ID, [medication_list] based on previous drug list
        id_medication = retrieveSynthea.retrieveMedications(drug_list)
        time2 = time.time()
        print("Patient ID, Condition, and Medications retrieved from Synthea (" + str(time2-start) + " sec)")

        with open('id_medication.txt', 'w') as f:
            for k, v in id_medication.items():
                f.write(str(k) + "," + str(v[0]) + ",")
                for medication in v[1:]:
                    f.write(str(medication) + ",")
                f.write("\n")

    drug_gene_interactions = []
    # read txt file if exists
    if os.path.exists("drug_gene_interactions.txt"):
        print("Extracting information from drug_gene_interactions.txt...")

        with open('drug_gene_interactions.txt', 'r') as f:
            lines = f.readlines()
            for line in lines:
                tokenized = line.lower().split(',')
                drug_gene_interactions.append([tokenized[0],
                                              tokenized[1:-1],
                                              tokenized[-1][:-1]])

    else:
        print("Retrieving drug gene interaction information from DGIdb...")

        drug_gene_interactions = retrieveDGIdb.getInteractions()
        time3 = time.time()
        print("Interactions retrieved from DGIdb (" + str(time3-start) + " sec)")

        with open('drug_gene_interactions.txt', 'w') as f:
            for dgi in drug_gene_interactions:
                f.write(str(dgi[0]) + ",")
                for interactions in dgi[1]:
                    f.write(str(interactions) + ",")
                f.write(str(dgi[2]) + "\n")


    # combining everything into one hashmap (dictionary)
    patient_information = {}
    for k, v in id_medication.items():

        # patient ID (key)
        patient_information[k] = []

        # disease (value[0])
        patient_information[k].append(v[0])

        # medication list (value[1])
        patient_information[k].append(v[1:])

        all_interactions = []
        for interaction in drug_gene_interactions:
            if interaction[0] in v[1:]:
                all_interactions.append(interaction)

        # drug-gene interactions (value[2])
        patient_information[k].append(all_interactions)

    for k, v in patient_information.items():
        print("Here is the information for patient (" + str(k) + ")")
        print("/tThey have the condition: " + str(v[0]))
        for medication in v[1]:
            for interaction in v[2]:
                if medication == interaction[0]:
                    print("The medication/drug, " + str(medication) + " is an " + str(interaction[1] + ".") +
                          " with the gene, " + str(interaction[2]))


    # track time of program
    end = time.time()
    print("Program took : " + str(end - start) + " seconds to run")

if __name__ == "__main__":
    main()
