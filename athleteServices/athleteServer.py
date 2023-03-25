from flask import Flask
import json
from flask import request
import random
from flask_cors import CORS,cross_origin
import uuid
from athleteObject import athletePrimary
import athleteDatabaseService

app = Flask(__name__)
cors = CORS(app)

def generateAthleteID():
    id = uuid.uuid1()
    return str(id.int)[0:6]

@app.route('/createAthlete', methods=['POST'])
def upload_file():
    athleteID = generateAthleteID()
    athleteFirstName = request.args.get('athleteFirstName')
    athleteLastName = request.args.get('athleteLastName')
    athleteImage = request.args.get('athleteImage')
    athleteCity = request.args.get('athleteCity')
    athleteState = request.args.get('athleteState')
    athleteSubscription = request.args.get('athleteSubscription')
    athletePrimaryObject = athletePrimary(athleteID, athleteFirstName, athleteLastName, athleteImage, athleteCity, athleteState)
    
    #writing to database
    athleteDatabaseService.writeToAthletePrimary(athletePrimaryObject.get())


if(__name__ == "__main__"):
    # app.run(debug=True, port=5005)
    # print(generateAthleteID())
    pass

