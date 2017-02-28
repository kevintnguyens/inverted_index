# Lab 3

import json
import ijson

with open('bookkeeping.json', 'r') as fd:
    parser = ijson.parse(fd)

    for item in ijson.items():
        print(item)

#function read_tsv file for dhruti
#create a function call read_tsv that takes in a file name as a parameter.
#checs if you can read the file else return nothing
'''
 read_tsv(file_name)
    read file
    for each line
      split it such that this line
      0/132	www.ics.uci.edu/~kay/courses/31/collab.html
      is in a format that is readable for us
      you might want to use a library that readds excel file so its alot easier to store
      google opening tsv,csv for python

      once you are able to read the file.
      store the values in variables, we will figure out what to do with it later
      the values are
      0/132	www.ics.uci.edu/~kay/courses/31/collab.html
      path_1=0, path_2=132, url =www.ics.uci.edu/~kay/courses/31/collab.html
      ****make sure it is in the right format. Reject other wise. ***
      ** you can store a boolean value saying it is rejected. **
    use external library to read the tsv file in a format simaler to excel for 2.7
    for each row in the tsv file
        path1=line[0]
        path2=line[1]
        url=url
'''
