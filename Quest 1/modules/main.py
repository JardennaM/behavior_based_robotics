import numpy as np

class main:
    def setDependencies(self, modules):
        self.globals = modules.getModule("globals")
    def start(self):
        self.globals.setProxies()
        self.globals.posProxy.goToPosture("StandInit", 1.0)

        self.square_no_turn(1)
        self.square_with_turn(1)
        self.circle(0.5)
        
        self.globals.motProxy.rest()

    def square_no_turn(self, distance):
        """
        Input: Distance: Distance of edges of square in meters
        Function: Makes the robot walk a square with edges of certain distance without turning
        """
        self.globals.motProxy.moveTo(distance,0,0)
        self.globals.motProxy.moveTo(0,distance,0)
        self.globals.motProxy.moveTo(-1*distance,0,0)
        self.globals.motProxy.moveTo(0,-1*distance,0)

    def square_with_turn(self, distance):
        """
        Input: Distance: Distance of edges of square in meters
        Function: Makes the robot walk a square with edges of certain distance with turning
        """
        for _ in range(4):
            self.globals.motProxy.moveTo(distance,0,0)
            self.globals.motProxy.moveTo(0,0, (np.pi * 0.5))

    def circle(self, diameter):
        """
        Input: Diameter: Diameter of circles that is going to be walked
        Function: Makes the robot walk a circle with the given diameter
        """
        distance = 2 * np.pi * (0.5 * diameter)
        self.globals.motProxy.moveTo(0, (0.5 * distance), np.pi)
        self.globals.motProxy.moveTo(0, (0.5 * distance), np.pi)





