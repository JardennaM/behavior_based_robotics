# import cv2.cv as cv
import cv2
import numpy, math
import numpy as np
from itertools import combinations

def cv2_wait():
    key = cv2.waitKey(-1) & 0xFF
    if key==27:    # Esc key to stop
        cv2.destroyAllWindows()
        exit()
    return key

class vision_v1():
    globals = None

    def setDependencies(self, modules):
        self.globals = modules.getModule("globals")

    #Filter RGB Image with given values
    def filterImage(self, img, min_bgr, max_bgr):
        '''
        Input: RGB Image, 2 List of min and max RGB values
        Output: Black White Matrix/Image
        '''
        ## implement your filtering here.
        img = img
        min_scal = np.array(min_bgr)
        max_scal = np.array(max_bgr)

        resultimg = cv2.inRange(img, min_scal, max_scal)

        return cv2.blur(resultimg, (3,3))
        
       
    #Find Circle in a filtered image
    def findCircle(self,imgMat):
        '''
        Input: Black White Image
        Return: List of center position of found Circle
        '''
        img = imgMat

        # Hough algorithm parameters
        dp = 2
        minD = 30  
        p1 = 255
        p2 = 27
        minS = 8
        maxS = 70
        circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, dp, minD, None, p1, p2, minS, maxS)

        try:
            n_circles = len(circles)
            return np.reshape(circles,(circles.shape[1],circles.shape[2]))
        except TypeError:
            return np.asarray([])

    def in_range_bgr(self,img,bgr_low,bgr_high):
        return cv2.inRange(img, np.array(bgr_low), np.array(bgr_high))


    def filter_find_circle(self, image, bgr_low, bgr_high):
        """
        Input: RGB image, lower RGB threshold, higher RGB threshold
        Filters image to black and white inbetween color range. 
        Returns circles found in black and white image
        """
        bw_image = self.filterImage(image, bgr_low, bgr_high)
        blobs = self.findCircle(bw_image)
        return blobs, bw_image

    def cutout_paper(self, image, blueBlobs):
        """
        Input: Image, xy position of blue Circle
        Masks paper out of the whole image by filling up the shape from center of largest contour found
        Returns: Blacked out image with only white paper preserved
        """
        # Prepare image
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, 160, 255, 0)
        # Create mask
        mask = np.full(gray.shape, 255, dtype=np.uint8)

        # Find contours of Hough lines
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        biggest_contour = 0
        mid_paper = blueBlobs[0][:2]
        for c, h in zip(contours, hierarchy[0]):
            if h[3] == -1 and h[2] > -1:
                cv2.drawContours(mask, [c], -1, (0,255,0), 1)
                if len(c) > biggest_contour:
                    mid_paper = np.mean(c, axis=0, dtype=int)
                    biggest_contour = len(c)
        
        # Create mask for floodfill
        h, w = mask.shape[:2]
        mask2 = np.zeros((h+2, w+2), np.uint8)

        # Fill mask from blob
        cv2.floodFill(mask, mask2, tuple(mid_paper[0]), 0)
        image[mask.astype(np.bool), :] = 0

        return image

    def slice_coords(self, blobsList):
        """
        Input: blobsList with [x , y , radius]
        Returns: Array with x, y coordinates according to number of blobs found
        """
        xyblobsList = []
        for blobList in blobsList:
            if len(blobList) == 0:
                xyblobsList.append([])
            else:
                xyblobsList.append(blobList[:, :2])

        return np.asarray(xyblobsList)

    # Proces image to detect color blobs
    def getBlobsData(self, image):
        '''
        Input: Image
        Function: Will find the centers (in pixel coordinates) of blue, green and red circles
        in image using HoughCircles function from OpenCV
        Return: numberOfBlobsFound , [List [center-pixels] of blobs]
        '''

        # Filter blue circle
        blueBlobs, bw_image_blue = self.filter_find_circle(image, [80,0,0],[255,100,100])

        # Check wether blue circle was found
        blueLen = len(blueBlobs)

        # Cut out section with blobs from picture
        if blueLen == 1:
            image = self.cutout_paper(image, blueBlobs)
        
        # Filter for green blobs
        greenBlobs, bw_image_green = self.filter_find_circle(image, [0,80,0],[120,255,120])
        # Filter for red blobs
        redBlobs, bw_image_red = self.filter_find_circle(image, [0,0,170], [100,130,255])

        ########## OPTIONAL ###############
        # Add all filtered images for total black/white image
        filter_image = bw_image_blue + bw_image_green + bw_image_red

        # Check whether green and red circle were found
        greenLen = len(greenBlobs)
        redLen = len(redBlobs)

        blobsList = [blueBlobs, greenBlobs, redBlobs]
        print("Full bloblist", blobsList)

        xyblobsList = self.slice_coords(blobsList)
        drawn_circles = self.drawCircles(blobsList)
        return blueLen + greenLen + redLen, xyblobsList, filter_image, drawn_circles


    def drawCircles(self,circle_data):
        if circle_data != []:
            img = np.zeros((240,320,3), np.uint8)
            for colour in circle_data:
                # Only 1 blob found
                if colour != []:
                    if type(colour[0]) is float or type(colour[0]) is int:
                        if colour != []:
                            cv2.circle(img,(colour[0],colour[1]),colour[2],(255,255,255),-1)
                    # Multiple blobs found
                    else: 
                        for circle in colour:
                            if circle != []:
                                cv2.circle(img,(circle[0],circle[1]),circle[2],(255,255,255),-1)
            return img
        else:
            print "NO CIRCLES"


    # Get Average Distance between multiple blobs
    def calcAvgBlobDistance(self, blobList):
        '''
        Input: [Blue, Green, Red]
        Output: Average Distance in pixels
        '''

        # Check if there are enough blobs
        if len(blobList) == 0 or len(blobList) == 1:
            return None
        Distance = 0
        total_combinations = 0
        
        # Adds up distances of all possible combinations
        combs = combinations(blobList, 2)
        for comb in combs:
            Distance += numpy.linalg.norm(comb[0] - comb[1])  
            total_combinations += 1         

        # Calculate average distance
        Distance /= total_combinations
        return Distance

    # Find centre of a Landmark
    def calcMidLandmark(self, blobList):
        '''
        Input: [Blue, Green, Red]
        Output: center pixel as (x,y)
        '''
        if blobList == []:
            return []
        return np.sum(blobList, 0) / len(blobList)

    def calcDistanceFromCenter(self, blobList, center):
        '''
        Input: [Blue, Green, Red]
        Output: Avarege Distance in pixels per blob
        '''
        return [numpy.linalg.norm(blob - center) for blob in blobList]

    # Find the angle between a found Landmark and the Nao
    def calcAngleLandmark(self, center):
        '''
        Input: center pixel, (x,y)
        Output: Angle in radians
        '''
        if center == []:
            return None

        # Correct for middle of picture
        center -= np.asarray([120, 160])
        
        # Calculate angle with 0.0038 degrees for every pixel
        center *= 0.0038

        # Return only horizontal angle
    
        return center[0]

    # Find the Signature
    def findSignature(self,blobList):
        '''
        Input: [Blue, Green, Red]
        Output: Signature
        '''
        # Calculate relative position of blue for green and red respectively
        blue_green = blobList[0] - blobList[1]
        blue_red = blobList[0] - blobList[2]

        # Blue blob above both others
        if blue_green[1] < 0 and blue_red[1] < 0 and blue_green[0] > 0 and blue_red[0] < 0:
            return "Finish"

        # Green above and to left, red below and to left of blue
        if blue_green[0] > 0 and blue_red[0] > 0 and blue_green[1] > 0 and blue_red[1] < 0:
            return "Right"
        
        # Red above and to right, green below and to right of blue
        if blue_green[0] < 0 and blue_red[0] < 0 and blue_green[1] < 0 and blue_red[1] > 0:
            return "Left"

        # Blue blob under both others
        if blue_green[1] > 0 and blue_red[1] > 0 and blue_green[0] < 0 and blue_red[0] > 0:
            return "Back"

        # Unknown orientation of blobs
        return -1
        

    def get_correct_blobsList(self, blobsList):
        """
        Input: found blobsList
        Output: Returns list with 3 circles coordinates if there is one circle of each colour
        """
        lenList = [len(colour) for colour in blobsList]
        if max(lenList) == min(lenList) == 1:
            new_blobsList = []
            for colour in blobsList:
                new_blobsList.append(colour[0])
            return 3, new_blobsList
        return 0, []

    def getInformation(self, coords):
        """
        Input: list of xy Coordinates of 3 circles
        Output: Various calculations based on xy coordinates
        """
        distance = self.calcAvgBlobDistance(coords)
        center = self.calcMidLandmark(coords)
        angle = self.calcAngleLandmark(center)
        signature = self.findSignature(coords)
        return distance, center, angle, signature


