import time
import numpy as np
import math
from naoqi import ALProxy
import cv2

class behaviour_v1():    
    globals = None

    def setDependencies(self, modules):
        self.globals = modules.getModule("globals")
        self.motion = modules.getModule("motion")
        self.tools = modules.getModule("tools")
        self.vision = modules.getModule("vision")
        self.sonar = modules.getModule("sonar")
        self.behaviour = modules.getModule("behaviour")

# ************************************************************************************************************************* #
# ********************************************** NEW NEW VERSION ********************************************************** #
# ************************************************************************************************************************* #

    def solve_maze(self):
        """
        Robot will try to find the finish of a maze.
        """
        self.globals.setProxies()
        self.motion.init()
        signature = None
        last_direction = 0
        self.globals.speechProxy.say("I will begin my quest now!")
        self.globals.posProxy.goToPosture("Stand", 1)
        self.globals.posProxy.goToPosture("StandInit", 1)
        # self.walk_stop()

        # Keep collecting and searching for clues
        while signature != "Finish":
            while self.walk_stop() == False:
                # n_blobs, blobsList, direction = self.check_left_right()
                # if n_blobs == 1 or n_blobs == 3:
                #     last_direction = direction
                #     break
                last_direction = 0
            
            clue = self.look_for_clues()
            distance, center, angle, signature, n_blobs, blobsList = clue

            # if last_direction != 0 and signature == None:
            #     self.globals.motProxy.moveTo(0, 0, -1 * last_direction)
            #     last_direction = 0
            if signature:
                self.follow_clue(clue)
            else:
                n_blobs, blobsList = self.wander_around()
                if n_blobs != -1:
                    clue = self.vision.getInformation(blobsList)
                    distance, center, angle, signature, n_blobs, blobsList = clue
                    self.follow_clue(clue)

        self.globals.motProxy.rest()

    ##########################################################################################
    #                                   REPOSITIONING                                        #
    ##########################################################################################

    def adjust_position(self, blueBlob=[]):
        '''
        Input: xy-coordinates of blue blob
        Function: adjusts position according to sonar and blue blob
        '''
        print("Adjust position")
        sonar = self.sonar.avg_sonar()

        if blueBlob != []:
            center = np.asarray([120, 160])
            pixels_from_center = blueBlob - center
            if pixels_from_center[1] > 60:
                self.globals.motProxy.moveTo(0, -0.10, 0)
            elif pixels_from_center[1] < -60:
                self.globals.motProxy.moveTo(0, 0.10, 0)

        if sonar[0] < 0.45 and sonar[1] < 0.45:
            for _ in range(3):
                if sonar[0] < 0.45 and sonar[1] < 0.45:
                    self.globals.motProxy.moveTo(-0.10, 0, 0)
                    sonar = self.sonar.avg_sonar()


    ##########################################################################################
    #                                       MOVEMENT                                         #
    ##########################################################################################

    def follow_clue(self, clue):
        """
        Input: distance, center, angle, signature, n_blobs, blobsList
        Robot turns according to signature found and corrects for angle of image.
        Robot then moves untill a wall is found
        """
        print("follow_clue")
        distance, center, angle, signature, n_blobs, blobsList = clue

        if signature != "Finish" or signature != -1:
            sentence = "Turning " + signature
            self.globals.speechProxy.say(sentence)
        elif signature == "Finish":
            self.globals.speechProxy.say("Yay, I'm finished.")
        # Turn directions per signature
        radians_per_signature = {"Left":0.45*np.pi, "Right": -0.45*np.pi, "Back": 0.9*np.pi, "Finish": 0, -1: None}

        # calculate angle to move
        radians = radians_per_signature[signature]
        # radians -= angle
        
        # move angle
        self.globals.motProxy.moveTo(0, 0, radians)

    def turn_straight(self, sonar=[]):
        print("Turn straight")
        if sonar == []:
            sonar = self.sonar.avg_sonar()

        while sonar[0] < 0.45 or sonar[1] < 0.45:
            if sonar[0] < 0.55 and sonar[1] < 0.55:
                # Turn around untill straigth in front of wall
                difference = sonar[0] - sonar[1]
                while abs(difference) > 0.1:
                    if difference < 0:
                        self.globals.motProxy.moveTo(0, 0, -np.pi/9)
                    else:
                        self.globals.motProxy.moveTo(0, 0, np.pi/9)
                    sonar = self.sonar.avg_sonar()
                    difference = sonar[0] - sonar[1]
                break
            if sonar[0] < 0.45:
                print("Turn right")
                self.globals.motProxy.moveTo(0, 0, -np.pi/9)
            elif sonar[1] < 0.45:
                print("Turn left")
                self.globals.motProxy.moveTo(0, 0, np.pi/9)
            sonar = self.sonar.avg_sonar()

    def walk_stop(self):
        """
        Robot walks using sonar and stops when encountering a wall.
        """
        print("walk_stop")
        self.globals.posProxy.goToPosture("StandInit", 1)
        sonar = self.sonar.avg_sonar()

        distance_walked = 0
        while sonar[0] > 0.55 or sonar[1] > 0.55:
            self.turn_straight(sonar)
            self.globals.motProxy.moveTo(0.13, 0, 0)
            distance_walked += 0.13
            sonar = self.sonar.avg_sonar()

            if distance_walked > 0.65:
                if sonar[0] < 0.55 and sonar[1] < 0.55:
                    return True
                return False

            
        return True



    def wander_around(self):
        """
        Robot will walk until encountering a wall and than turn into the free space. 
        After that it will walk 1 meter so it stands in the middle of a new cell
        """
        print("wander_around")
        attemps = 0
        while attemps < 10:

            # look around in different directions for clue
            n_blobs, blobsList, direction = self.turn_head()

            # turn into free space when no blobs found
            if n_blobs == -1:
                for _ in range(3):
                    sonar = self.sonar.avg_sonar()
                    if sonar[0] > 0.55 and sonar[1] > 0.55:
                        break
                    self.globals.motProxy.moveTo(0, 0, 0.5*np.pi)
                    

            # Turn to blobs if found and return n_blobs, blobsList
            elif n_blobs == 3:
                # self.globals.motProxy.moveTo(0,0, direction)
                return n_blobs, blobsList

            distance = 0
            while distance < .50:
                self.turn_straight(sonar)
                self.globals.motProxy.moveTo(0.13, 0, 0)
                distance += 0.13
                sonar = self.sonar.avg_sonar()
            attemps += 1
        
        return -1, []

    ##########################################################################################
    #                                  VISUAL SEARCHING                                      #
    ##########################################################################################

    def look_for_clues(self):
        """
        Robot searches for clues and returns information if found
        Output: distance, center, angle, signature, n_blobs, blobsList
        """
        print("look_for_clues")
        sonar = self.sonar.avg_sonar()

        # Go stand in front of wall
        if sonar[0] < 0.50 and sonar[1] < 0.50:
            self.globals.posProxy.goToPosture("StandInit", 1)
            self.globals.motProxy.moveTo(-0.08, 0, 0)
            self.turn_straight()

        n_blobs, blobsList = self.search_3_blobs()

        # No blobs found
        if n_blobs == -1 or len(blobsList) == 0:
            return None, None, None, None, None, None
        
        # Return information of blobs
        n_blobs, blobsList = self.vision.get_correct_blobsList(blobsList)
        distance, center, angle, signature = self.vision.getInformation(blobsList)
        return distance, center, angle, signature, n_blobs, blobsList

    def search_3_blobs(self):
        """
        Funtion: Find 3 blobs on paper by looking in front, left, behind and to the right.
        Output: NumberOfBlobs and blobsList (x, y coordinates) if found otherwise None, None
        """
        print("search_3_blobs")

        # Take picture
        n_blobs, blobsList = self.see_picture()
        n_blobs_per_colour = [len(colour) for colour in blobsList]

        # Did not find exactly enough blobs
        if max(n_blobs_per_colour) != 1 or min(n_blobs_per_colour) != 1:
            # Try 4 more times to find blobs
            for i in range(4):
                # Make picture slightly higher
                n_blobs, blobsList = self.see_picture([0, -0.2])
                n_blobs_per_colour = [len(colour) for colour in blobsList]
                if n_blobs == 3 and min(n_blobs_per_colour) == max(n_blobs_per_colour) == 1:
                    break

                # Make picture slightly to the left
                n_blobs, blobsList = self.see_picture([-0.15, -0.15])
                n_blobs_per_colour = [len(colour) for colour in blobsList]
                if n_blobs == 3 and min(n_blobs_per_colour) == max(n_blobs_per_colour) == 1:
                    break
            
                # Make picture slightly to the right
                n_blobs, blobsList = self.see_picture([0.15, -0.15])
                n_blobs_per_colour = [len(colour) for colour in blobsList]
                if n_blobs == 3 and min(n_blobs_per_colour) == max(n_blobs_per_colour) == 1:
                    break
                
                # Get blue blob if possible
                if len(blobsList[0]) > 0:
                    blueBlob = blobsList[0][0][:2]
                    # Adjust position and take new picture
                    self.adjust_position(blueBlob)
                    n_blobs, blobsList = self.see_picture()
                    n_blobs_per_colour = [len(colour) for colour in blobsList]
                elif i == 0:
                    self.globals.motProxy.moveTo(-0.1, 0, 0)
                else:
                    break

                # Break out of for loop if correct blobs are found
                if n_blobs == 3 and min(n_blobs_per_colour) == max(n_blobs_per_colour) == 1:
                    break
            
        # Return blobs if there is 1 blob of every colour
        if n_blobs == 3 and min(n_blobs_per_colour) == max(n_blobs_per_colour) == 1:
            return n_blobs, blobsList

        return -1, []

    def see_picture(self, headPos=[0, -0.15]):
        print("see_picture")
        # Take snapshot
        self.motion.setHead(headPos[0], headPos[1])
        self.tools.cSubscribe()
        time.sleep(2)
        img, _ = self.tools.getSnapshot()

        self.tools.SaveImage("test_image.jpg", img)

        # Try to find circles   
        amount_of_blobs, coords, black_white_im, drawn_circle_img = self.vision.getBlobsData(img)

        print(amount_of_blobs, coords)
        try:
            self.tools.SaveImage("test_bw_image.jpg", black_white_im)
        except:
            print("black and white filter image not saved")
        try:
            self.tools.SaveImage("test_image_found_circles.jpg", drawn_circle_img)
        except:
            print("Drawn circle image not saved")

        self.tools.cUnsubscribe()
        return amount_of_blobs, coords

    def turn_head(self, in_front=True):
        print("Turn_head")
        # Lookleft
        if in_front:
            directions = [0, 0.45*np.pi, -1.05*np.pi]
        else:
            directions = [0.45*np.pi, -1.05*np.pi]

        for direction in directions:
            self.globals.motProxy.moveTo(0, 0, direction)
            # self.turn_straight()
            n_blobs, blobsList = self.see_picture()
            n_blobs_per_colour = [len(colour) for colour in blobsList]
            if n_blobs == 3 and min(n_blobs_per_colour) == max(n_blobs_per_colour) == 1:
                if direction < 0:
                    direction = -0.45 * np.pi
                return n_blobs, blobsList, direction
            elif len(blobsList[0]) == 1:
                if direction < 0:
                    direction = -0.45 * np.pi
                return 1, blobsList, direction
        self.globals.motProxy.moveTo(0, 0, 0.45 * np.pi)
        return -1, [], 0
   
    def check_left_right(self):
        n_blobs, blobsList, direction = self.turn_head(in_front=False)
        if n_blobs == 3:
            return n_blobs, blobsList, direction
        elif n_blobs == 1:
            return n_blobs, blobsList, direction
        return -1, [], 0