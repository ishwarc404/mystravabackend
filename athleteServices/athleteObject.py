class athletePrimary:
    def __init__(self, athleteID, athleteFirstName, athleteLastName, athleteImage, athleteCity, athleteState):
        self.athleteID = athleteID
        self.athleteFirstName = athleteFirstName
        self.athleteLastName = athleteLastName
        self.athleteImage = athleteImage
        self.athleteCity = athleteCity
        self.athleteState = athleteState

    def get(self):
        return {
        "athleteID" : self.athleteID,
        "athleteFirstName" : self.athleteFirstName,
        "athleteLastName" : self.athleteLastName,
        "athleteImage" : self.athleteImage,
        "athleteCity" : self.athleteCity,
        "athleteState" : self.athleteState,
        }