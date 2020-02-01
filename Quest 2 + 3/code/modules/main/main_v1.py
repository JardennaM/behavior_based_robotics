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

    def walk(self, distance):
        """
        Input: Distance
        Function: Makes robot walk forwards
        """
        self.globals.motProxy.moveTo(distance, 0, 0)

    def turn(self, angle=(0.5 * np.pi)):
        """
        Input: Angle in radians
        Function: Turns robot according to angle given
        """
        self.globals.motProxy.moveTo(0, 0, angle)

    def walk_through_maze(self):
        """
        Function: Make robot walk through maze with customized actions before starting
        """
        self.globals.posProxy.goToPosture("Stand", 1)
        self.globals.posProxy.goToPosture("StandInit", 1)
        self.walk(0.5)
        self.turn(-0.5*np.pi)
        self.behaviour.solve_maze()


    def start(self):
        self.globals.setProxies()
        self.motion.init()
        
        self.behaviour.solve_maze()

        self.globals.motProxy.rest()




       



        

        

        
     
        
        



        
