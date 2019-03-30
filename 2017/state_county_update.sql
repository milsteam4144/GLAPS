UPDATE all_3_Data
SET State_Cty = (SELECT StateAndCounty
FROM States_Counties
WHERE States_Counties.CountyCode = all_3_Data.CountyCode
AND States_Counties.StateCode = all_3_Data.StateCode);