import sys
import math
import cv2
import numpy as np  

#resolution of the picture / video stream
height = 240
width = 320

#finds the average position of pixels after the mask is applied, basically center of the object
def getAveragePostion(mask):
    xAvg = 0
    yAvg = 0
    count = 0
    resolution = 10
    #goes through every pixel and add all the x and y coodinates
    for y in range(0, height, resolution):
        for x in range (0, width, resolution):
            if mask[y][x] != 0:
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
    #bounds of the HSV
    lower_bound = np.array([20,160,120])
    upper_bound = np.array([40,255,255])

    cap = cv2.VideoCapture(1)   
    ret, frame = cap.read()
    print(type(ret))
    c = 0

    while ret:
        c += 1
        #stream / picture being analyzed
        ret, frame = cap.read()
        frame = cv2.resize(frame, None, fx = 0.5, fy = 0.5)

        #converts the image
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        #creates the mask (black and white) and the res (black and colored mask)
        mask = cv2.inRange(hsv, lower_bound, upper_bound)
        res = cv2.bitwise_and(frame, frame, mask=mask)

        #finds the fartest pixels
        x, y, w, h = cv2.boundingRect(mask) 
        #calculate mean
        mean = getAveragePostion(mask)

        #finds and prints the angle that the cone's tip is at
        tip = locateTip(x, np.argmax(mask[:, x]), x+w-1, np.argmax(mask[:, x+w-1]), np.argmax(mask[y, :]), y, np.argmax(mask[y+h-1, :]), y+h-1, getAveragePostion(mask))
        print(produceAngle(mean, tip))

        cv2.circle(frame, mean, 8, (0,0,255), -1)
        cv2.circle(frame, tip, 8, (0,0,255), -1)
        cv2.line(frame, mean, tip, (0,0,255), 3, cv2.LINE_AA)

        if c % 10 == 0:
            cv2.imshow("Angle", frame)
            cv2.waitKey(300)
            cv2.destroyAllWindows()
    return 0

if __name__ == "__main__":
    main(sys.argv[1:])
