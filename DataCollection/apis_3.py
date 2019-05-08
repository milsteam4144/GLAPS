import requests
import json

'''
creates a list from the api of the County and State names as well as the codes
'''
def codesAndNames():
    allStatesandCounties = []
    state_county = ()
        
    url = requests.get("https://api.census.gov/data/2011/acs/acs1?get=NAME,B01001_001E&for=county:*&in=state:*&key=c64b663f57b72887707719c1318350c2fb6f9146")
    responseJson = list(json.loads(url.text))
    
    for item in responseJson:
        state_county = item[0],item[3],item[2]
        if item[2] != '72': # code 72 is puerto rico
            allStatesandCounties.append(state_county)
    
    allStatesandCounties.pop(0)
    
    return allStatesandCounties

'''
creates a list from the api of the various pieces of information obtained from each table set
'''
def getCensusData(year, census_table):

    #list
    TableData = []
    #list of lists
    AllCountiesData = []
       
    if census_table.startswith('B'):
        url = requests.get("https://api.census.gov/data/" + str(year) + "/acs/acs1/?get="+census_table+",NAME&for=county:*&in=state:*&key=c64b663f57b72887707719c1318350c2fb6f9146")
        responseJson = list(json.loads(url.text))
        
        #print(responseJson)

        for item in responseJson:
            TableData=[year,item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7]]
            
            if item [6] != '72':
                AllCountiesData.append(TableData)

        AllCountiesData.pop(0)
    
        return AllCountiesData

    if census_table.startswith('S'):
        url = requests.get("https://api.census.gov/data/"+str(year)+"/acs/acs1/subject?get="+census_table+",NAME&for=county:*&in=state:*&key=c64b663f57b72887707719c1318350c2fb6f9146")
        responseJson = list(json.loads(url.text))

        for item in responseJson:
            if year == 2017:
                TableData=[year,item[0],item[1],item[2],item[3],item[5],item[6],item[7]]
            else:
                TableData=[year,item[0],item[1],item[2],item[4],item[5],item[6],item[7]]
            
            if item [6] != '72':
                AllCountiesData.append(TableData)

        AllCountiesData.pop(0)
    
        return AllCountiesData

    if census_table.startswith('D'):
        url = requests.get("https://api.census.gov/data/" + str(year) + "/acs/acs1/profile?get="+census_table+",NAME&for=county:*&in=state:*&key=c64b663f57b72887707719c1318350c2fb6f9146")
        responseJson = list(json.loads(url.text))

        for item in responseJson:
            TableData=[year,item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7]]
            
            if item [6] != '72':
                AllCountiesData.append(TableData)

        AllCountiesData.pop(0)
    
        return AllCountiesData
    



