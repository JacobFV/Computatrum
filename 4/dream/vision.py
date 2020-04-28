#COPYRIGHT (C) JACOB VALDEZ 2019 ALL RIGHTS RESERVED
#YOU MAY NOT COPY ANY PART OF THIS PROGRAM FOR ANY PURPOSE WITHOUT THE EXPRESS PERMISSION OF JACOB VALDEZ
#PLEASE FOREWARD QUERRIES TO jacobfv@msn.com

from interfaces import Sensor, Actuator
import tensorflow as tf
import numpy as np

class Translator(Actuator):

    def __init__(
        self,
        unit_force = 1.0,
        max_speed = 2.0,
        initial_x = 0.0,
        initial_y = 0.0,
        initial_vel_x = 0.0,
        initial_vel_y = 0.0,
        bounds_x = 1.0,
        bounds_y = 1.0
    ):
        self.unit_force = unit_force
        self.max_speed = max_speed
        self.x = initial_x
        self.y = initial_y
        self.vel_x = initial_vel_x
        self.vel_y = initial_vel_y
        self.bounds_x = bounds_x
        self.bounds_y = bounds_y

    def d_vec_len(self, new):
        return 4 #in order: North, East, South, West

    def execute(self, d):
        d=d.eval()
        self.move(
            dx = d[0] - d[2], #N - S
            dy = d[1] - d[3]  #E - W
        )

    def move(self, dx, dy):
        self.vel_x += self.unit_force * dx
        self.vel_x = min([self.max_speed, self.vel_x])
        self.x += self.vel_x
        
        self.vel_y += self.unit_force * dy
        self.vel_y = min([self.max_speed, self.vel_y])
        self.y += self.vel_y

        self.tune_motion()

    def tune_motion(self):
        if self.x >= self.bounds_x:
            self.x = self.bounds_x
            self.vel_x = 0.0
        elif self.x <= 0.0:
            self.x = 0.0
            self.vel_x = 0.0

        if self.y >= self.bounds_y:
            self.y = self.bounds_y
            self.vel_y = 0.0
        elif self.y <= 0.0:
            self.y = 0.0
            self.vel_y = 0.0

        self.apply_motion()

    def apply_motion(self):
        pass

class Lookatable:
    def matrix(self) -> np.ndarray:
        raise NotImplementedError

class Eye(Sensor, Translator):

    def __init__(
        self,
        lookatable,
        viewport_size_x = 1.0,
        viewport_size_y = 1.0,
        unit_force = 1.0,
        max_speed = 2.0,
        initial_x = 0.0,
        initial_y = 0.0,
        initial_vel_x = 0.0,
        initial_vel_y = 0.0
    ):
        self.lookatable = lookatable
        self.viewport_size_x = viewport_size_x
        self.viewport_size_y = viewport_size_y
        super(Eye, self).__init__(
            unit_force = unit_force,
            max_speed = max_speed,
            initial_x = initial_x,
            initial_y = initial_y,
            initial_vel_x = initial_vel_x,
            initial_vel_y = initial_vel_y,
            bounds_x = lookatable.data.shape[0] - viewport_size_x,
            bounds_y = lookatable.data.shape[1] - viewport_size_y
        )

    def o_vec_len(self, new):
        return self.viewport_size_x * self.viewport_size_y

    def get_observation(self):
        return tf.constant(self.lookatable.data[
            round(self.x) : round(self.x) + self.viewport_size_x,
            round(self.y) : round(self.y) + self.viewport_size_y
        ].flatten())
        # NOTE
        # while this approach maps shape[0] -> x
        # and shape[1] -> y, np.ndarray's are displayed
        # inversely. 
        #
        # [[1, 2, 3],
        #  [4, 5, 6],
        #  [7, 8, 9]][1,2] = 2 (and does not equal 4)
        #
        # Just keep this in mind if an ordered
        # pair does appear where visually expected 