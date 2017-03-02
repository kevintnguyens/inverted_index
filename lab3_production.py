# Lab 3, CS 121
# Python 3.5
# Quinn Casey 78016851
# Kevin Nguyen 13942307
# D dogg

###
#
#   Main Goals of program (creating 3 dicts):
#
#   1. Parse bookkeeping files and create dict of docCodes and document URLS
#      {'folderID/docID' : 'documentURL'}
#      This is useful for returning search results later
#
#   2. Transverse documents in file system, parse with BeautifulSoup.
#      Return a NEW dictionary of [{'folderID/docID' : {'term' : frequency} }].
#      This is useful for not having to do 95% of the proj before Wed
#      Can be depreciated later if memory is an issue
#
#   3. (Should be step 2.5) Transform dict from step 2 into inverted index.
#      Structured like {'term' : ['folderID/docID']} (tentative - will need tag support) 
#      This is useful as a small size, sorted dict by TF-IDF.
#      Essentially compressed by using docCodes ['folderID/docID']
#
#   4. Add a search functionality? Definitely need, not sure how to implement
#      She'll probably clarify next week
#      
###

###
# TODO BY WEDNESDAY March 1st:
#   Steps 1 & 2 above. Functions:
#   * getJson [DONE]
#   * getTsv [NOT NEEDED?]
#   * parseDocumentDict [DONE]
#   * printDocumentDict for our M1 report [DONE]
###

###
# TODO BY March 8th:
#   Step 3 above. Functions:
#   - createInvertedIndex
#   - searchIndex
###

###
# TODO by final due date
#   - IDK
###

import json
import os.path
from bs4 import BeautifulSoup

def getJson(jsonFile):
    """
    *** Reads a json file
    *** NOTE: READ USING BLOCKS OR WHATEVER. NOT ALL AT ONCE (ijson?)
    *** Returns a dict {'folderID/docID' : 'documentURL'}
    """

    with open(jsonFile, 'r', encoding="UTF-8") as jsonData:
        data = json.load(jsonData)

    return data

def getTsv(tsvFile):
    """
    *** Reads a tsv file, splits by newlines & spaces?
    *** NOTE: READ USING BLOCKS OR WHATEVER. NOT ALL AT ONCE
    *** Returns a dict {'folderID/docID' : 'documentURL'}
    """

    return dict()


def parseDocumentDict(documentDict):
    """
    *** Meaty part of the script. Used for M1
    *** For each document in documentDict, split the key docCode ('folderID/docID')
    *** by ':' -- get document in [0] (folderID) with name [1] (docID)
    *** Open document and parse with BS.
    *** FOR NOW: STRIP TAGS AND GET WORDS (TEXT) ONLY!
    *** Add terms and their respective freq to a dict. Append dict of
    *** 'folderID/docID' to final index.
    *** Returns {'folderID/docID' : {'term' : frequency} }

    *** TODO LATER (NOT WED):
    *** - Tag support.
    ***   Differentiate between <p>What's gucci</p> and <h1>What's gucci</h1>
    ***   maybe in createInvertedIndex() idk
    """

    index = dict()

    #mostly pseudo code
    for docCode in documentDict:
        if(os.path.isfile(docCode)):
            htmlData = open(docCode, 'r', encoding="UTF-8")
            soup = BeautifulSoup(htmlData, 'html.parser')
            #BS.stripTags()
            
            pureText = soup.get_text()
            termFreqDict = dict()

            
            for term in pureText.split():
                if(term in termFreqDict):
                    termFreqDict[term] += 1
                else:
                    termFreqDict[term] = 1

            # append to final index
            index[docCode] = termFreqDict
        
    return index

def printDocumentDict(indexDict):
    """
    *** FOR WEDNESDAY'S M1 REPORT ONLY!!
    *** Print the following info (to file maybe):
    ***     - # of documents in index
    ***     - # of unique words
    ***     - computed size of index file
    *** Returns void
    """

    # num of documents
    print('Number of documents: '+str(len(indexDict)))

    # num of unique words
    termSet = set()
    # iterate over terms, add to set
    for document in indexDict:
        for term in indexDict[document]:
            termSet.add(term)
    print('Number of unique terms: '+str(len(termSet)))

    # Compute size of index file
    f = open('index.json', 'w', encoding="UTF-8")
    f.write(json.dumps(indexDict, ensure_ascii=False))
    f.close()

    print('File size of current index: '+str(os.path.getsize('index.json'))+' bytes')
    

def createInvertedIndex(indexDict):
    """
    *** Given an index [{'folderID/docID' : {'term' : frequency} }]
    *** 1. Create new index, in the structure of {'term' : ['folderID/docID']}
    *** EDIT STRUCTURE MAYBE? May need to change ['folderID/docID'] to {'folderID/docID' : frequency}
    *** Returns {'term' : ['folderID/docID']}
    """

    pass

# POSSIBLY NOT NEEDED??
def searchIndexUI():
    """
    *** Prompts user for valid input??? NECESSARY?
    *** Returns a search query string
    """

    pass

def searchIndex(inIndex, query):
    """
    *** Given an Inverted Index and query
    *** 1. Compute TF-IDF of documents relative to query
    *** 2. Sort by highest ranking folderID/docID (docCode)
    *** 3. Return an ordered list of ['folderID/docID'] as a search result
    """

    pass

if __name__ == "__main__":

    #    #
    # M1 #
    #    #

    # Get data from json (dict)
    comboDict = getJson('bookkeeping.json')

    # Get data from tsv (dict) & append to json data
    comboDict.update(getTsv('bookkeeping.tsv'))

    # With the large combined dict, parse through each document
    # structured as {'folderID/docID' : 'documentURL'}
    # Return an index (list of dicts of dicts)
    #   index = [{'folderID/docID' : {'term' : frequency} }]
    simpleDocIndex = parseDocumentDict(comboDict)

    # FOR WEDNESDAY ONLY, COMMENT OUT IN PRODUCTION
    printDocumentDict(simpleDocIndex)

    #    #
    # M2 #
    #    #

    # Create legit inverted index
    '''index = createInvertedIndex(simpleDocIndex)'''

    # Search index for given query
    '''results = searchIndex(index, "crista lopes") # also the other 2 testing queries
'''
    
    # Print query results (all relevant document URLS)
    '''
    print("Found "+len(results)+" results!")
    for docCode in results:
        print(simpleDocIndex[docCode])
    '''
    
    #    #
    # M3 #
    #    #
    # who da hell knows
    

    
