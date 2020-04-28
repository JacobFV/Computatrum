import tensorflow as tf
import dream

session = tf.Session()
with session.as_default():
    #create sensors and actuators
    #create observation abstractor, decision abstractor, decider, predictor, and conscience networks
    #create DREAM
    #run the thought loop

"""
#COPYRIGHT (C) JACOB VALDEZ 2019 ALL RIGHTS RESERVED
#YOU MAY NOT COPY ANY PART OF THIS PROGRAM FOR ANY PURPOSE WITHOUT THE EXPRESS PERMISSION OF JACOB VALDEZ
#PLEASE FOREWARD QUERRIES TO jacobfv@msn.com
import time
t0 = time.time()

import os
import sys
import traceback

import core
import vision
import computer

print('lob0 modules imported',t0-time.time())

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

VOCABULARY = ['a', 'b', 'c', 'd', 'e', ' ']
LAYER_SIZES = [20, 15, 20]

d_console, d_keyboard, d_display, d_eye = computer.Console_Interface.Create(
    buffer_size = 16,
    keys = VOCABULARY
)
u_console, u_keyboard, u_display, u_eye = computer.Console_Interface.Create(
    buffer_size = 16,
    keys = VOCABULARY
)

random = core.Random(size = 1, amplitude = 1.0)
punishment = core.Punishment(punisher = lambda : 0.5, size = 1)
#memory = core.Memory(size = 10)

predictor_fitter = core.Predictor_Fitter()
prediction_minimizer = core.Prediction_Minimizer()


dream = core.Dream(
    senses = [
        random,
        punishment,
        d_eye,
        u_eye
    ],
    actuators = [d_keyboard],
    d_layer_sizes = LAYER_SIZES,
    p_layer_sizes = LAYER_SIZES,
    predictor_fitter = predictor_fitter,
    prediction_minimizer = prediction_minimizer
)
#the following are convenience functions for CUI
def say(text):
    u_console.write_to_buffer(text)

def stop():
    pass
    #shutdown

say('`1234567890-=qwertyuiop[]\\')
print(u_console)
dream.think()
while True:
    cmd = input()
    if cmd == 'stop':
        break
    try:
        print(eval(cmd))
    except Exception:
        print(traceback.format_exc())"""
