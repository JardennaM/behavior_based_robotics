import time
import numpy as np

class behaviour_v1():    
    globals = None

    def setDependencies(self, modules):
        self.globals = modules.getModule("globals")
        self.motion = modules.getModule("motion")
        self.sonar = modules.getModule("sonar")
        
    #React to found observations  
    def calcDirection(self, blobsFound, blobDist, angle, signature):
        '''
        Input: Stuff
        Output: less to no stuff
        '''

    def walk_stop(self):
        self.globals.posProxy.goToPosture("StandInit", 1)
        sonar = self.sonar.avg_sonar()

        while self.no_wall(sonar, 0.55):
            # self.drift_control(sonar)
            # Free walk space
            sonar = self.sonar.avg_sonar()
            self.globals.motProxy.moveTo(self.calc_walk_distance(sonar), 0, 0)
            sonar = self.sonar.avg_sonar()
        



    def calc_walk_distance(self, sonar):
        distance = min(sonar) * 0.5
        if distance < 0.2:
            distance = 0.2
        return distance

    def no_wall(self, sonar, threshold):
        if sonar[0] > threshold and sonar[1] > threshold:
            return True
        return False




    def drift_control(self, sonar, min, max):
        pass








    #     while self.drift_control(sonar, 0.5, 0.8):
    #         sonar = self.sonar.avg_sonar()
    #         print(sonar)
    #         # self.globals.posProxy.goToPosture("StandInit", 1)
    #         self.globals.motProxy.moveTo((min(sonar)* 0.25), 0, 0)
    #         # self.globals.posProxy.goToPosture("Stand", 1)
            
    #     return sonar
    
    # def drift_control(self, sonar, mini, maxi):
    #     l, r = sonar
    #     while l < mini or r < mini:
    #         if (l < mini and r < maxi) or (l < maxi and r < mini):
    #             self.stand_perp()
    #             print("False")
    #             return False
    #         elif l < mini and r >= maxi:
    #             print("Turn right")
    #             self.globals.motProxy.moveTo(0, 0, -0.25 * np.pi)
    #         elif r < mini and l >= maxi:
    #             print("Turn left")
    #             self.globals.motProxy.moveTo(0, 0, 0.25 * np.pi)
    #         l, r = self.sonar.avg_sonar()
    #         print(l, r)
    #     print("True")
    #     return True
        


    def stand_perp(self):
        '''
        Input: sonardata
        
        Checks if robot faces the wall perpendicularly.
        If not, it positions itself.
        '''
        sonar = self.sonar.avg_sonar()
        difference = sonar[0] - sonar[1]
        if min(sonar) < 0.9 and min(sonar) >= 0.5 and abs(difference) >= (min(sonar) * 0.01):
            # if right side closer to wall
            if difference >= 0:
                self.turn_until_straigt(-0.18, sonar, 0.01)
            
            # if left side closer to wall
            elif difference < 0:
                self.turn_until_straigt(0.18, sonar, 0.01)

        elif min(sonar) < 0.5 and abs(difference) >= (min(sonar) * 0.06):
            # if right side closer to wall
            if difference >= 0:
                self.turn_until_straigt(-0.10, sonar, 0.06)
  
            # if left side closer to wall
            elif difference < 0:
                self.turn_until_straigt(0.10, sonar, 0.06)
                

    def turn_until_straigt(self, radians, sonar, distance_param):
        self.globals.posProxy.goToPosture("StandInit", 1)
        difference = sonar[0] - sonar[1]
        if difference >= 0:
            while difference >= (min(sonar) * distance_param):
                self.globals.motProxy.moveTo(0, 0, radians)
                sonar = self.sonar.avg_sonar()
                difference = sonar[0] - sonar[1]
        elif difference < 0:
            while difference < (min(sonar) * distance_param):
                self.globals.motProxy.moveTo(0, 0, radians)
                sonar = self.sonar.avg_sonar()
                difference = sonar[0] - sonar[1]


    def explore_sideways(self):
        pass


    def nav_to_middle(self):
        '''
        Input: sonardata
        
        Checks if robot walk in middle of maze path.
        If not, it turns to return to the middle.
        '''
        # sonar = self.sonar.avg_sonar()
        # if min(sonar > 0.8)

        pass


    def follow_wall(self):
        '''
        Input: sonardata

        Follows wall until end.
        '''
        pass

    
    def look_around(self, direction):
        '''
        Input: direction: left, right, up, down, straigt

        '''
        if direction == "straight":
            print(direction)
            self.motion.setHead(0, 0)

        if direction == "left":
            print(direction)
            self.motion.setHead(0, 0)
            self.motion.setHead(0.15, 0)

        if direction == "right":
            print(direction)
            self.motion.setHead(0, 0)
            self.motion.setHead(-0.15, 0)

        if direction == "up":
            print(direction)
            self.motion.setHead(0, 0)
            self.motion.setHead(0, -0.15)

        if direction == "down":
            print(direction)
            self.motion.setHead(0, 0)
            self.motion.setHead(0, 0.15)


    def explore(self):
        pass

    def follow_signature(self, signature):
        if signature == "Finish":
            self.globals.motProxy.rest()
            return True
        elif signature == "Right":
            self.globals.motProxy.moveTo(0, 0, (-0.5 * np.pi))
            return True
        elif signature == "Left":
            self.globals.motProxy.moveTo(0, 0, (0.5 * np.pi))
            return True
        else:
            return False