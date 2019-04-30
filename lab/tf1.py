import tensorflow as tf
import numpy as np

x = tf.Variable(1.0)
y = tf.Variable(2.5)
f_xy = (0
    + 15 * x * x * y * y
    - 2 * x * y
    + 3 * x * x
    + 1 * y * y
    - 3 * y
    - 13 * x
)

opt = tf.train.AdamOptimizer(0.1).minimize(f_xy, var_list=[x,y])
with tf.Session() as s:
    s.run(tf.global_variables_initializer())
    for i in range(int(1e3)):
        print("f({0},{1}) = {2}".format(
            int(s.run(x)*100)/100,
            int(s.run(y)*100)/100,
            int(s.run(f_xy)*100)/100
        ))
        s.run(opt)
print('done')