# Delayed Reinforcement Executive Actuary Multilayer (DREAM &#x1F9E0;) Architecture

The DREAM's &#x1F9E0; architecture enables it to learn and make decisions with long range forsight.

## Algorithm

### Multilayer top-down control

<pre><b>Algorithm 1. Intelligence Loop</b> <b>I</b><sub>t</sub>: &#x1F9E0;, <b>o</b><sub>t</sub>, g<sub>t</sub>
1       learn from bottom up
1.1     iterate through all layers from bottom up that are elapsing their timestep
1.1.1   <b>for</b> &Lscr; <b>in</b> &#x1F9E0;.layers ascending <b>where</b> t % &Lscr;.&Delta;<sub>t</sub> = 0: 
1.2         calculate abstraction based on children
1.2.1       &Lscr;.<b>a</b><sub>t</sub> &larr; &Lscr;.&Ascr;<sub>t</sub>([(&Lscr;<sub>child</sub>.<b>o</b><sub>t</sub>, &Lscr;<sub>child</sub>.<b>d</b><sub>t</sub>, &Lscr;<sub>child</sub>.<b>a</b><sub>t</sub>) <b>for</b> &Lscr;<sub>child</sub> <b>in</b> &Lscr;.children])
1.3         train conscience
1.3.1       fit &Lscr;.&Cscr;(&Lscr;.<b>o</b><sub>t</sub>, &Lscr;.<b>a</b><sub>t</sub>) &rarr; g<sub>t</sub>  &eta; = &eta;<sub>&Cscr;</sub> &times; &Lscr;.&Delta;<sub>t</sub><sup>c<sub>&eta;</sub></sup>
1.4         train predictor
1.4.1       fit &Lscr;.&Pscr;<sub>t-&Lscr;.&Delta;<sub>t</sub></sub>(&Lscr;.<b>o</b><sub>t-&Lscr;.&Delta;<sub>t</sub></sub>, &Lscr;.<b>d</b><sub>t-2&times;&Lscr;.&Delta;<sub>t</sub></sub>, &Lscr;.<b>a</b><sub>t-&Lscr;.&Delta;<sub>t</sub></sub>, [&Lscr;<sub>parent</sub>.<b>d</b><sub>t</sub> for &Lscr;<sub>parent</sub> in &Lscr;.parents]) &rarr; &Lscr;.<b>o</b><sub>t</sub>, &Lscr;.<b>a</b><sub>t</sub>  &eta; = &eta;<sub>&Pscr;</sub> &times; &Lscr;.&Delta;<sub>t</sub><sup>c<sub>&eta;</sub></sup>
1.5         train decider to maximize cumulative discounted predicted goodness g<sub>&Sigma;</sub>
1.5.1       initialize prediction p variable
1.5.1.1     p<sub>t<sub>pred.</sub></sub>.<b>o</b> &larr; &Lscr;.<b>o</b><sub>t</sub>
1.5.1.2     p<sub>t<sub>pred.</sub></sub>.<b>a</b> &larr; &Lscr;.<b>a</b><sub>t</sub>
1.5.1.3     p<sub>t<sub>pred.</sub>-&Lscr;.&Delta;<sub>t</sub></sub>.<b>d</b> &larr; &Lscr;.<b>d</b><sub>t-&Lscr;.&Delta;<sub>t</sub></sub>
1.5.2       intialize cumulative predicted goodness g<sub>&Sigma;</sub> to zero 
1.5.2.1     g<sub>&Sigma;</sub> &larr; 0
1.5.3       predict future states for &Lscr;.N<sub>iter.</sub> iterations
1.5.3.1     <b>while</b> t<sub>p</sub> &le; t + &Lscr;.N<sub>iter.</sub>&Lscr;.&Delta;<sub>t</sub>:
1.5.3.2         make decision p<sub>t<sub>p</sub></sub>.<b>d</b> &larr; &Lscr;.&Dscr;<sub>t<sub>p</sub></sub>(p<sub>t<sub>p</sub></sub>.<b>o</b>, p<sub>t<sub>p</sub></sub>.<b>a</b>, p<sub>t<sub>p</sub>-&Lscr;.&Delta;<sub>t</sub></sub>.<b>d</b>, [&Lscr;<sub>parent</sub>.<b>d</b><sub>t<sub>p</sub></sub> for &Lscr;<sub>parent</sub> in &Lscr;.parents])
1.5.3.3         predict resulting observation and abstraction p<sub>t<sub>p</sub>+&Lscr;.&Delta;<sub>t</sub></sub>.<b>o</b>, p<sub>t<sub>p</sub>+&Lscr;.&Delta;<sub>t</sub></sub>.<b>a</b> &larr; &Lscr;.&Pscr;<sub>t<sub>p</sub></sub>(p<sub>t<sub>p</sub></sub>.<b>o</b>, p<sub>t<sub>p</sub></sub>.<b>a</b>, p<sub>t<sub>p</sub>-&Lscr;.&Delta;<sub>t</sub></sub>.<b>d</b>, [&Lscr;<sub>parent</sub>.<b>d</b><sub>t<sub>p</sub></sub> for &Lscr;<sub>parent</sub> in &Lscr;.parents], learn=<b>False</b>)
1.5.3.2         g<sub>&Sigma;</sub> &larr; g<sub>&Sigma;</sub> + &Lscr;.&Cscr;(&Lscr;.<b>o</b><sub>t</sub>, &Lscr;.<b>a</b><sub>t</sub>)
1.5.3.3         t<sub>p</sub> &larr; t<sub>p</sub> + &Lscr;.&Delta;<sub>t</sub>
1.5.4       adjust decision policy &Lscr;.&Dscr;<sub>&Theta;</sub> to maximize cumulative predicted discounted goodness g<sub>&Sigma;</sub>
1.5.4.1     max<sub>&Lscr;.&Dscr;<sub>&Theta;</sub></sub> g<sub>&Sigma;</sub>  &eta; = &eta;<sub>&Dscr;</sub> &times; &Lscr;.&Delta;<sub>t</sub><sup>c<sub>&eta;</sub></sup>
2       make decision from top down
2.1     iterate through all layers from top down that are elapsing their timestep
2.1.1   <b>for</b> &Lscr; <b>in</b> &#x1F9E0;.layers descending <b>where</b> t % &Lscr;.&Delta;<sub>t</sub> = 0: 
2.2         make decision &Lscr;<sub>i</sub>.<b>d</b><sub>t</sub> = &Lscr;<sub>i</sub>.&Dscr;<sub>t</sub>(&Lscr;<sub>i</sub>.<b>o</b><sub>t</sub>, &Lscr;<sub>i</sub>.<b>a</b><sub>t</sub>, &Lscr;<sub>i</sub>.<b>d</b><sub>t-1</sub>, &Lscr;<sub>i</sub>.parents.<b>d</b><sub>t</sub>)
2.3         make prediction (to update &Lscr;.&Pscr; state)
2.3.1       &#x1F5D1; &larr; &Lscr;.&Pscr;<sub>t</sub>(&Lscr;.<b>o</b><sub>t</sub>, &Lscr;.<b>d</b><sub>t</sub>, &Lscr;.<b>a</b><sub>t</sub>, [&Lscr;<sub>parent</sub>.<b>d</b><sub>t</sub> for &Lscr;<sub>parent</sub> in &Lscr;.parents], learn=<b>True</b>)
3       return decision {&Lscr;<sub>i</sub>.<b>d</b><sub>raw,t</sub> | &Lscr;<sub>i</sub> &in; &#x1F9E0;}
</pre>

In all layers &Lscr;.<b>d</b><sub>t</sub> &supe; &Lscr;.<b>d</b><sub>raw,t</sub>. However, in childless layers &Lscr;.<b>d</b><sub>raw,t</sub> = &Lscr;.<b>d</b><sub>t</sub>, but in parent layers, usuallyL.<b>d</b><sub>raw,t</sub> = &empty;. In layers that have both children and motor control &Lscr;.<b>d</b><sub>raw,t</sub> &sub; &Lscr;.<b>d</b><sub>t</sub>, &Lscr;.<b>d</b><sub>raw,t</sub> &ne; &Lscr;.<b>d</b><sub>t</sub>.

### Single Controller

<pre><b>Algorithm 2. Single &Dscr; Intelligence Loop</b> <b>I</b><sub>t</sub>: &#x1F9E0;, <b>o</b><sub>t</sub>, g<sub>t</sub>
Learn from bottom up by iterating through all layers from bottom up that are elapsing their timestep
<b>for</b> layer &Lscr; <b>in</b> &#x1F9E0;.layers ascending <b>where</b> t % &Lscr;.&Delta;<sub>t</sub> = 0: 
&Lscr;.update()

Train decider to maximize cumulative discounted predicted goodness g<sub>&Sigma;</sub>
initialize prediction variable p at t
t<sub>p</sub> &larr; t
p<sub>t<sub>p</sub></sub>.<b>o</b> &larr; &Lscr;.<b>o</b><sub>t</sub>
p<sub>t<sub>p</sub></sub>.<b>a</b> &larr; &Lscr;.<b>a</b><sub>t</sub>
p<sub>t<sub>p</sub>-&Lscr;.&Delta;<sub>t</sub></sub>.<b>d</b> &larr; &Lscr;.<b>d</b><sub>t-&Lscr;.&Delta;<sub>t</sub></sub>
intialize cumulative predicted goodness g<sub>&Sigma;</sub> to zero 
g<sub>&Sigma;</sub> &larr; 0
predict future states for &Lscr;.N<sub>iter.</sub> iterations
<b>while</b> t<sub>p</sub> &le; t + &Lscr;.N<sub>iter.</sub>&Lscr;.&Delta;<sub>t</sub>:
make decision p<sub>t<sub>p</sub></sub>.<b>d</b> &larr; &#x1F9E0;.&Dscr;<sub>t<sub>p</sub></sub>(p<sub>t<sub>p</sub></sub>.<b>o</b>, p<sub>t<sub>p</sub></sub>.<b>a</b>, p<sub>t<sub>p</sub>-&Lscr;.&Delta;<sub>t</sub></sub>.<b>d</b>, [&Lscr;<sub>parent</sub>.<b>d</b><sub>t<sub>p</sub></sub> for &Lscr;<sub>parent</sub> in &Lscr;.parents])
predict resulting observation and abstraction p<sub>t<sub>p</sub>+&Lscr;.&Delta;<sub>t</sub></sub>.<b>o</b>, p<sub>t<sub>p</sub>+&Lscr;.&Delta;<sub>t</sub></sub>.<b>a</b> &larr; &Lscr;.&Pscr;<sub>t<sub>p</sub></sub>(p<sub>t<sub>p</sub></sub>.<b>o</b>, p<sub>t<sub>p</sub></sub>.<b>a</b>, p<sub>t<sub>p</sub>-&Lscr;.&Delta;<sub>t</sub></sub>.<b>d</b>, [&Lscr;<sub>parent</sub>.<b>d</b><sub>t<sub>p</sub></sub> for &Lscr;<sub>parent</sub> in &Lscr;.parents], learn=<b>False</b>)
g<sub>&Sigma;</sub> &larr; g<sub>&Sigma;</sub> + &Lscr;.&Cscr;(&Lscr;.<b>o</b><sub>t</sub>, &Lscr;.<b>a</b><sub>t</sub>)
t<sub>p</sub> &larr; t<sub>p</sub> + &Lscr;.&Delta;<sub>t</sub>
adjust decision policy &Lscr;.&Dscr;<sub>&Theta;</sub> to maximize cumulative predicted discounted goodness g<sub>&Sigma;</sub>
max<sub>&Lscr;.&Dscr;<sub>&Theta;</sub></sub> g<sub>&Sigma;</sub>  &eta; = &eta;<sub>&Dscr;</sub> &times; &Lscr;.&Delta;<sub>t</sub><sup>c<sub>&eta;</sub></sup>
return decision &Lscr;.&Dscr;()
</pre>

<pre>
ChildLayer.update:

train conscience
fit &Lscr;.&Cscr;(&Lscr;.<b>o</b><sub>t</sub>, &Lscr;.<b>a</b><sub>t</sub>) &rarr; ave(g<sub>t-&Lscr;.&Delta;<sub>t</sub></sub> ... g<sub>t</sub>)  &eta; = &eta;<sub>&Cscr;</sub> &times; &Lscr;.&Delta;<sub>t</sub><sup>c<sub>&eta;</sub></sup>
train predictor with prediction and actual data
fit &Lscr;.&Pscr;<sub>t-&Lscr;.&Delta;<sub>t</sub></sub>(&Lscr;.<b>o</b><sub>t-1, <b>d</b><sub>t-2) &rarr; (&Lscr;.<b>o</b><sub>t</sub>, &Lscr;.<b>a</b><sub>t</sub>, 1)  &eta; = &eta;<sub>&Pscr;</sub> &times; &Lscr;.&Delta;<sub>t</sub><sup>c<sub>&eta;</sub></sup>
&Delta;<sub>&Pscr;</sub> &larr; Div((&Lscr;.p<sub>t-&Lscr;.&Delta;<sub>t</sub></sub>.<b>o</b>, &Lscr;.p<sub>t-&Lscr;.&Delta;<sub>t</sub></sub>.<b>a</b>), (&Lscr;.<b>o</b><sub>t</sub>, &Lscr;.<b>a</b><sub>t</sub>))
fit &Lscr;.&Pscr;<sub>t-&Lscr;.&Delta;<sub>t</sub></sub>(&Lscr;.<b>o</b><sub>t-&Lscr;.&Delta;<sub>t</sub></sub>, <b>d</b><sub>t-2&times;&Lscr;.&Delta;<sub>t</sub></sub>, &Lscr;.<b>a</b><sub>t-&Lscr;.&Delta;<sub>t</sub></sub>) &rarr; (&Lscr;.p<sub>t</sub>.<b>o</b>, &Lscr;.p<sub>t</sub>.<b>a</b>, &Delta;<sub>&Pscr;</sub>)  &eta; = &eta;<sub>&Pscr;</sub> &times; &Lscr;.&Delta;<sub>t</sub><sup>c<sub>&eta;</sub></sup>
make prediction
&Lscr;.p<sub>t+&Lscr;.&Delta;<sub>t</sub></sub> &larr; &Lscr;.&Pscr;<sub>t</sub>(&Lscr;.<b>o</b><sub>t</sub>, <b>d</b><sub>t-&Lscr;.&Delta;<sub>t</sub></sub>, &Lscr;.<b>a</b><sub>t</sub>)
</pre>

<pre>
ParentLayer.update:

calculate abstraction based on children
&Lscr;.<b>a</b><sub>t</sub> &larr; &Lscr;.&Ascr;<sub>t</sub>([(&Lscr;<sub>child</sub>.<b>o</b><sub>t</sub>, &Lscr;<sub>child</sub>.<b>a</b><sub>t</sub>) <b>for</b> &Lscr;<sub>child</sub> <b>in</b> &Lscr;.children])
train conscience
fit &Lscr;.&Cscr;(&Lscr;.<b>o</b><sub>t</sub>, &Lscr;.<b>a</b><sub>t</sub>) &rarr; ave(g<sub>t-&Lscr;.&Delta;<sub>t</sub></sub> ... g<sub>t</sub>)  &eta; = &eta;<sub>&Cscr;</sub> &times; &Lscr;.&Delta;<sub>t</sub><sup>c<sub>&eta;</sub></sup>
train predictor with prediction and actual data
fit &Lscr;.&Pscr;<sub>t-&Lscr;.&Delta;<sub>t</sub></sub>(&Lscr;.<b>o</b><sub>t-&Lscr;.&Delta;<sub>t</sub></sub>, <b>d</b><sub>t-2&times;&Lscr;.&Delta;<sub>t</sub></sub>, &Lscr;.<b>a</b><sub>t-&Lscr;.&Delta;<sub>t</sub></sub>) &rarr; (&Lscr;.<b>o</b><sub>t</sub>, &Lscr;.<b>a</b><sub>t</sub>, 1)  &eta; = &eta;<sub>&Pscr;</sub> &times; &Lscr;.&Delta;<sub>t</sub><sup>c<sub>&eta;</sub></sup>
&Delta;<sub>&Pscr;</sub> &larr; Div((&Lscr;.p<sub>t-&Lscr;.&Delta;<sub>t</sub></sub>.<b>o</b>, &Lscr;.p<sub>t-&Lscr;.&Delta;<sub>t</sub></sub>.<b>a</b>), (&Lscr;.<b>o</b><sub>t</sub>, &Lscr;.<b>a</b><sub>t</sub>))
fit &Lscr;.&Pscr;<sub>t-&Lscr;.&Delta;<sub>t</sub></sub>(&Lscr;.<b>o</b><sub>t-&Lscr;.&Delta;<sub>t</sub></sub>, <b>d</b><sub>t-2&times;&Lscr;.&Delta;<sub>t</sub></sub>, &Lscr;.<b>a</b><sub>t-&Lscr;.&Delta;<sub>t</sub></sub>) &rarr; (&Lscr;.p<sub>t</sub>.<b>o</b>, &Lscr;.p<sub>t</sub>.<b>a</b>, &Delta;<sub>&Pscr;</sub>)  &eta; = &eta;<sub>&Pscr;</sub> &times; &Lscr;.&Delta;<sub>t</sub><sup>c<sub>&eta;</sub></sup>
make prediction
&Lscr;.p<sub>t+&Lscr;.&Delta;<sub>t</sub></sub> &larr; &Lscr;.&Pscr;<sub>t</sub>(&Lscr;.<b>o</b><sub>t</sub>, <b>d</b><sub>t-&Lscr;.&Delta;<sub>t</sub></sub>, &Lscr;.<b>a</b><sub>t</sub>)
</pre>


1.2.1 omits including <b>d</b><sub>t</sub> in abstractions. However, individual layers may make their observations <b>o</b> differentiably set to equal <b>d</b><sub>t-&Lscr;.&Delta;<sub>t</sub></sub>

higher layers might not include <b>d</b> in their predictors' signatures

I would prefer <b>a</b> smooth continuous approach to decision making even for layers with very large &delta;<sub>t</sub>'s

I also want to add an abstracted decision to reduce decider and predictor input size. However this could just be <b>a</b> feature of those functions

Times referenced out of bounds should default to the nearest available time