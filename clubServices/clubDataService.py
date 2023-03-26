import json
from peewee import *
import random
# import gpxparser
# from activityObject import activityPrimary
#database name is: mystravabackend
from kafka import KafkaProducer, KafkaConsumer


db = MySQLDatabase('mystravabackend', host='localhost', port=3306, user='root', password='password')

class athleteSecondary(Model):
    athleteID = TextField() 
    athleteClubs = TextField()
    athleteFollowers = TextField()
    athleteFollowing = TextField()
    athleteNetDistance = FloatField()
    athleteNetTime = FloatField()
    athleteNetElevation = FloatField()

    class Meta:
        database=db
        db_table='athleteSecondary'


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

def updateUserClubs(athleteID):
    athleteSecondaryObjs = athleteSecondary.select().where(athleteSecondary.athleteID == athleteID)
    athleteNetDistance = 0
    athleteNetTime = 0
    athleteNetElevation = 0
    athleteClubs = ''
    for each in athleteSecondaryObjs:
        athleteNetDistance = each.athleteNetDistance
        athleteNetTime = each.athleteNetTime
        athleteNetElevation = each.athleteNetElevation
        athleteClubs = json.loads(each.athleteClubs)
    
    #now that we have a list of clubs, we can go through them one by one and one and update it with the user's details
    for clubID in athleteClubs:
        print("Club we are updating is: ", clubID)
        #more logic to come,




if __name__ == '__main__':

    # create a Kafka consumer
    club_consumer = KafkaConsumer('club-service', bootstrap_servers=['localhost:9092'])

    while True:
        for message in club_consumer:
            print("Received in club service")
            athleteID = json.loads(message.value)['athleteID']
            break

        if(athleteID):
            updateUserClubs(athleteID)
