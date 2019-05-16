 #This checks the version of keras of the saved model

import h5py

f = h5py.File('Model_2017_4.h5', 'r')
print(f.attrs.get('keras_version'))
