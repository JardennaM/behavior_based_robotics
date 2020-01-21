# import cv2
# # import cv2.cv as cv
# import numpy, math
# import numpy as np
# from itertools import combinations

# def cv2_wait():
#     key = cv2.waitKey(-1) & 0xFF
#     if key==27:    # Esc key to stop
#         cv2.destroyAllWindows()
#         exit()
#     return key

# class vision_v1():
#     globals = None

#     def setDependencies(self, modules):
#         self.globals = modules.getModule("globals")

#     #Filter HSV Image with given values
#     def filterImage(self, img, min_bgr, max_bgr):
#         '''
#         Input: HSV Image, 2 List of min and max HSV values
#         Output: Black White Matrix/Image
#         '''
#         ## implement your filtering here.
#         img = img
#         min_scal = np.array(min_bgr)
#         max_scal = np.array(max_bgr)

#         resultimg = cv2.inRange(img, min_scal, max_scal)

#         return cv2.blur(resultimg, (3,3))
#         # return resultimg
        
       
#     #Find Circle in a filtered image
#     def findCircle(self,imgMat):
#         '''
#         Input: Black Whit Image
#         Return: List of center position of found Circle
#         '''

#         img = imgMat

#         # Hough algorithm parameters
#         dp = 2
#         minD = 30  
#         p1 = 255
#         p2 = 27
#         minS = 15
#         maxS = 70
#         circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, dp, minD, None, p1, p2, minS, maxS)

#         # # Hough algorithm parameters
#         # dp = 2
#         # minD = 30  
#         # p1 = 255
#         # p2 = 27
#         # minS = 20 #15
#         # maxS = 100 #80
#         # circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, dp, minD, None, p1, p2, minS, maxS)

#         try:
#             n_circles = len(circles)
#             return np.reshape(circles,(circles.shape[1],circles.shape[2]))
#         except TypeError:
#             return None

#         # if n_circles == 0: # circles == None
#         #     return None
#         # else:
#         #     return np.reshape(circles,(circles.shape[1],circles.shape[2]))

#     def in_range_bgr(self,img,bgr_low,bgr_high):
#         return cv2.inRange(img, np.array(bgr_low), np.array(bgr_high))


#     # Proces image to detect color blobs
#     def getBlobsData(self, image):
#         '''
#         Input: Image
#         Return: numberOfBlobsFound , [List [center-pixels] of blobs]
#         '''

#         # Samen vs Apart filters testen
#         bw_img_blue = self.filterImage(image, [90,0,0],[255,100,100])
#         blueBlobs = self.findCircle(bw_img_blue)

#         try:
#             blueLen = len(blueBlobs)
#         except:
#             print("No blue")
#             return 0, None, None, None

#         # only white paper
#         gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#         canny = cv2.Canny(gray, 130, 255, 10)

#         # cv2.imshow("result", canny)
#         # cv2.waitKey(0)

#         mask = np.ones(gray.shape)
#         lines = cv2.HoughLines(canny,1,np.pi/180,75)
#         print(lines)
#         for line in lines:
#             for rho,theta in line:
#                 a = np.cos(theta)
#                 b = np.sin(theta)
#                 x0 = a*rho
#                 y0 = b*rho
#                 x1 = int(x0 + 1000*(-b))
#                 y1 = int(y0 + 1000*(a))
#                 x2 = int(x0 - 1000*(-b))
#                 y2 = int(y0 - 1000*(a))

#                 cv2.line(image,(x1,y1),(x2,y2),(0,0,0),2)

#         # cv2.imshow("result", mask)
#         # cv2.waitKey(0)



#         # cnts = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#         # cnts = cnts[0] if len(cnts) == 2 else cnts[1]

#         # for c in cnts:
#         #     cv2.drawContours(image, [c], 0, (0, 255, 0), 3)
#         #     print(len(c))

#         # mask = np.ones(gray.shape)
#         # mask = cv2.drawContours(mask, cnts[3:6], -1, 0, cv2.FILLED)
        
#         # h, w = mask.shape[:2]
#         # mask2 = np.zeros((h+2, w+2), np.uint8)

#         output = image.copy()
#         output[mask.astype(np.bool), :] = 0

#         # cv2.floodFill(mask, mask2, (0,0), 255)

#         cv2.imshow("result", output)
#         cv2.waitKey(0)
#         # cv2.imwrite("images/input.png", input)
#         # cv2.imwrite("images/mask.png", np.uint8(255 * mask))
#         # cv2.imwrite("images/output.png", output)
        
        

#         bw_img_green = self.filterImage(image, [0,90,0],[100,255,100])
#         greenBlobs = self.findCircle(bw_img_green)

#         bw_img_red = self.filterImage(image, [0,0,170], [95,130,255])
#         redBlobs = self.findCircle(bw_img_red)

#         imagearray = bw_img_blue + bw_img_green + bw_img_red

#         print("Amount of blue blobs:", len(blueBlobs), blueBlobs)
#         print("Amount of green blobs:", len(greenBlobs), greenBlobs)
#         print("Amount of red blobs:", len(redBlobs), redBlobs)

#         if (len(blueBlobs) != 1 or len(greenBlobs) != 1 or len(redBlobs) != 1):
#             blobsList = np.asarray(blueBlobs + greenBlobs + redBlobs)
#             found_img = self.drawCircles(blobsList)
#             print(blobsList)
#             return len(blobsList), blobsList, imagearray, found_img

#         blobsList = np.asarray([blueBlobs[0], greenBlobs[0], redBlobs[0]])
#         blobsFound = len(blobsList)
#         print(blobsList)


#         found_img = self.drawCircles(blobsList)

#         # bw_img_blue = self.filterImage(image, [45,0,0],[255,100,100])
#         # bw_img_green = self.filterImage(image, [0,45,0],[100,255,100])
#         # bw_img_red = self.filterImage(image, [0,0,130], [95,130,255])
#         # imagearray = bw_img_blue + bw_img_green + bw_img_red
#         # blobsList = self.findCircle(imagearray)
#         # if blobsList != []:
#         #     blobsFound = len(blobsList)
#         # else:
#         #    0
            
#         return blobsFound, blobsList[:, :2], imagearray, found_img

#     def drawCircles(self,circle_data):
#         if circle_data != []:
#             # img = np.zeros((320,400,3), np.uint8)
#             img = np.zeros((240,320,3), np.uint8)
#             for i in circle_data:
#                 if i != []:
#                     cv2.circle(img,(i[0],i[1]),i[2],(255,255,255),-1)
#             # return cv.fromarray(img)
#             return img
#         else:
#             print "NO CIRCLES"


#     # Get Average Distance between multiple blobs
#     def calcAvgBlobDistance(self, blobList):
#         '''
#         Input: [Pink, Blue, Orange]
#         Output: Avarege Distance in pixels
#         '''
    
#         if len(blobList) == 0 or len(blobList) == 1:
#             return None
#         Distance = 0
#         total_combinations = 0
        
#         combs = combinations(blobList, 2)
#         for comb in combs:
#             Distance += numpy.linalg.norm(comb[0] - comb[1])  
#             total_combinations += 1         


#         Distance /= total_combinations
#         return Distance

#     # Find centre of a Landmark
#     def calcMidLandmark(self, blobList):
#         '''
#         Input: [Pink, Blue, Orange]
#         Output: center pixel as (x,y)
#         '''
#         if blobList == []:
#             return []
#         return np.sum(blobList, 0) / len(blobList)

#     # Find the angle between a found Landmark and the Nao
#     def calcAngleLandmark(self, center):
#         '''
#         Input: center pixel, (x,y)
#         Output: Angle in radians
#         '''
#         if center == []:
#             return None

#         center -= np.asarray([120, 160])
#         center *= 0.0038

#         return abs(center[0])

#     # Find the Signature
#     def findSignature(self,blobList):
#         '''
#         Input: [Pink, Blue, Orange]
#         Output: Signature
#         '''

#         blue_green = blobList[0] - blobList[1]
#         blue_red = blobList[0] - blobList[2]
#         print(blue_green)
#         print(blue_red)

#         if blue_green[1] > 0 and blue_red[1] > 0 and blue_green[0] < 0 and blue_red[0] > 0:
#             return "Finish"

#         if blue_green[0] > 0 and blue_red[0] > 0 and blue_green[1] > 0 and blue_red[1] < 0:
#             return "Right"
        
#         if blue_green[0] < 0 and blue_red[0] < 0 and blue_green[1] < 0 and blue_red[1] > 0:
#             return "Left"

#         return -1
        
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

        # return resultimg
        return cv2.blur(resultimg, (3,3))
        
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

        try:
            n_circles = len(circles)
            return np.reshape(circles,(circles.shape[1],circles.shape[2]))
        except TypeError:
            return None

    def in_range_bgr(self,img,bgr_low,bgr_high):
        return cv2.inRange(img, np.array(bgr_low), np.array(bgr_high))


    # Proces image to detect color blobs
    def getBlobsData(self, image):
        '''
        Input: Image
        Return: numberOfBlobsFound , [List [center-pixels] of blobs]
        '''

        # Filter blue circle
        bw_img_blue = self.filterImage(image, [90,0,0],[255,100,100])
        blueBlobs = self.findCircle(bw_img_blue)

        # Check wether blue circle was found
        try:
            blueLen = len(blueBlobs)
        except:
            print("No blue circles found")
            return 0, [], None, None

        # Cut out section with blobs from picture
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        canny = cv2.Canny(gray, 130, 255, 10)
        mask = np.full(gray.shape, 255 ,dtype=np.uint8)
        lines = cv2.HoughLines(canny,1,np.pi/180,75)
        
        # Draw Hough Lines
        for line in lines:
            for rho,theta in line:
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a*rho
                y0 = b*rho
                x1 = int(x0 + 1000*(-b))
                y1 = int(y0 + 1000*(a))
                x2 = int(x0 - 1000*(-b))
                y2 = int(y0 - 1000*(a))

                cv2.line(mask,(x1,y1),(x2,y2),0,2)
        
        # Find contours of Hough lines
        contours = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = contours[0] if len(contours) == 2 else contours[1]
        
        # Create mask for floodfill
        h, w = mask.shape[:2]
        mask2 = np.zeros((h+2, w+2), np.uint8)

        # Fill mask from blob
        cv2.floodFill(mask, mask2, tuple(blueBlobs[0][:2]), 0)
        image[mask.astype(np.bool), :] = 0
        
        # Filter for green blobs
        bw_img_green =  self.filterImage(image, [0,90,0],[100,255,100])
        greenBlobs =  self.findCircle(bw_img_green)

        # Filter for red blobs
        bw_img_red =  self.filterImage(image, [0,0,170], [95,130,255])
        redBlobs =  self.findCircle(bw_img_red)

        ########## OPTIONAL ###############
        # Add all filtered images for total black/white image
        filter_image = bw_img_blue + bw_img_green + bw_img_red

        # Check wether green and red circle was found
        try:
            greenLen = len(greenBlobs)
            redLen = len(redBlobs)
        except:
            print("No green circles found")
            return 0, [], None, None

        # Temporary prints for amount of blobs
        print("Amount of blue blobs:", len(blueBlobs), blueBlobs)
        print("Amount of green blobs:", len(greenBlobs), greenBlobs)
        print("Amount of red blobs:", len(redBlobs), redBlobs)

        # Get dimensions of picture and reverse them for ease of use (x, y)
        image_dim = np.asarray(list(image.shape[:2])[::-1], dtype=float)

        # Find all blobs in dimensions of picture
        in_bounds_blobs = []
        for blobList in [blueBlobs, greenBlobs, redBlobs]:
            legal_blobs = []
            for blob in blobList:
                blob_dim = blob[:2]
                # Blob out of bounds
                if blob_dim[0] > image_dim[0] or blob_dim[1] > image_dim[1]:
                    continue
                # Legal blob
                else:
                    legal_blobs.append(blob)
            # No legal blobs found of certain colour
            if legal_blobs == []:
                return 0, [], None, None
            in_bounds_blobs.append(legal_blobs)

        # Radius check for all blobs
        mean_blobs = np.mean([len(blobList) for blobList in in_bounds_blobs])
        if mean_blobs != 1:
        
            
            total = np.sum(in_bounds_blobs, axis=0)
            total = np.sum(total, axis=0)
            total = np.sum(total, axis=0)
            print("Sum of blobs", total)


        # Create bloblist
        blobsList = np.asarray([blueBlobs[0], greenBlobs[0], redBlobs[0]])
        blobsFound = len(blobsList)

        ########## OPTIONAL ###############
        # Make reconstruction of black/white blobs
        found_image =  self.drawCircles(blobsList)
            
        return blobsFound, blobsList[:, :2], filter_image, found_image

    def drawCircles(self,circle_data):
        if circle_data != []:
            img = np.zeros((240,320,3), np.uint8)
            for i in circle_data:
                if i != []:
                    cv2.circle(img,(i[0],i[1]),i[2],(255,255,255),-1)
            return img
        else:
            print "NO CIRCLES"


    # Get Average Distance between multiple blobs
    def calcAvgBlobDistance(self, blobList):
        '''
        Input: [Pink, Blue, Orange]
        Output: Avarege Distance in pixels
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

        # Correct for middle of picture
        center -= np.asarray([120, 160])

        # Calculate angle with 0.0038 degrees for every pixel
        center *= 0.0038

        # Return only horizontal angle
        ####### !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ##################
        # Goede dimensie gereturned?? Moet misschien center[1] zijn?????
        return abs(center[0])

    # Find the Signature
    def findSignature(self,blobList):
        '''
        Input: [Pink, Blue, Orange]
        Output: Signature
        '''

        # Calculate relative position of blue for green and red respectively
        blue_green = blobList[0] - blobList[1]
        blue_red = blobList[0] - blobList[2]

        # Blue blob above both others
        if blue_green[1] > 0 and blue_red[1] > 0 and blue_green[0] < 0 and blue_red[0] > 0:
            return "Finish"

        # Green above and to left, red below and to left of blue
        if blue_green[0] > 0 and blue_red[0] > 0 and blue_green[1] > 0 and blue_red[1] < 0:
            return "Right"
        
        # Red above and to right, green below and to right of blue
        if blue_green[0] < 0 and blue_red[0] < 0 and blue_green[1] < 0 and blue_red[1] > 0:
            return "Left"

        # Unknown orientation of blobs
        return -1
        




