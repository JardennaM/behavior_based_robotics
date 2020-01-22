class behaviour_v1():    
    globals = None

    def setDependencies(self, modules):
        self.globals = modules.getModule("globals")
        self.motion = modules.getModule("motion")
        
    #React to found observations  
    def calcDirection(self, blobsFound, blobDist, angle, signature):
        '''
        Input: Stuff
        Output: less to no stuff
        '''


    def nav_to_middle(self, sonar):
        '''
        Input: sonardata
        
        Checks if robot walk in middle of maze path.
        If not, it turns to return to the middle.
        '''

    def follow_wall(self, sonar):
        '''
        Input: sonardata

        Follows wall until end.
        '''


    def face_wall(self, sonar):
        '''
        Input: sonardata
        
        Checks if robot faces the wall perpendicularly.
        If not, it positions itself.
        '''

    
    def look_around(self, sonar):
        '''
        Input: amount of blobs

        
        '''

    def explore(self):
        