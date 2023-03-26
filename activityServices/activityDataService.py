import json
from peewee import *
import random
import gpxparser
from activityObject import activityPrimary
#database name is: mystravabackend
from kafka import KafkaProducer, KafkaConsumer

# create a Kafka producer
producer = KafkaProducer(bootstrap_servers=['localhost:9092'])


db = MySQLDatabase('mystravabackend', host='localhost', port=3306, user='root', password='password')


class Activity (Model):
    athleteID=TextField()
    activityID=TextField()
    activityFieldName=TextField()
    activityFieldValue=TextField()
    class Meta:
        database=db
        db_table='athleteActivities'

def setUpActivtyTable():
    db.connect()
    db.create_tables([Activity])

def tearDownActivityTable():
    db.connect()
    db.drop_tables([Activity])



# create a Kafka consumer
create_consumer_athleteID = KafkaConsumer('create-activity-via-gpx-athleteID', bootstrap_servers=['localhost:9092'])
# create_consumer = KafkaConsumer('create-activity-via-gpx', bootstrap_servers=['localhost:9092'])


def createActivityViaGPX(athleteID, activityID):
    results = gpxparser.parsefile(activityID)
    activityObjectObj = activityPrimary(athleteID, activityID, results[0], 'Run', results[1], results[2], results[3], results[4], results[5].seconds).get()
    print(activityObjectObj)
    #need to write this to the database now
    for key in activityObjectObj.keys():
        q = Activity.insert(athleteID=athleteID,activityID=activityID, activityFieldName=key, activityFieldValue=activityObjectObj[key])
        q.execute()
    
    #now we need to update athleteSecondary database
    dataObject = {
        'kafka_type': 'update_athlete_secondary_activity_stat',
        'athleteID': athleteID,
        'activityDistance': results[1],
        'activityElevation': results[2],
        'activityTime': results[5].seconds, #need to convert this into seconds before adding it up
    }
    #writing to database - sending it to the athlete-service via kafka
    producer.send('athlete-service', json.dumps(dataObject).encode('utf-8'))
    #now we need to call club service
    producer.send('club-service', json.dumps(dataObject).encode('utf-8'))
    producer.flush()



if __name__ == '__main__':

    # setUpActivtyTable()
    #tearDownActivityTable()

    while True:
        # read messages from the 'create-activity-via-gpx' topic
        for message in create_consumer_athleteID:
            print(json.loads(message.value))
            athleteID = json.loads(message.value)['athleteID']
            activityID = json.loads(message.value)['activityID']
            print("Received 1:")
            print(athleteID, activityID)
            break

        # for message in create_consumer_athleteID:
        #     uploadedFile = message.value
        #     print("Received 2:")
        #     break


        if(athleteID):
            createActivityViaGPX(athleteID, activityID)