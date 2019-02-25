# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 13:35:14 2019

@author: canjurag4010
"""
import requests
import json
"""
def countyCodesRandom():
    allStatesandCounties = []
    state_county = ()
    
    url = requests.get("https://api.census.gov/data/2011/acs/acs1?get=NAME,B01001_001E&for=county:*&in=state:*&key=c64b663f57b72887707719c1318350c2fb6f9146")
    responseJson = list(json.loads(url.text))
    
    print(responseJson)
    
    for item in responseJson:
        state_county = item[2],item[3]
        if item[2] != '72':
            allStatesandCounties.append(state_county)
    
    allStatesandCounties.pop(0)

countyCodesRandom()
"""
def getAllDetailedTCensusData(year, census_table):

    DetailedTableData = []
    AllCountiesDetailed = []
       
    if census_table.startswith('B'):
        url = requests.get("https://api.census.gov/data/" + str(year) + "/acs/acs1/?get="+census_table+",NAME&for=county:*&in=state:*&key=c64b663f57b72887707719c1318350c2fb6f9146")
        responseJson = list(json.loads(url.text))
        
        #print(responseJson)

        for item in responseJson:
            DetailedTableData=[item[0],item[1],item[2],item[3],item[4],item[6], item[7]]
            
            if item [6] != '72':
                AllCountiesDetailed.append(DetailedTableData)
    
    AllCountiesDetailed.pop(0)
    
    print(AllCountiesDetailed)

getAllDetailedTCensusData(2011, 'B01003_001E,B25103_001E,B25105_001E,C25075_001E,B25077_001E')