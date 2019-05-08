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
#Define declarative base class
Base = declarative_base()
engine = create_engine("sqlite:///"+path, echo = False)#Set to false to git rid of log
#Link a session to the engine and initialize it
conn = engine.connect()
metadata = Base.metadata

Session = sessionmaker(bind=engine)
session = Session()

#Upload the CensusTables table as a Table object
censusTables = Table('CensusTables',metadata, autoload = True, autoload_with=engine)

#The following are three tables with various attributes (columns)
class Subject_T(Base):
    
    __tablename__ = "Subject"
    year = Column('year', Integer, primary_key = True, nullable=False)
    stateCountyName = Column('StateCountyName', String) 
    stateCode = Column('StateCode', String, primary_key=True)
    countyCode = Column('CountyCode', String, primary_key = True)
    meanIncome = Column('meanIncome', Integer)
    medianIncome = Column('medianIncome', Integer)
    povertyPop = Column('povertyPop', Integer)
    medianAge = Column('medianAge', Integer)
    
    def __init__(self, year, stateCountyName, stateCode, countyCode, meanIncome,medianIncome,povertyPop,medianAge):
        
        self.year = year
        self.stateCountyName = stateCountyName
        self.stateCode = stateCode
        self.countyCode = countyCode
        self.meanIncome = meanIncome
        self.medianIncome = medianIncome
        self.povertyPop = povertyPop
        self.medianAge = medianAge
        
        
class Data_Profile_T(Base):
    
    __tablename__ = "Data_Profile"
    year = Column('year', Integer, primary_key = True, nullable=False)
    stateCountyName = Column('StateCountyName', String) 
    stateCode = Column('StateCode', String, primary_key=True)
    countyCode = Column('CountyCode', String, primary_key = True)
    workers = Column('workers', Integer)
    medianHouseIncome = Column('medianHouseIncome', Integer)
    medianFamilyIncome = Column('medianFamilyIncome', Integer)
    medianNonFamIncome = Column('medianNonFamIncome', Integer)
    medianWorkerIncome = Column('medianWorkerIncome', Integer)
    
    
    def __init__(self, year, stateCountyName, stateCode, countyCode,\
                 workers, medianHouseIncome, medianFamilyIncome, medianNonFamIncome, medianWorkerIncome):
        
        self.year = year
        self.stateCountyName = stateCountyName
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
        stateCountyName = Column('StateCountyName', String) 
        stateCode = Column('StateCode', String, primary_key=True)
        countyCode = Column('CountyCode', String, primary_key = True)
        population = Column('population', Integer)
        medianRealEstateTax = Column('medianRealEstateTax', Integer)
        medianHouseholdCosts = Column('medianHouseholdCosts', Integer)
        totalHouses = Column('totalHouses', Integer)
        medianHomeVal= Column('medianHomeVal', Integer)

        def __init__(self, year, stateCountyName, stateCode,countyCode, population\
                 ,medianRealEstateTax,medianHouseholdCosts\
                 ,totalHouses,medianHomeVal):

            self.year = year
            self.stateCountyName = stateCountyName
            self.stateCode = stateCode
            self.countyCode = countyCode
            self.population = population
            self.medianRealEstateTax = medianRealEstateTax
            self.medianHouseholdCosts = medianHouseholdCosts
            self.totalHouses = totalHouses
            self.medianHomeVal = medianHomeVal

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

'''
Gets string of table names needed for apis
'''
censusList = []
for row1 in session.query(censusTables).all():
    censusList.append(row1.TableNames)

'''
gets a list of names and codes for all counties and states
'''
allStatesAndCounties = codesAndNames()

'''
sends the info in list above to db
'''
for item in allStatesAndCounties:
    new = StatesAndCounties_T(stateAndCounty = item[0], countyCode = item[1], stateCode = item[2])
    session.add(new)

session.commit()
session.flush()

AllDetailedCounties = []
AllSubjectCounties = []
AllDataProfilesCounties = []

'''
creates list of lists with data for all years in all counties and states
'''
for year in years:

    AllDetailedCounties.append(getCensusData(year, censusList[2]))
    AllDataProfilesCounties.append(getCensusData(year, censusList[1]))
    AllSubjectCounties.append(getCensusData(year, censusList[0]))

'''
puts data into detailed table in db
'''
for data in AllDetailedCounties:
    for item in data:
        year = item[0]
        population = item[1] 
        medianRealEstateTax = item[2]
        medianHouseholdCosts = item[3]
        totalHouses = item[4]
        stateCountyName = item[6] 
        medianHomeVal = item[5]
        stateCode = item[7]
        countyCode = item[8]

        new = Detailed_T(year, stateCountyName, stateCode, countyCode, population, medianRealEstateTax,medianHouseholdCosts,totalHouses,medianHomeVal)
        session.add(new)
   
session.commit()
session.flush()

'''
puts data into data profiles table in db
'''   
for data in AllDataProfilesCounties:
    for item in data:
        year = item[0]
        workers = item[1] 
        medianHouseIncome = item[2]
        medianFamilyIncome = item[3]
        medianNonFamIncome = item[4]
        stateCountyName = item[6] 
        medianWorkerIncome = item[5]
        stateCode = item[7]
        countyCode = item[8]

        new = Data_Profile_T(year, stateCountyName, stateCode, countyCode, workers, medianHouseIncome, medianFamilyIncome, medianNonFamIncome, medianWorkerIncome)
        session.add(new)
   
session.commit()
session.flush()

'''
puts data into subject table in db
'''

for data in AllSubjectCounties:
    for item in data:
        year = item[0]
        meanIncome = item[1] 
        medianIncome = item[2]
        povertyPop = item[3]
        medianAge = item[4]
        stateCountyName = item[5] 
        stateCode = item[6]
        countyCode = item[7]

        new = Subject_T(year, stateCountyName, stateCode, countyCode, meanIncome, medianIncome, povertyPop, medianAge)
        session.add(new)
   
session.commit()
session.flush()

