import tensorflow as tf
import numpy as np

timesteps = 5
num_inputs = 2
num_outputs = 4
batch_size = 1

x = tf.placeholder(tf.float32, [None, timesteps, num_inputs])
feed_dict = {
    x: np.random.random(size=(batch_size, timesteps, num_inputs))
}

lstmLayer, state_h, state_c = tf.keras.layers.LSTM(
    units=num_outputs,
    return_state=True,
    return_sequences=True
)(x)

with tf.Session() as s:
    s.run(tf.global_variables_initializer())

    print('h', s.run([state_h], feed_dict=feed_dict))

    x_dat, lstmLayer_dat, state_h_dat, state_c_dat = s.run(
            [x, lstmLayer, state_h, state_c],
            feed_dict=feed_dict
    )
    print('- ' * 32 + '\n')
    print('input:')
    print(x_dat)

    print('- ' * 32 + '\n')
    print('output:')
    print(lstmLayer_dat)

    print('- ' * 32 + '\n')
    print('final h:')
    print(state_h_dat)

    print('- ' * 32 + '\n')
    print('final c:')
    print(state_c_dat)

    print('- ' * 32 + '\n')
    print('h', s.run([state_h], feed_dict=feed_dict))
    print('y', s.run([lstmLayer], feed_dict=feed_dict))
    print('h', s.run([state_h], feed_dict=feed_dict))