import os
import sys
import json

def extract_data(file):

    with open(file, encoding='utf-8') as f:
        data = json.load(f)

    dic = {} # Dictionary holding all the years and key word counts {year:{keyword:count, keyword:count}, year:{keyword:count, keyword:count} ... }

    # Loops through summary json created by getpapers to extract articles that have keyword metadata and its year of publication
    # Counts the occurence of those keywords to generate the summary dic
    count = 0
    for item in data:
        count += 1
        # Ignore items that don't have keywords
        try:
            keywords = item['keywordList'][0]['keyword'] # list
            date =  int(item['journalInfo'][0]['yearOfPublication'][0]) # int

            # Loop through keywords in keywords list to count
            for word in keywords:
                word = word.lower() # Standardize keyword format
                print(word)

                # Check if year has been encountered and create entry if not
                if date not in dic:
                    dic[date] = {}

                # Check if keyword has been encountered and create entry and starting count if not
                try:
                    dic[date][word] += 1
                except KeyError:
                    dic[date][word] = 1

        except:
            pass


    print((sorted(dic[2021].values(), reverse=True)))
    for item in dic[2020]:
        if dic[2021][item] == 90:
            print(item)

    print(count)

    return dic



if __name__ == '__main__':

    dirname = os.path.dirname(__file__)
    data = os.path.join(dirname, '../resources/1000_biotechnology/eupmc_results.json')


    print(extract_data(data).keys())
    #print(extract_data(data))
