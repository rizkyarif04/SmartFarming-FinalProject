from config import CONFIG
import requests
import time

class Action:
    def __init__(self, control_id):
        self.control_id = control_id

    def find_action(self, get_action, mL_param):
        action = []
        self.ml_value = []
        for i in range(len(get_action)):
            action.append(CONFIG['VALVE']['pwm_input'][get_action[i]])
            self.ml_value.append(get_action[i]*10*mL_param[i]/100)

        return action

    def valve_act(self, arr_action, on_off):
        if on_off == 'on':
            open_valve = ''
            for i in range (len(arr_action)):
                open_valve = open_valve + arr_action[i]
        elif on_off == 'off':
            open_valve = '000000000'

        for i in range (len(self.control_id)):    
            requests.post(CONFIG['GETDATA']['urlControl'] + '/' + self.control_id[i], headers = CONFIG['HEADERS'], data = {'value' : open_valve[3*i:(3*i)+3]})
            time.sleep(3)

