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

        # bw_img_blue = self.vision.filterImage(img, [90,0,0],[255,100,100])
        # bw_img_green = self.vision.filterImage(img, [0,90,0],[100,255,100])
        # bw_img_red = self.vision.filterImage(img, [0,0,170], [95,130,255])

        # bw_img_blue = self.vision.filterImage(img, [45,0,0],[255,100,100])
        # bw_img_green = self.vision.filterImage(img, [0,45,0],[100,255,100])
        # bw_img_red = self.vision.filterImage(img, [0,0,130], [95,130,255])

        # bw_img = bw_img_blue + bw_img_green + bw_img_red

        # circles = self.vision.findCircle(bw_img)

        # found_img = self.vision.drawCircles(circles)
        # self.tools.SaveImage("test_bw_image.jpg", bw_img)
        # self.tools.SaveImage("test_image_found_circles.jpg", found_img)

        amount_of_blobs, coords, imagearray = self.vision.getBlobsData(img)

        Distance = self.vision.calcAvgBlobDistance(coords)
        center = self.vision.calcMidLandmark(coords)
        angle = self.vision.calcAngleLandmark(center)
        foo = self.vision.findSignature(coords)
        print(coords, Distance, center, angle, foo)

        
        self.globals.motProxy.rest()
        



        
