from time import sleep
import threading
import urllib.request
import json
import time
from datetime import datetime
import csv
import matplotlib.pyplot as plt
import numpy as np
# new_data= np.array([0.0,0.0])
# new_data= [0,0]
reading={'lat1':0.0,'lon1':0.0,'tms':" ",'dt':" ",'lat':" ",'lon':" "}

def DMS(Decimal):
    d = int(Decimal)#we get degrees
    m = int((Decimal - d) * 60)#we get minutes
    s = (Decimal - d - m/60) * 3600.00#we get seconds
    z= round(s, 2) #rounding s 
    if d >= 0:
        return str("N "+ str(abs(d))+ "º "+ str(abs(m))+ "' "+ str(abs(z))+ '" ')# for positive N
    else:
        return str("S "+ str(abs(d))+ "º "+ str(abs(m))+ "' "+ str(abs(z))+ '" ')# for negative S

def read():
    now = datetime.now()
    reading['dt'] = now.strftime("%d/%m/%Y %H:%M:%S")# get date and time
    req = 'http://api.open-notify.org/iss-now.json'
    response = urllib.request.urlopen(req)
    obj = json.loads(response.read())
    reading['tms']=str(obj['timestamp'])# get timestamp
    reading['lat1']= float(obj['iss_position']['latitude'])
    reading['lon1']= float(obj['iss_position']['longitude'])
    reading['lat']=DMS(reading['lat1'])# get latitude in DMS
    reading['lon']=DMS(reading['lon1'])# get longitude in DMS
    time.sleep(1)

def write(writer,tms,dt,lat,lon):
    print([tms,dt,lat,lon])
    writer.writerow([tms,dt,lat,lon])
    time.sleep(3) #create new row
    


def visualize(hl, new_data):
    print(new_data)
    hl.set_xdata(np.append(hl.get_xdata(), new_data[0]))
    hl.set_ydata(np.append(hl.get_ydata(), new_data[1]))
    ax = plt.gca()
    # recompute the ax.dataLim
    ax.relim()
    # update ax.viewLim using the new dataLim
    ax.autoscale_view()
    plt.draw()        # draw new data
    plt.pause(0.5)
    time.sleep(5)    # update graph every 0.5 second



with open('data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Timestamp", "Date and  Time", "Latitute","Longitude"])
    hl, = plt.plot([], []) #empty plot
    plt.title('Space station Coordinates')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    while 1 : #the loop creates a new csv row and updates the values every 5 seconds
        t1 = threading.Thread(target=read)
        t2 = threading.Thread(target=visualize,args=(hl,[reading['lon1'],reading['lat1']]))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        write(writer,reading['tms'],reading['dt'],reading['lat'],reading['lon'])
        # t1 = threading.Thread(target=read)
        # t2 = threading.Thread(target=visualize,args=(hl,[reading['lon1'],reading['lat1']]))
        # t3 =  threading.Thread(target=write,args=(writer,reading['tms'],reading['dt'],reading['lat'],reading['lon']))
        # t1.start()
        # t2.start()
        # t3.start
        # t1.join()
        # t2.join()
        # t3.join()
        
        




