from naoqi import ALProxy

class globals:
    ipadress = "146.50.60.53"
    def setDependencies(self, modules):
        pass

    def setProxies(self):
        self.motProxy = ALProxy("ALMotion", self.ipadress, 9559)
        self.posProxy = ALProxy("ALRobotPosture", self.ipadress, 9559)
        self.vidProxy = ALProxy("ALVideoDevice", self.ipadress, 9559)
        self.sonarProxy = ALProxy("ALSonar", self.ipadress, 9559)
        self.memoryProxy = ALProxy("ALMemory", self.ipadress, 9559)
        self.speechProxy = ALProxy("ALTextToSpeech", self.ipadress, 9559)

   

        # Subscribe to sonars, this will launch sonars (at hardware level) and start data acquisition.
        

        # Uncomment to access sonars
        self.sonarProxy = ALProxy("ALSonar", self.ipadress, 9559)
        self.memoryProxy = ALProxy("ALMemory", self.ipadress, 9559)