# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 13:44:15 2019

@author: canjurag4010
"""

import json
from urllib.request import urlopen
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
from apis import getAllDetailedTCensusData, codesAndNames, countyCodesRandom, getCensusData


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


#Upload the Stadiums table as a Table object
stadiums = Table('Stadiums', metadata, autoload = True, autoload_with=engine)
censusTables = Table('CensusTables',metadata, autoload = True, autoload_with=engine)
#print(stadiums.columns)

#The following are three tables with various attributes (columns)

"""
class Subject_T(Base):
    
    __tablename__ = "Subject"
    year = Column('year', Integer, primary_key = True, nullable=False)
    locationID = Column(Integer, primary_key = True, nullable=False)
    meanIncome = Column('meanIncome', Integer)
    medianIncome = Column('medianIncome', Integer)
    povertyPop = Column('povertyPop', Integer)
    medianAge = Column('medianAge', Integer)
    
    def __init__(self, year, locationID, meanIncome,medianIncome,povertyPop,medianAge):
        
        self.year = year
        self.locationID = locationID
        self.meanIncome = meanIncome
        self.medianIncome = medianIncome
        self.povertyPop = povertyPop
        self.medianAge = medianAge
        
        
class Data_Profile_T(Base):
    
    __tablename__ = "Data_Profile"
    year = Column('year', Integer, primary_key = True, nullable=False)
    locationID = Column(Integer, primary_key = True, nullable=False)
    workers = Column('workers', Integer)
    medianHouseIncome = Column('medianHouseIncome', Integer)
    medianFamilyIncome = Column('medianFamilyIncome', Integer)
    medianNonFamIncome = Column('medianNonFamIncome', Integer)
    medianWorkerIncome = Column('medianWorkerIncome', Integer)
    
    
    def __init__(self, year, locationID, \
                 workers, medianHouseIncome, medianFamilyIncome, medianNonFamIncome, medianWorkerIncome):
        
        self.year = year
        self.locationID = locationID
        self.workers = workers
        self.medianHouseIncome = medianHouseIncome
        self.medianFamilyIncome = medianFamilyIncome
        self.medianNonFamIncome = medianNonFamIncome
        self.medianWorkerIncome = medianWorkerIncome
        
class Detailed_T(Base):
    
    __tablename__ = "Detailed"
    year = Column('year', Integer, primary_key = True, nullable=False)
    locationID = Column(Integer, primary_key = True, nullable=False)
    population = Column('population', Integer)
    medianRealEstateTax = Column('medianRealEstateTax', Integer)
    medianHouseholdCosts = Column('medianHouseholdCosts', Integer)
    totalHouses = Column('totalHouses', Integer)
    medianHomeVal= Column('medianHomeVal', Integer)

    
    
    def __init__(self, year, locationID, population\
                 ,medianRealEstateTax,medianHouseholdCosts,totalHouses,medianHomeVal):
        
        self.year = year
        self.locationID = locationID
        self.population = population
        self.medianRealEstateTax = medianRealEstateTax
        self.medianHouseholdCosts = medianHouseholdCosts
        self.totalHouses = totalHouses
        self.medianHomeVal = medianHomeVal
        
class Locations(Base):
    
    __tablename__ = "Locations"
    __table_args__ = {'sqlite_autoincrement':True}
    locationID = Column(Integer, primary_key = True)
    countyCode = Column('CountyCode', String)
    stateCode = Column('StateCode', String)
    stadiumExists = Column('StadiumExists', Integer)
    
    def __init__(self, locationID, countyCode, stateCode, stadiumExists):
        
        self.locationID = locationID
        self.countyCode = countyCode
        self.stateCode = stateCode
        self.stadiumExists = stadiumExists
"""
class StatesAndCounties_T(Base):
    
    __tablename__ = "States_Counties"
    stateAndCounty = Column('StateAndCounty', String, primary_key=True)
    stateCode = Column('StateCode', String)
    countyCode = Column('CountyCode', String)

    def __init__(self, stateAndCounty, stateCode, countyCode):
        
        self.stateAndCounty = stateAndCounty
        self.stateCode = stateCode
        self.countyCode = countyCode

class Detailed_2011_T(Base):
    
    __tablename__ = "Detailed_2011"
    stateCode = Column('StateCode', String, primary_key=True)
    countyCode = Column('CountyCode', String, primary_key = True)
    population = Column('population', Integer)
    medianRealEstateTax = Column('medianRealEstateTax', Integer)
    medianHouseholdCosts = Column('medianHouseholdCosts', Integer)
    totalHouses = Column('totalHouses', Integer)
    medianHomeVal= Column('medianHomeVal', Integer)

    def __init__(self, stateCode,countyCode, population\
                 ,medianRealEstateTax,medianHouseholdCosts\
                 ,totalHouses,medianHomeVal):
        
        self.stateCode = stateCode
        self.countyCode = countyCode
        self.population = population
        self.medianRealEstateTax = medianRealEstateTax
        self.medianHouseholdCosts = medianHouseholdCosts
        self.totalHouses = totalHouses
        self.medianHomeVal = medianHomeVal

class Detailed_2014_T(Base):
    
    __tablename__ = "Detailed_2014"
    stateCode = Column('StateCode', String, primary_key=True)
    countyCode = Column('CountyCode', String, primary_key = True)
    population = Column('population', Integer)
    medianRealEstateTax = Column('medianRealEstateTax', Integer)
    medianHouseholdCosts = Column('medianHouseholdCosts', Integer)
    totalHouses = Column('totalHouses', Integer)
    medianHomeVal= Column('medianHomeVal', Integer)

    def __init__(self, stateCode,countyCode, population\
                 ,medianRealEstateTax,medianHouseholdCosts\
                 ,totalHouses,medianHomeVal):
        
        self.stateCode = stateCode
        self.countyCode = countyCode
        self.population = population
        self.medianRealEstateTax = medianRealEstateTax
        self.medianHouseholdCosts = medianHouseholdCosts
        self.totalHouses = totalHouses
        self.medianHomeVal = medianHomeVal

class Detailed_2012_T(Base):
    
    __tablename__ = "Detailed_2012"
    stateCode = Column('StateCode', String, primary_key=True)
    countyCode = Column('CountyCode', String, primary_key = True)
    population = Column('population', Integer)
    medianRealEstateTax = Column('medianRealEstateTax', Integer)
    medianHouseholdCosts = Column('medianHouseholdCosts', Integer)
    totalHouses = Column('totalHouses', Integer)
    medianHomeVal= Column('medianHomeVal', Integer)

    def __init__(self, stateCode,countyCode, population\
                 ,medianRealEstateTax,medianHouseholdCosts\
                 ,totalHouses,medianHomeVal):
        
        self.stateCode = stateCode
        self.countyCode = countyCode
        self.population = population
        self.medianRealEstateTax = medianRealEstateTax
        self.medianHouseholdCosts = medianHouseholdCosts
        self.totalHouses = totalHouses
        self.medianHomeVal = medianHomeVal

class Detailed_2013_T(Base):
    
    __tablename__ = "Detailed_2013"
    stateCode = Column('StateCode', String, primary_key=True)
    countyCode = Column('CountyCode', String, primary_key = True)
    population = Column('population', Integer)
    medianRealEstateTax = Column('medianRealEstateTax', Integer)
    medianHouseholdCosts = Column('medianHouseholdCosts', Integer)
    totalHouses = Column('totalHouses', Integer)
    medianHomeVal= Column('medianHomeVal', Integer)

    def __init__(self, stateCode,countyCode, population\
                 ,medianRealEstateTax,medianHouseholdCosts\
                 ,totalHouses,medianHomeVal):
        
        self.stateCode = stateCode
        self.countyCode = countyCode
        self.population = population
        self.medianRealEstateTax = medianRealEstateTax
        self.medianHouseholdCosts = medianHouseholdCosts
        self.totalHouses = totalHouses
        self.medianHomeVal = medianHomeVal
        
# Create the tables
Base.metadata.create_all(engine)

       
# A list of years that we need data for
years = [2011, 2012, 2013, 2014]

censusList = []
x = 0
for row1 in session.query(censusTables).all():
    censusList.append(row1.TableNames)
    
#print(censusList[0]+"Next:"+ censusList[1]+"Next:"+ censusList[2])

allStatesAndCounties = codesAndNames()

for year in years:
    AllDetailedCounties = getAllDetailedTCensusData(year, censusList[2])
    
    for item in AllDetailedCounties: 
        population = item[0] 
        medianRealEstateTax = item[1]
        medianHouseholdCosts = item[2]
        totalHouses = item[3]
        medianHomeVal = item[4]
        stateCode = item[5]
        countyCode = item[6]
        
        if year == 2011:
            new = Detailed_2011_T(stateCode, countyCode, population, medianRealEstateTax,medianHouseholdCosts,totalHouses,medianHomeVal)
    
            session.add(new)
        
        if year == 2012:
            new = Detailed_2012_T(stateCode, countyCode, population, medianRealEstateTax,medianHouseholdCosts,totalHouses,medianHomeVal)
    
            session.add(new)
        
        if year == 2013:
            new = Detailed_2013_T(stateCode, countyCode, population, medianRealEstateTax,medianHouseholdCosts,totalHouses,medianHomeVal)
    
            session.add(new)
        
        if year == 2014:
            new = Detailed_2014_T(stateCode, countyCode, population, medianRealEstateTax,medianHouseholdCosts,totalHouses,medianHomeVal)
    
            session.add(new)
            
   
    session.commit()
    session.flush() 
    

for item in allStatesAndCounties:
    new = StatesAndCounties_T(stateAndCounty = item[0], countyCode = item[1], stateCode = item[2])
    session.add(new)

session.commit()
session.flush() 

"""      
#allCounties = countyCodesRandom()

#print(allCounties)

x = 0  
for item in allCounties: 
    x += 1
    new = Locations(locationID = x, countyCode = item[1], stateCode = item[0], stadiumExists = 0)
    session.add(new)

session.commit()
session.flush()

for row in session.query(Locations).all():
    for year in years:
        meanIncome, medianIncome, povertyPop, medianAge = getCensusData(year, row.countyCode, row.stateCode, censusList[0])
        new = Subject_T(year, row.locationID,  meanIncome, medianIncome, povertyPop, medianAge)
        session.add(new)
    
        workers,medianHouseIncome,medianFamilyIncome,medianNonFamIncome,medianWorkerIncome = getCensusData(year, row.countyCode, row.stateCode, censusList[1])
        new = Data_Profile_T(year, row.locationID, workers, medianHouseIncome, medianFamilyIncome, medianNonFamIncome, medianWorkerIncome)
        session.add(new)
        
        population,medianRealEstateTax,medianHouseholdCosts,totalHouses,medianHomeVal = getCensusData(year, row.countyCode, row.stateCode, censusList[2])
        new = Detailed_T(year, row.locationID, population, medianRealEstateTax,medianHouseholdCosts,totalHouses,medianHomeVal)
        session.add(new)
    
    session.commit()
    session.flush()


    print(year, meanIncome, medianIncome, povertyPop) 
    print(year, medianHomeVal,workers,medianHouseIncome,medianFamilyIncome,medianNonFamIncome,medianWorkerIncome,medianAge)
    print(year, population,medianRealEstateTax,medianHouseholdCosts,totalHouses )       
        
        #print (row.Stadium, year, getPop(year, countyName=row.County, state = row.State))
        #new = Attributes(str(year), row.Stadium, atList[0][0],  atList[0][1],
        #atList[0][2],  atList[0][3], atList[1][0], atList[1][1], atList[1][2], atList[1][3]
        #, atList[1][4], atList[1][5], atList[1][6], atList[2][0], atList[2][1], atList[2][3])
        #session.add(new) THIS LINE AND THE ONE BELOW IT SHOULD ADD THE DATA TO A NEW TABLE CALLED "POPULATION"
        #session.commit() IT KEPT THROWING AN ERROR THAT DATABASE IS LOCKED

    #for row in session.query(zipCodes).filter_by(ZipCode= '48317').first():
    """