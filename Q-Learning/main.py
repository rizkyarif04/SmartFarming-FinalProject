#!/usr/bin/python3

from config import *
from Agent import Agent
import requests
import time
#import datetime

csv_name = 'Q_Matrix'
json_data = requests.get(CONFIG['GETDATA']['urlSensor'], headers = CONFIG['HEADERS'])
json_control = requests.get(CONFIG['GETDATA']['urlControl'], headers = CONFIG['HEADERS'])
LH_mL = LH_mil

agent = Agent(Threshold, dev, calibrate_param, epsilon, learning_rate, discount_factor, initial_matrix, json_data, json_control, csv_name)


agent.get_state_action(LH_mL)
#Time = datetime.datetime.now()

#while datetime.datetime.now() < Time + datetime.timedelta(minutes = )
agent.do_action('on')
print('Do Action Now, WAIT!!!')
time.sleep(time_on)
agent.do_action('off')
print('Im Finisshhh!!')

time.sleep(time_delay)
agent.do_update_q_matrix(LH_mL)

agent.save_data(index_list)




