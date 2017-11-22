from interface import CommunicationInterface
from converter import OutputGenerator
from test_env import TestEnvironment

from dqn.RL_brain import DeepQNetwork
import numpy as np

# kommunikál a szerverrel
# interface = CommunicationInterface()
# A szervertől érkező adatokat konvertálja, megjeleníti
generator = OutputGenerator()

#interface.login()

# teszt környezet
test_env = TestEnvironment()

actions = ["up", "down", "left", "right"]
unit_index = 0

def run_sim():
    step = 0
    for episode in range(1000000):

        # initial observation
        test_env.init(0)
        response = test_env.receive()
        state_vector = generator.convert(response.cells, response.units, response.enemies)
        observation = np.asarray(state_vector)

        level = response.info.level
        while True:

            # RL choose action based on observation
            action_index = RL.choose_action(observation)


            # RL take action and get next observation and reward
            done = test_env.update([[unit_index, actions[action_index]]])

            response = test_env.receive()
            state_vector = generator.convert(response.cells, response.units, response.enemies)
            observation_ = np.asarray(state_vector)

            generator.show(state_vector)

            if response.info.level > level:
                level = response.info.level
                reward = 1
            else:
                reward = 0

            RL.store_transition(observation, action_index, reward, observation_)

            if (step > 200) and (step % 5 == 0):
                RL.learn()

            # swap observation
            observation = observation_

            # break while loop when end of this episode
            if not done:
                break
            step += 1

    # end of game
    print('game over')


if __name__ == "__main__":
    # maze game

    RL = DeepQNetwork(4, 8000,
                      learning_rate=0.01,
                      reward_decay=0.9,
                      e_greedy=0.9,
                      replace_target_iter=200,
                      memory_size=2000,
                      # output_graph=True
                      )
    run_sim()
    RL.plot_cost()

