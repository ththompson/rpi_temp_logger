#!/usr/bin/env python

import sqlite3

import os
import time
import glob

# global variables
speriod=(15*60)-1
#dbname='/var/www/templog.db'
dbname='/var/www/html/templogmulti.db'


# store the temperature in the database
def log_temperature(temp1,temp2,temp3 ):
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()
    curs.execute("INSERT INTO temps values(datetime('now'), (?), (?), (?))", (temp1,temp2,temp3))
    # commit the changes
    conn.commit()
    conn.close()


# display the contents of the database
def display_data():
    print "Checking DB..."
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    for row in curs.execute("SELECT * FROM temps"):
        print str(row[0])+"	"+str(row[1]) +" | "+str(row[2]) +" | "+str(row[3]) 

    conn.close()


# get temerature
# returns None on error, or the temperature as a float
def get_temp(devicefile):

    try:
        fileobj = open(devicefile,'r')
        lines = fileobj.readlines()
        fileobj.close()
    except:
        return None

    # get the status from the end of line 1 
    status = lines[0][-4:-1]

    # is the status is ok, get the temperature from line 2
    if status=="YES":
        print status
        tempstr= lines[1][-6:-1]
        tempvalue=float(tempstr)/1000
        print tempvalue
        return tempvalue
    else:
        print "There was an error."
        return None



# main function
# This is where the program starts 
def main():

    # enable kernel modules
    os.system('sudo modprobe w1-gpio')
    os.system('sudo modprobe w1-therm')

    # search for a device file that starts with 28
    devicelist = glob.glob('/sys/bus/w1/devices/28*')
    if devicelist=='':
        return None
    else:
        # append /w1slave to the device file
        w1devicefile1 = devicelist[0] + '/w1_slave'
        w1devicefile2 = devicelist[1] + '/w1_slave'
        w1devicefile3 = devicelist[2] + '/w1_slave'


    # get the temperatureS from the device fileS
    temperature1 = get_temp(w1devicefile1)
    temperature2 = get_temp(w1devicefile2)
    temperature3 = get_temp(w1devicefile3)

    if temperature1 != None or temperature2 != None or temperature3 != None:
        print "|"+str(temperature1) + " | " +str(temperature2) + " | "+str(temperature3) + " | "
    else:
        # Sometimes reads fail on the first attempt
        # so we need to retry
        temperature1 = get_temp(w1devicefile1)
        temperature2 = get_temp(w1devicefile2)
        temperature3 = get_temp(w1devicefile3)
        print "|"+str(temperature1) + " | " +str(temperature2) + " | "+str(temperature3) + " | "
        # Store the temperature in the database
    
    log_temperature(temperature1, temperature2, temperature3 )

    # display the contents of the database
    display_data()



if __name__=="__main__":
    main()

