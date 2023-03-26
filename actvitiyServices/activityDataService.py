import json
from peewee import *
import random
import gpxParserService.gpxparser
#database name is: mystravabackend
from kafka import KafkaProducer, KafkaConsumer


# create a Kafka consumer
create_consumer = KafkaConsumer('create-activity-via-gpx', bootstrap_servers=['localhost:9092'])

def createActivityViaGPX(uploadedFile):
    results = gpxParserService.gpxparser.parsefile(uploadedFile)
    print(results)



if __name__ == '__main__':
    while True:
        # read messages from the 'create-athlete' topic
        for message in create_consumer:
            uploadedFile = message.value
            createActivityViaGPX(uploadedFile)