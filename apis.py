import requests
import json
import random 

"""
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
    
    stadiumCountyStateCodes = []
    state_county=[]
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


    #Upload the stadiums table as a Table object
    stadiums = Table('Stadiums', metadata, autoload = True, autoload_with=engine)


    url = requests.get("https://api.census.gov/data/2011/acs/acs1?get=NAME,B01001_001E&for=county:*&in=state:*&key=02a32d03b6dff733b0973d974df5e01c2de1daf3")
    #response = url.read().decode('utf-8')
    responseJson = list(json.loads(url.text))
    
    for row in session.query(stadiums).all():  
        for item in list(responseJson):
            if item[0] == str(row.County) + " County, " + str(row.State):
                state_county.append(item[2])
                state_county.append(item[3])
                stadiumCountyStateCodes.append(state_county)
    
    return stadiumCountyStateCodes
    print(stadiumCountyStateCodes)
"""
def countyCodesRandom():
    allStatesandCounties = []
    state_county = ()
    selectedLocations = []
    
    i = 1
    
    url = requests.get("https://api.census.gov/data/2011/acs/acs1?get=NAME,B01001_001E&for=county:*&in=state:*&key=02a32d03b6dff733b0973d974df5e01c2de1daf3")
    responseJson = list(json.loads(url.text))
    
    for item in responseJson:
        state_county = item[2],item[3]
        allStatesandCounties.append(state_county)
    
    allStatesandCounties.pop(0)
    
    #print(allStatesandCounties)
    
    while i < 101:
       x = random.randint(1,len(responseJson))
       selectedLocations.append(allStatesandCounties[x])
       i +=1
    
    return selectedLocations 

def codesAndNames():
    allStatesandCounties = []
    state_county = ()
        
    url = requests.get("https://api.census.gov/data/2011/acs/acs1?get=NAME,B01001_001E&for=county:*&in=state:*&key=02a32d03b6dff733b0973d974df5e01c2de1daf3")
    responseJson = list(json.loads(url.text))
    
    for item in responseJson:
        state_county = item[0],item[3],item[2]
        allStatesandCounties.append(state_county)
    
    allStatesandCounties.pop(0)
    
    return allStateandCounties

def getCensusData(year, county, state, census_table):    

    url = ''    
    if census_table.startswith('S'):
        url = requests.get("https://api.census.gov/data/"+str(year)+"/acs/acs1/subject?get="+census_table+",NAME&for=county:"+str(county)+"&in=state:"+str(state)+"&key=02a32d03b6dff733b0973d974df5e01c2de1daf3")
        responseJson = list(json.loads(url.text))
        if year == 2017:
            return responseJson [1][0], responseJson[1][1], responseJson[1][2], responseJson[1][3]
        else:
            return responseJson [1][0], responseJson[1][1], responseJson[1][2], responseJson[1][4]
    if census_table.startswith('D'):
        url = requests.get("https://api.census.gov/data/" + str(year) + "/acs/acs5/profile?get="+census_table+",NAME&for=county:"+str(county)+"&in=state:"+str(state)+"&key=02a32d03b6dff733b0973d974df5e01c2de1daf3")
        responseJson = list(json.loads(url.text))
        return responseJson [1][0], responseJson[1][2], responseJson[1][2],responseJson[1][3], responseJson [1][4]
    if census_table.startswith('B'):
        url = requests.get("https://api.census.gov/data/"+str(year)+"/acs/acs1/?get="+census_table+",NAME&for=county:"+str(county)+"&in=state:"+str(state)+"&key=02a32d03b6dff733b0973d974df5e01c2de1daf3")
        responseJson = list(json.loads(url.text))
        return responseJson [1][0], responseJson[1][1], responseJson[1][2],responseJson[1][3],responseJson[1][4]
    else:
        return 0

#cumbPop = getPop(2011, "Cumberland", "North Carolina")
#print(cumbPop)

