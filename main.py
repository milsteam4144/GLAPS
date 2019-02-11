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
from apis import getCountyCode, getStadiumCensusData, getRandomCensusData


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


#Upload the ZipCodes table as a Table object
zipCodes = Table('ZipCodes', metadata, autoload = True, autoload_with=engine)
censusTables = Table('CensusTables',metadata, autoload = True, autoload_with=engine)
#print(zipCodes.columns)

#The following are three tables with various attributes (columns)

class Subject_T(Base):
    
    __tablename__ = "Subject"
    year = Column('year', Integer, primary_key = True)
    stadiumName = Column('stadium', String(40), primary_key = True)
    stadiumID = Column(Integer, ForeignKey("ZipCodes.ID"), nullable=False)
    meanIncome = Column('meanIncome', Integer)
    medianIncome = Column('medianIncome', Integer)
    povertyPop = Column('povertyPop', Integer)
    medianAge = Column('medianAge', Integer)
    
    def __init__(self, year, stadiumName, stadiumID, meanIncome,medianIncome,povertyPop,medianAge):
        
        self.year = year
        self.stadiumName = stadiumName
        self.stadiumID = stadiumID
        self.meanIncome = meanIncome
        self.medianIncome = medianIncome
        self.povertyPop = povertyPop
        self.medianAge = medianAge
        
        
class Data_Profile_T(Base):
    
    __tablename__ = "Data_Profile"
    year = Column('year', Integer, primary_key = True)
    stadiumName = Column('stadium', String(40), primary_key = True)
    stadiumID = Column(Integer, ForeignKey("ZipCodes.ID"), nullable=False)
    workers = Column('workers', Integer)
    medianHouseIncome = Column('medianHouseIncome', Integer)
    medianFamilyIncome = Column('medianFamilyIncome', Integer)
    medianNonFamIncome = Column('medianNonFamIncome', Integer)
    medianWorkerIncome = Column('medianWorkerIncome', Integer)
    
    
    def __init__(self, year, stadiumName, stadiumID, \
                 workers, medianHouseIncome, medianFamilyIncome, medianNonFamIncome, medianWorkerIncome):
        
        self.year = year
        self.stadiumName = stadiumName
        self.stadiumID = stadiumID
        self.workers = workers
        self.medianHouseIncome = medianHouseIncome
        self.medianFamilyIncome = medianFamilyIncome
        self.medianNonFamIncome = medianNonFamIncome
        self.medianWorkerIncome = medianWorkerIncome
        
class Detailed_T(Base):
    
    __tablename__ = "Detailed"
    year = Column('year', Integer, primary_key = True)
    stadiumName = Column('stadium', String(40), primary_key = True)
    stadiumID = Column(Integer, ForeignKey("ZipCodes.ID"), nullable=False)
    population = Column('population', Integer)
    medianRealEstateTax = Column('medianRealEstateTax', Integer)
    medianHouseholdCosts = Column('medianHouseholdCosts', Integer)
    totalHouses = Column('totalHouses', Integer)
    medianHomeVal= Column('medianHomeVal', Integer)

    
    
    def __init__(self, year, stadiumName, stadiumID, population\
                 ,medianRealEstateTax,medianHouseholdCosts,totalHouses,medianHomeVal):
        
        self.year = year
        self.stadiumName = stadiumName
        self.stadiumID = stadiumID
        self.population = population
        self.medianRealEstateTax = medianRealEstateTax
        self.medianHouseholdCosts = medianHouseholdCosts
        self.totalHouses = totalHouses
        self.medianHomeVal = medianHomeVal
       
# Create the tables
Base.metadata.create_all(engine)
    
"""  
jimmystadium = session.query(zipCodes).filter_by(ZipCode = 48317).one() #This returns the item from the table as an object
print(jimmystadium.City) #Then you can access it's attributes directly
"""
       

# A list of years that we need data for
years = [2011, 2012, 2013, 2014, 2015, 2016, 2017]

censusList = []

for row1 in session.query(censusTables).all():
    censusList.append(row1.TableNames)
    
#print(censusList[0]+"Next:"+ censusList[1]+"Next:"+ censusList[2])


for row in session.query(zipCodes).all():
    for year in years:
        meanIncome, medianIncome, povertyPop, medianAge = getStadiumCensusData(year, row.County, row.State, censusList[0])
        new = Subject_T(year, row.Stadium, row.ID, meanIncome, medianIncome, povertyPop, medianAge)
        session.add(new)
        
        workers,medianHouseIncome,medianFamilyIncome,medianNonFamIncome,medianWorkerIncome = getStadiumCensusData(year, row.County, row.State, censusList[1])
        new = Data_Profile_T(year, row.Stadium, row.ID, workers, medianHouseIncome, medianFamilyIncome, medianNonFamIncome, medianWorkerIncome)
        session.add(new)
        
        population,medianRealEstateTax,medianHouseholdCosts,totalHouses,medianHomeVal = getStadiumCensusData(year, row.County, row.State, censusList[2])
        new = Detailed_T(year, row.Stadium, row.ID, population, medianRealEstateTax,medianHouseholdCosts,totalHouses,medianHomeVal)
        session.add(new)
    session.commit()
    session.flush()

for year in years:
    meanIncome, medianIncome, povertyPop, medianAge = getRandomCensusData(year, censusList[0])
    new = Subject_T(year, row.Stadium, row.ID, meanIncome, medianIncome, povertyPop, medianAge)
    session.add(new)
        
    workers,medianHouseIncome,medianFamilyIncome,medianNonFamIncome,medianWorkerIncome = getRandomCensusData(year,censusList[1])
    new = Data_Profile_T(year, row.Stadium, row.ID, workers, medianHouseIncome, medianFamilyIncome, medianNonFamIncome, medianWorkerIncome)
    session.add(new)
        
    population,medianRealEstateTax,medianHouseholdCosts,totalHouses,medianHomeVal = getRandomCensusData(year,censusList[2])
    new = Detailed_T(year, row.Stadium, row.ID, population, medianRealEstateTax,medianHouseholdCosts,totalHouses,medianHomeVal)
    session.add(new)
    
session.commit()
session.flush()
    
"""
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




