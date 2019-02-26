# Welcome 

In this project, I programmed an artificial intelligence that was able to beat a random agent in the popular game "four in a row". The AI is based on reinforcement learning, that means that the AI learns from positive or negative feedback of its environment. In this case, positive feedback would be the AI winning the current game and negative feedback would be losing the current game. The AI is based on a simple multi-layered perceptron that determines the scores/rewards of the next move.

We can see that after about 2000 games, the AI wins against the random agent with a probability of ~98%. 
![success rate](https://github.com/STrucks/4gewinnt/blob/master/imgs/success_rate.png)

Note that beating a random agent does not require deep learning, but the purpose of this project is to play around with deep reinforcement learning.

## Prerequisites
To run the programm, you need to have chainer installed.
