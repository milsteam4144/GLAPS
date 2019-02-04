import json
from urllib.request import urlopen
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy import MetaData
import os 

def getCensusTables():
    tablesList = []
    avgValuesList = []

    path = os.path.abspath("MinorLeague.db")
    print(path)
    #connects to DB
    engine = create_engine("sqlite:///"+path)# use direct path instead
    conn = engine.connect()
    meta = MetaData(engine, reflect = True)
    census_t = meta.tables['CensusTables']
    selectTables = census_t.select()
    res = conn.execute(selectTables)
    
    for row in res:
        tables= row[1]
        tablesList.append(tables)
    
    print(tablesList)
    
    for item in tablesList:
        avgValue=getCensusData(item)
        avgValuesList.append(avgValue)

        #Create a dictionary and input the value, zip is the key and average home value is the value             
    for item in avgValuesList:
        print(item)

def getCensusData(census_table):
    
    url = ''
    year = 2011
    #eventually get all from DB
    #census_table = "S1501_C01_018E,S1902_C01_001E,S1903_C01_001E,S1701_C01_001E" # test
    state = "37" #test
    county = "051" #test
    
    
    if census_table.startswith('S'):
        url = "https://api.census.gov/data/"+str(year)+"/acs/acs1/subject?get="+census_table+",NAME&for=county:"+county+"&in=state:"+state
    if census_table.startswith('D'):
        url = "https://api.census.gov/data/" + str(year) + "/acs/acs5/profile?get="+census_table+",NAME&for=county:"+county+"&in=state:"+state
    if census_table.startswith('B'):
        url = "https://api.census.gov/data/"+str(year)+"/acs/acs1/?get="+census_table+",NAME&for=county:"+county+"&in=state:"+state
    response = urlopen(url).read().decode('utf-8')
    responseJson = json.loads(response)
    return responseJson

getCensusTables()
    

