import geopy.distance

class distanceCalculate:
    def __init__(self, _trackpoints) -> None:
        self.trackpoints = _trackpoints

    
    def calculateDistance(self):
        netdistance = 0
        for i in range(0,len(self.trackpoints)-2):
            netdistance += geopy.distance.geodesic(self.trackpoints[i], self.trackpoints[i+1]).km
        
        return netdistance

    
    def calculatekmSplits(self):
        pass