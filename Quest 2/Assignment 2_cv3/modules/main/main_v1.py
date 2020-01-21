import cv2
import numpy as np
from naoqi import ALProxy
import time
import sys
class main_v1:
    def setDependencies(self, modules):
        self.globals = modules.getModule("globals")
        self.motion = modules.getModule("motion")
        self.tools = modules.getModule("tools")
        self.vision = modules.getModule("vision")
        self.sonar = modules.getModule("sonar")
    
    def avg_sonar(self):
        self.sonar.sSubscribe()
        left = right = 0
        reading_nr = 5
        for i in range(reading_nr):
            time.sleep(0.1)
            l,r = self.sonar.getSonarData(value=0)
            print(l, r)
            left += l
            right += r
        left /= reading_nr
        right /= reading_nr
        self.sonar.sUnsubscribe() 
        return [left, right]

    def start(self):
        self.globals.setProxies()
        self.motion.init()
        self.tools.cSubscribe()
        
        # self.globals.posProxy.goToPosture("StandZero", 1)
        # sonar = self.avg_sonar()

        # while sonar[0] > 0.3 and sonar[1] > 0.3:
        #     print(sonar)
        #     time.sleep(1)
        #     self.globals.posProxy.goToPosture("StandInit", 1)
        #     self.globals.motProxy.moveTo(0.2, 0, 0)
        #     time.sleep(1)
        #     self.globals.posProxy.goToPosture("Stand", 1)
        #     sonar = self.avg_sonar()



        

        self.globals.motProxy.rest()

        
        # self.globals.posProxy.goToPosture("StandInit", 1)
        # self.globals.motProxy.moveTo(0.5, 0, 0)




        

        img, pos = self.tools.getSnapshot()

        self.tools.SaveImage("test_image.jpg", img)

        amount_of_blobs, coords, imagearray, found_img = self.vision.getBlobsData(img)

        print(coords)
     
        if amount_of_blobs > 0:

            try:
                self.tools.SaveImage("test_bw_image.jpg", imagearray)
                self.tools.SaveImage("test_image_found_circles.jpg", found_img)
            except:
                print("Opslaan niet gelukt")

            Distance = self.vision.calcAvgBlobDistance(coords)
            center = self.vision.calcMidLandmark(coords)
            angle = self.vision.calcAngleLandmark(center)
            signature = self.vision.findSignature(coords)
            print(coords, Distance, center, angle, signature)
          
            self.globals.motProxy.rest()
        
        else:
            print("No blobs")
        



        
