class Network:

    #state: list/dict [int:state] or simply state    

    def trainable_vars(self):
        raise NotImplementedError

    def __call__(self, inputs, state=None, learn=True):
        #state: recurrent state information. fed in but not out
        #learn: whether to use this as data for unsupervised learning (if applicable)
        return self.call(inputs, self.get_state_if_any(state), learn)

    def call(self, inputs, state=None, learn=True):
        #override this function in making subclass networks
        #if using state, save new state prior to returning
        return input

    def fit(self, X, Y, state=None):
        #I can use tf minimizers but if the network is a keras model, the keras.models.model.fit function may be specially optimized
        self._fit(X, Y, self.get_state_if_any(state))

    def _fit(self, X, Y, state=None):
        if state 
        #I can use tf minimizers but if the network is a keras model, the keras.models.model.fit function may be specially optimized
        raise NotImplementedError

    def get_state_if_any(self):
        raise NotImplementedError
        #NOTE: while a list or dictionary can be used to provide handles to states at previous points in time, mixing that approach does not take advantage of object-oriented programming and requires more work to dispose of old resources
        if state is None and hasattr(self, 'state'):
            if isinstance(self.state, dict):
                return self.call(inputs, self.state.values()[-1])
            elif isinstance(self.state, list):
                return self.call(inputs, self.state[-1])
            else:
                return self.call(inputs, self.state)
        else:
            return self.call(inputs, state, learn)