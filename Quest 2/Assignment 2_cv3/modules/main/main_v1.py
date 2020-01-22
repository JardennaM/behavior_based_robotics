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
        self.behaviour = modules.getModule("behaviour")
    
    

    def start(self):
        self.globals.setProxies()
        self.motion.init()
        self.tools.cSubscribe()

        # self.globals.motProxy.getHeadPos()
        
        self.behaviour.look_around("u")

        
        # self.globals.posProxy.goToPosture("StandInit", 1)

        # self.globals.motProxy.moveTo(0, 0, (-np.pi * 0.5))


    
 
        # self.globals.motProxy.rest()

        



        

        # img, pos = self.tools.getSnapshot()

        # self.tools.SaveImage("test_image.jpg", img)

        # amount_of_blobs, coords, imagearray, found_img = self.vision.getBlobsData(img)

        # print(coords)
     
        # if amount_of_blobs > 0:

        #     try:
        #         self.tools.SaveImage("test_bw_image.jpg", imagearray)
        #         self.tools.SaveImage("test_image_found_circles.jpg", found_img)
        #     except:
        #         print("Opslaan niet gelukt")

        #     Distance = self.vision.calcAvgBlobDistance(coords)
        #     center = self.vision.calcMidLandmark(coords)
        #     angle = self.vision.calcAngleLandmark(center)
        #     signature = self.vision.findSignature(coords)
        #     print(coords, Distance, center, angle, signature)
          
        #     self.globals.motProxy.rest()
        
        # else:
        #     print("No blobs")
        



        
