import cv2
# import cv2.cv as cv
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

    #Filter HSV Image with given values
    def filterImage(self, img, min_bgr, max_bgr):
        '''
        Input: HSV Image, 2 List of min and max HSV values
        Output: Black White Matrix/Image
        '''
        ## implement your filtering here.
        img = img
        min_scal = np.array(min_bgr)
        max_scal = np.array(max_bgr)

        resultimg = cv2.inRange(img, min_scal, max_scal)

        return cv2.blur(resultimg, (3,3))
        # return resultimg
        
       
    #Find Circle in a filtered image
    def findCircle(self,imgMat):
        '''
        Input: Black Whit Image
        Return: List of center position of found Circle
        '''

        img = imgMat

        # Hough algorithm parameters
        dp = 2
        minD = 30  
        p1 = 255
        p2 = 27
        minS = 15
        maxS = 70
        circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, dp, minD, None, p1, p2, minS, maxS)

        # # Hough algorithm parameters
        # dp = 2
        # minD = 30  
        # p1 = 255
        # p2 = 27
        # minS = 20 #15
        # maxS = 100 #80
        # circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, dp, minD, None, p1, p2, minS, maxS)




        if len(circles[0]) == 0: # circles == None
            return None
        else:
            return np.reshape(circles,(circles.shape[1],circles.shape[2]))

    def in_range_bgr(self,img,bgr_low,bgr_high):
        return cv2.inRange(img, np.array(bgr_low), np.array(bgr_high))


    # Proces image to detect color blobs
    def getBlobsData(self, image):
        '''
        Input: Image
        Return: numberOfBlobsFound , [List [center-pixels] of blobs]
        '''

        # Samen vs Apart filters testen
        bw_img_blue = self.filterImage(image, [90,0,0],[255,100,100])
        blueBlobs = self.findCircle(bw_img_blue)

        bw_img_green = self.filterImage(image, [0,90,0],[100,255,100])
        greenBlobs = self.findCircle(bw_img_green)

        bw_img_red = self.filterImage(image, [0,0,170], [95,130,255])
        redBlobs = self.findCircle(bw_img_red)

        imagearray = bw_img_blue + bw_img_green + bw_img_red


        if (len(blueBlobs) != 1 or len(greenBlobs) != 1 or len(redBlobs) != 1):
            return 0, None, imagearray 

        blobsList = np.asarray([blueBlobs[0], greenBlobs[0], redBlobs[0]])
        blobsFound = len(blobsList)
        print(blobsList)


        found_img = self.drawCircles(blobsList)
        self.tools.SaveImage("test_bw_image.jpg", imagearray)
        self.tools.SaveImage("test_image_found_circles.jpg", found_img)

        # bw_img_blue = self.filterImage(image, [45,0,0],[255,100,100])
        # bw_img_green = self.filterImage(image, [0,45,0],[100,255,100])
        # bw_img_red = self.filterImage(image, [0,0,130], [95,130,255])
        # imagearray = bw_img_blue + bw_img_green + bw_img_red
        # blobsList = self.findCircle(imagearray)
        # if blobsList != []:
        #     blobsFound = len(blobsList)
        # else:
        #    0
            
        return blobsFound, blobsList[:, 1:], imagearray

    def drawCircles(self,circle_data):
        if circle_data != []:
            img = np.zeros((320,400,3), np.uint8)
            for i in circle_data:
                if i != []:
                    cv2.circle(img,(i[0],i[1]),i[2],(255,255,255),-1)
            # return cv.fromarray(img)
            return img
        else:
            print "NO CIRCLES"


    # Get Average Distance between multiple blobs
    def calcAvgBlobDistance(self, blobList):
        '''
        Input: [Pink, Blue, Orange]
        Output: Avarege Distance in pixels
        '''

        if len(blobList) == 0 or len(blobList) == 1:
            return None
        Distance = 0
        total_combinations = 0
        
        combs = combinations(blobList, 2)
        for comb in combs:
            Distance += numpy.linalg.norm(comb[0] - comb[1])  
            total_combinations += 1         


        Distance /= total_combinations
        return Distance

    # Find centre of a Landmark
    def calcMidLandmark(self, blobList):
        '''
        Input: [Pink, Blue, Orange]
        Output: center pixel as (x,y)
        '''
        if blobList == []:
            return []
        return np.sum(blobList, 0) / len(blobList)

    # Find the angle between a found Landmark and the Nao
    def calcAngleLandmark(self, center):
        '''
        Input: center pixel, (x,y)
        Output: Angle in radians
        '''
        if center == []:
            return None

        center -= np.asarray([160, 120])
        center *= 0.0038

        return abs(center[0])

    # Find the Signature
    def findSignature(self,blobList):
        '''
        Input: [Pink, Blue, Orange]
        Output: Signature
        '''
        
        blue_green = blobList[0] - blobList[1]
        blue_red = blobList[0] - blobList[2]

        print("1")
        if blue_green[1] > 0 and blue_red[1] > 0 and blue_green[0] < 0 and blue_red[0] > 0:
            return "Finish"

        if blue_green[0] > 0 and blue_red[0] > 0 and blue_green[1] > 0 and blue_red[1] < 0:
            return "Right"
        
        if blue_green[0] < 0 and blue_red[0] < 0 and blue_green[1] < 0 and blue_red[1] > 0:
            return "Left"

        return -1
        


