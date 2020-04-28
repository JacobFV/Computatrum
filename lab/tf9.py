import tensorflow as tf
import numpy as np

#a = np.random.rand(4,2)

#x = tf.placeholder(tf.float64, (4.0,2.0))
tf_b = tf.get_variable('b3454',(1))
tf_loss = tf_b * tf_b + 2

opt = tf.train.AdamOptimizer().minimize(tf_loss,var_list=tf_b)

b = 0.0

with tf.Session() as s:
    s.run(tf.global_variables_initializer())
    for _ in range(5):
        _, b = s.run([opt, tf_b], feed_dict={tf_b: b})
        print('loss:',s.run(loss, feed_dict={tf_b: b}))
        print('b:',b)
        #feed_dict = {
        #    x: [[1.0, 2.0],
        #        [4.0, 2.4],
        #        [5.3, 1.1],
        #        [0.02, 0.1]]
        #})