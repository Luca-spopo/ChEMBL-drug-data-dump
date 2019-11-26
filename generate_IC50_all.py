"""
generate_IC50_all.py: Downloads data for all activity compounds from
the CHEMBL database that satisfy the requirement standard_type:IC50 and standard_value:90 to 120 nM.
Author: Anirudh katoch
"""

import json
import requests

allchems = {}

headers = {
    'Expect': '',
    'Content-Type': 'application/json',
}

data = '{\n  "size": 10000,\n  "_source": [\n    "molecule_chembl_id",\n    "standard_type",\n    "standard_relation",\n    "standard_value",\n    "standard_units"\n  ],\n  "query": {\n    "bool": {\n      "filter": [\n        { "term":  { "standard_type": "IC50" }},\n        { "term":  { "standard_units": "nM" }},\n        { "range":  { "standard_value": { "gte": "90" , "lte": "120" } }}\n      ]\n    }\n  },\n  "sort": ["_doc"]\n}'
response = requests.post('https://www.ebi.ac.uk/chembl/glados-es/chembl_activity/_search?scroll=1m', headers=headers, data=data)
response = json.loads(response.text)
chems = response["hits"]["hits"]
scroll_id = response["_scroll_id"]

while len(chems):
    print("Got %d more items including %s"%(len(chems), chems[0]["_source"]["molecule_chembl_id"]))
    for chem in chems:
        allchems[chem["_source"]["molecule_chembl_id"]] = chem["_source"]
    scroll_id = response["_scroll_id"]
    data = '\n{\n    "scroll" : "1m", \n    "scroll_id" : "%s"\n}\n'%scroll_id
    response = requests.post('https://www.ebi.ac.uk/chembl/glados-es/_search/scroll', headers=headers, data=data)
    response = json.loads(response.text)
    chems = response["hits"]["hits"]


with open("IC50_all2.json", "w") as outputfile:
    json.dump(allchems, outputfile)

with open("IC50_all2.json", "r") as verify_file:
    filedata = json.load(verify_file)
    print(len(filedata.keys()))
    print(len(allchems.keys()))
