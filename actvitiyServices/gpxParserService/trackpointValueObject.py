class trackpointValueObject:
    def __init__(self, _latitude, _longitude, _elevation, _time):
        self.latitude = _latitude
        self.longitude = _longitude
        self.elevation = _elevation
        self.time = _time

    def getObject(self):

        object_ =  {
            "latitude" : self.latitude,
            "longitude" : self.longitude,
            'elevation' : self.elevation,
            'time' : self.time
        }

        return object_ 