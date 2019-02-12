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
    
def countyCodesRandom():
    countyStateList = []
    states = []
    state_county = []
    i = 1
    
    url = requests.get("https://api.census.gov/data/2011/acs/acs1?get=NAME,B01001_001E&for=county:*&in=state:*&key=02a32d03b6dff733b0973d974df5e01c2de1daf3")
    responseJson = list(json.loads(url.text))
    #print (responseJson)

    while i<=56:
        if i == 3 or i == 7 or i == 14 or i == 43 or i == 52:
            i += 1
        states.append(i)
        i+=1
          
    for state in states:
        x = random.randint(1,300)
        
        state_county.append(state)
        state_county.append(x)
        countyStateList.append(state_county)
    
    for pair in countyStateList:
        for item in responseJson:
            while pair[0] == item[2] and pair[1] != item[3]:
                pair[1]= random.randint(1,300)
    
    for item in countyStateList:
        if int(item[1]) < 100:
            if int(item[1]) < 10:
                item[1] = '00'+str(item[1])
            else:
                item[1]= '0'+str(item[1])
        else:
            item[1] = str(item[1])
        if int(item[0]) < 10:
            item[0] = '0'+str(item[0])
        else:
            item[0] = str(item[0])

        state_county.append(item[0])
        state_county.append(item[1])
        countyStateList.append(state_county)
        
    return countyStateList
    print (countyStateList) 

def getAllCounties():
    
    allCounties = []
    
    list0 = getCountyCode()
    list1 = countyCodesRandom()
    list2 = countyCodesRandom()

    allCounties.append(list0)
    allCounties.append(list1)
    allCounties.append(list2)
        
    return allCounties
    
def getCensusData(year, county, state, census_table):    

    url = ''    
    if census_table.startswith('S'):
        url = requests.get("https://api.census.gov/data/"+str(year)+"/acs/acs1/subject?get="+census_table+",NAME&for=county:"+str(county)+"&in=state:"+str(state)+"&key=02a32d03b6dff733b0973d974df5e01c2de1daf3")
        responseJson = list(json.loads(url.text))
        if year == 2017:
            return responseJson [1][0], responseJson[1][1], responseJson[1][2], responseJson[1][3]
        elif year < 2017:
            return responseJson [1][0], responseJson[1][1], responseJson[1][2], responseJson[1][4]
        else:
            return 0
    if census_table.startswith('D'):
        url = requests.get("https://api.census.gov/data/" + str(year) + "/acs/acs5/profile?get="+census_table+",NAME&for=county:"+str(county)+"&in=state:"+str(state)+"&key=02a32d03b6dff733b0973d974df5e01c2de1daf3")
        responseJson = list(json.loads(url.text))
        return responseJson [1][0], responseJson[1][2], responseJson[1][2],responseJson[1][3], responseJson [1][4]
    else:
            return 0
    if census_table.startswith('B'):
        url = requests.get("https://api.census.gov/data/"+str(year)+"/acs/acs1/?get="+census_table+",NAME&for=county:"+str(county)+"&in=state:"+str(state)+"&key=02a32d03b6dff733b0973d974df5e01c2de1daf3")
        responseJson = list(json.loads(url.text))
        return responseJson [1][0], responseJson[1][1], responseJson[1][2],responseJson[1][3],responseJson[1][4]
    else:
        return 0

#cumbPop = getPop(2011, "Cumberland", "North Carolina")
#print(cumbPop)

