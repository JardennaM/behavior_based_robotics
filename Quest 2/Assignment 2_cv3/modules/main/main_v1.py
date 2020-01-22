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
        # self.globals.posProxy.goToPosture("Stand", 1)
        # sonar = self.sonar.avg_sonar()

        # while sonar[0] > 0.3 and sonar[1] > 0.3:
        #     print(sonar)
        #     time.sleep(3)
        #     self.globals.posProxy.goToPosture("StandInit", 1)
        #     time.sleep(3)
        #     self.globals.motProxy.moveTo(0.2, 0, 0)
        #     time.sleep(3)
        #     self.globals.posProxy.goToPosture("Stand", 1)
        #     sonar = self.sonar.avg_sonar()

        
        # self.globals.posProxy.goToPosture("StandInit", 1)

        # self.globals.motProxy.moveTo(0, 0, (-np.pi * 0.5))


    
 
        # self.globals.motProxy.rest()

        



        

        img, pos = self.tools.getSnapshot()

        self.tools.SaveImage("test_image.jpg", img)

        amount_of_blobs, coords, black_white_im, drawn_circle_img = self.vision.getBlobsData(img)
        amount_of_blobs, coords = self.vision.get_correct_blobsList(coords)

        print(amount_of_blobs, coords)
        try:
            self.tools.SaveImage("test_bw_image.jpg", black_white_im)
        except:
            print("black and white filter image not saved")
        try:
            self.tools.SaveImage("test_image_found_circles.jpg", drawn_circle_img)
        except:
            print("Drawn circle image not saved")
     
        if amount_of_blobs == 3:
            Distance = self.vision.calcAvgBlobDistance(coords)
            center = self.vision.calcMidLandmark(coords)
            angle = self.vision.calcAngleLandmark(center)
            signature = self.vision.findSignature(coords)
            print(Distance, center, angle, signature)
        else:
            print("No blobs")
        self.globals.motProxy.rest()
        



        
