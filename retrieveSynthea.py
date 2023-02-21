import csv
import keyword
from rake_nltk import Rake


# removes tag if the string contains one
def removeTag(condition):
    if '(' in condition:
        return condition[:condition.index('(')-1]
    return condition

def extractName(medication, extracted_medication):
    medication_list = []
    for word in medication.split(" "):
        if word in extracted_medication:
            medication_list.append(word)
    return medication_list

'''
get list of conditions and patient id with those conditions
returns list with element [patient ID, condition]
'''
def retrieveConditions():
    id_condition = []
    with open('synthea/conditions.csv') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            # row[2] = patient ID
            # row[5] = patient condition
            id_condition.append([row[2], removeTag(row[5].lower())])
    return id_condition

'''
get list of patient id and medications ONLY if is prescribed to treat a condition
return list with element [patient ID, condition, medication]
'''
def retrieveMedications(extracted_medication):
    id_medication = {}
    with open('synthea/medications.csv') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=",")
        for row in spamreader:

            '''
            row[2] = patient ID
            row[6] = medication
            row [12] = condition
            '''

            # skip medication without specified condition or title column
            if row[12] == "" or row[2] == "PATIENT":
                continue

            if row[2] not in id_medication:
                id_medication[row[2]] = [removeTag(row[12].lower())]

            for element in row[6].lower().split(" "):
                if element in extracted_medication and element not in id_medication[row[2]]:
                    id_medication[row[2]].append(element)

            # if no medication match from extracted_medication, continue
            #medication = extractName(row[6].lower(), extracted_medication)
            #if not medication:
            #    continue
            #id_medication.append([row[2], removeTag(row[12].lower()), medication])

            # for word in row[6].lower():
            #     if word in extracted_medication and word not in id_medication[row[2]]:
            #         id_medication[row[2]].append(word)

    return id_medication

