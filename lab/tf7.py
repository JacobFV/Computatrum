from os import system
import tensorflow as tf
import numpy as np

timesteps = 5
num_inputs = 2
num_outputs = 4
batch_size = 1

x0 = np.random.random(size=(batch_size, timesteps, num_inputs))

x_in = tf.placeholder(tf.float32, [None, timesteps, num_inputs])
h_in = tf.placeholder(tf.float32, [1, num_outputs])
c_in = tf.placeholder(tf.float32, [1, num_outputs])

y_out, h_out, c_out = tf.keras.layers.LSTM(
    units=num_outputs,
    return_state=True,
    return_sequences=True
)(x_in)

with tf.Session() as s:
    s.run(tf.global_variables_initializer())
    h = [[0.] * num_outputs]
    c = [[0.] * num_outputs]
    while input('continue (y/n)') == 'y':
        feed_dict = {
            x_in: x0,
            h_in: h,
            c_in: c
        }
        h_input = h
        c_input = c
        x, y, h, c = s.run([x_in, y_out, h_out, c_out], feed_dict=feed_dict)
        system('cls')
        for v in [
            #'x[0]',
            'h_input',
            'c_input',
            #'y[0]',
            'h',
            'c']:
            print('- ' * 32 + '\n' * 2 + v)
            eval('print({0})'.format(v))
