'''
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()

message = tf.constant('Hello world!')
session = tf.Session()
session.run(message)

import tensorflow as tf1
msg = tf1.constant('Hello, TensorFlow!')
tf1.print(msg)

import keras.backend as K
print(K.epsilon())

print("Num GPUs Available: ", len(tf1.config.experimental.list_physical_devices('GPU')))
'''

import os
import tensorflow as tf
import keras.backend as K

#os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
#os.environ["CUDA_VISIBLE_DEVICES"] = "0"

msg = tf.constant('Hello, TensorFlow!')
tf.print(msg)

print(K.epsilon())
print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))