import tensorflow as tf

class Sensor:
    def get_observation(self): pass
    def o_vec_len(self, new): pass

class Actuator:
    def execute(self, d): pass
    def d_vec_len(self, new): pass

class Random(Sensor):
    def __init__(self, size, mean=0.0, stddev=1.0):
        self.size=size
        self.mean=mean
        self.stddev=stddev
    def get_observation(self):
        return tf.random.normal(shape=(self.size,), mean=self.mean, stddev=self.stddev)
    def o_vec_len(self, new):
        return self.size

class ConsolePunishment(Sensor):
    def get_observation(self):
        return tf.Variable(1.0 if 'y' in input() else 0.0, trainable=False)
    def o_vec_len(self, new):
        return 1