print('starting')

import tensorflow as tf
import numpy as np
print('imported')

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Dense(3, activation='relu', input_shape=(3,)))
model.add(tf.keras.layers.Dense(3, activation='tanh'))
model.add(tf.keras.layers.Dense(3, activation='tanh'))
#model.add(tf.keras.layers.LSTM((,3)))
print('build')

def fit():
    def L0(yTrue, yPred):
        return tf.keras.backend.sum(yTrue - yPred)

    def L1(yTrue, yPred):
        return tf.keras.backend.sum(
            model.predict(yPred, steps=1)
        )

    model.compile(optimizer='Adam', loss=L1, metrics=['accuracy'])
    print('compiled')

    print(model.predict(np.ones((1,3))))

    data = np.random.random((5,3))
    model.fit(x=data, y=data, epochs=5)
    print(model.predict(np.ones((1,3))))
#fit()

def mnz():
    data = np.random.random((1,3))
    #may need to define x as tf.constant so its on the GPU

    print(
        model.predict(data)
    )
    #this doesn't work because it's a static number
    #L2 = tf.keras.backend.sum(
    #    model.predict(x)
    #)
    #L2 = tf calc some vec from model.predict(x)
    """modelFunc = function.Declare(
        "MF",
        [],
        [("y_out", tf.float32)]
    )  
    @function.Defun(
        tf.float32,
        func_name="MF",
        out_names=["y_out"]
    )
    def ModelFunc():
        return tf.keras.backend.sum(model.predict(x))
    ModelFunc.add_to_graph(tf.get_default_graph())
    cost = modelFunc()"""

    x = tf.placeholder(tf.float32)

    def tfModelCost(x):
        #return tf.keras.backend.sum(
        #    model.predict(x)
        #)
        xsum = tf.keras.backend.sum(
            model.predict(x)
        )
        if 7 < xsum < 7.5:
            return xsum + 10
        else:
            return xsum
    cost = tf.contrib.eager.py_func(
        func=tfModelCost,
        inp=[x],
        Tout=tf.float32
    )

    modelResult = tf.get_variable("modelResult", [1], trainable=False)

    with tf.Session() as s:
        modelResult = s.run(cost, feed_dict={
            x: np.random.random((1,3))
            })

    """
    #need to define L2 as a dynamic var (perhaps tensorflow var)
    w = model.weights
    opt = tf.train.AdamOptimizer(0.1).minimize(L2, var_list=w)
    #ERROR: no gradients supplied for any variable
    with tf.Session() as s:
        s.run(tf.global_variables_initializer())
        print(model.predict(x))
        s.run(opt)
        print(model.predict(x))
    """
mnz()
print('done')