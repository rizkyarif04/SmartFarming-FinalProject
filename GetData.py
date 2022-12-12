from config import CONFIG
import numpy as np
import requests

class GetData:
    def __init__(self, dev_id, cal_param):
        #self.dev = dev
        self.dev_id = dev_id
        self.cal_param = cal_param

    def get_device(self, json_data, json_control):
        resp = json_data.json()
        resp_control = json_control.json()
        self.database_id = self.get_id(resp, CONFIG['SM']['DATASET'])
        #self.device = self.set_dev(self.dev)
        self.control_id = self.get_id(resp_control, CONFIG['VALVE']['NAME'])
        #self.dev_id = self.get_id(self.get_json(), self.device)

    def get_id(self, json, id): #id = Nama variabel untuk yang ingin dicari id nya
        arr = []
        dev_id = []
        
        for i in range (len(json)):
            arr.append(json[i]['name'])

        for i in id:
            num = arr.index(i)
            for id in {'_id', 'device_id', 'control_id'}:
                try:
                    dev_id.append(json[num][id])
                except KeyError:
                    continue
            
        return tuple(dev_id)

    def get_json(self):
        jsondev = requests.get(CONFIG['GETDATA']['urlSensor'] +'/'+ self.database_id[0] + '/device', headers = CONFIG['HEADERS'])
        jsondev = jsondev.json()
        
        return jsondev

    def get_value(self):
        val = []
        Value = []
        for n in range (len(self.dev_id)):
            value = []
            for i in range (len(self.database_id)):
                if (n == 0) or (n == 2):
                    resp_value = requests.get(CONFIG['GETDATA']['urlSensor']+'/'+self.database_id[1]+'/'+ self.dev_id[n], headers = CONFIG['HEADERS'])
                else:
                    resp_value = requests.get(CONFIG['GETDATA']['urlSensor']+'/'+self.database_id[i]+'/'+ self.dev_id[n], headers = CONFIG['HEADERS'])
                value.append(resp_value.json()[-1])
            Value.append(value)
        
        Value = self.sort_v(Value)
        
        for i in range (len(Value)) :
            #val_sensor = self.calibrate(Value[i]['value'], i)
            #val.append(np.round(val_sensor, decimals=0))
            val.append(Value[i]['value'])

        return val

    def find(self, s, el):
        for i in range(len(s)):
            if s[i] == el: 
                return i
        return None

    def detect_outlier(self, data_sensor):
        outliers = []
        threshold = 1.4
        mean_1 = np.mean(data_sensor)
        std_1 =np.std(data_sensor)
        
        for y in data_sensor:
            if std_1 == 0:
                break
            else:
                z_score= (y - mean_1)/std_1 
                if np.abs(z_score) > threshold:
                    outliers.append(y)
                
        if len(outliers)!= 0:
            data_sensor.pop(self.find(data_sensor,outliers[0]))

    def filter_sensor(self, sensor_read):
        read = []
        for i in range(3):
            box = []
            for n in range(3):
                box.append(sensor_read[3*i+(n)])
            
            Box = box.copy()
            self.detect_outlier(Box)
            
            read.append(np.mean(Box))
            
        sensorRead = read

        return sensorRead

    def sort_v(self, value):
        val = []
        for i in range (len(self.dev_id)):
            for n in range (len(self.database_id)):
                val.append(value[i][n])
            
        return val

    def set_dev(self, dev):
        device = []
        for i in dev:
            device.append('[PPKI] [New! Outdoor] Soil Moisture '+str(i))
            
        return device

    def calibrate(self, val, i):
        if val == 1024:
            cal_value = 100
        else:
            cal_value = (self.cal_param[i][1] - val)/(self.cal_param[i][1]-self.cal_param[i][0])*100
            if cal_value > 100:
                cal_value = 100
            elif cal_value < 0:
                cal_value = 0
        
        return cal_value

    


    


