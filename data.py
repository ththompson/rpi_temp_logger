#!/usr/bin/env python

import sqlite3

# global variables
speriod=(15*60)-1

dbname='/var/www/html/templogmulti.db'

# display the contents of the database
def display_data():
    print "Checking DB..."
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    for row in curs.execute("SELECT * FROM temps"):
        print str(row[0])+"	"+str(row[1]) +" | "+str(row[2]) +" | "+str(row[3]) 

    conn.close()

# main function
# This is where the program starts 
def main():

    # display the contents of the database
    display_data()


if __name__=="__main__":
    main()

