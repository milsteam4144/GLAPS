"""
These classes represent objects that are rows in specific tables.
The class name should reference the table name
"""

class eduPoverty_row:
    def __init__(self, state, year, higherEdu, meanIncome, medianIncome, numPoverty):
        self.state = state
        self.year = year
        self.higherEdu = higherEdu
        self.meanIncome = meanIncome
        self.medianIncome = medianIncome
        self.numPoverty = numPoverty
        
class popTax_row:
    def __init(self, totalPop, realEstateTax):
        self.totalPop = totalPop
        self.realEstateTax = realEstateTax