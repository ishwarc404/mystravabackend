import json
from peewee import *
import random
# import gpxparser
# from activityObject import activityPrimary
#database name is: mystravabackend
from kafka import KafkaProducer, KafkaConsumer


db = MySQLDatabase('mystravabackend', host='localhost', port=3306, user='root', password='password')


class clubPrimary (Model):
    clubID=TextField()
    clubdName=TextField()
    clubOwnerAthleteID=TextField()
    class Meta:
        database=db
        db_table='clubPrimary'

class clubSecondary (Model):
    clubID=TextField()
    clubTotalDistance = TextField()
    clubTotalTime = TextField()
    clubTotalAthletes = TextField()
    clubLeaderBoard = TextField() #this is where the top 10 athletes will live
    class Meta:
        database=db
        db_table='clubSecondary'


def setUpClubTable():
    db.connect()
    db.create_tables([clubPrimary, clubSecondary])

def tearDownClubTable():
    db.connect()
    db.drop_tables([clubPrimary, clubSecondary])


"""
We also need to check if club is actually in user's club list

When ever a user uploads an activity, their time, distance and elevation is calculated.
^ this is calculated and stored , in athleteDataService code
We then get get the user's totals from athleteSecondary database and :
    - check if user is in top 10 of club
        - if not: compare it with the 10th guy, and see if it is higher or lower
        - if yes, increase and resort the top 10
"""

# create a Kafka consumer

if __name__ == '__main__':
    club_consumer = KafkaConsumer('club-service', bootstrap_servers=['localhost:9092'])

    while True:
        print("Club Service Started")
        for message in club_consumer:
            print("Received in club service:")
            athleteID = json.loads(message.value)['athleteID']
            print(athleteID)
            break

        if(athleteID):
            pass
