"""
get_interesting_bioactive_chems.py: Downloads associated bioactivities for all given proteins from
the CHEMBL database that satisfy the requirement standard_type:IC50 and standard_value:90 to 120 nM.
Author: Anirudh katoch
"""

import requests, json, csv

with open("IC50_all.json") as file, open('CHEMBL25-GPCR.csv') as input_csv_file, open('CHEMBL25-GPCR_output.csv', "w") as output_csv_file:
    csv_reader = csv.reader(input_csv_file, delimiter=',')
    csv_writer = csv.writer(output_csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
    IC50_chems = json.dumps(list(json.load(file).keys()))

    headers = {
        'Content-Type': 'application/json',
        'Expect': '',
    }

    lines = -1

    for row in csv_reader:

        csv_writer.writerow(row)

        lines += 1
        if lines < 2:
            continue

        param_chem = row[0]

        data =  """
        {
            "size": 10000,
            "_source": [
            "molecule_chembl_id"
            ],
            "query": {
                "bool": {
                    "must": [
                        {
                            "query_string": {
                                "analyze_wildcard": true,
                                "query": "_metadata.related_targets.all_chembl_ids:%s"
                            }
                        }
                    ],
                    "filter": [
                        { "terms":  { "molecule_chembl_id": %s }}
                    ]
                }
            },
            "sort": []
        }
        """%(param_chem, IC50_chems)

        response = requests.post('https://www.ebi.ac.uk/chembl/glados-es/chembl_molecule/_search', headers=headers, data=data)
        drugs = json.loads(response.text)["hits"]["hits"]

        print("Made request for %s, got %d drugs to list"%(param_chem, len(drugs)))

        for drug in drugs:
            row[4] = drug["_source"]["molecule_chembl_id"]
            csv_writer.writerow(row)

