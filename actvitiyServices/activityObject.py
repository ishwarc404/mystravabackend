class activityPrimary:
    def __init__(self, athleteID, activtiyID, activityName, activityType, activityDistance, activityElevationGain, activityPolyline, activityStartTime, activityElapsedTime):
        self.athleteID = athleteID
        self.activtiyID = activtiyID
        self.activityName = activityName
        self.activityType = activityType
        self.activityDistance = activityDistance
        self.activityElevationGain = activityElevationGain
        self.activityPolyline = activityPolyline
        self.activityStartTime = activityStartTime
        self.activityElapsedTime = activityElapsedTime

    def get(self):
        return {
        'athleteID' : self.athleteID,
        'activtiyID' : self.activtiyID,
        'activityName' : self.activityName,
        'activityType' : self.activityType,
        'activityDistance' : self.activityDistance,
        'activityElevationGain' : self.activityElevationGain,
        'activityPolyline' : self.activityPolyline,
        'activityStartTime' : self.activityStartTime,
        'activityElapsedTime' : self.activityElapsedTime,
        }