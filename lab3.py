# Lab 3

import json
import ijson

with open('bookkeeping.json', 'r') as fd:
    parser = ijson.parse(fd)

    for item in ijson.items():
        print(item)
