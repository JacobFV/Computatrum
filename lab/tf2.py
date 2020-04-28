import tensorflow as tf
import numpy as np
inputLayer = tf.keras.layers.Input(shape=(16, ))
outputLayer = tf.keras.layers.Dense(8, activation='softmax')(inputLayer)
model = tf.keras.models.Model(inputLayer, outputLayer)
#print(model.predict(np.random.random((1, 16))))

x=tf.placeholder(tf.float32)
z0=tf.get_variable('z', shape=(1), initializer=tf.zeros_initializer())
z1=z0+1
def costFunc(x):
    #print(x)
    #return otherFunc(x)
    #return tf.nn.softmax(tf.matmul)
    return tf.keras.backend.sum(
        inputLayer(x)
    )
    #model.predict(x)
    #does not throw a bug when I use a tensor here

def otherFunc(m):
    #xin = tf.get_variable("xin")
    #xin.assign(m)
    #r = tf.get_variable("r")
    #r.assign(model.predict(xin))
    r=m
    print (r)
    return r

tfCostFunc = tf.py_function(
    func=costFunc,
    inp=[x],
    Tout=tf.float32,
    name="tfCostFunc"
)
with tf.Session() as s:
    s.run(tfCostFunc, feed_dict={
        x: np.random.random((1,16))
        })