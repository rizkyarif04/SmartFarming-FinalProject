import numpy as np
import pandas as pd
from State import State

class Environment:
    def __init__(self, threshold, dev, cal_param, epsilon, learning_rate, disc_factor, init_matrix, json_data, json_control):
        self.state_action = State(threshold, dev, cal_param, json_data, json_control)
        self.control_id = self.state_action.control_id
        self.epsilon = epsilon
        self.learning_rate = learning_rate
        self.disc_factor = disc_factor
        self.init_matrix = init_matrix

    def get_current_q_matrix(self, csv_name, n_valve = 3):
        self.Q_matrix = []
        for i in range(n_valve):
            try:
                q_matrix = pd.read_csv("/home/rizky/sarsa/"+csv_name+'_'+str(i+1)+'.csv')
                q_matrix = q_matrix.to_numpy()
                q_matrix = q_matrix[-12:, 0:11]
                self.Q_matrix.append(q_matrix)

            except FileNotFoundError:
                self.Q_matrix.append(self.init_matrix[i])


    def get_action(self, LH_mL):
        self.state_action.get_state(LH_mL)
        self.state = self.state_action.state
        self.current_sensorRead = self.state_action.current_sensorRead
        self.action = []
        self.action_type = []
        for i in range(len(self.Q_matrix)):
            if np.random.random() > self.epsilon:
                self.action.append(np.argmax(self.Q_matrix[i][self.state[i]-1]))
                self.action_type.append('Exploit')
            else:
                self.action.append(np.random.randint(11))
                self.action_type.append('Exploration')
    
    def update_q_matrix(self, LH_mL):
        self.state_action.get_next_state(LH_mL, self.action)
        self.next_state = self.state_action.next_state
        self.next_sensorRead = self.state_action.next_sensorRead
        self.reward = self.state_action.get_reward(self.state, self.next_state, self.action)

        for j in range(len(self.Q_matrix)):
            q_value = self.Q_matrix[j][self.state[j]-1, self.action[j]]
            temporal_difference = self.reward[j] + (self.disc_factor * self.Q_matrix[j][self.next_state[j]-1, self.action[j]]) - q_value
            new_q_value = q_value + (self.learning_rate * temporal_difference)
            self.Q_matrix[j][self.state[j]-1,self.action[j]] = new_q_value
