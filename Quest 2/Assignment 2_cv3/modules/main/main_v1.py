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

    def start(self):
        self.globals.setProxies()
        self.motion.init()
        self.globals.motProxy.rest()
        # self.globals.posProxy.goToPosture("Stand", 1)
        self.tools.cSubscribe()


        img, pos = self.tools.getSnapshot()

        self.tools.SaveImage("test_image.jpg", img)

        amount_of_blobs, coords, imagearray, found_img = self.vision.getBlobsData(img)


     
        if amount_of_blobs > 0:
            # print(len(found_img), len(found_img[0]))
            # print(len(imagearray), len(imagearray[0]))

            try:
                self.tools.SaveImage("test_bw_image.jpg", imagearray)
                self.tools.SaveImage("test_image_found_circles.jpg", found_img)
            except:
                print("Opslaan niet gelukt")

            Distance = self.vision.calcAvgBlobDistance(coords)
            center = self.vision.calcMidLandmark(coords)
            angle = self.vision.calcAngleLandmark(center)
            foo = self.vision.findSignature(coords)
            print(coords, Distance, center, angle, foo)

            
            self.globals.motProxy.rest()
        
        else:
            print("No blobs")
        



        
