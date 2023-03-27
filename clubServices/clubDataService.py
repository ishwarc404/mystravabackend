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
    clubLeaderBoard = { 'elevationLeaderboard': [], 'distanceLeaderBoard': [], 'timeLeaderBoard': []} #set of tuple values (athleteID, activityValue) 
    clubLeaderBoard = json.dumps(clubLeaderBoard)
    q = clubSecondary.insert(clubID=clubID,clubTotalDistance=clubTotalDistance, 
    clubTotalTime=clubTotalTime, clubTotalElevationGain = clubTotalElevationGain,
    clubTotalAthletes = clubTotalAthletes, clubLeaderBoard=clubLeaderBoard)
    q.execute()

def checkIfClubExists(clubID):
    #we can use this from the athleteService to check if it exists before the user adds it to their secondary table
    pass

def updateClubAfterAthleteAdded(athleteID, clubID):
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
    #we also have athlete individuals
    
    #now that we have a list of clubs, we can go through them one by one and one and update it with the user's details
    #here we need to check if those clubIDs are real and if the user is actually a part of those clubs
    print("Club we are updating is: ", clubID)
    #more logic to come,
    #let's update the club totals first
        
    print(dataObject)
    #we add the activity stats to it

    #we even need to update the club leaderboard
    #let's get the leaderboards first
    clubDetails = clubSecondary.select().where(clubSecondary.clubID == clubID)
    #there will be only one row
    finalLeaderBoards = []
    for row in clubDetails:
        currentLeaderboard = json.loads(row.clubLeaderBoard)                        
        elevationLeaderboard = currentLeaderboard['elevationLeaderboard'] #set of tuple values (athleteID, activityValue)
        distanceLeaderBoard = currentLeaderboard['distanceLeaderBoard']
        timeLeaderBoard = currentLeaderboard['timeLeaderBoard']
        leaderBoards = [elevationLeaderboard, distanceLeaderBoard, timeLeaderBoard]
        currentAthleteValues = [athleteNetElevation, athleteNetDistance, athleteNetTime]

        for eachLeaderboardIndex in range(0,len(leaderBoards)):
            if(len(leaderBoards[eachLeaderboardIndex]) != 0):
                #assuming athlete is already not in the leaderboard
                athletesInLeaderboard = [i for i, j in leaderBoards[eachLeaderboardIndex]]
                if(athleteID not in athletesInLeaderboard):
                    leaderBoards[eachLeaderboardIndex] = sorted(leaderBoards[eachLeaderboardIndex], key=lambda tup: tup[1], reverse=True) #sorting based on 2nd value which is the acvity value
                    if(currentAthleteValues[eachLeaderboardIndex] > leaderBoards[eachLeaderboardIndex][-1][1]):
                        leaderBoards[eachLeaderboardIndex].append((athleteID, currentAthleteValues[eachLeaderboardIndex]))
                    else:
                        if(len(leaderBoards[eachLeaderboardIndex]) < 10):
                            #if there aren't 10 spots already filled
                            leaderBoards[eachLeaderboardIndex].append((athleteID, currentAthleteValues[eachLeaderboardIndex]))
                        else:
                            #if there already are 10 spotsa filled, we do not do anything
                            pass
                else:
                    #if athelete is already part of the leaderboard, we just update his value and sort the list
                    tupleIndex = [x for x, y in enumerate(leaderBoards[eachLeaderboardIndex]) if y[0] == athleteID][0]
                    #replacing it with new value
                    leaderBoards[eachLeaderboardIndex][tupleIndex] = (athleteID, currentAthleteValues[eachLeaderboardIndex])
                    #sorting the list again
                    leaderBoards[eachLeaderboardIndex] = sorted(leaderBoards[eachLeaderboardIndex], key=lambda tup: tup[1], reverse=True) #sorting based on 2nd value which is the acvity value
            
            else:
                #if there are no other athlete values
                leaderBoards[eachLeaderboardIndex].append((athleteID, currentAthleteValues[eachLeaderboardIndex]))

            
            finalLeaderBoards.append(sorted(leaderBoards[eachLeaderboardIndex], key=lambda tup: tup[1], reverse=True))

    leaderBoardObject = {
        'elevationLeaderboard': finalLeaderBoards[0],
        'distanceLeaderBoard': finalLeaderBoards[1],
        'timeLeaderBoard': finalLeaderBoards[2]
    }
    leaderBoardObject = json.dumps(leaderBoardObject)


    #finally updating it all
    q = clubSecondary.update({
        clubSecondary.clubTotalDistance : clubSecondary.clubTotalDistance + athleteNetDistance,
        clubSecondary.clubTotalTime : clubSecondary.clubTotalTime + athleteNetTime,
        clubSecondary.clubTotalElevationGain : clubSecondary.clubTotalElevationGain + athleteNetElevation,
        clubSecondary.clubLeaderBoard : leaderBoardObject,
    }).where(clubSecondary.clubID == clubID)



    q.execute()

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
            
        print(dataObject)
        #we add the activity stats to it

        #we even need to update the club leaderboard
        #let's get the leaderboards first
        clubDetails = clubSecondary.select().where(clubSecondary.clubID == eachClubID)
        #there will be only one row
        finalLeaderBoards = []
        for row in clubDetails:
            currentLeaderboard = json.loads(row.clubLeaderBoard)                        
            elevationLeaderboard = currentLeaderboard['elevationLeaderboard'] #set of tuple values (athleteID, activityValue)
            distanceLeaderBoard = currentLeaderboard['distanceLeaderBoard']
            timeLeaderBoard = currentLeaderboard['timeLeaderBoard']
            leaderBoards = [elevationLeaderboard, distanceLeaderBoard, timeLeaderBoard]
            currentAthleteValues = [athleteNetElevation, athleteNetDistance, athleteNetTime]

            for eachLeaderboardIndex in range(0,len(leaderBoards)):
                if(len(leaderBoards[eachLeaderboardIndex]) != 0):
                    #assuming athlete is already not in the leaderboard
                    athletesInLeaderboard = [i for i, j in leaderBoards[eachLeaderboardIndex]]
                    if(athleteID not in athletesInLeaderboard):
                        leaderBoards[eachLeaderboardIndex] = sorted(leaderBoards[eachLeaderboardIndex], key=lambda tup: tup[1], reverse=True) #sorting based on 2nd value which is the acvity value
                        if(currentAthleteValues[eachLeaderboardIndex] > leaderBoards[eachLeaderboardIndex][-1][1]):
                            leaderBoards[eachLeaderboardIndex].append((athleteID, currentAthleteValues[eachLeaderboardIndex]))
                        else:
                            if(len(leaderBoards[eachLeaderboardIndex]) < 10):
                                #if there aren't 10 spots already filled
                                leaderBoards[eachLeaderboardIndex].append((athleteID, currentAthleteValues[eachLeaderboardIndex]))
                            else:
                                #if there already are 10 spotsa filled, we do not do anything
                                pass
                    else:
                        #if athelete is already part of the leaderboard, we just update his value and sort the list
                        tupleIndex = [x for x, y in enumerate(leaderBoards[eachLeaderboardIndex]) if y[0] == athleteID][0]
                        #replacing it with new value
                        leaderBoards[eachLeaderboardIndex][tupleIndex] = (athleteID, currentAthleteValues[eachLeaderboardIndex])
                        #sorting the list again
                        leaderBoards[eachLeaderboardIndex] = sorted(leaderBoards[eachLeaderboardIndex], key=lambda tup: tup[1], reverse=True) #sorting based on 2nd value which is the acvity value
                
                else:
                    #if there are no other athlete values
                    leaderBoards[eachLeaderboardIndex].append((athleteID, currentAthleteValues[eachLeaderboardIndex]))

                
                finalLeaderBoards.append(leaderBoards[eachLeaderboardIndex])

        leaderBoardObject = {
            'elevationLeaderboard': finalLeaderBoards[0],
            'distanceLeaderBoard': finalLeaderBoards[1],
            'timeLeaderBoard': finalLeaderBoards[2]
        }
        leaderBoardObject = json.dumps(leaderBoardObject)


        #finally updating it all
        q = clubSecondary.update({
            clubSecondary.clubTotalDistance : clubSecondary.clubTotalDistance + dataObject['activityDistance'],
            clubSecondary.clubTotalTime : clubSecondary.clubTotalTime + dataObject['activityTime'],
            clubSecondary.clubTotalElevationGain : clubSecondary.clubTotalElevationGain + dataObject['activityElevation'],
            clubSecondary.clubLeaderBoard : leaderBoardObject,
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

        if(dataObject['kafka_type'] == 'club-service-existing-athlete'):
            updateUserClubs(dataObject)
        elif(dataObject['kafka_type'] == 'club-service-new-athlete'):
            updateClubAfterAthleteAdded(dataObject['athleteID'], dataObject['clubID'])
