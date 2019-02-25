from Environment import Board
import numpy as np
from Models import MLP, REINFORCEAgent, Adam

if __name__ == '__main__':
    WIDTH, HEIGHT = 7, 10
    max_env_steps = 100
    board = Board(WIDTH, HEIGHT, max_env_steps)

    network = MLP(n_output=WIDTH, n_hidden=20)
    agent = REINFORCEAgent(board.get_action_space, network, optimizer=Adam())

    episode_count = 10001
    done = False
    reward = 0

    R = np.zeros(episode_count)
    winners = []
    for i in range(episode_count):
        #print(i)
        board.reset()
        ob = board.get_state()
        loss = 0
        while True:

            action, policy = agent.act(ob, reward, done)
            ob, reward, done, winner = board.step(action[0])
            #print(policy)
            # get reward associated with taking the previous action in the previous state
            agent.rewards.append(reward)
            R[i] += reward

            # recompute score function: grad_theta log pi_theta (s_t, a_t) * v_t
            agent.scores.append(agent.compute_score(action, policy))

            # we learn at the end of each episode
            if done:
                loss += agent.compute_loss()
                agent.model.cleargrads()
                loss.backward()
                loss.unchain_backward()
                agent.optimizer.update()
                winners.append(winner)
                if len(winners) > 500:
                    winners = winners[1:]
                if i % 100 == 0:
                    #print(len(agent.rewards))
                    #print(loss)
                    os = len([o for o in winners if o == 1])
                    xs = len([x for x in winners if x == 2])
                    print(i, ":", os, "|", xs, "|", os/(xs+os))
                agent.rewards = []
                agent.scores = []

                break


    players = [1,2]
    player_index = 0
    for i in range(1):
        possible = board.possible_positions()
        move = possible[np.random.randint(0, len(possible))]
        valid = board.move(move[0],move[1], players[player_index])
        if not valid:
            print("move", move, "is not valid")
            break
        win, who = board.is_winning_state()
        if win:
            break
        player_index += 1
        player_index %= len(players )
        print(board.to_string())
    print(board.to_string())
    print(board.possible_positions())