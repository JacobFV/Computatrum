import tensorflow as tf
import numpy as np
L = tf.keras.layers

timesteps = 10
num_inputs = 2
num_outputs = 3

x = tf.placeholder(tf.float32, [None, timesteps, num_inputs])
feed_dict = {
    x:
        np.array([
            [0., 0.],
            [.9, 0.],
            [0., 0.],
            [0., 0.],
            [0., 0.],
            [0., 0.],
            [0., 0.],
            [0., 0.],
            [0., 0.],
            [0., 0.],
        ])
        #np.random.random((1, timesteps, num_inputs))
        .reshape((1, timesteps, num_inputs))
    
    }

#inputLayer = L.Input(dtype=float, batch_shape=(1,timesteps, num_inputs))
lstm1 = L.LSTM(
    num_outputs,
    stateful=False,
    return_sequences=True,
    input_shape=(timesteps,1)
    )(x)
lstm2 = L.LSTM(
    num_outputs,
    stateful=False,
    return_sequences=True,
    input_shape=(timesteps,1)
    )(lstm1)
lstm3 = L.LSTM(
    num_outputs,
    stateful=False,
    return_sequences=True,
    input_shape=(timesteps,1)
    )(lstm2)
lstm4 = L.LSTM(
    num_outputs,
    stateful=False,
    return_sequences=True,
    input_shape=(timesteps,1)
    )(lstm3)
y = lstm4

error = tf.keras.backend.sum(
        y - 0
    )
#outputs = L.Dense(1)(lstm1)

for _ in range(1):
    with tf.Session() as s:
        s.run(tf.global_variables_initializer())
        x, y = s.run([x, y], feed_dict=feed_dict)
        index = 0
        for xi, yi in zip(x[0], y[0]):
            print(
                't:' + str(index),
                'x:', xi,
                'y:', yi
            )
            index+=1
    #for i in range(timesteps):
        #print(i)
        #print(s.run(lstm1, feed_dict=feed_dict))