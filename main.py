import retrieveReactome
import retrieveSynthea
import retrieveDGIdb
import time
import os


'''
patientID -> disease -> medication -> gene 

disease -> medication
SYNTHEA data: https://synthea.mitre.org
- retrieve medication from those prescribed due to disease

medication/drug -> gene interaction
DGIdb: https://www.dgidb.org/api
- retrieve drug-gene interactions

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

    # throw everything into a text file
    # patient ID, disease
    # \t medication1, type1, gene1, type2, gene2, type3, gene3...
    if os.path.exists('patient_information.txt'):
        print("Information will be retrieved from patient_information.txt...")
    else:
        with open('patient_information.txt', 'w') as f:
            for k, v in id_medication.items():
                f.write(str(k) + "," + v[0] + "," + str(len(v[1:-1])+1) + "\n")
                for medication in v[1:]:
                    f.write(str(medication) + ",")
                    for interaction in drug_gene_interactions:
                        if medication == interaction[0]:
                            # if no interaction type - influencer
                            if not interaction[1:-1][0]:
                                f.write("influencer,")
                            else:
                                f.write(str(interaction[1:-1][0][0]) + ",")
                            f.write(str(interaction[-1]) + ",")
                f.write("\n")
        print("Patient information stored in patient_information.txt")

    # track time of program
    end = time.time()
    print("Program took : " + str(end - start) + " seconds to run")
    print()

    with open('output.txt', 'w') as f:
        pass
    print("All information is stored in patient_information.txt")
    print()
    print("What information would you like to query?")
    print(" PATIENT | DISEASE | MEDICATION | GENE")
    query_type = input()

    if query_type.lower() == "patient":
        print("Which patient would you like to receive information for? "
              "If you would like to list all patient IDs, please type \"all.\"")
        patient_input = input()
        if patient_input.lower() == "all":
            with open('output.txt', 'w') as f:
                for patient_ID in id_medication.keys():
                    f.write(str(patient_ID) + "\n")
        elif patient_input.lower() in id_medication.keys():
            to_write = []
            with open('patient_information.txt', 'r') as f:
                lines = f.readlines()
                for line in lines:
                    tokenized = line.split(",")
                    if tokenized[0] == patient_input.lower():
                        to_write.append(str(tokenized[0]) + "," + str(tokenized[1]) + "\n")
                        for i in range(0, int(tokenized[2])):
                            to_write.append(lines[lines.index(line)+i+1])
            with open('output.txt', 'w') as f:
                for line in to_write:
                    f.write(str(line))
        else:
            print("Invalid patient ID.")
    elif query_type.lower() == "disease":
        print("Which disease would you like to receive information for? "
              "If you would like to list all diseases, please type \"all.\"")
        disease_input = input()
        if disease_input.lower() == "all":
            with open('output.txt', 'w') as f:
                disease_set = set()
                for k, v in id_medication.items():
                    disease_set.add(v[0])
                for disease in disease_set:
                    f.write(str(disease) + "\n")
        else:
            with open('output.txt', 'w') as f:
                f.write(str(disease_input.lower()) + " is currently treated with the following medications:\n")
                medication_set = set()
                for k, v in id_medication.items():
                    if disease_input.lower() == v[0]:
                        for medication in v[2:]:
                            medication_set.add(medication)
                for medication in medication_set:
                    f.write(str(medication) + "\n")
        if os.path.getsize('output.txt') == 0:
            print("Invalid disease name.")
    elif query_type.lower() == "medication":
        print("Which medication would you like to receive information for? "
              "If you would like to list all medications, please type \"all.\"")
        medication_input = input()
        if medication_input.lower() == "all":
            with open('output.txt', 'w') as f:
                medication_set = set()
                for k, v in id_medication.items():
                    for medication in v[1:]:
                        medication_set.add(medication)
                for medication in medication_set:
                    f.write(str(medication) + "\n")
        else:
            with open('output.txt', 'w') as f:
                for interaction in drug_gene_interactions:
                    if medication_input.lower() == interaction[0]:
                        if not interaction[1]:
                            f.write(str(interaction[0]) + " is influencer of " + str(interaction[2] + "\n"))
                        else:
                            f.write(str(interaction[0]) + "," + str(interaction[1][0]) + "," + str(interaction[2] + "\n"))
        if os.path.getsize('output.txt') == 0:
            print("Invalid medication name.")
    elif query_type.lower() == "gene":
        print("Which gene would you like to receive information for? "
              "If you would like to list all genes, please type \"all.\"")
        gene_input = input()
        if gene_input.lower() == "all":
            with open('output.txt', 'w') as f:
                gene_set = set()
                for interaction in drug_gene_interactions:
                    gene_set.add(interaction[2])
                for gene in gene_set:
                    f.write(str(gene) + "\n")
        if os.path.getsize('output.txt') == 0:
            print("Invalid gene name.")
    else:
        print("Unknown input.")
        return
    print("Query retrieved and results placed in output.txt")

if __name__ == "__main__":
    main()
