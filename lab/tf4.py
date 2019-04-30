import tensorflow as tf
import numpy as np
L = tf.keras.layers

timesteps = 4
num_inputs = 1

print(1)
x = tf.placeholder(tf.float32, [None, timesteps, num_inputs])
feed_dict = {x: np.random.random(1, timesteps, num_inputs)}

print(2)
inputs = L.Input(batch_shape=(1, timesteps, num_inputs))
lstm1 = L.LSTM(1, stateful=True, return_sequences=True)(inputs)
outputs = L.Dense(1)(lstm1)

print(3)
with tf.Session() as s:
    s.run(tf.global_variables_initializer())
    s.run(outputs, feed_dict=feed_dict)