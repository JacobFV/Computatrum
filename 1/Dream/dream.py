import tensorflow as tf
import numpy as np
import Interface.interface
import Interface.core

class Dream:

    #layers: array of JSON key, value pairs [{type:'dense/LSTM/etc.', size:int}, ... ]
    def __init__(self,
            decider_layer_sizes, predictor_layer_sizes, regular_interfaces,
            predictor_fitter, minimizer###, fit_decider
            ):
    
        self.network_vocab = {
                'predictor': 'observation',
                'decider': 'action'
            }

        self.senses = []
        self.reg_actuators = []

        self.observation_vec_length = 0
        self.action_vec_length = 0
        for interface in regular_interfaces:
            if interface is Sense:
                self.senses.append(interface)
                self.observation_vec_length += interface.observation_vec_length()
            #not 'elif' because some interface objects
            #pose as both a sense and actuator
            if interface is Actuator:
                self.reg_actuators.append(interface)
                self.action_vec_length += interface.action_vec_length()

        self.minimizer = minimizer
        self.predictor_fitter = predictor_fitter
        self.action_vec_length += self.minimizer.action_vec_length(recalc=True)
        self.action_vec_length += self.predictor_fitter.action_vec_length(recalc=True)
                    
        for network, data in self.network_vocab:
            exec(
                    """#build predictor
                    self.{0}: tf.keras.models.Sequential = 
                        tf.keras.models.Sequential([tf.keras.layers.Input(
                                self.action_vec_length + self.observation_vec_length
                            )])
                    for layer_size in self.{0}_layer_sizes:
                        self.{0}.add(tf.keras.layers.CuDNNLSTM(layer_size))
                    self.{0}.add(tf.keras.layers.CuDNNLSTM(self.{1}_vec_length))
                    self.{0}.compile(
                            optimizer='adadelta',
                            loss='sparse_categorical_crossentropy',
                            metrics=['accuracy']
                        )"""
                    .format(network, data)
                )

    #complete iteration of Dream from observation to action and training
    def think(self):
        #get observations o from all senses
        self.observation = []
        for sense in self.senses:
            #append individual sensory observations to 'observation'
            self.observation += sense.sense()

        #decide on action a
        self.action = self.decider(np.array([self.observation, self.action]).flatten())
            #MAKE SURE this action affects STM state

        #execute action on all actuators 
        # (order not important provided training predictor precedes minimization)
        actuator_index = 0
        for actuator in [self.predictor_fitter, self.minimizer] + self.reg_actuators:
            start_index = actuator_index
            actuator_index += actuator.action_vec_length()
            action_vec = self.action[start_index:actuator_index]
            actuator.do(action_vec)
            actuator.log(action_vec)

    def min_o_comp(self, o_coef, iterations, learning_rate):
        with tf.Session() as sess:
            def loss():
                #TODO get STM state of predictor & decider
                #temp_state =  
                def V(o, a, i, o_c):
                    a1 = self.decider(np.array([o, a]).flatten())
                    o1 = self.predictor(np.array([o, a1]).flatten()) #predict future
                    if i > 0: o1 += V(o1, a1, i-1, o_c) #calculate loss given predicted future
                    return o_c * o1 #only count loss that is being minimized for
                given_loss = V(
                        o = self.predictor(self.observation),
                            #predicted_observation_and_action[:self.get_observation_vec_length()],
                        a = self.decider(self.action),
                            #predicted_observation_and_action[self.get_observation_vec_length():],
                        i = 8,
                        o_c = o_coef
                    )
                #TODO reassign temp state to predictor & decider
                # = temp_state
                return given_loss
            
            #minimize with loss func on trainable vars
            min_opt = tf.train.AdadeltaOptimizer(learning_rate=learning_rate).minimize(loss,
                var_list = self.decider.trainable_weights)
            sess.run(tf.global_variables_initializer())
            for i in range(iterations):
                sess.run(min_opt)
                print('min '+(i*'#')+((iterations-i)*' ')+'{0}/{1}'.format(i,iterations))

    def fit_predictor(self, o0, a, o1, epochs: int = 5):
        assert epochs <= 10
        self.predictor.fit(
                x=np.array([o0, a]).flatten(),
                y=o1,
                epochs=epochs
            )
        
    def get_observation_vec_length(self): return self.observation_vec_length

    def get_actuator_vec_length(self): return self.action_vec_length

    #for network, data in self.network_vocab:
        #{'predictor': 'observation', 'decider': 'action'}
        #exec(
                #"""
                #    #I want to half this code below
                #"""
                #.format(network)
            #)
    
    #STM: LSTM recurrent state
    def load_STM(self, filepath):
        raise NotImplementedError()
    def save_STM(self, filepath):
        raise NotImplementedError()

    #LTM: weights and biases
    def load_LTM(self, folderpath):
        self.decider = tf.keras.models.load_model(folderpath+'\\decider.h5')
        self.predictor = tf.keras.models.load_model(folderpath+'\\predictor.h5')
    def save_LTM(self, folderpath):
        self.decider.save(folderpath+'\\decider.h5')
        self.predictor.save(folderpath+'\\predictor.h5')
        raise NotImplementedError()