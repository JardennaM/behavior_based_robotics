import cv2
import numpy, math
import numpy as np
from itertools import combinations, product

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
        """Filters image to black and white inbetween color range. 
        Returns circles found in black and white image"""
        bw_image = self.filterImage(image, bgr_low, bgr_high)
        blobs = self.findCircle(bw_image)
        return blobs, bw_image


    def cutout_paper(self, image, blueBlobs):
        """Masks paper out of the whole image by filling up the shape where the blueBlob was found"""
        # Prepare image
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        canny = cv2.Canny(gray, 130, 255, 10)
        mask = np.full(gray.shape, 255 ,dtype=np.uint8)     # Create mask
        
        
        # Draw Hough Lines
        lines = cv2.HoughLines(canny,1,np.pi/180,75)
        try:
            len(lines)
        except:
            return image
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

    def find_in_bound_blobs(self, blobsList, image_dim):
        in_bounds_blobs = []
        for blobList in blobsList:
            legal_blobs = []
            for blob in blobList:
                blob_dim = blob[:2]
                # Blob out of bounds
                if blob_dim[0] > image_dim[0] or blob_dim[1] > image_dim[1]:
                    continue
                # Legal blob
                else:
                    legal_blobs.append(blob)
            # Append all legal blobs
            in_bounds_blobs.append(np.asarray(legal_blobs))
        return np.asarray(in_bounds_blobs)

    def find_plausible_blobs(self, blobsList):
        ps = list(product(*blobsList))
        plausible_blobLists = []
        for p in ps:
            blue, green, red = p
            coords = [blue[:2], green[:2], red[:2]]
            center = self.calcMidLandmark(coords)
            
            DistFromCenter = self.calcDistanceFromCenter(coords, center)
            std_DistanceFromCenter = np.std(DistFromCenter)

            if std_DistanceFromCenter > max(DistFromCenter) * 0.2:
                continue

            else:
                plausible_blobLists.append(p)
        return plausible_blobLists

    # Proces image to detect color blobs
    def getBlobsData(self, image):
        '''
        Input: Image
        Return: numberOfBlobsFound , [List [center-pixels] of blobs]
        '''

        # Filter blue circle
        # blueBlobs, bw_image_blue = self.filter_find_circle(image, [70,0,0],[255,100,100])
        blueBlobs, bw_image_blue = self.filter_find_circle(image, [80,0,0],[255,100,100])
        

        # Check wether blue circle was found
        blueLen = len(blueBlobs)

        # Cut out section with blobs from picture
        if blueLen == 1:
            image = self.cutout_paper(image, blueBlobs)
        
        # Filter for green blobs
        # greenBlobs, bw_image_green = self.filter_find_circle(image, [0,70,0],[100,255,100])
        greenBlobs, bw_image_green = self.filter_find_circle(image, [0,80,0],[120,255,120])
        # Filter for red blobs
        # redBlobs, bw_image_red = self.filter_find_circle(image, [0,0,170], [95,130,255])
        redBlobs, bw_image_red = self.filter_find_circle(image, [0,0,170], [100,130,255])

        ########## OPTIONAL ###############
        # Add all filtered images for total black/white image
        filter_image = bw_image_blue + bw_image_green + bw_image_red

        # Check wether green and red circle was found
        greenLen = len(greenBlobs)
        redLen = len(redBlobs)

        print("Blue blobs", blueBlobs)
        print("green blobs", greenBlobs)
        print("red blobs", redBlobs)

        blobsList = [blueBlobs, greenBlobs, redBlobs]
        print("Full bloblist", blobsList)
        # print(blobsList)
        if blueLen == 0 or greenLen == 0 or redLen == 0:
            xyblobsList = self.slice_coords(blobsList)
            drawn_circles = self.drawCircles(blobsList)
            return blueLen + greenLen + redLen, xyblobsList, filter_image, drawn_circles

        # Get dimensions of picture and reverse them for ease of use (x, y)
        image_dim = np.asarray(list(image.shape[:2])[::-1], dtype=float)

        # Find all blobs in dimensions of picture
        blobsList = self.find_in_bound_blobs(blobsList, image_dim)
        # blobsList = np.asarray([np.asarray([np.asarray([121,  127,   22])]),

        # np.asarray([np.asarray([195,  175,   21]), np.asarray([1,2,3])]),

        # np.asarray([np.asarray([199,   83,   21])])])

        # print("=================================================================")
        # print(blobsList)

        # print("=============================================================")

        # Recalculate number of found blobs
        blueLen = len(blobsList[0])
        greenLen = len(blobsList[1])
        redLen = len(blobsList[2])

        # Check if there is a blob of each colour
        if blueLen == 0 or greenLen == 0 or redLen == 0:
            xyblobsList = self.slice_coords(blobsList)
            drawn_circles = self.drawCircles(blobsList)
            return blueLen + greenLen + redLen, xyblobsList, filter_image, drawn_circles

        # Radius check for all blobs
        n_blobs_per_colour = [len(blobList) for blobList in blobsList]
        mean_blobs = np.mean(n_blobs_per_colour)
        n_blobs = sum(n_blobs_per_colour)

        print(mean_blobs)
        print(n_blobs)
        print(blueLen, greenLen, redLen)

        print(min(blueLen, greenLen, redLen))
        print(max(blueLen, greenLen, redLen))
        print(3 > n_blobs > 7)
        # Check combinations if there 4 or 5 blobs and each list contains at least 1 and at most 2 blobs
        if mean_blobs != 1.0 and n_blobs > 3 and n_blobs < 7 and min(blueLen, greenLen, redLen) > 0 and max(blueLen, greenLen, redLen) < 4:
            print("AVERAGE IS NOT EQUAL TO ONE. LOOKING FOR PLAUSIBLE BLOB COMBINATIONS")
            plausible_blobLists = self.find_plausible_blobs(blobsList)
                
            if len(plausible_blobLists) == 1:
                print("One plausible blob combination found")
                blobsList = plausible_blobLists[0]
                n_blobs = len(xyblobsList[0]) + len(xyblobsList[1]) + len(xyblobsList[2])
                
            else:
                print("Too many or too little plausible blobs found")
                return 0, np.asarray([[], [], []]), filter_image, filter_image

        print(blobsList)
        xyblobsList = self.slice_coords(blobsList)
        drawn_circles = self.drawCircles(blobsList)
        return n_blobs, xyblobsList, filter_image, drawn_circles

    def get_correct_blobsList(self, blobsList):
        lenList = [len(colour) for colour in blobsList]
        if max(lenList) == min(lenList) == 1:
            new_blobsList = []
            for colour in blobsList:
                new_blobsList.append(colour[0])
            return 3, new_blobsList
        return 0, []
            

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

    def calcDistanceFromCenter(self, blobList, center):
        '''
        Input: [Pink, Blue, Orange]
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
        
    def getInformation(self, coords):
        distance = self.calcAvgBlobDistance(coords)
        center = self.calcMidLandmark(coords)
        angle = self.calcAngleLandmark(center)
        signature = self.findSignature(coords)
        return distance, center, angle, signature

