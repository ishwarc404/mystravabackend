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
    clubName=TextField()
    clubOwnerAthleteID=TextField()
    class Meta:
        database=db
        db_table='clubPrimary'

class clubSecondary (Model):
    clubID=TextField()
    clubTotalDistance = FloatField()
    clubTotalTime = FloatField()
    clubTotalElevationGain = IntegerField()
    clubTotalAthletes = IntegerField()
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

def createClubPrimary(clubID, clubName, clubOwnerAthleteID):
    q = clubPrimary.insert(clubID=clubID,clubName=clubName, clubOwnerAthleteID=clubOwnerAthleteID)
    q.execute()

    createClubSecondary(clubID)

def createClubSecondary(clubID):
    clubTotalDistance = 0
    clubTotalTime = 0
    clubTotalElevationGain = 0
    clubTotalAthletes = 0
    clubLeaderBoard = ''
    q = clubSecondary.insert(clubID=clubID,clubTotalDistance=clubTotalDistance, 
    clubTotalTime=clubTotalTime, clubTotalElevationGain = clubTotalElevationGain,
    clubTotalAthletes = clubTotalAthletes, clubLeaderBoard=clubLeaderBoard)
    q.execute()

def checkIfClubExists(clubID):
    #we can use this from the athleteService to check if it exists before the user adds it to their secondary table
    pass

def updateUserClubs(dataObject):
    athleteID = dataObject['athleteID']

    #this is to get athlete totals - will be used for leaderboard
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
    
    #we also have athlete individuals
    
    #now that we have a list of clubs, we can go through them one by one and one and update it with the user's details
    for eachClubID in athleteClubs:
        #here we need to check if those clubIDs are real and if the user is actually a part of those clubs
        print("Club we are updating is: ", eachClubID)
        #more logic to come,
        #let's update the club totals first
        #let's get the club details
        clubRows = clubSecondary.select().where(clubSecondary.clubID == eachClubID)
            
        print(dataObject)
        #we add the activity stats to it
        q = clubSecondary.update({
            clubSecondary.clubTotalDistance : clubSecondary.clubTotalDistance + dataObject['activityDistance'],
            clubSecondary.clubTotalTime : clubSecondary.clubTotalTime + dataObject['activityTime'],
            clubSecondary.clubTotalElevationGain : clubSecondary.clubTotalElevationGain + dataObject['activityElevation'],
        }).where(clubSecondary.clubID == eachClubID)

        q.execute()










if __name__ == '__main__':


    # RUN THE FOLLOWING ONLY ONCE, OR ELSE REPEATED ROWS!
    # setUpClubTable()
    # createClubPrimary(1,'First Club', '971753') #also creates secondary automatically
    # createClubPrimary(2,'Second Club', '971753')
    # createClubPrimary(3,'Third Club', '971753')
    # createClubPrimary(4,'Fourth Club', '174831')
    # createClubPrimary(5,'Fifth Club', '174831')

    # create a Kafka consumer
    club_consumer = KafkaConsumer('club-service', bootstrap_servers=['localhost:9092'])

    while True:
        for message in club_consumer:
            print("Received in club service")
            dataObject = json.loads(message.value)
            break

        if(dataObject):
            updateUserClubs(dataObject)
