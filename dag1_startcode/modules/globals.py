# Phineas: "146.50.60.28"
# Mio: "146.50.60.39"
from naoqi import ALProxy
class globals:
    ipaddress = "146.50.60.53"

    def setDependencies(self, module):
        pass

    def setProxies(self):
        # For talking
        self.speechProxy = ALProxy("ALTextToSpeech", self.ipaddress, 9559)
        # For moving
        self.motProxy = ALProxy("ALMotion", self.ipaddress, 9559)
        # For posing
        self.posProxy = ALProxy("ALRobotPosture", self.ipaddress, 9559)




