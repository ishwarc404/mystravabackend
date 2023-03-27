from flask import Flask
import json
from flask import request
import random
from flask_cors import CORS,cross_origin
import uuid
from athleteObject import athletePrimary
import athleteDataService

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
    athleteObject['athleteClubs']= request.args.get('athleteClubs')
    athleteObject['athleteFollowers']= request.args.get('athleteFollowers')
    athleteObject['athleteFollowing']= request.args.get('athleteFollowing')
    athleteObject['athleteNetDistance']= request.args.get('athleteNetDistance')
    athleteObject['athleteNetTime']= request.args.get('athleteNetTime')
    athleteObject['athleteNetElevation']= request.args.get('athleteNetElevation')


    athleteObject['kafka_type'] = 'create_athlete' #to distinguish from other kafka messages

    #writing to database
    producer.send('athlete-service', json.dumps(athleteObject).encode('utf-8'))
    producer.flush()

    return athleteID


@app.route('/retrieveAthlete', methods=['GET'])
def retrieveAthlete():
    #this will be blocking, because not using kafka but ok for now
    athleteID = request.args.get('athleteID')
    #reading from database
    retrievedAthleteData = athleteDataService.readFromAthletePrimary(athleteID)
    return json.dumps(retrievedAthleteData)


@app.route('/joinClub', methods=['POST'])
def joinClub():
    #this will be blocking, because not using kafka but ok for now
    athleteID = request.args.get('athleteID')
    clubID = request.args.get('clubID')
    #reading from database
    athleteDataService.joinClub(clubID, athleteID)
    #updating club statistics
    return clubID


if(__name__ == "__main__"):
    app.run(debug=True, port=5005)
    # print(generateAthleteID())
    pass

