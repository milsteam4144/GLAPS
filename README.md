# GLAPS
Geographical Location Attribute Predictor System - Capstone Project using Python Machine Learning

GLAPS uses 2017 US Census data to predict the values of homes within a specific county dependent upon whether or not a minor/major leauge baseball stadium exists in the county. It uses a keras regression model to predict the value of a home, given the current value as well as the median value of all home within the county. 

Initially, the project's goal was to create a time-series forecasting model to predict the value of the home a specified number of years after the stadium was built. However, the US Census data did not provide enough data points for us to be able to successfully train a time-series model. In lieu of the time-series model, we created a simple regression model using the Census data from 2017 (the most recent data available at the time).



# Data Obtained from:
- U.S. Census Bureau

# Developers
- Gabriela Canjura
- Mallory Milstead

# Built with:
- Python
- SqlAlchemy
- Keras
- SQLite3

# Live Hosting:
- PythonAnywhere
- www.glaps.live




