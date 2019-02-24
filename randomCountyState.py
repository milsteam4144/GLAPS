# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 17:38:39 2019

@author: gmastorg
"""
import requests
import json
import random 
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy import MetaData, Table
import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean
from sqlalchemy import Index
from sqlalchemy.orm import relationship, backref
import logging
from sqlalchemy.orm import sessionmaker

def countyCodesRandom():
    allStatesandCounties = []
    state_county = ()
    selectedLocations = []
    
    i = 0
    
    url = requests.get("https://api.census.gov/data/2011/acs/acs1?get=NAME,B01001_001E&for=county:*&in=state:*&key=02a32d03b6dff733b0973d974df5e01c2de1daf3")
    responseJson = list(json.loads(url.text))
    
    for item in responseJson:
        state_county = item[2],item[3]
        allStatesandCounties.append(state_county)
    
    allStatesandCounties.pop(0)
    
    print(allStatesandCounties)
    
    while i < 50:
       x = random.randint(1,len(responseJson))
       selectedLocations.append(allStatesandCounties[x])
       i +=1
    
    print (selectedLocations) 
       
countyCodesRandom()