import numpy as np

class main:
    def setDependencies(self, modules):
        self.globals = modules.getModule("globals")
    def start(self):
        self.globals.setProxies()
        # self.globals.posProxy.goToPosture("Stand", 1.0)
        self.globals.posProxy.goToPosture("StandInit", 1.0)
        
        
        # self.globals.speechProxy.say("Hello Jardenna en Bart")
        # # Tests whether robot has fallen and makes stand up in that case
        # self.globals.posProxy.goToPosture("Stand", 1.0)
        # # Move
        # self.globals.motProxy.moveTo(1,0,0)
        # # Walk velocity
        # self.globals.motProxy.setWalkTargetVelocity(1,0,0,0)
        
        # self.globals.motProxy.rest()

        self.circle(0.5)
        
        self.globals.motProxy.rest()

    def square_no_turn(self, distance):
        self.globals.motProxy.moveTo(distance,0,0)
        self.globals.motProxy.moveTo(0,distance,0)
        self.globals.motProxy.moveTo(-1*distance,0,0)
        self.globals.motProxy.moveTo(0,-1*distance,0)

    def square_with_turn(self, distance):
        for i in range(4):
            self.globals.motProxy.moveTo(distance,0,0)
            self.globals.motProxy.moveTo(0,0, (np.pi * 0.5))

    def circle(self, diameter):
        distance = 2 * np.pi * (0.5 * diameter)
        self.globals.motProxy.moveTo(0, (0.5 * distance), np.pi)
        self.globals.motProxy.moveTo(0, (0.5 * distance), np.pi)





