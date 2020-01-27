import time
import numpy as np
import math

class behaviour_v1():    
    globals = None

    def setDependencies(self, modules):
        self.globals = modules.getModule("globals")
        self.motion = modules.getModule("motion")
        self.tools = modules.getModule("tools")
        self.vision = modules.getModule("vision")
        self.sonar = modules.getModule("sonar")
        self.behaviour = modules.getModule("behaviour")
        
    # #React to found observations  
    # def calcDirection(self, blobsFound, blobDist, angle, signature):
    #     '''
    #     Input: Stuff
    #     Output: less to no stuff
    #     '''

    # def walk_stop(self):
    #     self.globals.posProxy.goToPosture("StandInit", 1)
    #     sonar = self.sonar.avg_sonar()

    #     while self.no_wall(sonar, 0.55):
    #         # self.drift_control(sonar)
    #         # Free walk space
    #         sonar = self.sonar.avg_sonar()
    #         self.globals.motProxy.moveTo(self.calc_walk_distance(sonar), 0, 0)
    #         sonar = self.sonar.avg_sonar()
        



    # def calc_walk_distance(self, sonar):
    #     distance = min(sonar) * 0.5
    #     if distance < 0.2:
    #         distance = 0.2
    #     return distance

    # def no_wall(self, sonar, threshold):
    #     if sonar[0] > threshold and sonar[1] > threshold:
    #         return True
    #     return False




    # def drift_control(self, sonar, min, max):
    #     pass








    # #     while self.drift_control(sonar, 0.5, 0.8):
    # #         sonar = self.sonar.avg_sonar()
    # #         print(sonar)
    # #         # self.globals.posProxy.goToPosture("StandInit", 1)
    # #         self.globals.motProxy.moveTo((min(sonar)* 0.25), 0, 0)
    # #         # self.globals.posProxy.goToPosture("Stand", 1)
            
    # #     return sonar
    
    # # def drift_control(self, sonar, mini, maxi):
    # #     l, r = sonar
    # #     while l < mini or r < mini:
    # #         if (l < mini and r < maxi) or (l < maxi and r < mini):
    # #             self.stand_perp()
    # #             print("False")
    # #             return False
    # #         elif l < mini and r >= maxi:
    # #             print("Turn right")
    # #             self.globals.motProxy.moveTo(0, 0, -0.25 * np.pi)
    # #         elif r < mini and l >= maxi:
    # #             print("Turn left")
    # #             self.globals.motProxy.moveTo(0, 0, 0.25 * np.pi)
    # #         l, r = self.sonar.avg_sonar()
    # #         print(l, r)
    # #     print("True")
    # #     return True
        


    # def stand_perp(self):
    #     '''
    #     Input: sonardata
        
    #     Checks if robot faces the wall perpendicularly.
    #     If not, it positions itself.
    #     '''
    #     sonar = self.sonar.avg_sonar()
    #     difference = sonar[0] - sonar[1]
    #     if min(sonar) < 0.9 and min(sonar) >= 0.5 and abs(difference) >= (min(sonar) * 0.01):
    #         # if right side closer to wall
    #         if difference >= 0:
    #             self.turn_until_straigt(-0.18, sonar, 0.01)
            
    #         # if left side closer to wall
    #         elif difference < 0:
    #             self.turn_until_straigt(0.18, sonar, 0.01)

    #     elif min(sonar) < 0.5 and abs(difference) >= (min(sonar) * 0.06):
    #         # if right side closer to wall
    #         if difference >= 0:
    #             self.turn_until_straigt(-0.10, sonar, 0.06)
  
    #         # if left side closer to wall
    #         elif difference < 0:
    #             self.turn_until_straigt(0.10, sonar, 0.06)
                

    # def turn_until_straigt(self, radians, sonar, distance_param):
    #     self.globals.posProxy.goToPosture("StandInit", 1)
    #     difference = sonar[0] - sonar[1]
    #     if difference >= 0:
    #         while difference >= (min(sonar) * distance_param):
    #             self.globals.motProxy.moveTo(0, 0, radians)
    #             sonar = self.sonar.avg_sonar()
    #             difference = sonar[0] - sonar[1]
    #     elif difference < 0:
    #         while difference < (min(sonar) * distance_param):
    #             self.globals.motProxy.moveTo(0, 0, radians)
    #             sonar = self.sonar.avg_sonar()
    #             difference = sonar[0] - sonar[1]


    # def explore_sideways(self):
    #     pass


    # def nav_to_middle(self):
    #     '''
    #     Input: sonardata
        
    #     Checks if robot walk in middle of maze path.
    #     If not, it turns to return to the middle.
    #     '''
    #     # sonar = self.sonar.avg_sonar()
    #     # if min(sonar > 0.8)

    #     pass


    # def follow_wall(self):
    #     '''
    #     Input: sonardata

    #     Follows wall until end.
    #     '''
    #     pass

    
    # def look_around(self, direction):
    #     '''
    #     Input: direction: left, right, up, down, straigt

    #     '''
    #     if direction == "straight":
    #         print(direction)
    #         self.motion.setHead(0, 0)

    #     if direction == "left":
    #         print(direction)
    #         self.motion.setHead(0, 0)
    #         self.motion.setHead(0.15, 0)

    #     if direction == "right":
    #         print(direction)
    #         self.motion.setHead(0, 0)
    #         self.motion.setHead(-0.15, 0)

    #     if direction == "up":
    #         print(direction)
    #         self.motion.setHead(0, 0)
    #         self.motion.setHead(0, -0.15)

    #     if direction == "down":
    #         print(direction)
    #         self.motion.setHead(0, 0)
    #         self.motion.setHead(0, 0.15)


    # def explore(self):
    #     pass

    # def follow_signature(self, signature):
    #     if signature == "Finish":
    #         self.globals.motProxy.rest()
    #         return True
    #     elif signature == "Right":
    #         self.globals.motProxy.moveTo(0, 0, (-0.5 * np.pi))
    #         return True
    #     elif signature == "Left":
    #         self.globals.motProxy.moveTo(0, 0, (0.5 * np.pi))
    #         return True
    #     else:
    #         return False



# ************************************************************************************************************************* #
# ************************************************** NEW VERSION ********************************************************** #
# ************************************************************************************************************************* #

    # UNUSED FUNCTION. NOG NODIG?
    # def calcDirection(self, blobsFound, blobDist, angle, signature):
    #     '''
    #     Input: Stuff
    #     Output: less to no stuff
    #     '''

    ##########################################################################################
    #                                       CHECK                                            #
    ##########################################################################################
    def not_finished(self, clue):
        """
        Input: Found singature clue
        Output: True if robot is not finished. Else returns False
        """
        if clue == "Finish":
            return False
        return True

    def no_wall(self, sonar, threshold=.55):
        """
        Returns True if robot does not stand in front of a wall. Else returns False
        """
        if sonar[0] > threshold and sonar[1] > threshold:
            return True
        return False

    ##########################################################################################
    #                                   REPOSITIONING                                        #
    ##########################################################################################

    def face_direction(self, angle):
        """
        Input: Angle in radians
        Funtion: Faces robot to the closest wall (if possible) and rotates angle radians relative to this wall
        """
        self.stand_perp()
        self.motion.moveTo(0, 0, angle)

    def adjust_position(self, blueBlob):
        '''
        Input: xy-coordinates of blue blob
        Function: adjusts position according to sonar and blue blob
                Calculations on triangle with points A, B, C for robot, Left, Right respectively
                Sides a, b, c are opposite to A, B, C respectively
        '''
        # Sonar meting
        c, b = self.sonar.avg_sonar()

        # a = sqrt(b^2 + c^2 - 2bc cos(A))
        a = math.sqrt(b**2 + c**2 - 2 * b * c * math.cos(np.pi/3))

        # Calculate angle C
        C_angle = math.acos((a**2 + b**2 - c**2) / (2*a*b))

        # Calculate distance to point D on wall (Loodlijn)
        h_a = b * math.sin(C_angle)

        # B and C are points relative to optimal point 55 centimeters from wall (0, 0)
        B = np.asarray([-0.5 * a, .55])
        C = np.asarray([0.5 * a, .55])

        # Calculate CD, distance from Right to closest wall point D
        CD = (b**2 - c**2 + a**2) / (2*a)

        # Calculate Robot position relative to optimal position
        A = C - np.asarray([CD, h_a])

        # Calculate angle to wall
        correction_angle = math.acos(h_a / b) - np.pi/6

        # Adjust for blue blob
        center = np.asarray([120, 160])
        pixels_from_center = blueBlob - center

        # Blob to the right of center. Move more towards right
        if pixels_from_center[0] >= 0:
            A[1] += (0.5/h_a) 
        # Blob to the left of center
        else:
            A[1] -= (0.5/h_a) 

        # Correct for angle and move to optimal point
        self.motion.moveTo(0, 0, correction_angle)
        self.motion.moveTo(A[0], A[1])

    def stand_perp(self):
        """
        Robot will try to stand perpendicular to closest wall
        """
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
        """
        Turns robot to wall untill differences between sonar is small enough
        """
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

    def drift_control(self, sonar):
        """
        Input: Sonar
        Function: Will counteract random drift of the robot using sonar observations
        """
        # Bereken difference
        l, r = sonar
        
        difference = abs(l - r)

        # Calculate distance to wall
        if l > r:
            LR = math.sqrt(l**2 + r**2 - 2*l*r*math.cos(np.pi/3))
            C_angle = math.acos((LR**2 + r**2 - l**2)/(2 * LR * r))
            distance_to_wall = r * math.sin(C_angle)
            correction_angle = math.acos(distance_to_wall/r) - np.pi/6
        else:
            LR = math.sqrt(l**2 + r**2 - 2*l*r*math.cos(np.pi/3))
            B_angle = math.acos((LR**2 + l**2 - r**2)/(2 * LR * l))
            distance_to_wall = l * math.sin(B_angle)
            correction_angle = math.acos(distance_to_wall/l) + np.pi/6

        # Beide sensoren ver genoeg van muur, difference klein
        if min(sonar) >= 0.6 and difference < 0.3:
            return sonar
            
        # Beide sensoren ver genoeg van muur, difference groot
        if min(sonar) >= 0.6 and difference >=0.3:
            self.motion.moveTo(0, 0, correction_angle)
            
        # 1 of 2 sensoren dichtbij muur, difference klein
        if min(sonar) < 0.6 and difference < 0.3:
            return sonar

        # 1 of 2 sensoren dichtby muur, difference groot
        if min(sonar) < 0.6 and difference >= 0.3:
            self.motion.moveTo(0, 0, correction_angle)
            self.stand_perp()
        
        sonar = self.sonar.avg_sonar()
        return sonar

    ##########################################################################################
    #                                       MOVEMENT                                         #
    ##########################################################################################

    def follow_clue(self, clue):
        """
        Input: distance, center, angle, signature, n_blobs, blobsList
        Robot turns according to signature found and corrects for angle of image.
        Robot then moves untill a wall is found
        """
        distance, center, angle, signature, n_blobs, blobsList = clue

        # Kloppen deze radians???
        # Turn directions per signature
        radians_per_signature = {"Left":0.5*np.pi, "Right": -0.5*np.pi, "Back": np.pi, "Finish": 0, -1: None}

        # calculate angle to move
        radians = radians_per_signature[signature]
        radians -= angle
        
        # move angle
        self.motion.moveTo(0, 0, radians)
        self.walk_stop()
    
    def walk_stop(self):
        """
        Robot walks using sonar and stops when encountering a wall.
        """
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
        """
        Input: Sonar
        Calculate distance that robot could walk according to sonar. Minimum distance is 0.2m 
        Output: Distance to walk
        """
        distance = min(sonar) * 0.5
        if distance < 0.2:
            distance = 0.2
        return distance

    def wander_around(self):
        """
        Robot will walk untill encountering a wall and than turn into the free space. 
        After that it will walk 1 meter so it stands in the middle of a new cell
        """
        # walk until stop
        self.walk_stop()
    
        # draai naar een vrije kant
        for _ in range(3):
            # Face direction (quarter turn to left)
            self.face_direction(angle=0.5 * np.pi)
            sonar = self.sonar.avg_sonar()
            if self.no_wall(sonar):
                break

        # loop 1 meter
        if self.no_wall(sonar):
            distance = self.calc_walk_distance(sonar)
            self.motion.moveTo(distance, 0, 0)

    ##########################################################################################
    #                                  VISUAL SEARCHING                                      #
    ##########################################################################################

    def look_for_clues(self):
        """
        Robot searches for clues and returns information if found
        Output: distance, center, angle, signature, n_blobs, blobsList
        """
        n_blobs, blobsList = self.search_3_blobs()

        # If no blobs are found go to wander around
        if n_blobs == None or blobsList == None:
            return None, None, None, None, None, None
        distance, center, angle, signature = self.vision.getInformation(blobsList)
        return distance, center, angle, signature, n_blobs, blobsList

    def search_3_blobs(self):
        """
        Funtion: Find 3 blobs on paper by looking in front, left, behind and to the right.
        Output: NumberOfBlobs and blobsList (x, y coordinates) if found otherwise None, None
        """
        directions = ["front", "left", "back", "right"]
        for _ in directions:
            # Face direction (quarter turn to left)
            self.face_direction(angle=0.5 * np.pi)

            # Take picture
            n_blobs, blobsList = self.see_picture()
            n_blobs_per_colour = [len(colour) for colour in blobsList]

            # Blue blob is found but too many or little other blobs
            if len(blobsList[0]) > 0 and min(n_blobs_per_colour) != max(n_blobs_per_colour):
                blueBlob = blobsList[0][0][:2]
                n_blobs, blobsList = self.search_more_blobs(blueBlob, n=3)
                
            # Return blobs if there is 1 blob of every colour
            if n_blobs == 3 and min(n_blobs_per_colour) == max(n_blobs_per_colour) == 1:
                return n_blobs, blobsList

        # Return to begin position if no blobs are found
        self.face_direction("front")
        return None, None

    def search_more_blobs(self, blueBlob, n=3):
        """
        Input: xy-coordinates of blue Blob, Number of Adjustment Tries
        Function: For n tries, reposition robot according to blue Blob position and sonar and tries to find 3 blobs.
        Output: Returns new numberofblobs and blobsList
        """
        # Make n tries to find 3 blobs
        for _ in range(n):
            # Adjust position and take picture
            self.adjust_position(blueBlob)
            n_blobs, blobsList = self.see_picture()
            n_blobs_per_colour = [len(colour) for colour in blobsList]

            # Break out of for loop if correct blobs are found
            if n_blobs == 3 and min(n_blobs_per_colour) == max(n_blobs_per_colour) == 1:
                break

            # Get new blueBlob position
            if len(blobsList[0]) > 0:
                blueBlob = blobsList[0][0][:2]
            # Blue blob is no longer on picture
            else:
                return n_blobs, blobsList

        return n_blobs, blobsList

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

    ##########################################################################################
    #                                      OTHER                                             #
    ##########################################################################################
    
    def solve_maze(self):
        """
        Robot will try to find the finish of a maze.
        """
        signature = None

        # Keep collecting and searching for clues
        while self.not_finished(signature):
            clue = self.look_for_clues()
            distance, center, angle, signature, n_blobs, blobsList = clue
            if signature:
                self.follow_clue(clue)
            else:
                self.wander_around()
        self.globals.motProxy.rest()