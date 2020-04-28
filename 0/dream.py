import tensorflow as tf

class Dream:

    def __init__(self, observers, actors, nna_internal_layer_deminsions, nno_internal_layer_deminsions, nnt_internal_layer_deminsions):
        self.nna
        for d in nna_internal_layer_deminsions:
        self.nno
        for d in nno_internal_layer_deminsions:
        self.nnt
        for d in nnt_internal_layer_deminsions:


    def full_iteration(self):

    def _calc_thoughts(self):
    def _calc_actions(self):
    def _calc_predictions(self):

    #resets all LSTM memory
    def refresh(self):

    #minimizes the output of an error function of state
    def min(self, error_func):

    #minimizes the dot product of weights and state for a given amount of future state predictions
    def predictive_minimize(self, weights, depreciation, iterations):

    #restores weights to a previously declared DREAM with already defined structure
    def restore_weights_and_biases(self, filepath):
        raise NotImplementedError()

    #saves weights and biases but not structure
    def save_weights_and_biases(self, filepath):
        raise NotImplementedError()