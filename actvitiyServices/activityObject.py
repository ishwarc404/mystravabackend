class activityPrimary:
    def __init__(self, athleteID, activtiyID, activityName, activityType, activityDistance, activityElevationGain, activityElapsedTime, activityPolyline):
        self.athleteID = athleteID
        self.activtiyID = activtiyID
        self.activityName = activityName
        self.activityType = activityType
        self.activityDistance = activityDistance
        self.activityElevationGain = activityElevationGain
        self.activityElapsedTime = activityElapsedTime
        self.activityPolyline = activityPolyline

    def get(self):
        return {
        'athleteID' : self.athleteID,
        'activtiyID' : self.activtiyID,
        'activityName' : self.activityName,
        'activityType' : self.activityType,
        'activityDistance' : self.activityDistance,
        'activityElevationGain' : self.activityElevationGain,
        'activityElapsedTime' : self.activityElapsedTime,
        'activityPolyline' : self.activityPolyline,
        }