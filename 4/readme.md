DREAM
=======

> Strong AI is near

## Overview

The Delayed Reinforcment Executive Action Model or DREAM is a general purpose artificial intelligence system.


## Project

- Define DREAM
- Program system
- Collect supervised training set
- Develop cirriculum
- Build robot
- Supervise free world exploration / interaction

## Operation

## Design
DREAM operates under the assumption that after making an observation of an environment and performing an action, a prediction can be made of what a future observation will be. Some these observations can be a green check mark, a raw numeric value, or a written 'correct'. DREAM percieves some of these observations as rewarding, others as neutral, and others as negative - and not necesarily in hard-cut classes, but with a range of aversion to pleasure. Since DREAM learns to predict observations at future points in time given its observations and actions in previous points in time, DREAM selects decisions in a way to maximize its predicted future reward. Since DREAM is farsighted in this way, it is willing to make 'sacrifices' if it forsees the total sum of that course of action to be greator than an immediantly rewarding action.

### Algorithm

<pre>
<b>think:</b>  
get <b>o</b><sub>t</sub>
<b>a</b><sub>t</sub> &larr; A<sub>s<sub>real</sub></sub>(<b>o</b><sub>t</sub>)
fit<sub>&theta;<sub>P</sub></sub> P()
</pre>

Where  
<code><b>o</b><sub>t</sub></code> &isin; &Ropf;<sup>N<sub><b>o</b></sub></sup>. Raw sensory input or observation at time `t`  
<code><b>a</b><sub>t</sub></code> is an abstract encoding of <code><b>o</b><sub>t</sub></code>  
<code><b>d</b><sub>t</sub></code> is the decision made at time `t` given <code><b>a</b><sub>t</sub></code>  
<code><b>p</b><sub>t</sub></code> is a prediction of <code><b>a</b><sub>t+1</sub></code>  
<code>g<sub>t</sub></code> is evaluation of the goodness or desireability of any abstract observation encoding <code><b>a</b><sub>t</sub></code>  
<code>&Ascr;</code> the abstractor; unsupervised information abstraction module   
<code>&Dscr;</code> the decider; makes a decision given the current abstract state encoding and previous decision made  
<code>&Pscr;</code> the predictor; predicts a new abstract state encoding given the current abstract state encoding and decision made in that state  
<code>&Cscr;</code> the conscience; evaluates the desirability of a situation as anywhere between good `+1` or bad `-1`  
<code>&Fscr;<sub>s<sub>t</sub>&rarr;s<sub>t+1</sub></sub>(<b>X</b>) &rarr; <b>Y</b></code> denotes the output of a stateful function such as a neural network where an input <code><b>X</b></code> is mapped to an output <code><b>Y</b></code> possibly dependent on information read from <code>s<sub>t</sub></code>. At the same time, information relevant to the next iteration of <code>&Fscr;</code> is assigned to a variable <code>s<sub>t+1</sub></code>. Calling a stateful function without providing a variable to save new state information to results in no new state information being saved. For example: <code>&Fscr;<sub>s<sub>t</sub></sub>(<b>X</b>) &rarr; <b>Y</b></code> saves no information other that <code><b>Y</b></code> 

### Code

Computer program algorithm implementation details

#### Variables

**internal_state**: irregularly shaped tensorflow variable used to keep track of recurrent data. It is important that this data be kept in a tensorflow tensor so that the internal_state remains backpropagatable. However, this is difficult to keep track of in a single tensor when layer sizes may differ. Additionally, these layers may have 1 (RNN), 2 (LSTM), or more internal state variables to keep track of. Being possibly irregularly shaped or jagged, this is likely not really a single tensorflow tensor, but an indefinite number of embedded python lists/dictionaries of with regularly shaped tensorflow variables at the bottom. For example: every layer may have its own tensorflow tensor representation of internal state. In a more complex scenerio, the predictor and decider networks variously share modular networks all with differring layer sizes and types (dense, RNN, LSTM). Triply embedded lists/dictionaries representing modules, submodules, and layers will finally hold dozens of tensors that carry recurrent state data (if any). In complex situations like these, it may be more convenient to write an internal class to structure this data. The exact python structure whether list, dictionary, or class instance does not matter. What is important is that a python variable handle to internal_state allows DREAMs to manage multiple "awarenesses". For example: if the predictor and decider competitively share base layers, then the predictor can be aware of the current decision while the decider is only aware of the previous decision.