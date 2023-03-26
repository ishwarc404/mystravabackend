from peewee import *

db = MySQLDatabase('mystravabackend', host='localhost', port=3306, user='root', password='password')



class athletePrimary(Model):
    athleteID = TextField() 
    athleteFirstName = TextField()
    athleteLastName = TextField()
    athleteImage = TextField()
    athleteCity = TextField()
    athleteState = TextField()
    
    class Meta:
        database=db
        db_table='athletePrimary'


class athleteSecondary(Model):
    athleteID = TextField() 
    athleteClubs = TextField()
    athleteFollowers = TextField()
    athleteFollowing = TextField()
    athleteNetDistance = TextField()
    athleteNetTime = TextField()
    athleteNetElevation = TextField()
    
    class Meta:
        database=db
        db_table='athleteSecondary'
