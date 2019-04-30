import tensorflow as tf
import numpy as np

from os import system

timesteps = 5
num_inputs = 2
num_outputs = 4
batch_size = 1

tf_x = tf.placeholder(tf.float32, [None, timesteps, num_inputs])
L = tf.keras.layers.LSTM(
    units=num_outputs,
    return_state=True,
    return_sequences=True
)
tf_y, tf_h, tf_c = L(tf_x)

with tf.Session() as s:
    x = np.array([[
        [.0, .0],
        [.3, .1],
        [.0, .0],
        [.0, .0],
        [.1, .0]
    ]])
    h = np.array([[.0, .0, .1, .0]])
    c = np.array([[.0, .1, .0, .0]])

    s.run(tf.global_variables_initializer())
    while input('continue? (y/n)') == 'y':
        L.states[0] = h #these assignment operations
        L.states[1] = c #don't do anything
        #I can still take advantage of tensorflow's
        #gpu usage, but I will have to write my own
        #LSTM network

        y, h, c = s.run(
            [tf_y, tf_h, tf_c],
            feed_dict={
                tf_x: x
        })

        #system('cls')
        for v in ['y[0][0]', 'y[0][4]', 'h[0]', 'c[0]']:
            print('- ' * 32)
            print(v + ':')
            print(eval(v))