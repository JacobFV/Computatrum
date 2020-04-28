import tensorflow as tf

"""Self-Organizing-Map:
Unsupervised learning neural layer that adjusts to allocate most neurons to the most frequent input patterns but is not affected by backpropagation.

Output activations can be based on cluster standard deviation, vector component analysis, planar datum arrangement, or additional learned distributions.

See the Wikipedia articles on "Self Organizing Map" and "Growing Self Organizing Map" for more information."""
def SOM (tf.keras.layers.Layer):

    def __init__ (
        self,
        num_outputs: int,
        sizes: [int],
        birth_rate = 0.0,
        death_rate = 0.0
    ):
        #TODO: build nodes here
        self.birth_rate = birth_rate
        self.death_rate = death_rate

    def build(self, input_shape):
        super(SOM, self).build(input_shape)

    def call(self, x):
        #TODO: return composite competitive activations

    def compute_output_shape(self, input_shape):
        return (input_shape[0], len(self.nodes)