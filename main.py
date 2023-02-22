import retrieveReactome
import retrieveSynthea
import retrieveDGIdb
import time


'''
disease -> medication -> pathway -> pathway information

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

    retrieveDGIdb.getInteractions()

    # retrieve list of drugs from DGIdb database
    drug_list = retrieveDGIdb.getDrugList()
    print("Drugs retrieved from DGIdb")

    # extract [patient ID, [medication_list]] based on previous drug list
    id_medication = retrieveSynthea.retrieveMedications(drug_list)
    print("Patient ID, Condition, and Medications retrieved from Synthea")

    print(id_medication)

    # track time of program
    end = time.time()
    print("Program took : " + str(end - start) + " seconds to run")

if __name__ == "__main__":
    main()
