import numpy as np
from random import uniform

CONFIG = {
    'GETDATA': {
        'urlSensor' : 'https://api.smartfarmingunpad.com/developer/dataset',
        'urlControl' : 'https://api.smartfarmingunpad.com/developer/control',
    },
    
    'HEADERS': {
        'X-DEVACCOUNT-TOKEN' : 'banknJS8Qc0B3TL6vUBxL6GTkfLjBn5PIzlA9mIsGTiDPN66gpeWsXNStN8hQifepB7mFpJdjhFUL1gtEck56qOhhB8PAOOLFMVC8XGMvhHCYYux7nmpsC3yUTpJc1Wc'
    },
    
    'DATA_LOGIN' : {
        'email':'smartfarmingunpad@gmail.com',
        'password':'smartfarmingunpad1199'
    },
    
    'SM' : {
        'DATASET': [
            'Dataset RKI 1',
            'Dataset RKI 2',
            'Dataset RKI 3'
        ],

        'threshold' : 80
    },

    'REWARD' : [
        3,      #Value State 1
        0,      #Value State 2
        -1,     #Value State 3
        -2,     #Value State 4
        -3,     #Value State 5
        -4,      #Value State 6
        1,      #Value State 7
        -2,     #Value State 8
        -3,     #Value State 9
        -4,     #Value State 10
        -5,     #Value State 11
        -2      #Value State 12
    ],

    'VALVE' : {
        'NAME' : [
            'Control Valve 1-1',
            'Control Valve 1-2',
            'Control Valve 1-3'
        ],
        'ml_value' : {
            '1' : 0,
            '2' : 0,
            '3' : 0,
            '4' : 0,
            '5' : 0,
            '6' : 0
        },
        'pwm_input' : [
            '000',
            '026',
            '051',
            '077',
            '102',
            '128',
            '153',
            '179',
            '204',
            '230',
            '252'
        ]
    }
}

dev = ['XniD6mBlnKqagRJ8qD9WhR6JGK4yle1d',
 'XniD6mBlnKqagRJ8qD9WhR6JGK4yle1d',
 'Tdr4a4bKp5AzrCe6KGki8bUDF0ynE9l9']

calibrate_param = [
    [600, 1023], [510, 1023], [516, 1023],  
    [600, 1023], [510, 1023], [516, 1023],
    [614, 1023], [420, 1023],[603, 1023],
]

ml_parameter = [
    0,
    0,
    0
]

epsilon = 0.1
learning_rate = 0.75
discount_factor = 0.8

LH_mil = 300

index_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

Threshold = 80

time_on = 240
time_delay = 300

init_matrix_1 = 0
init_matrix_2 = 0
init_matrix_3 = 0

init_matrix = np.matrix(np.ones(shape = (12,11)))
init_matrix *= -1
init_matrix[5,0] = 0

init_matrix_1 = init_matrix.copy()
init_matrix_2 = init_matrix.copy()
init_matrix_3 = init_matrix.copy()

initial_matrix = [init_matrix_1, init_matrix_2, init_matrix_3]

name_val = []
for i in range(3):
    for j in range(6):
        name_val.append('qval_'+str(i+1)+str(j+1))


add_val = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22]