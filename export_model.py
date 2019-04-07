import keras
from keras.layers import *
import tensorflow as tf
from keras.models import load_model
import os

# gets the path for the model
path = os.path.abspath('model_2017_4.h5')

# loads the model
model = load_model(path)

model_builder = tf.saved_model.builder.SavedModelBuilder("exported_model")

inputs = {
    'input': tf.saved_model.utils.build_tensor_info(model.input)
}
print(inputs)
outputs = {
    'housing': tf.saved_model.utils.build_tensor_info(model.output)
}
print(outputs)
signature_def=tf.saved_model.signature_def_utils.build_signature_def(
    inputs=inputs,
    outputs=outputs,
    method_name=tf.saved_model.signature_constants.PREDICT_METHOD_NAME
)

model_builder.add_meta_graph_and_variables(
    K.get_session(),
    tags=[tf.saved_model.tag_constants.SERVING],
    signature_def_map={
        tf.saved_model.signature_constants.DEFAULT_SERVING_SIGNATURE_DEF_KEY:signature_def
    }
)

model_builder.save()