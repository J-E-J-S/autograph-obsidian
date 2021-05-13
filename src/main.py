import os
import sys
import json

def extract_data(file):

    with open(file, encoding='utf-8') as f:
        data = json.load(f)

    for item in data:
        try:
            keywords = item['keywordList'][0]['keyword'] # list
            date =  (item['journalInfo'][0]['yearOfPublication']) # str


        except:
            pass


if __name__ == '__main__':

    dirname = os.path.dirname(__file__)
    data = os.path.join(dirname, '../resources/1000_biotechnology/eupmc_results.json')

    extract_data(data)
