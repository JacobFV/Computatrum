import time
import keyboard

import numpy as np
import tensorflow as tf

from computatrum.computer_interface import Computer_Interface
from computatrum.intelligence import Intelligence
from dreamai.encoders import Encoder, raw
from dreamai.encoders.eye import SimpleEye


computer_interface = Computer_Interface(eye=SimpleEye(retina_size=50))

o_enc_len = [enc.encoding_length() for enc in computer_interface.get_observation_encoders().values()]
a_enc_len = [enc.encoding_length() for enc in computer_interface.get_action_encoders().values()]


"""
P = tf.keras.models.Sequential([
    tf.keras.layers.Input(mem_len, o_enc_len + a_enc_len),
    tf.keras.layers.Dense(100),
    tf.keras.layers.LSTM(50),
    tf.keras.layers.LSTM(50),
    tf.keras.layers.Dense(200),
    tf.keras.layers.Dense(o_enc_len + a_enc_len)
])
C = tf.keras.models.Sequential([
    tf.keras.layers.Input(mem_len, o_enc_len + a_enc_len),
    tf.keras.layers.LSTM(100),
    tf.keras.layers.LSTM(50),
    tf.keras.layers.LSTM(20),
    tf.keras.layers.Dense(1)
])

mem_len = 10
M_tm2 = mem_len * [[cpt.get_observation(), cpt.get_action()]]
M_tm1 = mem_len * [[cpt.get_observation(), cpt.get_action()]]
M_now = mem_len * [[cpt.get_observation(), cpt.get_action()]]

d_t = None
d_tm1 = None
"""

def observe():
    return computer_interface.get_observation()
def actual_previous_action():
    return computer_interface.get_action()
def reward():
    return computer_interface.get_reward()
def punishment():
    return computer_interface.get_punishment()
def execute(decision):
    computer_interface.execute(decision)

observation_encoders = o_enc = computer_interface.get_observation_encoders()
decision_encoders = d_enc = computer_interface.get_action_encoders()
conscience_encoders = c_enc = {'reward': raw.Single_Raw_Value(), 'punishment': raw.Single_Raw_Value()}

T = 20
observations = o = (1+T) * [observe()]
decisions = d = (2+T) * [actual_previous_action()]

decider = D = Intelligence(seq_len=T, o_enc=o_enc, d_enc=d_enc, out_dec=d_enc)
predictor = P = Intelligence(seq_len=T, o_enc=o_enc, d_enc=d_enc, out_dec=o_enc)
conscience = C = Intelligence(seq_len=T, o_enc=o_enc, d_enc=d_enc, out_dec=c_enc)

steps_to_predict = T_horizon = 20
discount = eta = 0.9
def V(o, d):
    # TODO convert o, d dicts into lists of encodings
    g_cum = tf.Variable(0)
    for dt in range(T_horizon):
        d[:] = d[1:] + [D(o[:], d[:], already_encoded=True)]
        o[:] = o[1:] + [P(o[:], d[:], already_encoded=True)]
        j = C(o[:], d[:], already_encoded=True)
        g_cum = g_cum + pow(0.5, dt) * (j['reward'] - j['punishment'])
    return g_cum

fps = 5
duration = 60
pause_time = 5
ofset_time = 0
start = time.time()
for frame in range(1, fps*duration + 1):
    #wait until proper time to begin frame
    desired_time = frame * fps
    actual_time = time.time()
    wait_time = desired_time - actual_time - ofset_time
    time.sleep(max(wait_time, 0))

    print('frame', frame)

    """
        # get o_t, a_t, r_t, p_t
        o_t = cpt.get_observation()
        a_t = cpt.get_action()
        r_t = cpt.get_reward()
        p_t = cpt.get_punishment()
        g_t = r_t# - p_t

        def batch_tensorize(M: list, real=False):
            o_enc = tf.reshape(tf.Variable(initial_value=[[
                cpt.get_observation_encoders()[k].encode(v, real=real)
                for k, v in s[0]
                ] for s in M
                ]), (1, len(M), -1))
            a_enc = tf.reshape(tf.Variable(initial_value=[[
                cpt.get_action_encoders()[k].encode(v, real=real)
                for k, v in s[1]
                ] for s in M
                ]), (1, len(M), -1))
            return tf.concat(concat_dim=2, values=[o_enc, a_enc])

        def V(M):
            return 1.0

        # DUAL MODEL OBVERSO-ACTION CONSCIENCE MODEL-RL
        # ========================
        # M_t <- M_t-1 + o_t, a_t
        M_tm1[-1][1] = a_t
        M_now[:-2] = M_tm1[1:]
        M_now[-1][0] = o_t #M_now[-1][1] is technically a_t-1 because it was not overriden with the shift
        # fit P (M_t-2 (with a_t-1)) -> <o_t-1, a_t>
        P.fit(x=batch_tensorize(M_tm2), y=batch_tensorize([[M_now[-2][0], a_t]]), epochs=1)
        # if a_t != d_t-1:
        if a_t != d_tm1:
            # max V(M_t-1 (with a_t)) on theta_C
        # fit C (M_t-1 (with a_t)) -> r_t - p_t
        # decide d_t = arg d_t max V(M_t (with a_t+1 = d_t))
        d_t_enc = tf.Variable(tf.random.uniform(shape=(a_enc_len))
        M_t
        with tf.Session() as sess:

        # update M_t-2 <- M_t-1; M_t-1 <- M_t
        M_tm2 = M_tm1
        M_tm1 = M_now
        d_tm1 = d_t
    """

    # TODO include encoders in the trainable_vars

    # DECIDER PREDICTOR CONSCIENCE MODEL-RL
    # ========================
    # get o_t, a_t-1, and g_t
    o[-T-1:] = o[-T:] + [observe()]
    actual_prev_action = actual_previous_action()
    # if a_t-1 != d_t-1:
    if actual_prev_action != d[-1]:
        # train D (o_t-T-1 ... o_t-1, d_t-T-2 ... d_t-2) -> actual_prev_action
        D.fit(o[-T-1:-1], d[-T-2:-2], desired_output=actual_prev_action)
        d[-1] = actual_prev_action
    # train P (o_t-T-1 ... o_t-1, d_t-T-1 ... d_t-1) -> o_t
    P.fit(o[-T-1:-1], d[-T-1:], desired_output=o[-1], train_encoders=True)
    # train C (o_t-T-1 ... o_t-1, d_t-T-1 ... d_t-1) -> <r_t, p_t>
    reinforcement = {'reward': reward(), 'punishment': punishment()}
    C.fit(o[-T-1:-1], d[-T-1:], desired_output=reinforcement)
    # adjust theta_D to max V(o_t-T ... o_t, d_t-T-1 ... d_t-1)
    minr = tf.train.AdamOptimizer(learning_rate=0.1).minimize(loss=-tf.square(V(o[-T:], d[-T-1:]))).run()
    # decide d_t = D (o_t-T ... o_t, d_t-T-1 ... d_t-1)
    with tf.Session() as sess: decision = D(o[-T:], d[-T-1:]).eval()
    d[-T-2:] = d[-T-1:] + [D.decode(decision)]
    # execute d_t
    cpt.execute(d[-1])

    if keyboard.is_pressed('ctrl+alt+P'):
        time.sleep(pause_time)
        ofset_time += pause_time
    if keyboard.is_pressed('ctrl+alt+Q'):
        break

print('running time:', time.time() - start)