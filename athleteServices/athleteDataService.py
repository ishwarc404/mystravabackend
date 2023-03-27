#export PATH=$PATH:/usr/local/mysql/bin
#mysql -u root -p            

import json
from peewee import *
import random
#database name is: mystravabackend
import athleteObject
from kafka import KafkaProducer, KafkaConsumer
import  athleteDatabaseModels
# create a Kafka consumer
create_consumer = KafkaConsumer('athlete-service', bootstrap_servers=['localhost:9092'])
# read_consumer = KafkaConsumer('read-athlete', bootstrap_servers=['localhost:9092'])


# create a Kafka producer
producer = KafkaProducer(bootstrap_servers=['localhost:9092'])



def setUpAthletePrimaryTable():
    athleteDatabaseModels.db.connect()
    athleteDatabaseModels.db.create_tables([athleteDatabaseModels.athletePrimary, athleteDatabaseModels.athleteSecondary])

def tearDownAthletePrimaryTable():
    athleteDatabaseModels.db.connect()
    athleteDatabaseModels.db.drop_tables([athleteDatabaseModels.athletePrimary, athleteDatabaseModels.athleteSecondary])


def writeToAthletePrimary(athletePrimaryObject):
    print("Populating Athlete Primary:", athletePrimaryObject['athleteID'])
    q = athleteDatabaseModels.athletePrimary.insert(athleteID=athletePrimaryObject['athleteID'], athleteFirstName=athletePrimaryObject['athleteFirstName'], athleteLastName=athletePrimaryObject['athleteLastName'], athleteImage=athletePrimaryObject['athleteImage'], athleteCity=athletePrimaryObject['athleteCity'], athleteState=athletePrimaryObject['athleteState'])
    q.execute()

    athleteSecondaryObject = {
        'athleteID' : athletePrimaryObject['athleteID'],
        'athleteClubs' : athletePrimaryObject['athleteClubs'],
        'athleteFollowers' : athletePrimaryObject['athleteFollowers'],
        'athleteFollowing' : athletePrimaryObject['athleteFollowing'],
        'athleteNetDistance' : athletePrimaryObject['athleteNetDistance'],
        'athleteNetTime' : athletePrimaryObject['athleteNetTime'],
        'athleteNetElevation' : athletePrimaryObject['athleteNetElevation'],
    }
    writeToAthleteSecondary(athleteSecondaryObject)

def writeToAthleteSecondary(athleteSecondaryObject):
    print("Populating Athlete Secondary:", athleteSecondaryObject['athleteID'])
    q = athleteDatabaseModels.athleteSecondary.insert(
        athleteID=athleteSecondaryObject['athleteID'], 
        athleteClubs = athleteSecondaryObject['athleteClubs'], #this will be an array in string form
        athleteFollowers = athleteSecondaryObject['athleteFollowers'], #this will be an array in string form
        athleteFollowing = athleteSecondaryObject['athleteFollowing'], #this will be an array in string form
        athleteNetDistance = athleteSecondaryObject['athleteNetDistance'],
        athleteNetTime = athleteSecondaryObject['athleteNetTime'],
        athleteNetElevation = athleteSecondaryObject['athleteNetElevation'],
    )
    q.execute()



def updateAthleteSecondaryActivityStat(stats):
    #we need to find the right athleteID and add the stats to their current stat
    #we are not doing weekly, just overall since beginning of time
    
    q = athleteDatabaseModels.athleteSecondary.update({
        athleteDatabaseModels.athleteSecondary.athleteNetDistance : athleteDatabaseModels.athleteSecondary.athleteNetDistance + stats['activityDistance'],
        athleteDatabaseModels.athleteSecondary.athleteNetTime : athleteDatabaseModels.athleteSecondary.athleteNetTime + stats['activityTime'],
        athleteDatabaseModels.athleteSecondary.athleteNetElevation : athleteDatabaseModels.athleteSecondary.athleteNetElevation + stats['activityElevation'],
    }).where(athleteDatabaseModels.athleteSecondary.athleteID == stats['athleteID'])

    q.execute()
    
    pass


def readFromAthletePrimary(athleteID):
    rows = athleteDatabaseModels.athletePrimary.select().where(athleteDatabaseModels.athletePrimary.athleteID == athleteID)
    for each in rows:
        retrievedAthletePrimaryObject = athleteObject.athletePrimary(athleteID=each.athleteID, athleteFirstName=each.athleteFirstName, athleteLastName=each.athleteLastName, athleteImage=each.athleteImage, athleteCity=each.athleteCity, athleteState=each.athleteState)
    return retrievedAthletePrimaryObject.get()


def joinClub(clubID,athleteID):
    rows = athleteDatabaseModels.athleteSecondary.select().where(athleteDatabaseModels.athleteSecondary.athleteID == athleteID)
    for row in rows:
        athleteClubs = json.loads(row.athleteClubs)
        break

        
    if(clubID not in athleteClubs):
        athleteClubs.append(int(clubID))
    
    #let's put back this new club list into the database
    q = athleteDatabaseModels.athleteSecondary.update({
        athleteDatabaseModels.athleteSecondary.athleteClubs : athleteClubs
    }).where(athleteDatabaseModels.athleteSecondary.athleteID == athleteID)    

    q.execute()
    dataObject = {
        'kafka_type' : 'club-service-new-athlete',
        'athleteID' : athleteID,
        'clubID' : clubID
    }
    producer.send('club-service', json.dumps(dataObject).encode('utf-8'))
    producer.flush()


#run only once while set-up
if(__name__ == "__main__"):
    setUpAthletePrimaryTable()
    while(True):
        # read messages from the 'create-athlete' topic
        for message in create_consumer:
            dataObject = json.loads(message.value)
            if(dataObject['kafka_type'] == 'create_athlete'):
                writeToAthletePrimary(dataObject)
            elif (dataObject['kafka_type'] == 'update_athlete_secondary_activity_stat'):
                updateAthleteSecondaryActivityStat(dataObject)
