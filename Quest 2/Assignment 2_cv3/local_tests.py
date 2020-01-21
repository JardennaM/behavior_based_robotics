import cv2
# import cv2.cv as cv
import numpy, math
import numpy as np
from itertools import combinations
# from naoqi import ALProxy
import time
import sys


#Filter HSV Image with given values
def filterImage( img, min_bgr, max_bgr):
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
def findCircle(imgMat):
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

def in_range_bgr(img,bgr_low,bgr_high):
    return cv2.inRange(img, np.array(bgr_low), np.array(bgr_high))


# Proces image to detect color blobs
def getBlobsData(image):
    '''
    Input: Image
    Return: numberOfBlobsFound , [List [center-pixels] of blobs]
    '''

    # Filter blue circle
    bw_img_blue = filterImage(image, [90,0,0],[255,100,100])
    blueBlobs = findCircle(bw_img_blue)

    # Check wether blue circle was found
    try:
        blueLen = len(blueBlobs)
    except:
        print("No blue circles found")
        return 0, None, None, None

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
    bw_img_green = filterImage(image, [0,90,0],[100,255,100])
    greenBlobs = findCircle(bw_img_green)

    # Filter for red blobs
    bw_img_red = filterImage(image, [0,0,170], [95,130,255])
    redBlobs = findCircle(bw_img_red)

    # Add all filtered images for total black/white image
    imagearray = bw_img_blue + bw_img_green + bw_img_red

    # Check wether green or red circle was found
    try:
        greenLen = len(greenBlobs)
        redLen = len(redBlobs)
    except:
        print("No green circles found")
        return 0, None, None, None

    # print("Amount of blue blobs:", len(blueBlobs), blueBlobs)
    # print("Amount of green blobs:", len(greenBlobs), greenBlobs)
    # print("Amount of red blobs:", len(redBlobs), redBlobs)

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

    blobsList = np.asarray(in_bounds_blobs)
    blobsFound = len(blobsList)

    found_img = drawCircles(blobsList)
        
    return blobsFound, blobsList[:, :2], imagearray, found_img

def drawCircles(circle_data):
    if circle_data != []:
        # img = np.zeros((320,400,3), np.uint8)
        img = np.zeros((240,320,3), np.uint8)
        for i in circle_data:
            if i != []:
                cv2.circle(img,(i[0],i[1]),i[2],(255,255,255),-1)
        # return cv.fromarray(img)
        return img
    else:
        print "NO CIRCLES"

def main():
    image = cv2.imread("test_image.jpg")

    amount_of_blobs, coords, imagearray, found_img = getBlobsData(image)
    # cv2.imshow("image", image)
    # cv2.imshow("imagearray", imagearray)
    # cv2.imshow("foundimg", found_img)
    # key = cv2.waitKey(4000)



if __name__ == "__main__":
    main()