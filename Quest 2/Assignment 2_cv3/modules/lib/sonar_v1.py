import cv2
from naoqi import ALProxy
import math
import time

class sonar_v1():    
    globals = None
    def setDependencies(self, modules):
        self.globals = modules.getModule("globals")

    #unsubscribe from sonars
    def sUnsubscribe(self):
        """ Try to unsubscribe from the camera """ 
        try:
            self.globals.sonarProxy.unsubscribe(self.sonar_sub)
            print "gotHERE----------------------------------------"
        except Exception as inst:
            print "Unsubscribing impossible:", inst

    #subscribe to camera        
    def sSubscribe(self):
        '''subscribe to the nsonar feed'''
        self.sonar_sub = self.globals.sonarProxy.subscribe("myApplication")
       
    # get snapshot from camera
    def getSonarData(self,value = 0):
        """
        GEt data from sonar echos
        """
        if value==0:
            left = self.globals.memoryProxy.getData("Device/SubDeviceList/US/Left/Sensor/Value")
            # Same thing for right.
            right = self.globals.memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value")
        else:
            left = self.globals.memoryProxy.getData("Device/SubDeviceList/US/Left/Sensor/Value"+str(value))
            # Same thing for right.
            right = self.globals.memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value2"+str(value))
        # Get camPos
        # getPosition(name, space={0,1,2}, useSensorValues)
        return left,right

    def avg_sonar(self):
        reading_nr = 5
        error = True
        while error == True:
            left = right = 0
            for i in range(reading_nr):
                time.sleep(0.1)
                l,r = self.getSonarData(value=0)
                left += l
                right += r
            left /= reading_nr
            right /= reading_nr
            if max(left, right) < 2.0:
                error = False
            else:
                print("Invalid sonar:", left, right)
        return [left, right]
        