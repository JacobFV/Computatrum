from interface import Sense, Actuator
import numpy as np

class Data_Space(Sense):

    def __init__(self, size):
        self.size = size
        self.data = np.zeros(size)
    
    def sense(self): 
        return self.data
    
    def observation_vec_length(self):
        return self.size

    def log_observation(self, observation):
        print(observation)


class Updatable:
    def update(self): pass


class Transformed_Data_Space(Updatable, Actuator, Data_Space):
    
    def __init__(self, base_data_space, transformed_size):
        self.base_data_space = base_data_space
        super.__init__(size=transformed_size)


class Translating_Actuator(Updatable, Actuator):
    
    def __init__(self, speed=1): pass



class Bounded_Translating_Actuator(Translating_Actuator):
    
    def __init__(self, translation_ranges, speed=1, loc=None):
        if loc is None: loc = np.zeros(translation_ranges)
        self.translation_ranges = translation_ranges
        self.speed = speed
        self.loc = loc
        
    def do(self, action):
        deltas = []
        for i in range(0, len(action), 2): #use self.size if NumPy arrays don't support len()
            deltas.append(action[i] - action[i+1])
        self.deltify(deltas)
        
    def deltify(self, deltas):
        for i in range(len(deltas)):
            self.loc[i] += self.speed * deltas[i]
            #constrain location
            if self.loc[i] > self.translation_ranges[i]:
                self.loc[i] = self.translation_ranges[i]
            if self.loc[i] < 0: self.loc[i] = 0
        self.update()

    def action_vec_length(self):
        #even though 1 vec/dimension is needed,
        #2 remains compatable with strictly positive output networks
        return 2 * len(self.translation_ranges)
        
    def log_action(self, action):
        message = "moved to ("
        for x in self.loc:
            message += str(x) + ", "
        return message.rstrip([',',' ']) + ")"


class Translated_Data_Space(Translating_Actuator, Transformed_Data_Space):
    
    def __init__(self, base_data_space, window_size=None, speed=1, loc=None):
        if window_size is None: window_size = base_data_space.size
        translation_ranges = []
        #for i in range(len(window_size)):
        #    translation_ranges.append(base_data_space.size[i]-window_size[i])
        for base_space_length, window_length in zip(base_data_space.size, window_size):
            translation_ranges.append(base_space_length - window_length)
        super.__init__(
            base_data_space=base_data_space,
            transformed_size=window_size,
            translation_ranges=translation_ranges,
            speed=speed,
            loc=loc
            )
    
    def update(self):
        pass
        #TODO update actual values of self.data given self.loc from self.base_data_space
        #self.data = self.base_data_space.data.subset(window_loc, window_size)
        # but this must work with n-dimensional windows


class Peripheral:

    def __init__(computer)


class Mouse(Peripheral, Translating_Actuator):
    class Listener:
        def mouse_up(self, button): pass
        def mouse_down(self, button): pass
        def mouse_move(self, delta): pass
        def wheel_rot(self, rot): pass

    listeners = []

    def __init__(computer, sensitivity):
        super.__init__(
            translation_ranges=computer.screen.data.size,
            speed=sensitivity
            )

    def update(self):
        for listener in self.listeners:
            listener.mouse_move(self.loc)


class Keyboard(Actuator):
    class Listener:
        def key_down(self, key): pass
        def key_up(self, key): pass


class Computer(Mouse.Listener, Keyboard.Listener):

    def __init__(self, peripherals):
        self.peripherals = peripherals

    def mouse_up(self, button): pass
    def mouse_down(self, button): pass
    def mouse_move(self, delta): pass
    def wheel_rot(self, rot): pass
        
    def key_down(self, key): pass
    def key_up(self, key): pass


class Display(Translated_Data_Space):

    def __init__(self, resolution):
        super.__init__(size=[resolution[0], resolution[1]])
        self.screen = np.zeros(self.size)


class Browser(Computer):
    
    def mouse_up(self, button): pass
    def mouse_down(self, button): pass
    def mouse_move(self, delta): pass
    def wheel_rot(self, rot): pass
        
    def key_down(self, key): pass
    def key_up(self, key): pass


class Linux_Container(Computer):

    def mouse_up(self, button): pass
    def mouse_down(self, button): pass
    def mouse_move(self, delta): pass
    def wheel_rot(self, rot): pass
        
    def key_down(self, key): pass
    def key_up(self, key): pass