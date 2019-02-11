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

def getCountyCode():
    
    stadiumCountyStateCodes = {}
    
    path = os.path.abspath("MinorLeague.db")
    #dir_path = os.path.dirname(os.path.realpath("/MinorLeague/MinorLeague.db"))
    #Define declarative base class
    Base = declarative_base()
    engine = create_engine("sqlite:///"+path, echo = False)#Set to false to git rid of log
    #Link a session to the engine and initialize it
    conn = engine.connect()
    metadata = Base.metadata


    Session = sessionmaker(bind=engine)
    session = Session()


    #Upload the ZipCodes table as a Table object
    zipCodes = Table('ZipCodes', metadata, autoload = True, autoload_with=engine)


    url = requests.get("https://api.census.gov/data/2011/acs/acs1?get=NAME,B01001_001E&for=county:*&in=state:*&key=02a32d03b6dff733b0973d974df5e01c2de1daf3")
    #response = url.read().decode('utf-8')
    responseJson = list(json.loads(url.text))
    
    for row in session.query(zipCodes).all():  
        for item in list(responseJson):
            if item[0] == str(row.County) + " County, " + str(row.State):
                stadiumCountyStateCodes[item[2]]=item[3]
                return stadiumCountyStateCodes

def countyCodesRandom():
    countyStateDict = {}
    counties = []
    states = []
    i = 1
    
    url = requests.get("https://api.census.gov/data/2011/acs/acs1?get=NAME,B01001_001E&for=county:*&in=state:*&key=02a32d03b6dff733b0973d974df5e01c2de1daf3")
    responseJson = list(json.loads(url.text))
    #print (responseJson)

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
    
    return countyStateDict
    #print (countyStateDict)
"""    
def getStadiumCensusData(year,countyName,state,census_table):
    countyInfo = getCountyCode(countyName, state)
    url = ''    
    state = countyInfo[1]
    county = countyInfo[0]
    
    
    if census_table.startswith('S'):
        url = requests.get("https://api.census.gov/data/"+str(year)+"/acs/acs1/subject?get="+census_table+",NAME&for=county:"+county+"&in=state:"+state+"&key=02a32d03b6dff733b0973d974df5e01c2de1daf3")
        responseJson = list(json.loads(url.text))
        if year == 2017:
            return responseJson [1][0], responseJson[1][1], responseJson[1][2], responseJson[1][3]
        else:
            return responseJson [1][0], responseJson[1][1], responseJson[1][2], responseJson[1][4]
    if census_table.startswith('D'):
        url = requests.get("https://api.census.gov/data/" + str(year) + "/acs/acs5/profile?get="+census_table+",NAME&for=county:"+county+"&in=state:"+state+"&key=02a32d03b6dff733b0973d974df5e01c2de1daf3")
        responseJson = list(json.loads(url.text))
        return responseJson [1][0], responseJson[1][2], responseJson[1][2],responseJson[1][3], responseJson [1][4]
    if census_table.startswith('B'):
        url = requests.get("https://api.census.gov/data/"+str(year)+"/acs/acs1/?get="+census_table+",NAME&for=county:"+county+"&in=state:"+state+"&key=02a32d03b6dff733b0973d974df5e01c2de1daf3")
        responseJson = list(json.loads(url.text))
        return responseJson [1][0], responseJson[1][1], responseJson[1][2],responseJson[1][3],responseJson[1][4]
    else:
        return 0
"""
    
def getCensusData(year, census_table, countiesDict):    
    
    allCounties  = {}
    allCounties.append(getCountyCode())
    allCounties.append(countyCodesRandom())
    allCounties.append(countyCodesRandom())
    url = ''    
  
    for key in allCounties:
        if census_table.startswith('S'):
            url = requests.get("https://api.census.gov/data/"+str(year)+"/acs/acs1/subject?get="+census_table+",NAME&for=county:"+allCounties[key]+"&in=state:"+key+"&key=02a32d03b6dff733b0973d974df5e01c2de1daf3")
            responseJson = list(json.loads(url.text))
            if year == 2017:
                return responseJson [1][0], responseJson[1][1], responseJson[1][2], responseJson[1][3]
            else:
                return allCounties[key], key, responseJson [1][0], responseJson[1][1], responseJson[1][2], responseJson[1][4]
        if census_table.startswith('D'):
            url = requests.get("https://api.census.gov/data/" + str(year) + "/acs/acs5/profile?get="+census_table+",NAME&for=county:"+allCounties[key]+"&in=state:"+key+"&key=02a32d03b6dff733b0973d974df5e01c2de1daf3")
            responseJson = list(json.loads(url.text))
            return allCounties[key], key, responseJson [1][0], responseJson[1][2], responseJson[1][2],responseJson[1][3], responseJson [1][4]
        if census_table.startswith('B'):
            url = requests.get("https://api.census.gov/data/"+str(year)+"/acs/acs1/?get="+census_table+",NAME&for=county:"+allCounties[key]+"&in=state:"+key+"&key=02a32d03b6dff733b0973d974df5e01c2de1daf3")
            responseJson = list(json.loads(url.text))
            return allCounties[key], key, responseJson [1][0], responseJson[1][1], responseJson[1][2],responseJson[1][3],responseJson[1][4]
        else:
            return 0

#cumbPop = getPop(2011, "Cumberland", "North Carolina")
#print(cumbPop)

