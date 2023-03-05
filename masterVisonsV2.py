import sys
import math
import cv2
import numpy as np  

#resolution of the picture / video stream
height = 300
width = 397

#finds the average position of pixels after the mask is applied, basically center of the object
def getAveragePostion(mask):
    xAvg = 0
    yAvg = 0
    count = 0
    resolution = 25
    #goes through every pixel and add all the x and y coodinates
    for y in range(0, height, resolution):
        for x in range (0, width, resolution):
            if mask[y][x] == 0:
                xAvg += x
                yAvg += y
                count += 1
    #divides the total number by the amount of pixels counted to get avg coords
    if count > 0:
        x = int(xAvg / count)
        y = int(yAvg / count)
    return (x, y)

#takes the farthest left(l), rigth(r), top(t) and bottom(b) pixels of the mask and caluculates which one is farthest from the mean 
def locateTip(lX, lY, rX, rY, tX, tY, bX, bY, mean):
    #splits the (x,y) of the mean
    mX, mY = mean
    #creates a 2d array to store the coords and the length in the format [x][y][distance from mean]    
    array = [[lX, lY, math.sqrt((mX-lX)**2 + (mY-lY)**2)], [rX, rY, math.sqrt((mX-rX)**2 + (mY-rY)**2)], [tX, tY, math.sqrt((mX-tX)**2 + (mY-tY)**2)], [bX, bY, math.sqrt((mX-bX)**2 + (mY-bY)**2)]]
    #sorts teh array by the distance from the mean
    array = sorted(array, key=lambda x: x[2])
    #returns the last one (farthest from the mean aka the tip)
    return array[3][0], array[3][1]

#locates the angle the ip is at given the coordinates of the farthest and the mean
def produceAngle(c1, c2):
    a, b = c1
    c, d = c2
    return (math.cos((b-d) / math.sqrt((a-c)**2 + (b-d)**2)))*(180/np.pi)

def main(argv): 
    #stream / picture being analyzed
    frame = cv2.imread(r'coneStream.png')
    #converts the image
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #bounds of the HSV
    lower_bound = np.array([0,90,0])
    upper_bound = np.array([50,255,255])

    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    res = cv2.bitwise_and(frame, frame, mask=mask)
    x, y, w, h = cv2.boundingRect(mask)      
    mean = getAveragePostion(mask)
    tip = locateTip(x, np.argmax(mask[:, x]), x+w-1, np.argmax(mask[:, x+w-1]), np.argmax(mask[y, :]), y, np.argmax(mask[y+h-1, :]), y+h-1, getAveragePostion(mask))
    print(produceAngle(mean, tip))

    cv2.circle(res, mean, 8, (0,0,255), -1)
    cv2.circle(res, tip, 8, (0,0,255), -1)
    cv2.line(res, mean, tip, (0,0,255), 3, cv2.LINE_AA)
    
    cv2.imshow("Angle", res)
    cv2.waitKey()
    cv2.destroyAllWindows()
    return 0

if __name__ == "__main__":
    main(sys.argv[1:])
