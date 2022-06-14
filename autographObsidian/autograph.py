import os
import sys
import subprocess
import json
import shutil
import click
import signal

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
            try:
                # Clean keyword, handle some weird symbol edge cases
                keyword = keyword.replace('\n', '')
                keyword = keyword.replace('–', '-')
                keyword = keyword.replace('‘',"'")
                keyword= keyword.replace('’', "'")
            except:
                pass
            for char in invalidChars:
                try:
                    keyword = keyword.replace(char, '')
                except:
                    pass
            # Add links to the index file and the title at the start of the links
            try:
                f = open(os.path.join(outPath, keyword + '.md'), 'a')
                for html in fontStyles:
                        title = title.replace(html, '')
                try:
                    f.write(title + '\n')
                except:
                    print('Warning: title was unwritable for', keyword)
                # NEED TO REFACTOR SO THIS ONLY OCCURS ONCE
                for link in keywords:
                    if link != keyword:
                        link = link.replace('–', '-')
                        link = link.replace('‘',"'")
                        link = link.replace('’', "'")
                        for char in invalidChars:
                            link = link.replace(char, '')
                        try:
                            f.write('[[' + link + ']]\n')
                        except:
                            pass
                f.close()
            except:
                pass
    return

def signalHandler(signum, frame, mineFolderPath):
    # Removes local resources if mining interrupted
    print('Process interrupted.')
    shutil.rmtree(mineFolderPath)
    print('Exiting...')
    sys.exit()

def _getVersion(ctx,param, value):

    if not value or ctx.resilient_parsing:
        return
    folder = os.path.abspath(os.path.dirname(__file__))
    init = os.path.join(folder, '__init__.py')
    f = open(init, 'r')
    version = f.read()
    version = version.replace('__version__ = ', '')
    version = version.replace('\'', '')
    version = version.replace('\n', '' )
    f.close()
    click.echo(version)
    ctx.exit()


@click.command()
@click.argument('query')
@click.option('-l', '--limit', default = 500, type=int, help = 'Number of papers to mine. Default = 500')
@click.option('-v', '--version', is_flag=True, callback=_getVersion, expose_value=False, is_eager=False, help='Show version number and exit.')
def cli(query, limit):

    """Arguments:\n
    QUERY The main search string.
    """

    pathQuery = query.replace(' ', '-') # Format for multi-word query strings

    # Getting bug when chaning directory as this is fed to shell in getpapersWrapper fn
    mineFolderPath =  os.path.join(os.getcwd(), pathQuery + '-mine-' + str(limit)) # Mine will be made in working directory
    if os.path.exists(mineFolderPath):
        print('WARNING: Directory destination for journal mine: ' + mineFolderPath + ', already exists! ')
        print('Please rename or move this directory.')
        print('Exiting...')
        sys.exit()


    # Check folder doesn't already exit, create unique ID if it does
    vaultName = pathQuery + '-vault-' + str(limit)
    if os.path.exists(vaultName):
        count = 1
        while os.path.exists(vaultName):
            vaultName = pathQuery + '-vault-' + str(limit) + ' (' + str(count) + ')'
            count += 1

    signal.signal(signal.SIGINT, lambda signum, frame: signalHandler(signum, frame, mineFolderPath))
    while True:
        getpapersWrapper(query, mineFolderPath, limit)
        minedKeywords = generateKeywords(os.path.join(mineFolderPath, 'eupmc_results.json'))
        buildGraph(minedKeywords, vaultName)
        shutil.rmtree(mineFolderPath)
        sys.exit()

if __name__ == '__main__':
    cli()
