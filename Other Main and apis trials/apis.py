import requests
import json
import random 

def countyCodesRandom():
    allStatesandCounties = []
    state_county = ()
    selectedLocations = []
    
    i = 1
    
    url = requests.get("https://api.census.gov/data/2011/acs/acs1?get=NAME,B01001_001E&for=county:*&in=state:*&key=c64b663f57b72887707719c1318350c2fb6f9146")
    responseJson = list(json.loads(url.text))
    
    for item in responseJson:
        state_county = item[2],item[3]
        if item[2] != '72':
            allStatesandCounties.append(state_county)
    
    allStatesandCounties.pop(0)
    
    #print(allStatesandCounties)
    
    while i < 101:
       x = random.randint(1,len(allStatesandCounties))
       selectedLocations.append(allStatesandCounties[x])
       i +=1
    
    return selectedLocations 

def codesAndNames():
    allStatesandCounties = []
    state_county = ()
        
    url = requests.get("https://api.census.gov/data/2011/acs/acs1?get=NAME,B01001_001E&for=county:*&in=state:*&key=c64b663f57b72887707719c1318350c2fb6f9146")
    responseJson = list(json.loads(url.text))
    
    for item in responseJson:
        state_county = item[0],item[3],item[2]
        if item[2] != '72':
            allStatesandCounties.append(state_county)
    
    allStatesandCounties.pop(0)
    
    return allStatesandCounties

def getAllDetailedTCensusData(year, census_table):

    DetailedTableData = []
    AllCountiesDetailed = []
       
    if census_table.startswith('B'):
        url = requests.get("https://api.census.gov/data/" + str(year) + "/acs/acs1/?get="+census_table+",NAME&for=county:*&in=state:*&key=c64b663f57b72887707719c1318350c2fb6f9146")
        responseJson = list(json.loads(url.text))
        
        #print(responseJson)

        for item in responseJson:
            DetailedTableData=[item[0],item[1],item[2],item[3],item[4],item[6],item[7]]
            
            if item [6] != '72':
                AllCountiesDetailed.append(DetailedTableData)
    
    AllCountiesDetailed.pop(0)
    
    return AllCountiesDetailed

def getCensusData(year, county, state, census_table):    

    url = ''    
    if census_table.startswith('S'):
        url = requests.get("https://api.census.gov/data/"+str(year)+"/acs/acs1/subject?get="+census_table+",NAME&for=county:"+str(county)+"&in=state:"+str(state)+"&key=c64b663f57b72887707719c1318350c2fb6f9146")
        responseJson = list(json.loads(url.text))
        if year == 2017:
            return responseJson [1][0], responseJson[1][1], responseJson[1][2], responseJson[1][3]
        else:
            return responseJson [1][0], responseJson[1][1], responseJson[1][2], responseJson[1][4]
    if census_table.startswith('D'):
        url = requests.get("https://api.census.gov/data/" + str(year) + "/acs/acs1/profile?get="+census_table+",NAME&for=county:"+str(county)+"&in=state:"+str(state)+"&key=c64b663f57b72887707719c1318350c2fb6f9146")
        responseJson = list(json.loads(url.text))
        return responseJson [1][0], responseJson[1][2], responseJson[1][2],responseJson[1][3], responseJson [1][4]
    if census_table.startswith('B'):
        url = requests.get("https://api.census.gov/data/"+str(year)+"/acs/acs1/?get="+census_table+",NAME&for=county:"+str(county)+"&in=state:"+str(state)+"&key=c64b663f57b72887707719c1318350c2fb6f9146")
        responseJson = list(json.loads(url.text))
        return state, county, responseJson [1][0], responseJson[1][1], responseJson[1][2],responseJson[1][3],responseJson[1][4]
    else:
        return 0

#cumbPop = getPop(2011, "Cumberland", "North Carolina")
#print(cumbPop)

