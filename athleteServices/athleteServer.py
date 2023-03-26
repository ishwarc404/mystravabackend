from flask import Flask
import json
from flask import request
import random
from flask_cors import CORS,cross_origin
import uuid
from athleteObject import athletePrimary
import athleteDatabaseService

from kafka import KafkaProducer, KafkaConsumer

#need to use gunicorn for non-blocking flask

# create a Kafka producer
producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

app = Flask(__name__)
cors = CORS(app)

def generateAthleteID():
    id = uuid.uuid1()
    return str(id.int)[0:6]

@app.route('/createAthlete', methods=['POST'])
def createAthlete():
    athleteID = generateAthleteID()
    #in the future we can add a check to see if the above athleteID already exists in the database or not
    athleteFirstName = request.args.get('athleteFirstName')
    athleteLastName = request.args.get('athleteLastName')
    athleteImage = request.args.get('athleteImage')
    athleteCity = request.args.get('athleteCity')
    athleteState = request.args.get('athleteState')
    athletePrimaryObject = athletePrimary(athleteID, athleteFirstName, athleteLastName, athleteImage, athleteCity, athleteState)
    
    #setting values for the secondary table - not setting part of the primaryObject
    #yeah looks funky but well, just need it to work for now
    athleteObject  = athletePrimaryObject.get()
    athleteObject['athleteClubs'] = athleteObject['athleteClubs']
    athleteObject['athleteFollowers'] = athleteObject['athleteFollowers']
    athleteObject['athleteFollowing'] = athleteObject['athleteFollowing']
    athleteObject['athleteNetDistance'] = athleteObject['athleteNetDistance']
    athleteObject['athleteNetTime'] = athleteObject['athleteNetTime']
    athleteObject['athleteNetElevation'] = athleteObject['athleteNetElevation']


    athleteObject['kafka_type'] = 'create_athlete' #to distinguish from other kafka messages

    #writing to database
    producer.send('athlete-service', json.dumps(athletePrimaryObject.get()).encode('utf-8'))
    producer.flush()

    return athleteID


@app.route('/retrieveAthlete', methods=['GET'])
def retrieveAthlete():
    #this will be blocking, because not using kafka but ok for now
    athleteID = request.args.get('athleteID')
    #reading from database
    retrievedAthleteData = athleteDatabaseService.readFromAthletePrimary(athleteID)
    return json.dumps(retrievedAthleteData)


if(__name__ == "__main__"):
    app.run(debug=True, port=5005)
    # print(generateAthleteID())
    pass

