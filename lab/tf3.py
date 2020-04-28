print('starting')
import tensorflow as tf
import numpy as np

x = tf.placeholder(tf.float32, [None, 5])
i = tf.keras.layers.Dense(6, input_shape=(5,))(x)
i = tf.keras.layers.Dense(16)(i)
#i = tf.keras.layers.CuDNNLSTM(16)(i)
y = tf.keras.layers.Dense(7)(i)

feed_dict = {x: np.random.random((1,5))}

with tf.Session() as s:
    s.run(tf.global_variables_initializer())
    s.run(y, feed_dict=feed_dict)