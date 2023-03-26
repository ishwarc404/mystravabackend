from flask import Flask
import json
from flask import request
import random
from flask_cors import CORS,cross_origin
import uuid
from kafka import KafkaProducer, KafkaConsumer

#need to use gunicorn for non-blocking flask


#first start server, then 
#open -a Google\ Chrome --args --disable-web-security --/

# create a Kafka producer
producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

app = Flask(__name__)
cors = CORS(app)

def generateActivityID():
    id = uuid.uuid1()
    return str(id.int)[0:8]

# def queryAllActivities(currentSportType, currentAthleteId, currentActivityType):

#     return dbaccess.readAllAthleteActivities(currentSportType,currentAthleteId, currentActivityType)

#     #commenting the following out and switching to db
#     with open('./importedData.json') as f:
#         data = json.load(f)
#     return data




# @app.route('/getAllActivities')
# @cross_origin()
# def getAllActivities():
#     currentSportType = request.args.get('currentSportType')
#     currentAthleteId = request.args.get('currentAthleteId')
#     currentActivityType = request.args.get('currentActivityType')
#     print(currentSportType)
#     response = json.dumps(queryAllActivities(currentSportType, currentAthleteId, currentActivityType))
#     return response
    

@app.route('/uploadActivityFile', methods=['POST'])
def upload_file():
    activityID = generateActivityID()
    uploadedFile = request.files['gpxfile']
    uploadedFile.save('./uploadedFiles/' + uploadedFile.filename)

    #sending it to ADS
    producer.send('create-activity-via-gpx', value = uploadedFile)
    producer.flush()

    return activityID



if(__name__ == "__main__"):
    app.run(debug=True, port=5006)
    pass

