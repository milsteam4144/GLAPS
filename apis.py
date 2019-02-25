import requests
import json
import random 

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

