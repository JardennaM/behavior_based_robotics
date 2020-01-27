# self.globals.posProxy.goToPosture("Stand", 1)
# self.globals.posProxy.goToPosture("StandInit", 1)
# sonar = self.sonar.avg_sonar()
# self.globals.motProxy.moveTo(0, 0, (-np.pi * 0.5))
# self.globals.motProxy.rest()


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
    
    def see_picture(self):
        # Take snapshot
        img, pos = self.tools.getSnapshot()

        self.tools.SaveImage("test_image.jpg", img)

        # Try to find circles   
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

        return amount_of_blobs, coords


    def seek_blobs(self):
        # Straigt "left", "right", "down", "up"
        head_positions = ["straight", "down", "up" "left", "right"]

        self.globals.posProxy.goToPosture("Stand", 1)
        for position in head_positions:
            # Straigt
            self.behaviour.look_around(position)
            time.sleep(3)
            self.tools.cSubscribe()
            amount_of_blobs, coords = self.see_picture()
            self.tools.cUnsubscribe()
            time.sleep(3)
            if amount_of_blobs == 3:
                return amount_of_blobs, coords
        return amount_of_blobs, coords
            
        



    def start(self):
        self.globals.setProxies()
        self.motion.init()
        
        # Walk until wall
        self.behaviour.walk_stop()

        print("Finish walk_stop")

        # Stand perpendicular to wall
        self.behaviour.stand_perp()

        print("Finish stand_perp")

        # Try to find blobs
        self.tools.cSubscribe()
        amount_of_blobs, coords = self.see_picture()

        if amount_of_blobs == 3:
            distance, center, angle, signature = self.vision.getInformation(coords)
            self.behaviour.follow_signature(signature)
            
        else:
            print("No blobs")

        self.globals.motProxy.rest()
        




        

        

        
     
        
        



        
