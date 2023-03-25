#export PATH=$PATH:/usr/local/mysql/bin
#mysql -u root -p            

import json
from peewee import *
import random
#database name is: mystravabackend
import athleteObject

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


def writeToAthletePrimary(athletePrimaryObject):
    print(athletePrimaryObject.get())
    q = athletePrimary.insert(athleteID=athletePrimaryObject.athleteID, athleteFirstName=athletePrimaryObject.athleteFirstName, athleteLastName=athletePrimaryObject.athleteLastName, athleteImage=athletePrimaryObject.athleteImage, athleteCity=athletePrimaryObject.athleteCity, athleteState=athletePrimaryObject.athleteState)
    q.execute()


def readFromAthletePrimary(athleteID):
    rows = athletePrimary.select().where(athletePrimary.athleteID == athleteID)
    for each in rows:
        retrievedAthletePrimaryObject = athleteObject.athletePrimary(athleteID=each.athleteID, athleteFirstName=each.athleteFirstName, athleteLastName=each.athleteLastName, athleteImage=each.athleteImage, athleteCity=each.athleteCity, athleteState=each.athleteState)
    return retrievedAthletePrimaryObject.get()

#run only once while set-up
if(__name__ == "__main__"):
    # setUpAthletePrimaryTable()
    pass