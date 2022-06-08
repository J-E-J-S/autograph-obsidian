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

    # This function generates a dictionary of articles with keyword data from literature scrape, in format {title_1: [keyword1_article1, keyword2_article1 ], title_2 :[keyword1_article2, keyword2_article2], ...  }

    with open(paperScrapePath, encoding='utf-8') as f:
        data = json.load(f)

    keywordsDic = {} # Holds { title_1 : [keyword1, keyword 2], title_2 : [keyword_1, .. , ]}
    count = 0
    for article in data:
        # Ignore items that don't have explicit keywords
        try:
            title = article['title'][0]
            keywordsDic[title] = article['keywordList'][0]['keyword']
        except:
            continue
        count += 1

    return keywordsDic

def buildGraph(minedKeywords, outPath):

    try:
        os.mkdir(outPath)
    except:
        print('WARNING: Outpath already exists.')
        pass

    invalidChars = '<>:/"/\|?*'
    fontStyles = ['<i>', '</i>', '<sub>', '</sub>', '<b>', '</b>', '<sup>', '</sup>' ]
    for title, keywords in minedKeywords.items():
        for keyword in keywords:
            # Clean keyword, handle some weird symbol edge cases
            keyword = keyword.replace('\n', '')
            keyword = keyword.replace('–', '-')
            keyword = keyword.replace('‘',"'")
            keyword= keyword.replace('’', "'")
            for char in invalidChars:
                keyword = keyword.replace(char, '')
            # See if keyword index file already exists, make index file if does not exist
            try:
                f = open(os.path.join(outPath, keyword + '.md'), 'x')
            except:
                pass
            # Add links to the index file and the title at the start of the links
            try:
                f = open(os.path.join(outPath, keyword + '.md'), 'a')
                for html in fontStyles:
                        title = title.replace(html, '')
                f.write(title + '\n')
                for link in keywords:
                    if link != keyword:
                        link = link.replace('–', '-')
                        link = link.replace('‘',"'")
                        link = link.replace('’', "'")
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
