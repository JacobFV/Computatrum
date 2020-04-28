import numpy as np
import tensorflow as tf

class Intelligence:
    
    def __init__(self, sensors, actuators):
        self.o_vec_len=0
        self.d_vec_len=0
        self.sensors=[]
        self.actuators=[]
        self.add_sensors(sensors)
        self.add_actuators(actuators)

    def __del__(self):
        pass#self.session.close()

    def think(self):
        """Public Intelligence think
            compiles a list of sensor observations o and calls the
            subclassed _think(o) -> d and then executes the decision
            tensor on appropriate actuators while remaining differentiability
            since some of these sensors and actuators may be used
            in backpropagation
            """
        observation=tf.zeros(shape=(self.o_vec_len,))
        observation
        o_index=0
        for sensor in self.sensors:
            new_o_index=o_index+sensor.o_vec_len(new=False)
            observation[o_index:new_o_index]=sensor.get_observation()
            o_index=new_o_index
        
        decision=self._think(observation)
        d_index=0
        for actuator in self.actuators:
            new_d_index=d_index+actuator.d_vec_len(self, new=False)
            actuator.execute(decision[d_index:new_d_index])
            d_index=new_d_index

    def _think(self, observation):
        """returns a decision tensor given an observation tensor.
            This is the foundation from which subclasses layer on logic just as a mighty redwood protrudes from California soil
            """
        raise NotImplementedError

    def add_sensors(self, sensors):
        for sensor in sensors:
            self.sensors.append(sensor)
            self.o_vec_len+=sensor.o_vec_len(self, new=True)

    def add_actuators(self, actuators):
        for actuator in actuators:
            self.actuators.append(actuator)
            self.d_vec_len+=actuator.d_vec_len(self, new=True)

class DREAM(Intelligence):

    O_REAL_LEN=40
    O_ABS_LEN=10
    D_INTERN_LEN=10
    D_REAL_LEN=15
    D_ABS_LEN=10

    PRED_STEPS_PER_CONF_CALC=3
    LEARNING_RATE=0.001
    NUM_MINIMIZATIONS=3

    def __init__(self, observation_abstractor, decision_abstractor, decider, predictor, conscience, sensors, actuators):
        super(DREAM, self).__init__(
            sensors=sensors,
            actuators=actuators
        )

        self.observation_abstractor=observation_abstractor
        self.decision_abstractor=decision_abstractor
        self.decider=decider
        self.predictor=predictor
        self.conscience=conscience

        self.min_confidence=0.5

        class Object(object): pass; self.past=Object()

    def _think(self, observation):
        """internal thinking function

            takes an observation and returns the decisoin made in that observation while statefully updating self.deciding_internal_state
            """
        
        observation_abstraction=self.observation_abstractor(observation)
        error=self.divergence(observation_abstraction, self.past.prediction_abstraction)
        self.predictor.fit(
            X=(self.past.observation_abstraction, self.past.decision_abstraction),
            Y=(observation_abstraction, error),
            state=self.past.predictor_state)
        self._maximize_mean_predicted_goodness(now=observation_abstraction, past=self.past)
        public_decision, private_decision = self.decider((observation_abstraction, self.past.decision_abstraction))
        decision_abstraction=self.decision_abstractor((public_decision, private_decision))
        self.conscience.fit(
            X=(observation_abstraction, decision_abstraction),
            Y=1.0)
        self.past.predictor_state=self.predictor.state
        prediction_abstraction, _ = self.predictor((observation_abstraction, decision_abstraction))
        self.past.prediction_abstraction=prediction_abstraction
        self.past.observation_abstraction=observation_abstraction
        self.past.decision_abstraction=decision_abstraction

        return public_decision

    def _maximize_mean_predicted_goodness(self, now, past):
        old_states = (self.observation_abstractor.state, self.decision_abstractor.state, self.decider.state, self.predictor.state)

        confidence=1.0
        decision_abstraction=past.decision_abstraction
        prediction_abstraction=now
        mean_predicted_goodness=0.0

        while confidence.eval()>=self.min_confidence:
            #don't want ot have to run confidence every iteration
            for _ in range(self.PRED_STEPS_PER_CONF_CALC):
                public_decision, private_decision = self.decider((prediction_abstraction, decision_abstraction))
                decision_abstraction=self.decision_abstractor((public_decision, private_decision))
                prediction_abstraction, new_confidence = self.predictor((prediction_abstraction, decision_abstraction))
                confidence*=new_confidence
                mean_predicted_goodness+=confidence*self.conscience((prediction_abstraction, decision_abstraction))
        
        #run minimizer
        badness=tf.log(1.0-mean_predicted_goodness)
        minimizer=tf.train.AdamOptimizer(learning_rate=self.LEARNING_RATE).minimize(loss=badness, var_list=self.decider.trainable_vars)
        for _ in range(self.NUM_MINIMIZATIONS):
            minimizer.run()

        self.observation_abstractor.state, self.decision_abstractor.state, self.decider.state, self.predictor.state = old_states

    @classmethod
    def divergence(cls, ideal, actual):
        #TODO: implement KL divergence
        return tf.reduce_mean(tf.pow(ideal-actual, 2.0))

class leftover_code:
    def build_networks(self):
        """builds decider and predictor networks, assigns handles to these networks in self accessible for later consumption by decide and predict, and returns an initial internal state variable to base changes from

            note:
            This function is called after Intelligence initializes, so o_vec_len and d_vec_len are fully initialized

            returns:
            initial internal state: irregularly shaped tensorflow variable used to keep track of recurrent data. See readme.md > Code > Variables > internal_state
            """
        raise NotImplementedError

    def decide(self, observation, prev_decision, internal_state, learn=False):
        """Makes decision based on current observation and previous decision

            ==========================
            Parameters:
            observation: 1 deminsional tf tensor representing current observation
            prev_decision: 1 deminsional tf tensor representing previous decision
            internal_state: irregularly shaped tensorflow variable used to keep track of recurrent data. See readme.md > Code > Variables > internal_state
            learn: whether or not the observation and decision values presented represent data from a real distribution that internal unsupervised learning (if any) should train itself on

            Returns:
            2-element tuple containing:
                0: selected decision encoded as a 1 deminsional array tensorflow operation 
                1: the new internal recurrent state expressed in an irregular data structure of tensorflow operations defined by the implementation subclass
        """
        raise NotImplementedError
    
    def predict(self, observation, decision, internal_state, learn=False):
        """Makes decision based on current observation and previous decision

            ==========================
            Parameters:
            observation: 1 deminsional tf tensor representing current observation
            decision: 1 deminsional tf tensor representing decision
            internal_state: irregularly shaped tensorflow variable used to keep track of recurrent data. See readme.md > Code > Variables > internal_state
            learn: whether or not the observation and decision values presented represent data from a real distribution that internal unsupervised learning (if any) should train itself on

            Returns:
            2-element tuple containing:
                0: the observation or abstract prediction expressed as a 1 deminsional array tensorflow operation identical in size to the observation or abstraction tensor
                1: new internal recurrent state expressed in an irregular data structure of tensorflow operations defined by the implementation subclass
        """
        raise NotImplementedError

    def fit_decider(self, observation, prev_decision, ideal_decision, internal_state, learning_rate):        
        """fits the decider such that the output of inputing observation and prev_decision into the decider with internal_state tends more towards ideal_decision

            This methods minimizes raw mean squared error with the tf Adam optimizer which is naturally slow. If subclassed model can use an custom minimizer or the keras fitting functions, they will be much faster.

            ==========================
            Parameters:
            observation: 1 deminsional tf tensor representing current observation
            prev_decision: 1 deminsional tf tensor representing previous decision
            ideal_decision: 1 deminsional tf tensor representing desired decision given the input parameters
            internal_state: irregularly shaped tensorflow variable used to keep track of recurrent data. See readme.md > Code > Variables > internal_state
            learning_rate: degree to which DREAM.decider_trainable_vars(self) are adjusted. In pure gradient descent: new_weights += learning_rate * weight_gradients. However, subclass implementations may use their own optimizers.

            Returns:
            nothing
        """
        actual_decision=self.decide(observation, prev_decision, internal_state)
        error=tf.pow(tf.reduce_mean(tf.pow(ideal_decision - actual_decision, 2.0)), 0.5)
        minimizer = tf.train.optimizers.Adam(learning_rate).minimize(self.decider_trainable_vars)
        with tf.session as session:
            minimizer.run()

    def fit_predictor(self, observation, decision, ideal_prediction, internal_state, learning_rate):
        """fits the predictor such that the output of inputing observation and decision into the predictor with internal_state tends more towards ideal_prediction

            This methods minimizes raw mean squared error with the tf Adam optimizer which is naturally slow. If subclassed model can use an custom minimizer or the keras fitting functions, they will be much faster.

            ==========================
            Parameters:
            observation: 1 deminsional tf tensor representing current observation
            decision: 1 deminsional tf tensor representing decision
            ideal_prediction: 1 deminsional tf tensor representing the ideal predictor prediction
            internal_state: irregularly shaped tensorflow variable used to keep track of recurrent data. See readme.md > Code > Variables > internal_state
            learning_rate: degree to which DREAM.predictor_trainable_vars(self) are adjusted. In pure gradient descent: new_weights += learning_rate * weight_gradients. However, subclass implementations may use their own optimizers.

            Returns:
            nothing
        """
        actual_prediction = self.predict(observation, decision, internal_state)
        error = tf.pow(tf.reduce_mean(tf.pow(ideal_prediction - actual_prediction, 2.0)), 0.5)
        minimizer = tf.train.optimizers.Adam(learning_rate).minimize(error, self.predictor_trainable_vars)
        with tf.session as session:
            minimizer.run()