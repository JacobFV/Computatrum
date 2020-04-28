from Interface import Sense, Actuator
import tensorflow
import numpy as np
from sys import stdin, stdout
import random

class Special_Actuator(Actuator):
    def __init__(self, dream): self.dream = dream
    def action_vec_length(self, recalc=False):
        if recalc: self._calc_action_vec_length()
        return self.vec_length
    #def _calc_action_vec_length(self): pass

class Predictor_Fitter(Special_Actuator):

    def name(self):
        return "predictor fitter"

    def _calc_action_vec_length(self):
        self.vec_length = 2 * (
                1 #learning rate
                + 2 * self.dream.get_observation_vec_length()
                + self.dream.get_action_vec_length()
            )

    def do(self, action):
        self.dream.fit_predictor(
                epochs = int(action[0] * 10),
                o0 = action[1:1 + self.dream.get_observation_vec_length()],
                o1 = action[
                        1 + self.dream.get_observation_vec_length() :
                        1 + (2 * self.dream.get_observation_vec_length())
                    ],
                a = np.array([
                        action[1 + (2 * self.dream.get_observation_vec_length()): ],
                        np.zeros(
                                  (2 * self.action_vec_length())
                                - (2 * self.dream.get_observation_vec_length()) 
                                - self.dream.get_action_vec_length()
                                - 1
                            )
                    ]).flatten()
            )

    def log(self, action):
        return "adjusting predictor to match " + str(action)


#I may never implement this
    #but origonally it was intended to both
    # 1) fit the 'thinker' network (before dissolved)
    # 2) make 'faith' resolves w/o the minimizer knowing why
###class Fit_Decider(Special_Actuator):

    #def name(self):
        #return "fit decider"

    #def do(self, action): 
        #pass

    #def log(self, action):
        #pass


class Minimizer(Special_Actuator):

    def name(self):
        return "minimizer"

    def _calc_action_vec_length(self):
        self.vec_length = self.dream.get_observation_vec_length()

    def do(self, action): 
        self.dream.min_o_comp(action)
    
    def log(self, action):
        pass


class Punishment(Sense):

    def __init__(self, judge = Punishment.console_punishment(), size = 1):
        self.judge = judge
        self.size = size

    @staticmethod
    def console_punishment():
        return 0.5

    def name(self):
        return "punishment"

    def sense(self): 
        return np.array(self.size * [self.judge()])
    
    def vec_length(self):
        return self.size

    def log(self, observation):
        return "punishment:" + str(observation)


class Random(Sense):

    def __init__(self, size=4):
        self.size = size

    def name(self):
        return "random"

    def sense(self): 
        rnds = []
        for _ in range(self.size): rnds.append(random.random)
        return np.array(rnds)
    
    def vec_length(self):
        return self.size

    def log(self, random_value):
        return "random:" + str(random_value)


class SimpleRecurrentData(Sense, Actuator):

    def __init__(self, size=10):
        self.data = np.zeros(size)

    def sense(self): 
        return self.data
        
    def do(self, action): 
        self.data = action
    
    def observation_vec_length(self):
        return self.data.size
    
    def action_vec_length(self):
        return self.data.size

    def log_observation(self, observation):
        return self.data
        
    def log_action(self, action):
        return self.data