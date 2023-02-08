

import requests
import json

'''
retrieving data from the reactome API
https://reactome.org/dev
https://reactome.org/download-data
'''



def test():
    response = requests.get("https://reactome.org/ContentService/data/diseases")

    print(response.status_code)
    print(response.text)

