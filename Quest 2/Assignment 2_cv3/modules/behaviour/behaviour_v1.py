import time

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
        self.globals.posProxy.goToPosture("Stand", 1)
        sonar = self.sonar.avg_sonar()

        while sonar[0] > 0.35 and sonar[1] > 0.35:
            print(sonar)
            time.sleep(2)
            self.globals.posProxy.goToPosture("StandInit", 1)
            self.globals.motProxy.moveTo(0.2, 0, 0)
            time.sleep(2)
            self.globals.posProxy.goToPosture("Stand", 1)
            sonar = self.sonar.avg_sonar()


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
                print(abs(difference))
                print((min(sonar) * distance_param))
                print('----')
        elif difference < 0:
            while difference < (min(sonar) * distance_param):
                self.globals.motProxy.moveTo(0, 0, radians)
                sonar = self.sonar.avg_sonar()
                difference = sonar[0] - sonar[1]
                print(abs(difference))
                print((min(sonar) * distance_param))
                print('----')


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

    
    def look_around(self, left, right):
        '''
        Input: direction: left, right, up, down

        '''
        self.globals.posProxy.goToPosture("StandInit", 1)
        if direction == "s":
            self.motion.changeHead(0, 0)

        if direction == "l":
            self.motion.changeHead(0.25, 0)

        if direction == "r":
            self.motion.changeHead(-0.25, 0)

        if direction == "u":
            self.motion.changeHead(0, -0.25)

        if direction == "d":
            self.motion.changeHead(0, 0.25)

        else:
            self.motion.changeHead(0, direction)

    def explore(self):
        pass