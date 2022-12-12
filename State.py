from GetData import GetData
from config import *

class State:
    def __init__(self, threshold, dev, cal_param, json_data, json_control) :
        self.threshold = threshold
        self.getdata = GetData(dev, cal_param)
        self.getdata.get_device(json_data, json_control)
        self.control_id = self.getdata.control_id

    def get_state(self, LH_mL):
        arr_sensor = self.getdata.get_value()
        self.current_sensorRead = self.getdata.filter_sensor(arr_sensor)
        self.state = []

        for i in range(len(self.current_sensorRead)):
            if 0 <= (self.current_sensorRead[i] - self.threshold) <= 10 and 225 <= LH_mL <= 375 :
                self.state.append(1)
            elif -10 <= (self.current_sensorRead[i] - self.threshold) < 0 and 225 <= LH_mL <= 375:
                self.state.append(2)
            elif -20 <= (self.current_sensorRead[i] - self.threshold) < -10 and 225 <= LH_mL <= 375:
                self.state.append(3)
            elif -40 <= (self.current_sensorRead[i] - self.threshold) < -20 and 225 <= LH_mL <= 375:
                self.state.append(4)
            elif (self.current_sensorRead[i] - self.threshold) < -40 and 225 <= LH_mL <= 375:
                self.state.append(5)
            elif (self.current_sensorRead[i] - self.threshold) > 10 and 225 <= LH_mL <= 375:
                self.state.append(6)
            elif 0 <= (self.current_sensorRead[i] - self.threshold) <= 10 and LH_mL < 225:
                self.state.append(7)
            elif -10 <= (self.current_sensorRead[i] - self.threshold) < 0 and LH_mL < 225:
                self.state.append(8)
            elif -20 <= (self.current_sensorRead[i] - self.threshold) < -10 and LH_mL < 225:
                self.state.append(9)
            elif -40 <= (self.current_sensorRead[i] - self.threshold) < -20 and LH_mL < 225:
                self.state.append(10)
            elif (self.current_sensorRead[i] - self.threshold) < -40 and LH_mL < 225:
                self.state.append(11)
            elif (self.current_sensorRead[i] - self.threshold) > 10 and LH_mL < 225:
                self.state.append(12)

    def get_next_state(self, LH_mL, action):
        arr_sensor = self.getdata.get_value()
        self.next_sensorRead = self.getdata.filter_sensor(arr_sensor)
        for j in range(len(self.next_sensorRead)):
            if self.next_sensorRead[j] < self.current_sensorRead[j]:
                val_added = np.round(np.random.uniform(add_val[action[j]],add_val[action[j]+1]), 2)
                self.next_sensorRead[j] = self.current_sensorRead[j] + val_added
                if self.next_sensorRead[j] > 100:
                    self.next_sensorRead[j] = 100
        self.next_state = []

        for i in range(len(self.next_sensorRead)):
            if 0 <= (self.next_sensorRead[i] - self.threshold) <= 10 and 225 <= LH_mL <= 375 :
                self.next_state.append(1)
            elif -10 <= (self.next_sensorRead[i] - self.threshold) < 0 and 225 <= LH_mL <= 375:
                self.next_state.append(2)
            elif -20 <= (self.next_sensorRead[i] - self.threshold) < -10 and 225 <= LH_mL <= 375:
                self.next_state.append(3)
            elif -40 <= (self.next_sensorRead[i] - self.threshold) < -20 and 225 <= LH_mL <= 375:
                self.next_state.append(4)
            elif (self.next_sensorRead[i] - self.threshold) < -40 and 225 <= LH_mL <= 375:
                self.next_state.append(5)
            elif (self.next_sensorRead[i] - self.threshold) > 10 and 225 <= LH_mL <= 375:
                self.next_state.append(6)
            elif 0 <= (self.next_sensorRead[i] - self.threshold) <= 10 and LH_mL < 225:
                self.next_state.append(7)
            elif -10 <= (self.next_sensorRead[i] - self.threshold) < 0 and LH_mL < 225:
                self.next_state.append(8)
            elif -20 <= (self.next_sensorRead[i] - self.threshold) < -10 and LH_mL < 225:
                self.next_state.append(9)
            elif -40 <= (self.next_sensorRead[i] - self.threshold) < -20 and LH_mL < 225:
                self.next_state.append(10)
            elif (self.next_sensorRead[i] - self.threshold) < -40 and LH_mL < 225:
                self.next_state.append(11)
            elif (self.next_sensorRead[i] - self.threshold) > 10 and LH_mL < 225:
                self.next_state.append(12)

    def get_reward(self, state, next_state, action):
        self.reward = []

        for i in range(len(state)):
            value_state = CONFIG['REWARD'][state[i]-1]
            value_next_state = CONFIG['REWARD'][next_state[i]-1]
            value_act = value_next_state - value_state

            if state[i] == 12 and state[i] == next_state[i]:
                self.reward.append(-1)
            elif state[i] == 6 and action[i] != 0:
                self.reward.append(-2)
            elif state[i] == 6 and action[i] == 0:
                self.reward.append(2)
            elif next_state[i] == 1:
                self.reward.append(5)
            elif value_act >= 2:
                self.reward.append(0)
            elif value_act == 1:
                self.reward.append(-1)
            elif value_act == 0:
                self.reward.append(-2)
            elif value_act < 0:
                self.reward.append(-2)

        return self.reward

