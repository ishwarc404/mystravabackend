from datetime import datetime 
import trackpointValueObject
import maxElevationCalculate
import distanceCalculate
import polyline

def parsefile(filename):

    gpxfile = open("./uploadedFiles/{}".format(filename))
    lines = gpxfile.read().split("\n")
    elevation_values = []
    time_values= []
    trackpointObjects = []
    i = 0
    elevation = 0
    time = 0
    latitude = 0
    longitude = 0
    first_timestamp = True

    trackpointLatLong = []
    polylinePoints = []


    while(i < len(lines)):
        each = lines[i]
        # print(each)
        if(each.strip()[0:5] == "<ele>"):
            elevation = each.strip()[5:-6]
            elevation = float(elevation)
            # elevation_values.append(float(elevation))
        if(each.strip()[0:6] == "<time>"):
            time = each.strip()[6:-12]
            try:
                datetime_object = datetime.strptime(time, '%Y-%m-%dT%H:%M:%S')
            except:
                datetime_object = datetime.now()
            time = datetime_object
            # time_values.append(datetime_object)
        if(each.strip()[0:6] == "<trkpt"):
            trkptvals = each.strip().split(" ")
            latitude = trkptvals[1].split("=")[1][1:-1]
            longitude = trkptvals[2].split("=")[1][1:-2]

        if(latitude !=0 and longitude!=0 and elevation!=0):
            elevation_values.append(elevation)
            trackpointLatLong.append([latitude,longitude])
            polylinePoints.append([float(latitude),float(longitude)])
            trackpointObject = trackpointValueObject.trackpointValueObject(latitude,longitude,elevation,time)
            trackpointObjects.append(trackpointObject.getObject())
            elevation = 0
            time = 0
            latitude = 0
            longitude = 0
        i+=1

    #lets calculate the biggestClimb
    elevationObject = maxElevationCalculate.maxElevation(elevation_values)
    net_gain =  elevationObject.netGain()
    biggest_climb = elevationObject.calculateBiggestClimb()
    highest_point = elevationObject.maxElevationReached()

    print("Net gain: ", net_gain)
    print("Biggest climb: ", elevationObject.calculateBiggestClimb())
    print("Highest point: ", elevationObject.maxElevationReached())


    #lets calculate distance
    distanceObject = distanceCalculate.distanceCalculate(trackpointLatLong)
    netdistance = distanceObject.calculateDistance()
    print("Net distance: ", netdistance)

    activityPolyline = polyline.encode(polylinePoints)
    print(activityPolyline)
    return ['Uploaded File', netdistance*1000, net_gain, 'default time return',activityPolyline]
