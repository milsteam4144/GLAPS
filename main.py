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
from apis import getCountyCode, getCensusData


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
    locationID = Column(Integer, primary_key = True, nullable=False)
    stadiumName = Column('stadiumName', String(40))
    meanIncome = Column('meanIncome', Integer)
    medianIncome = Column('medianIncome', Integer)
    povertyPop = Column('povertyPop', Integer)
    medianAge = Column('medianAge', Integer)
    
    def __init__(self, year, stadiumName, locationID, meanIncome,medianIncome,povertyPop,medianAge):
        
        self.year = year
        self.stadiumName = stadiumName
        self.locationID = locationID
        self.meanIncome = meanIncome
        self.medianIncome = medianIncome
        self.povertyPop = povertyPop
        self.medianAge = medianAge
        
        
class Data_Profile_T(Base):
    
    __tablename__ = "Data_Profile"
    year = Column('year', Integer, primary_key = True, nullable=False)
    locationID = Column(Integer, primary_key = True, nullable=False)
    stadiumName = Column('stadium', String(40))
    workers = Column('workers', Integer)
    medianHouseIncome = Column('medianHouseIncome', Integer)
    medianFamilyIncome = Column('medianFamilyIncome', Integer)
    medianNonFamIncome = Column('medianNonFamIncome', Integer)
    medianWorkerIncome = Column('medianWorkerIncome', Integer)
    
    
    def __init__(self, year, stadiumName, locationID, \
                 workers, medianHouseIncome, medianFamilyIncome, medianNonFamIncome, medianWorkerIncome):
        
        self.year = year
        self.stadiumName = stadiumName
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
    stadiumName = Column('stadium', String(40))
    population = Column('population', Integer)
    medianRealEstateTax = Column('medianRealEstateTax', Integer)
    medianHouseholdCosts = Column('medianHouseholdCosts', Integer)
    totalHouses = Column('totalHouses', Integer)
    medianHomeVal= Column('medianHomeVal', Integer)

    
    
    def __init__(self, year, stadiumName, locationID, population\
                 ,medianRealEstateTax,medianHouseholdCosts,totalHouses,medianHomeVal):
        
        self.year = year
        self.stadiumName = stadiumName
        self.locationID = locationID
        self.population = population
        self.medianRealEstateTax = medianRealEstateTax
        self.medianHouseholdCosts = medianHouseholdCosts
        self.totalHouses = totalHouses
        self.medianHomeVal = medianHomeVal
        
class Locations(Base):
    
    __tablename__ = "Locations"
    locationID = Column(Integer, primary_key = True, nullable=False)
    countyCode = Column('CountyCode', Integer)
    stateCode = Column('StateCode', Integer)
    stadiumExists = Column('StadiumExists', Integer)
    
    def __init__(self, locationID, countyCode, stateCode, stadiumExists):
        
        self.locationID = locationID
        self.countyCode = countyCode
        self.stateCode = stateCode
        self.stadiumExists = stadiumExists
       
# Create the tables
Base.metadata.create_all(engine)
    
"""  
jimmystadium = session.query(stadiums).filter_by(ZipCode = 48317).one() #This returns the item from the table as an object
print(jimmystadium.City) #Then you can access it's attributes directly
"""
       

# A list of years that we need data for
years = [2011, 2012, 2013, 2014, 2015, 2016, 2017]

censusList = []

for row1 in session.query(censusTables).all():
    censusList.append(row1.TableNames)
    
#print(censusList[0]+"Next:"+ censusList[1]+"Next:"+ censusList[2])


for row in session.query(stadiums).all():
    for year in years:
        
        #Add Locations objects to Locations table
        #variables = function(parameters)
        new = Locations(locationID = NULL, countyCode, stateCode, stadiumExists)
        session.add(new)
        
        meanIncome, medianIncome, povertyPop, medianAge = getCensusData(year, row.County, row.State, censusList[0])
        new = Subject_T(year, row.StadiumName, row.ID, meanIncome, medianIncome, povertyPop, medianAge)
        session.add(new)
        
        workers,medianHouseIncome,medianFamilyIncome,medianNonFamIncome,medianWorkerIncome = getCensusData(year, row.County, row.State, censusList[1])
        new = Data_Profile_T(year, row.StadiumName, row.ID, workers, medianHouseIncome, medianFamilyIncome, medianNonFamIncome, medianWorkerIncome)
        session.add(new)
        
        population,medianRealEstateTax,medianHouseholdCosts,totalHouses,medianHomeVal = getCensusData(year, row.County, row.State, censusList[2])
        new = Detailed_T(year, row.StadiumName, row.ID, population, medianRealEstateTax,medianHouseholdCosts,totalHouses,medianHomeVal)
        session.add(new)
    session.commit()
    session.flush()

    
    #for row in session.query(stadiums).filter_by(ZipCode= '48317').first():





