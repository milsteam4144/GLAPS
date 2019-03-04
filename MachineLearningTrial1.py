"""
Trial number one with Machine learning using TensorFlow
Plan on using 50 samples to train machine and 50 to test the machine
Will use Detailed Table data set and attempt to predict Median Home Value
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sqlalchemy
import time
import os
import logging
import numpy as np
import tensorflow as tf

print("Using TensorFlow version %s" % (tf.__version__))

COLUMNS = ['year','population','medianRealEsateTax', 'medianHouseholdCosts',
           'totalHouses','medianHomeVal']

import pandas as pd

path = os.path.abspath("MinorLeague.db")
engine = sqlalchemy.create_engine("sqlite:///"+path, echo = False) 
conn = engine.connect()
df = pd.read_sql_table('Detailed', conn)
df = df.drop(['CountyCode'], axis = 1)


#randomly takes half of the DB dataset and places it in train
train = df.sample(frac = 0.5, random_state=700)
train_target = train['medianHomeVal']
#places remaining items in test db
test = df.drop(train.index)

print(train_target)
print(train.head())
print(train.describe(include=[np.number]))
print(train.corr())

BATCH_SIZE = 10

def generate_input_fn(filename, batch_size=BATCH_SIZE):
    def _input_fn():
        filename_queue = tf.train.string_input_producer([filename])
        reader = tf.TextLineReader()
        key, rows = reader.read_up_to(filename_queue,
                                      num_records = batch_size)

        record_defaults = [[""],[""],[0],[0],[0],[0],[0]]

        rows = tf.expand_dims(row, axis=-1)

        # I think this needs to be changed to use the train data from pandas
        columns = tf.decode_csv(rows, record_defaults=record_defaults)

        all_columns = dict(zip(COLUMNS, columns))

        medianHomeVal = all_columns.pop('medianHomeVal')

        features = all_columns

        return features
    return _input_fn
    
print('input function configured')

from tensorflow.contrib import layers

year = layers.sparse_column_with_hash_bucket('year',
                                      hash_bucket_size=100)
                                
print('Sparse columns configured')
           
# Continuous base columns.
population = layers.real_valued_column("population")
medianRealEstateTax = layers.real_valued_column("mediaRealEstateTax")
medianHouseholdCosts = layers.real_valued_column("medianHouseholdCosts")
totalHouses = layers.real_valued_column("totalHouses")

print('continuous columns configured')


# Transformations.
year_buckets = layers.bucketized_column(
    year, boundaries=[ 2011, 2012, 2013, 2014, 2015, 2016, 2017])

print('Transformations complete')

# Wide columns and deep columns.

deep_columns = [
 population,
 medianRealEstateTax,
 medianHouseholdCosts,
 totalHouses,
]

print('deep columns configured')

from tensorflow.contrib import learn

def create_model_dir(model_type):
    return os.path.abspath('models/model_' + model_type + '_' + str(int(time.time())))

# If new_model=False, pass in the desired model_dir 
def get_model(model_type, new_model=False, model_dir=None):
    if new_model or model_dir is None:
        model_dir = create_model_dir(model_type) # Comment out this line to continue training a existing model
    print("Model directory = %s" % model_dir)
    
    m = None
    
    # Linear Classifier
    if model_type == 'WIDE':
        m = learn.LinearClassifier(
            model_dir=model_dir, 
            feature_columns=wide_columns)

    # Deep Neural Net Classifier
    if model_type == 'DEEP':
        m = learn.DNNClassifier(
            model_dir=model_dir,
            feature_columns=deep_columns,
            hidden_units=[100, 50])

    # Combined Linear and Deep Classifier
    if model_type == 'WIDE_AND_DEEP':
        m = learn.DNNLinearCombinedClassifier(
                model_dir=model_dir,
                linear_feature_columns=wide_columns,
                dnn_feature_columns=deep_columns,
                dnn_hidden_units=[100, 70, 50, 25])
        
    print('estimator built')

    return m, model_dir
    
MODEL_TYPE = 'WIDE_AND_DEEP'
model_dir = create_model_dir(model_type=MODEL_TYPE)
m, model_dir = get_model(model_type = MODEL_TYPE, model_dir=model_dir)


time 

train_file = train
# "gs://cloudml-public/census/data/adult.data.csv"
# storage.googleapis.com/cloudml-public/census/data/adult.data.csv

m.fit(input_fn=generate_input_fn(train_file, BATCH_SIZE), 
      steps=1000)

print('fit done')

test_file  = test 
# "gs://cloudml-public/census/data/adult.test.csv"
# storage.googleapis.com/cloudml-public/census/data/adult.test.csv

results = m.evaluate(input_fn=generate_input_fn(test_file), 
                     steps=200)
print('evaluate done')
print(results)
print('Accuracy: %s' % results['accuracy'])

# from here down is not working
from tensorflow.contrib.learn.python.learn.utils import input_fn_utils

def column_to_dtype(column):
    if column in CATEGORICAL_COLUMNS:
        return tf.string
    else:
        return tf.float32

def serving_input_fn():
    feature_placeholders = {
        column: tf.placeholder(column_to_dtype(column), [None])
        for column in FEATURE_COLUMNS
    }
    # DNNCombinedLinearClassifier expects rank 2 Tensors, but inputs should be
    # rank 1, so that we can provide scalars to the server
    features = {
        key: tensor[:, np.newaxis] # tf.expand_dims(tensor, axis=-1)
        for key, tensor in feature_placeholders.items()
    }
    
    return input_fn_utils.InputFnOps(
        features, # input into graph
        None,
        feature_placeholders # tensor input converted from request 
    )

export_folder = m.export_savedmodel(
    export_dir_base = model_dir+'\export',
    serving_input_fn=serving_input_fn
)

print('model exported successfully to {}'.format(export_folder))

from tensorflow.contrib.learn.python.learn import learn_runner
from tensorflow.contrib.learn.python.learn.utils import saved_model_export_utils

# output_dir is an arg passed in by the learn_runner.run() call.
def experiment_fn(output_dir):
    
    print(output_dir)
    
    train_input_fn = generate_input_fn(train_file, BATCH_SIZE)
    eval_input_fn = generate_input_fn(test_file)
    my_model, model_dir = get_model(model_type=MODEL_TYPE, 
                  model_dir=output_dir)

    experiment = tf.contrib.learn.Experiment(
        my_model,
        train_input_fn=train_input_fn,
        eval_input_fn=eval_input_fn,
        train_steps=1000
        ,
        export_strategies=[saved_model_export_utils.make_export_strategy(
            serving_input_fn,
            default_output_alternative_key=None,
            exports_to_keep=1
        )]
    )
    return experiment
# Run the experiment

model_dir=create_model_dir(model_type=MODEL_TYPE)
metrics, output_folder = learn_runner.run(experiment_fn, model_dir)

print('Accuracy: {}'.format(metrics['accuracy']))
print('Model exported to {}'.format(output_folder))

        
