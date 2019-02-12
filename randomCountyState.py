# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 12:04:38 2019

@author: canjurag4010
"""
import requests
import json
import random 

def countyCodesRandom():
    countyStateDict = {}
    counties = []
    states = []
    i = 1
    
    url = requests.get("https://api.census.gov/data/2011/acs/acs1?get=NAME,B01001_001E&for=county:*&in=state:*&key=02a32d03b6dff733b0973d974df5e01c2de1daf3")
    responseJson = list(json.loads(url.text))
    print (responseJson)

    while i<=56:
        if i == 3 or i == 7 or i == 14 or i == 43 or i == 52:
            i += 1
        states.append(i)
        i +=1    

    for state in states:
        x = random.randint(1,300)
        
        counties.append(x)  
    
    countyStateDict = dict(zip(states,counties))
    
    for key in countyStateDict:
        for item in responseJson:
            while key == item[2] and countyStateDict[key] != item[3]:
                countyStateDict[key] = random.randint(1,300)
    
    print (countyStateDict)

countyCodesRandom()