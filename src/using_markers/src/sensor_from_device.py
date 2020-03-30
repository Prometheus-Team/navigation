import urllib, json
import time

URL = "http://192.168.0.102:8080/sensors.json"
FREQ = 3 # Hertz

def main():
    while True:
        response = urllib.urlopen(URL)

        data = json.loads(response.read())

        nData = {}
        nData['accel'] = data['accel']
        nData['gyro'] = data['gyro']
        nData['lin_accel'] = data['lin_accel']
        nData['rot_vector'] = data['rot_vector']

        # publish sensor data to the topic
        # return nData

        time.sleep(1/FREQ)

if __name__=='__main__':
    main()