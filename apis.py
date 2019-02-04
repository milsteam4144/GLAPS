import requests
import json

def getCountyCode(countyName, state):
    url = requests.get("https://api.census.gov/data/2011/acs/acs1?get=NAME,B01001_001E&for=county:*&in=state:*&key=02a32d03b6dff733b0973d974df5e01c2de1daf3")
    #response = url.read().decode('utf-8')
    responseJson = list(json.loads(url.text))
    #print (len(responseJson))
    for item in list(responseJson):
        if item[0] == str(countyName) + " County, " + str(state):
            return item[3], item[2]
        #the first return is the countyCode and the second is the stateCode
    else:
        return None

def getCensusData(year,countyName,state,census_table):
    countyInfo = getCountyCode(countyName, state)
    url = ''    
    state = countyInfo[1]
    county = countyInfo[0]
    
    
    if census_table.startswith('S'):
        url = requests.get("https://api.census.gov/data/"+str(year)+"/acs/acs1/subject?get="+census_table+",NAME&for=county:"+county+"&in=state:"+state+"&key=02a32d03b6dff733b0973d974df5e01c2de1daf3")
        responseJson = list(json.loads(url.text))
        return responseJson [1][0], responseJson[1][1], responseJson[1][2]
    if census_table.startswith('D'):
        url = requests.get("https://api.census.gov/data/" + str(year) + "/acs/acs5/profile?get="+census_table+",NAME&for=county:"+county+"&in=state:"+state+"&key=02a32d03b6dff733b0973d974df5e01c2de1daf3")
        responseJson = list(json.loads(url.text))
        return responseJson [1][0], responseJson[1][2], responseJson[1][2],responseJson[1][3], responseJson [1][4], responseJson[1][5], responseJson[1][6]
    if census_table.startswith('B'):
        url = requests.get("https://api.census.gov/data/"+str(year)+"/acs/acs1/?get="+census_table+",NAME&for=county:"+county+"&in=state:"+state+"&key=02a32d03b6dff733b0973d974df5e01c2de1daf3")
        responseJson = list(json.loads(url.text))
        return responseJson [1][0], responseJson[1][1], responseJson[1][2],responseJson[1][3]
    else:
        return 0

#cumbPop = getPop(2011, "Cumberland", "North Carolina")
#print(cumbPop)

