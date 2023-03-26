import matplotlib.pyplot as plt

class maxElevation:
    def __init__(self,_elevationValues) -> None:
        self.elevationValues  = _elevationValues


    def calculateBiggestClimb(self):
        #lets calcylate the largest climb
        largest_climb = 0
        elevation_gain = 0
        previous_elevation = self.elevationValues[0]
        net_gain = 0
        for current_elevation in self.elevationValues:
            if(current_elevation >= previous_elevation):
                elevation_gain += current_elevation - previous_elevation
                net_gain += current_elevation - previous_elevation
            else:
                #means climb is over
                if(largest_climb < elevation_gain):
                    largest_climb = elevation_gain
                elevation_gain = 0
            previous_elevation = current_elevation

        return largest_climb

    def maxElevationReached(self):
        return max(self.elevationValues)


    def netGain(self):
        #lets calcylate the net gain
        previous_elevation = self.elevationValues[0]
        net_gain = 0
        for current_elevation in self.elevationValues:
            if(current_elevation >= previous_elevation):
                net_gain += current_elevation - previous_elevation
            previous_elevation = current_elevation

        return net_gain




# print(largest_climb)
# print(net_gain)

# plt.plot(x_axis[0:-1], y_axis)
# plt.xlabel('Time')
# plt.ylabel('Elevation')
# # plt.show()