import os
import sqlalchemy
from sqlalchemy import create_engine
import pandas as pd

"""
Gets data from DB
"""
path = os.path.abspath("MinorLeague.db")
engine = create_engine("sqlite:///"+path, echo = False)#Set to false to git rid of log
#Link a session to the engine and initialize it
conn = engine.connect()

df = pd.read_sql_table('Detailed', conn)
df = df[:800]
df = df.drop(['CountyCode'], axis = 1)
df = df.drop(['Year'], axis = 1)
df['StateCode'] = pd.to_numeric(df['StateCode'],errors='coerce').fillna(0)

features = ["StateCode", "population", "medianRealEstateTax", "medianHousholdCosts",
            "totalHouses", "Target"]

#randomly takes 50% of the DB dataset and places it in train
train_data = df.sample(frac = 0.5, random_state=800)

#places remaining items in test db
test_data = df.drop(train_data.index)

# Display the Dive visualization for the training data.
from IPython.core.display import display, HTML

jsonstr = train_data.to_json(orient='records')
HTML_TEMPLATE = """<link rel="import" href="https://raw.githubusercontent.com/PAIR-code/facets/master/facets-dist/facets-jupyter.html">
        <facets-dive id="elem" height="600"></facets-dive>
        <script>
          var data = {jsonstr};
          document.querySelector("#elem").data = data;
        </script>"""
html = HTML_TEMPLATE.format(jsonstr=jsonstr)
display(HTML(html))

# Clone the facets github repo to get access to the python feature stats generation code
!git clone https://github.com/pair-code/facets.git

# Add the path to the feature stats generation code.
import sys
sys.path.insert(0, '/content/facets/facets_overview/python/')

# Create the feature stats for the datasets and stringify it.
import base64
from generic_feature_statistics_generator import GenericFeatureStatisticsGenerator

gfsg = GenericFeatureStatisticsGenerator()
proto = gfsg.ProtoFromDataFrames([{'name': 'train', 'table': train_data},
                                  {'name': 'test', 'table': test_data}])
protostr = base64.b64encode(proto.SerializeToString()).decode("utf-8")
