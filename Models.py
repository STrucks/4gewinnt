from chainer import Chain
import chainer.links as L
import chainer.functions as F
from chainer.optimizers import Adam
from chainer import Variable
import numpy as np


class MLP(Chain):
    """Multilayer perceptron"""

    def __init__(self, n_output=1, n_hidden=5):
        super(MLP, self).__init__(l1=L.Linear(None, n_hidden), l2=L.Linear(n_hidden, n_output))

    def __call__(self, x):
        return F.softmax(self.l2(F.relu(self.l1(x))))


class REINFORCEAgent(object):
    """Agent trained using REINFORCE"""

    def __init__(self, action_space, model, optimizer=Adam()):
        self.action_space = action_space

        self.model = model

        self.optimizer = optimizer
        self.optimizer.setup(self.model)

        # monitor score and reward
        self.rewards = []
        self.scores = []

    def act(self, observation, reward, done):
        # linear outputs reflecting the log action probabilities and the value
        observation = np.reshape(observation, newshape=(1, -1))
        policy = self.model(Variable(np.atleast_2d(np.asarray(observation, 'float32'))))

        # generate action according to policy
        p = policy.data
        # normalize p in case tiny floating precision problems occur
        row_sums = p.sum(axis=1)
        p /= row_sums[:, np.newaxis]
        action = np.asarray([np.random.choice(p.shape[1], None, True, p[0])])

        return action, policy

    def compute_loss(self):
        """
        Return loss for this episode based on computed scores and accumulated rewards
        """
        # concat scores for sum
        scores = F.concat(self.scores, axis=0).T
        # negative loss cause of gradient ascent
        loss = - F.sum(np.asarray(self.rewards) * scores)
        return loss

    def compute_score(self, action, policy):
        """
        Computes score

        Args:
            action (int):
            policy:

        Returns:
            score
        """
        # grad_theta log pi_theta (s_t, a_t) * v_t
        return F.log(policy[:, action])