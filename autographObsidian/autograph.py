import os
import sys
import subprocess
import json
import shutil

def getpapersWrapper(query, mineFolderPath, limit):

    # This function will search EUPMC based on query and return eupmc_results.json with collated results

    base = 'cmd /c getpapers -q ' # base of getpapers request
    query = ('{}' + query + '{}').format('"', '"') # formatting search string for wrapper
    output_dir = ('{}' + mineFolderPath).format(' -o ') # spacing and option
    limit = ('{}' + str(limit)).format(' -k ')
    command = base + query + output_dir + limit + ' -x -a' # get xml and search all papers not just open-access
    # Try to see if getpapers is installed
    try:
        subprocess.run(command, check = True)
    except subprocess.CalledProcessError:
        print('getpapers not found, begining install with npm.')
        try:
            os.system('npm install -g getpapers')
            print('getpapers installed.')
            os.system(command)
        except:
            print('npm not found, please install npm.')

    return

def generateKeywords(paperScrapePath):

    # This function generates a list of articles with keyword data from literature scrape, in format [[keyword1_article1, keyword2_article1 ], [keyword1_article2, keyword2_article2], ...  ]

    with open(paperScrapePath, encoding='utf-8') as f:
        data = json.load(f)

    keywords = [] # Holds list of lists for keywords per article
    count = 0
    for article in data:
        count += 1
        # Ignore items that don't have explicit keywords
        try:
            keywords.append(article['keywordList'][0]['keyword']) # Appends list object
        except:
            continue

    return keywords

def buildGraph(minedKeywords, outPath):

    try:
        os.mkdir(outPath)
    except:
        pass

    invalidChars = '<>:/"/\|?*'
    for article in minedKeywords:
        for keyword in article:
            # Clean keyword
            keyword = keyword.replace('\n', '')
            for char in invalidChars:
                keyword = keyword.replace(char, '')
            try:
                f = open(os.path.join(outPath, keyword + '.md'), 'x')
            except:
                pass
            try:
                f = open(os.path.join(outPath, keyword + '.md'), 'a')
                for link in article:
                    if link != keyword:
                        try:
                            f.write('[[' + link + ']]\n')
                        except:
                            pass
                            f.close()
            except:
                pass
    return

def main(query, limit):

    pathQuery = query.replace(' ', '-') # Format for multi-word query strings
    mineFolderPath =  os.path.join(os.getcwd(), pathQuery + '-mine' + str(limit)) # Mine will be made in working directory of execution in form: query_mine500 (or limit)

    getpapersWrapper(query, mineFolderPath, limit)
    minedKeywords = generateKeywords(os.path.join(mineFolderPath, 'eupmc_results.json'))
    buildGraph(minedKeywords, 'vault')
    shutil.rmtree(mineFolderPath)

if __name__ == '__main__':

    main('genetic code expansion', 500)
