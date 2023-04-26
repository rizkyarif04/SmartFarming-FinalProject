from config import *
import pandas as pd
from Environment import Environment
import datetime
from Action import Action

class Agent:
    def __init__(self, threshold, dev, cal_param, epsilon, learning_rate, disc_factor, init_matrix, json_data, json_control, csv_name):
        self.environment = Environment(threshold, dev, cal_param, epsilon, learning_rate, disc_factor, init_matrix, json_data, json_control)
        control_id = self.environment.control_id
        self.action_command = Action(control_id)
        self.state_action = self.environment.state_action
        self.environment.get_current_q_matrix(csv_name)
        self.mL_param = ml_parameter
        self.name_val = name_val

    def get_state_action(self, LH_mL):
        self.environment.get_action(LH_mL)
        self.state = self.environment.state
        self.current_sensorRead = self.environment.current_sensorRead
        self.action = self.environment.action
        self.action_type = self.environment.action_type

    def do_update_q_matrix(self, LH_mL):
        self.environment.update_q_matrix(LH_mL)
        self.Q_matrix = self.environment.Q_matrix
        self.next_sensorRead = self.environment.next_sensorRead
        self.reward = self.environment.reward
        self.next_state = self.environment.next_state

    def do_action(self, on_off):
        action_value = self.action_command.find_action(self.action, self.mL_param)
        if on_off == 'on':
            self.ml_value = self.action_command.ml_value

        self.action_command.valve_act(action_value, on_off)

    def save_data(self, list_index):
        # Save Data Q-Matrix
        try:
            df1 = pd.read_csv('/home/rizky/sarsa/'+'Q_Matrix_1.csv')
            df2 = pd.read_csv('/home/rizky/sarsa/'+'Q_Matrix_2.csv')
            df3 = pd.read_csv('/home/rizky/sarsa/'+'Q_Matrix_3.csv')
            q_matrix_1 = pd.DataFrame(self.Q_matrix[0], columns = list_index)
            
            q_matrix_2 = pd.DataFrame(self.Q_matrix[1], columns = list_index)
            
            q_matrix_3 = pd.DataFrame(self.Q_matrix[2], columns = list_index)

            q_matrix_1.to_csv('/home/rizky/sarsa/'+'Q_Matrix_1.csv', sep = ',', index = False)
            q_matrix_2.to_csv('/home/rizky/sarsa/'+'Q_Matrix_2.csv', sep = ',', index = False)
            q_matrix_3.to_csv('/home/rizky/sarsa/'+'Q_Matrix_3.csv', sep = ',', index = False)

        except FileNotFoundError:
            for i in range(len(self.Q_matrix)):
                pd.DataFrame(self.Q_matrix[i], columns = list_index).to_csv('/home/rizky/sarsa/'+'Q_Matrix_'+str(i+1)+'.csv', sep = ',', index = False)

        try:
            q_val11 = pd.read_csv('/home/rizky/sarsa/'+'qval_11.csv').to_numpy()
            q_val12 = pd.read_csv('/home/rizky/sarsa/'+'qval_12.csv').to_numpy()
            q_val13 = pd.read_csv('/home/rizky/sarsa/'+'qval_13.csv').to_numpy()
            q_val14 = pd.read_csv('/home/rizky/sarsa/'+'qval_14.csv').to_numpy()
            q_val15 = pd.read_csv('/home/rizky/sarsa/'+'qval_15.csv').to_numpy()
            q_val16 = pd.read_csv('/home/rizky/sarsa/'+'qval_16.csv').to_numpy()
            q_val21 = pd.read_csv('/home/rizky/sarsa/'+'qval_21.csv').to_numpy()
            q_val22 = pd.read_csv('/home/rizky/sarsa/'+'qval_22.csv').to_numpy()
            q_val23 = pd.read_csv('/home/rizky/sarsa/'+'qval_23.csv').to_numpy()
            q_val24 = pd.read_csv('/home/rizky/sarsa/'+'qval_24.csv').to_numpy()
            q_val25 = pd.read_csv('/home/rizky/sarsa/'+'qval_25.csv').to_numpy()
            q_val26 = pd.read_csv('/home/rizky/sarsa/'+'qval_26.csv').to_numpy()
            q_val31 = pd.read_csv('/home/rizky/sarsa/'+'qval_31.csv').to_numpy()
            q_val32 = pd.read_csv('/home/rizky/sarsa/'+'qval_32.csv').to_numpy()
            q_val33 = pd.read_csv('/home/rizky/sarsa/'+'qval_33.csv').to_numpy()
            q_val34 = pd.read_csv('/home/rizky/sarsa/'+'qval_34.csv').to_numpy()
            q_val35 = pd.read_csv('/home/rizky/sarsa/'+'qval_35.csv').to_numpy()
            q_val36 = pd.read_csv('/home/rizky/sarsa/'+'qval_36.csv').to_numpy()

            qi_val = [q_val11, q_val12, q_val13, q_val14, q_val15, q_val16, q_val21, q_val22, q_val23, q_val24, q_val25, q_val26, q_val31, q_val32, q_val33, q_val34, q_val35, q_val36]

            for i in range(3):
                for j in range(6):
                    q_val = pd.DataFrame()
                    matr = pd.DataFrame(self.Q_matrix[i][j]).to_numpy().flatten()
                    #print (self.Q_matrix[i][j])
                    q_val['value'] = matr
                    q_val = q_val.transpose()
                    qval = pd.concat([pd.DataFrame(qi_val[6*i+j]), q_val], ignore_index=True, join = 'inner')
                    qval.to_csv('/home/rizky/sarsa/'+self.name_val[6*i+j]+'.csv', index = False)

        except FileNotFoundError:
            print ('error tadi')
            for i in range(3):
                for j in range(6):
                    q_val = pd.DataFrame()
                    matr = pd.DataFrame(self.Q_matrix[i][j]).to_numpy().flatten()
                    #print(matr)
                    q_val['value'] = matr
                    q_val = q_val.transpose()
                    #print(self.name_val[3*i+j])
                    q_val.to_csv('/home/rizky/sarsa/'+self.name_val[6*i+j]+'.csv', index = False)            
                
        # Save Data State-Action-Next State
        date = datetime.datetime.now()+datetime.timedelta(hours = 7)
        date_record = date.strftime("%d-%m-%Y %H:%M:%S")
        new_state_action_1 = pd.DataFrame({'Date' : [date_record], 'ReadSensor' : [self.current_sensorRead[0]], 'State' : [self.state[0]], 'Action' : [self.action[0]], 'Action Type' : [self.action_type[0]], 'NextSensorRead' : [self.next_sensorRead[0]], 'Next State' : [self.next_state[0]], 'Reward' : [self.reward[0]], 'mL Value' : [self.ml_value[0]]})
        new_state_action_2 = pd.DataFrame({'Date' : [date_record], 'ReadSensor' : [self.current_sensorRead[1]], 'State' : [self.state[1]], 'Action' : [self.action[1]], 'Action Type' : [self.action_type[1]], 'NextSensorRead' : [self.next_sensorRead[1]], 'Next State' : [self.next_state[1]], 'Reward' : [self.reward[1]], 'mL Value' : [self.ml_value[1]]})
        new_state_action_3 = pd.DataFrame({'Date' : [date_record], 'ReadSensor' : [self.current_sensorRead[2]], 'State' : [self.state[2]], 'Action' : [self.action[2]], 'Action Type' : [self.action_type[2]], 'NextSensorRead' : [self.next_sensorRead[2]], 'Next State' : [self.next_state[2]], 'Reward' : [self.reward[2]], 'mL Value' : [self.ml_value[2]]})
        
        try:
            state_action_1 = pd.read_csv('/home/rizky/sarsa/'+'state_action_1.csv')
            state_action_2 = pd.read_csv('/home/rizky/sarsa/'+'state_action_2.csv')
            state_action_3 = pd.read_csv('/home/rizky/sarsa/'+'state_action_3.csv')

            update_state_action_1 = pd.concat([state_action_1, new_state_action_1])
            update_state_action_2 = pd.concat([state_action_2, new_state_action_2])
            update_state_action_3 = pd.concat([state_action_3, new_state_action_3])

            update_state_action_1.to_csv('/home/rizky/sarsa/'+'state_action_1.csv', index = False)
            update_state_action_2.to_csv('/home/rizky/sarsa/'+'state_action_2.csv', index = False)
            update_state_action_3.to_csv('/home/rizky/sarsa/'+'state_action_3.csv', index = False)

        except FileNotFoundError:
            new_state_action_1.to_csv('/home/rizky/sarsa/'+'state_action_1.csv', index = False)
            new_state_action_2.to_csv('/home/rizky/sarsa/'+'state_action_2.csv', index = False)
            new_state_action_3.to_csv('/home/rizky/sarsa/'+'state_action_3.csv', index = False)

        




