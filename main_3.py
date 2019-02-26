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
from sqlalchemy.orm import relationship, backref, mapper
import logging
from sqlalchemy.orm import sessionmaker
from apis_3 import getCensusData, codesAndNames


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

class Subject_T(Base):
    
    __tablename__ = "Subject"
    year = Column('year', Integer, primary_key = True, nullable=False)
    stateCode = Column('StateCode', String, primary_key=True)
    countyCode = Column('CountyCode', String, primary_key = True)
    meanIncome = Column('meanIncome', Integer)
    medianIncome = Column('medianIncome', Integer)
    povertyPop = Column('povertyPop', Integer)
    medianAge = Column('medianAge', Integer)
    
    def __init__(self, year, stateCode, countyCode, meanIncome,medianIncome,povertyPop,medianAge):
        
        self.year = year
        self.stateCode = stateCode
        self.countyCode = countyCode
        self.meanIncome = meanIncome
        self.medianIncome = medianIncome
        self.povertyPop = povertyPop
        self.medianAge = medianAge
        
        
class Data_Profile_T(Base):
    
    __tablename__ = "Data_Profile"
    year = Column('year', Integer, primary_key = True, nullable=False)
    stateCode = Column('StateCode', String, primary_key=True)
    countyCode = Column('CountyCode', String, primary_key = True)
    workers = Column('workers', Integer)
    medianHouseIncome = Column('medianHouseIncome', Integer)
    medianFamilyIncome = Column('medianFamilyIncome', Integer)
    medianNonFamIncome = Column('medianNonFamIncome', Integer)
    medianWorkerIncome = Column('medianWorkerIncome', Integer)
    
    
    def __init__(self, year, stateCode, countyCode,\
                 workers, medianHouseIncome, medianFamilyIncome, medianNonFamIncome, medianWorkerIncome):
        
        self.year = year
        self.stateCode = stateCode
        self.countyCode = countyCode
        self.workers = workers
        self.medianHouseIncome = medianHouseIncome
        self.medianFamilyIncome = medianFamilyIncome
        self.medianNonFamIncome = medianNonFamIncome
        self.medianWorkerIncome = medianWorkerIncome
        
class Detailed_T(Base):
    
        __tablename__ = 'Detailed'
        year = Column('Year', Integer, primary_key=True)
        stateCode = Column('StateCode', String, primary_key=True)
        countyCode = Column('CountyCode', String, primary_key = True)
        population = Column('population', Integer)
        medianRealEstateTax = Column('medianRealEstateTax', Integer)
        medianHouseholdCosts = Column('medianHouseholdCosts', Integer)
        totalHouses = Column('totalHouses', Integer)
        medianHomeVal= Column('medianHomeVal', Integer)

        def __init__(self, year, stateCode,countyCode, population\
                 ,medianRealEstateTax,medianHouseholdCosts\
                 ,totalHouses,medianHomeVal):

            self.year = year
            self.stateCode = stateCode
            self.countyCode = countyCode
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

class StatesAndCounties_T(Base):
    
    __tablename__ = "States_Counties"
    stateAndCounty = Column('StateAndCounty', String, primary_key=True)
    stateCode = Column('StateCode', String)
    countyCode = Column('CountyCode', String)

    def __init__(self, stateAndCounty, stateCode, countyCode):
        
        self.stateAndCounty = stateAndCounty
        self.stateCode = stateCode
        self.countyCode = countyCode

# Create the tables
Base.metadata.create_all(engine)

# A list of years that we need data for
years = [2011, 2012, 2013, 2014, 2015, 2016, 2017]

censusList = []
for row1 in session.query(censusTables).all():
    censusList.append(row1.TableNames)

#print(censusList[0]+"Next:"+ censusList[1]+"Next:"+ censusList[2])

allStatesAndCounties = codesAndNames()

for item in allStatesAndCounties:
    new = StatesAndCounties_T(stateAndCounty = item[0], countyCode = item[1], stateCode = item[2])
    session.add(new)

session.commit()
session.flush()

x = 0  
for item in allStatesAndCounties: 
    x += 1
    new = Locations(locationID = x, countyCode = item[1], stateCode = item[2], stadiumExists = 0)
    session.add(new)

session.commit()
session.flush()

AllDetailedCounties = []
AllSubjectCounties = []
AllDataProfilesCounties = []

for year in years:

    AllDetailedCounties.append(getCensusData(year, censusList[2]))
    AllDataProfilesCounties.append(getCensusData(year, censusList[1]))
    AllSubjectCounties.append(getCensusData(year, censusList[0]))
    
for data in AllDetailedCounties:
    for item in data:
        year = item[0]
        population = item[1] 
        medianRealEstateTax = item[2]
        medianHouseholdCosts = item[3]
        totalHouses = item[4]
        medianHomeVal = item[5]
        stateCode = item[6]
        countyCode = item[7]

        new = Detailed_T(year, stateCode, countyCode, population, medianRealEstateTax,medianHouseholdCosts,totalHouses,medianHomeVal)
        session.add(new)
   
session.commit()
session.flush()
   
for data in AllDataProfilesCounties:
    for item in data:
        year = item[0]
        workers = item[1] 
        medianHouseIncome = item[2]
        medianFamilyIncome = item[3]
        medianNonFamIncome = item[4]
        medianWorkerIncome = item[5]
        stateCode = item[6]
        countyCode = item[7]

        new = Data_Profile_T(year, stateCode, countyCode, workers, medianHouseIncome, medianFamilyIncome, medianNonFamIncome, medianWorkerIncome)
        session.add(new)
   
session.commit()
session.flush()

for data in AllSubjectCounties:
    for item in data:
        year = item[0]
        meanIncome = item[1] 
        medianIncome = item[2]
        povertyPop = item[3]
        medianAge = item[4]
        stateCode = item[5]
        countyCode = item[6]

        new = Subject_T(year, stateCode, countyCode, meanIncome, medianIncome, povertyPop, medianAge)
        session.add(new)
   
session.commit()
session.flush()

