import os
import sys
import subprocess
import json

def getpapersWrapper(query, mineFolderPath, limit):

    base = 'cmd /c getpapers -q ' # base of getpapers request
    query = ('{}' + query + '{}').format('"', '"') # formatting search string for wrapper
    output_dir = ('{}' + mineFolderPath).format(' -o ') # spacing and option
    limit = ('{}' + str(limit)).format(' -k ')
    command = base + query + output_dir + limit + ' -x -a'
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

    print(keywords)
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
                f = open(outPath + keyword + '.md', 'x')
            except:
                pass
            f = open(outPath + keyword + '.md', 'a')
            for link in article:
                if link != keyword:
                    try:
                        f.write('[[' + link + ']]\n')
                    except:
                        pass
            f.close()

def main(query):

    pathQuery = query.replace(' ', '_') # Format for multi-word query strings
    mineFolderPath =  os.path.join(os.getcwd(), pathQuery + '_mine')

    getpapersWrapper(query, mineFolderPath, 500)
    minedKeywords = generateKeywords(os.path.join(mineFolderPath, 'eupmc_results.json'))
    buildGraph(minedKeywords, 'graph')


if __name__ == '__main__':

    main('Genetic Code Expansion')
