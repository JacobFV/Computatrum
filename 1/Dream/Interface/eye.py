from interface import Sense, Actuator
import numpy as np


class Translator(Actuator):

    def __init__(self, sensitivity): self.sensitivity = sensitivity

    def do(self, action): self.deltify(action)
    
    #converts perpendicular bidirectional vectors into single coordinate vector
    #and applies sensitivtiy but lets subclasses implement acceleration or jerk
    def deltify(self, action):
        delta = []
        for i in action.size / 2:
            delta.append(self.sensitivity * (action[2 * i] - action[2 * i + 1]))
        self.apply_delta(delta)

    def apply_delta(self, delta): pass

    def action_vec_length(self): return 4 #each cardinal direction

class VirtualEye(Translator, Sense):

    def __init__(self, data, focus_size=(1,1), sensitivity=1):
        self.data = data
        self.focus_size = focus_size
        self.sensitivity = sensitivity
        self.limits = [0, 0]
        self.loc = [0, 0]
        super.__init__()
        for i in range(self.data.ndim):
            self.limits[i] = self.data.shape[i] - self.focus_size[i]
            self.loc[i] = self.limits[i] / 2

    def sense(self): 
        return self.data[
            self.loc[0] : self.loc[0] + self.focus_size[0],
            self.loc[1] : self.loc[1] + self.focus_size[1]
            ].flatten()

    def track_to(self, loc):
        #applies a force in that direction but doesn't instantly move
        #designed for the computer to tell the eye to track_to the mouse
        #so the cursor doesn't get lost

        #at the same time, I may not want to use this because the eye
        #should ideally have freedom to scan the screen and then return
        #to looking at whatever it wants to focus on
        pass
    
    def observation_vec_shape(self): return self.data.size

    def log_observation(self, observation):
        return "observed: ({loc[0]}, {loc[1]})".format(loc=self.loc)
    
    def apply_delta(self, delta):
        for i in range(len(delta)):
            self.loc[i] += delta[i]
            if self.loc[i] < 0: self.loc[i] = 0
            if self.loc[i] >= self.limits[i]: self.loc[i] = self.limits[i]