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



# *************************************************************


    def not_finished(self, clue):
        pass

    def face_direction(self, direction):
        pass

    def search_more_blobs(self, blueBlob, tries=3):
        for i in range(tries):
            self.adjust_position(blueBlob)
            n_blobs, blobsList = self.see_picture
            # Break if 3 blobs
            # Get new blue blob
        return n_blobs, blobsList

    def adjust_position(self, blueBlob):
        '''
        Input: xy-coordinates of blue blob
        Function: adjusts position according to sonar and blue blob
        '''
        # Sonar meting
        # A.d.h.v. sonar en xy coords adjustment berekenen
            # beide sonar metingen groter dan 0.55, stap naar achter
            # perpendicular staan
            # waar was de blauwe blob, navigeer naar links of rechts
        # Move naar desired position

    
    def search_3_blobs(self):
        # 4x 90 graden draaien
        directions = ["front", "left", "back", "right"]
        for direction in directions:
            # Face direction
            self.face_direction(direction)

            # NOG DOEN: Check of de juiste 3 blobs gereturned worden
            n_blobs, blobsList = self.see_picture()
            if n_blobs == 3:
                return n_blobs, blobsList
            elif blueBlob_found:
                self.search_more_blobs(blueBlob, 3)
                if n_blobs == 3:
                    return n_blobs, blobsList
        self.face_direction("front")
        return None, None

    def look_for_clues(self):
        n_blobs, blobsList = self.search_3_blobs()
        # If no blobs are found go to wander around
        if n_blobs == None or blobsList == None:
            return None, None, None, None, None, None
        distance, center, angle, signature = self.vision.getInformation(blobsList)
        return distance, center, angle, signature, blobsList


    def follow_clue(self, clue):
        # calculate angle to move
        # move angle
        # self.walk_stop()

    def walk_stop(self):
        self.globals.posProxy.goToPosture("StandInit", 1)
        sonar = self.sonar.avg_sonar()

        total_distance = 0

        while self.no_wall(sonar, 0.55):
            if total_distance > 2.5:
                return False
            self.drift_control(sonar)
            # Free walk space
            sonar = self.sonar.avg_sonar()
            distance = self.calc_walk_distance(sonar)
            total_distance += distance
            self.globals.motProxy.moveTo(distance, 0, 0)
            sonar = self.sonar.avg_sonar()
        return True
        
    def calc_walk_distance(self, sonar):
        distance = min(sonar) * 0.5
        if distance < 0.2:
            distance = 0.2
        return distance

    def no_wall(self, sonar, threshold):
        if sonar[0] > threshold and sonar[1] > threshold:
            return True
        return False

    def drift_control(self, sonar):
        # Bereken difference
        # Cases:
            # Beide sensoren ver genoeg van muur, difference klein
                # Niks doen
            # 1 sensor dichtbij muur, difference groot
                # Corrigeer naar midden
                # Probeer perpendicular te staan als dat lukt
        
        pass

    def stand_perp(self):
        #kopieren van boven
        pass

    def turn_until_straigt(self):
        # kopieren van boven
        pass

    def wander_around(self):
        # walk until stop
        # draai naar een vrije kant
        # loop 1 meter
        pass

    def solve_maze(self):
        clue = None
        while self.not_finished(clue):
            clue = self.look_for_clues()
            if clue:
                self.follow_clue()
            else:
                self.wander_around()
        self.globals.motProxy.rest()