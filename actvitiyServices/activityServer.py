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

@app.route('/uploadActivityFile', methods=['POST'])
def upload_file():
    
    athleteID = request.args.get('athleteID')
    #need to check if athleteID is valid or not

    activityID = generateActivityID()
    uploadedFile = request.files['gpxfile']

    uploadedFile.save('./uploadedFiles/' + activityID)

    # #sending it to ADS
    producer.send('create-activity-via-gpx-athleteID', json.dumps(
        {
            'athleteID':athleteID,
            'activityID':activityID
        }
    ).encode('utf-8'))
    # with open('./uploadedFiles/' + activityID, 'rb') as file:
    #     file_data = file.read()
    # producer.send('create-activity-via-gpx-athleteID', file_data)
    producer.flush()

    return activityID



if(__name__ == "__main__"):
    app.run(debug=True, port=5006)
    pass

