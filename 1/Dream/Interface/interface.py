class Sense:

    def name(self):
        pass

    def sense(self): 
        pass
    
    def observation_vec_length(self):
        pass

    def log_observation(self, observation):
        return str(observation)


class Actuator:
    
    def name(self):
        pass

    def do(self, action): 
        pass
    
    def action_vec_length(self):
        pass

    def log_action(self, action):
        return str(action)