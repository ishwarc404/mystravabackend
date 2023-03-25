#export PATH=$PATH:/usr/local/mysql/bin
#mysql -u root -p            

import json
from peewee import *
import random
#database name is: mystravabackend

db = MySQLDatabase('mystravabackend', host='localhost', port=3306, user='root', password='password')

class athletePrimary(Model):
    athleteID = TextField() 
    athleteFirstName = TextField()
    athleteLastName = TextField()
    athleteImage = TextField()
    athleteCity = TextField()
    athleteState = TextField()
    
    class Meta:
        database=db
        db_table='athletePrimary'


def setUpAthletePrimaryTable():
    db.connect()
    db.create_tables([athletePrimary])

def tearDownAthletePrimaryTable():
    db.connect()
    db.drop_tables([athletePrimary])


def writeToAthletePrimary(athleteID, athleteFirstName, athleteLastName, athleteImage, athleteCity, athleteState):
    q = athletePrimary.insert(athleteID=athleteID, athleteFirstName=athleteFirstName, athleteLastName=athleteLastName, athleteImage=athleteImage, athleteCity=athleteCity, athleteState=athleteState)
    q.execute()


#run only once while set-up
if(__name__ == "__main__"):
    # setupAthleteActivityTable()
    pass