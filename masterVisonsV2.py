import sys
import math
import cv2
import numpy as np  

height = 300
width = 397

def getAveragePostion(mask):
    xAvg = 0
    yAvg = 0
    count = 0
    resolution = 25
    for y in range(0, height, resolution):
        for x in range (0, width, resolution):
            if mask[y][x] == 0:
                xAvg += x
                yAvg += y
                count += 1
    if count > 0:
        x = int(xAvg / count)
        y = int(yAvg / count)
    return (x, y)

def locateTip(lX, lY, rX, rY, tX, tY, bX, bY, mean):
    mX, mY = mean
    array = [[lX, lY, math.sqrt((mX-lX)**2 + (mY-lY)**2)], [rX, rY, math.sqrt((mX-rX)**2 + (mY-rY)**2)], [tX, tY, math.sqrt((mX-tX)**2 + (mY-tY)**2)], [bX, bY, math.sqrt((mX-bX)**2 + (mY-bY)**2)]]
    array = sorted(array, key=lambda x: x[2])
    return array[3][0], array[3][1]

def produceAngle(c1, c2):
    a, b = c1
    c, d = c2
    return (math.cos((b-d) / math.sqrt((a-c)**2 + (b-d)**2)))*(180/np.pi)

def main(argv): 
    frame = cv2.imread(r'coneStream.png')
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

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
