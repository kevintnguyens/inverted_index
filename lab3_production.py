# Lab 3, CS 121
# Python 3.5
# Quinn Casey 78016851
# Kevin Nguyen 13942307
# Dhruti Khetani 23968158

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

### To improve runtime -Kevin Also are nice to haves
#read from inverted index. Saw that we store the index in a json file
###

import json
import os.path
from bs4 import BeautifulSoup
import time
import math
import re
import csv

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
    *** Reads a tsv file, splits by newlines & spaces
    *** Returns a dict {'folderID/docID' : 'documentURL'}
    """

    with open(tsvFile) as csvFile: 
        tsvreader = csv.reader(csvFile, delimiter ="\n") #read the data and seperate it by newlines   
        dictionary = {} #create a dictionary
        for line in tsvreader: #for each seperated line in tsvreader
            if(line): #if there is a line
                (keys,values) = line[0].split("\t") #seperate with a tab, where the keys='folderID/docID' & values = 'documentURL'
                dictionary[keys]=values
	#print(line)
	# (k,v)=line.split("\t")
	# d[k]=v


    return dictionary


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
    ***   Differentiate between <p>What's gucyxzsci</p> and <h1>What's gucci</h1>
    ***   maybe in createInvertedIndex() idk
    """
    index = dict()

    TAG_MODIFIERS = {'title':2.0, 'h1':1.5, 'h2':1.4, 'h3':1.3, 'h4':1.2, 'h5':1.1, 'h6':1.05, 'p':1, 'strong':1.4, 'b': 1.4};
    modifiedFreqDict = dict()
    
    for docCode in documentDict:
        if(os.path.isfile(docCode)):
            htmlData = open(docCode, 'r', encoding="UTF-8")
            soup = BeautifulSoup(htmlData, 'html.parser')

            modifiedDict = dict()           
    
            # FIRST, get important tags
            for tagName in TAG_MODIFIERS.keys():
                tagData = soup.find_all(tagName)
                for tag in tagData:

                    # cleans text
                    tagData = (re.sub('[^\w\s+]',' ', tag.get_text())).lower()
                    for term in tagData.split():
                        if(term in modifiedDict):
                            modifiedDict[term] += TAG_MODIFIERS[tagName]
                        else:
                            modifiedDict[term] = TAG_MODIFIERS[tagName]

            termFreqDict = dict()
            
            # now work the the remaining text
            pureText = soup.get_text()
            
            # only take alphanumerical words and lower case it
            # just to narrow down the search results
            cleanedText=(re.sub('[^\w\s+]',' ',pureText)).lower()
            pureText=cleanedText
            
            for term in pureText.split():
                if(term in termFreqDict):
                    termFreqDict[term] += 1
                else:
                    termFreqDict[term] = 1

            # append to final index
            index[docCode] = termFreqDict
            if(modifiedDict): modifiedFreqDict[docCode] = modifiedDict
            
    # Change {'folderID/docID' : {'term' : frequency} } to
    # {'term' : {'docCode' : (freq,0)} }
    finalIndex = dict()
    
    for docCode in index:
        for term in index[docCode]:
            if(term not in finalIndex):
                finalIndex[term] = []
            finalIndex[term].append( (docCode, (index[docCode][term], 0)) )


    # Compute TF-IDF
    for term in finalIndex:
        for i in range(len(finalIndex[term])):
            docCode = finalIndex[term][i][0]
            freq_of_doc = finalIndex[term][i][1][0] 
            final_value = (1 + math.log(freq_of_doc)) * math.log(len(index) / len(finalIndex[term]))

            # If the term has a modifier, append to final value score
            if(docCode in modifiedFreqDict and term in modifiedFreqDict[docCode]):
                final_value += modifiedFreqDict[docCode][term]
            
            new_tupple=(docCode,(freq_of_doc,final_value))
            # * math.log(len(index) / len(finalIndex[term]))
            finalIndex[term][i]=new_tupple

    # Write to new index
    f = open('indexBEST.json', 'w', encoding="UTF-8")
    f.write(json.dumps(finalIndex, ensure_ascii=False, indent=2))
    f.close()
    
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

    print('File size of current index: '+str(os.path.getsize('index.json'))+' bytes')

# POSSIBLY NOT NEEDED??
# it is needed for m2
def searchIndexUI():
    """
    *** Prompts user for valid input
    *** Returns a search query string  
    """
    #example of UI
    #Enter a phrase you want to search. Press enter to search. Press q to quit
    # Top 5 urls with the words "your query here"
    #   1.google.com
    #   2. woow.com
    #..etc
    #Enter A phrase you want to search...
    ##do a while input. Return on input if q

    invertedIndex = getJson('indexBEST.json')  
    comboDict = getJson('comboDict.json')
	
    query = "" #given query is an empty string
    while(query is not "q"): #since query is an empty string aka not q, the loop will run atleast once
        print("Please enter your query, or 'q' to quit : ") #have the user input a query, or quit
        query = input() #the user entered query is saved in the variable "query"
        print(query)

        if query is not "q":
            results = searchIndex(invertedIndex, comboDict, query,5)
            count=0
            if(results):
                for line in results:
                    count+=1
                    print(str(count)+'. '+line[0])
            else:
                print("Query not found")
        else:
            break
        
#print("Thank you for searching")#exit with a message
#query = raw_input("Please enter your query, or 'q' to quit : ")#give another chance to type a query?
	
    
def searchIndex(invertedIndex, comboDict, query, x=5):
    """
    *** Given an Inverted Index and query
    *** 1. Compute TF-IDF of documents relative to query
    *** 2. Sort by highest ranking folderID/docID (docCode)
    *** 3. Return an ordered list of ['folderID/docID'] as a search result
    """

    relevantDocs = dict()
   
    print("looking for  "+query)

    #clean the query string so its alphanumeric lower for searching through the
    #inverted index
    query=(re.sub('[^\w\s+]',' ',query)).lower()

    #split the query into mutiple tokens to be search
    for term in query.split():

        # if term does not exist pass. If no terms found return null
        # if terms were found in the index
        if (term in invertedIndex):
            # look through all documents for the term.
            #each document has url and the idf score with it to use
            for docCode in invertedIndex[term]:
                docURL = comboDict[docCode[0]]

                #here we are appending all the idf score for urls found
                #if the url is in relevant doc. append the idf score for that url
                #else set the url to equal to the current idf score
                if(docURL in relevantDocs):
                
                    relevantDocs[docURL] += docCode[1][1]
                    
                else:
                    relevantDocs[docURL] = docCode[1][1]

    #sort the found documents from highest idf to lowest
    relevantDocs = sorted(relevantDocs.items(), key=lambda x: x[1], reverse=True)
    #if docs is greater the amount of urls requested reduce the list size
    if (len(relevantDocs) > x):
       relevantDocs=relevantDocs[0:x]

    return relevantDocs
    

if __name__ == "__main__":

    #    #
    # M1 #
    #    #

    # Get data from json (dict)
    comboDict = getJson('bookkeeping.json')

    # Get data from tsv (dict) & append to json data
    #json dic is in format of dict[path]:url
    comboDict.update(getTsv('bookkeeping.tsv'))

    # Write combo dict to file
    f = open('comboDict.json', 'w', encoding="UTF-8")
    f.write(json.dumps(comboDict, ensure_ascii=False))
    f.close()

    # With the large combined dict, parse through each document
    # structured as {'folderID/docID' : 'documentURL'}
    # Return an index (list of dicts of dicts)
    #   index = [{'folderID/docID' : {'term' : frequency} }]
    parseDocumentDict(comboDict)
    
    # FOR WEDNESDAY ONLY, COMMENT OUT IN PRODUCTION
    # printDocumentDict(simpleDocIndex)

    #    #
    # M2 #
    #    #

    # Search index for given query
    searchIndexUI()
    #results = searchIndex(invertedIndex, comboDict, "machine learning")
    
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
    

    
