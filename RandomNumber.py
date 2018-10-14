import threading
import time
import random
import matplotlib.pyplot as plt
from influxdb import InfluxDBClient
from datetime import datetime as dt

class Random_Number:

    def generate_random_values(self):
        dbname = 'sensorsdata'
        dbclient = InfluxDBClient('localhost',8086,'admin','admin',dbname)
        dblist = dbclient.get_list_database()
        db_found = False
        for db in dblist:
            if db['name'] == dbname:
                db_found=True
        if not(db_found):
            dbclient.create_database(dbname)
        r = random.sample(range(1,101),5)
        dbclient = InfluxDBClient('localhost',8086,'admin','admin',dbname)
        for i in range(len(r)):
            json_body = [
            {
                "measurement": "sensordata",
                "fields": 
                {
                    "value": r[i]
                }
            }]
            dbclient.write_points(json_body)
            time.sleep(1)

    def plot_data(self):
        dbclient = InfluxDBClient('localhost',8086,'admin','admin','sensorsdata')
        result = dbclient.query('select time,value from sensordata')
        points = result.get_points()
        times=[]
        value =[]
        tl=[]
        for point in points:
            times.append(point['time'])
            value.append(point['value'])
        print(times)
        for t in times:
            a = t.split('.',1)
            tl.append(a[0])
        plt.plot(tl,value)
        plt.show()
        #print(tl)

if __name__=='__main__':
    t = time.time()
    r = Random_Number()
    r.generate_random_values()
    r.plot_data()
    print(time.time()-t)