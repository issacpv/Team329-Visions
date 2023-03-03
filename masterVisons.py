import sys
import math
import cv2
import numpy as np  

i = 0

def nothing(x):
    pass

def arrayCreator(arr):
    print(1)
    array = [[0 for x in range(6)] for y in range(0, len(arr))]
    for a in range(0, len(arr)):
        b = arr[a][0]
        m = (b[3]-b[1])/(b[2]-b[0])
        l = int(math.sqrt((b[3]-b[1])**2 + (b[2]-b[0])**2))
        x1 = int((b[2]-b[0])/3) + b[0]
        y1 = int((x1-b[0])*m)+b[1]
        x2 = int(((b[2]-b[0])/3)+b[0]+b[0])
        y2 = int((x2-b[0])*m)+b[1]
        array.insert(a, [x1,y1,x2,y2,m,l])
    for c in range(0, len(arr)):
        array = np.delete(array, len(arr), 0)
    return array

def checkLines(arr, arrPr):
    print(arr)
    print(arrPr)
    print(2)
    arr=sorted(arr, key=lambda x: x[4])
    arrBackup = arr
    for a in range(0, len(arr) - 1):
        print(21)
        if arr[a][4] > arr[a+1][4] - 10 and arr[a][4] < arr[a+1][4] + 10:
            print(22)
            if (arr[a][5] > arr[a+1][5]):
                arrP = arrPr[a][0]
                print(230)
                if(((arr[a][0] - arrP[0])*arr[a][4])+arrP[1]>arr[a][1]-10 and ((arr[a][0] - arrP[0])*arr[a][4])+arrP[1] < arr[a][1]+10):
                    arrBackup = np.delete(arrBackup, a, 0)
                    print(240)
            else:
                arrP = arrPr[a+1][0]
                print(231)
                if(((arr[(a+1)][0] - arrP[0])*arr[(a+1)][4])+arrP[1]>arr[(a+1)][1]-10 and ((arr[(a+1)][0] - arrP[0])*arr[(a+1)][4])+arrP[1] < arr[(a+1)][1]+10):
                    arrBackup = np.delete(arrBackup, a+1, 0) 
                    print(241)                                                                     
    return arrBackup

def removeQuad(arr):
    for a in range(0, len(arr) - 1):
        if arr[a][4] > arr[a+1][4] - 10 and arr[a][4] < arr[a+1][4] + 10:
            arr = np.delete(arr, a, 0)
            arr = np.delete(arr, a+1, 0)
    return arr    

def restoreArray(arr):
    for a in range(0, len(arr) - 1):
        arr[a][4] = int(arr[a][4])
    return arr

##cv2.namedWindow("Tracking")
##cv2.createTrackbar("LH", "Tracking", 0, 255, nothing)
##cv2.createTrackbar("LS", "Tracking", 0, 255, nothing)
##cv2.createTrackbar("LV", "Tracking", 0, 255, nothing)
##cv2.createTrackbar("UH", "Tracking", 255, 255, nothing)
##cv2.createTrackbar("US", "Tracking", 255, 255, nothing)
##cv2.createTrackbar("UV", "Tracking", 255, 255, nothing)

##while(i < 500):
frame = cv2.imread(r'C:\Users\vjoji\OneDrive\Pictures\cone.png')
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

##l_h = cv2.getTrackbarPos("LH", "Tracking")
##l_s = cv2.getTrackbarPos("LS", "Tracking")
##l_v = cv2.getTrackbarPos("LV", "Tracking")
##u_h = cv2.getTrackbarPos("UH", "Tracking")
##u_s = cv2.getTrackbarPos("US", "Tracking")
##u_v = cv2.getTrackbarPos("UV", "Tracking")

lower_bound = np.array([0,90,0])
upper_bound = np.array([50,255,255])

mask = cv2.inRange(hsv, lower_bound, upper_bound)
res = cv2.bitwise_and(frame, frame, mask=mask)

##cv2.imshow('frame',frame)
##cv2.imshow('mask',mask)
cv2.imshow('res',res)

##print (i)
##i += 1  
##k = cv2.waitKey(1)
##if k == 27:
    ##break

def main(argv):
    default_file = r'C:\Users\vjoji\OneDrive\Pictures\coneMask.png'
    filename = argv[0] if len(argv) > 0 else default_file
    src = cv2.imread(cv2.samples.findFile(filename), cv2.IMREAD_GRAYSCALE)
    dst = cv2.Canny(src, 50, 200, None, 3)
    cdst = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)
    cdstP = np.copy(cdst)
    lines = cv2.HoughLines(dst, 1, np.pi / 180, 10000000, None, 0, 0)
    
    if lines is not None:
        for i in range(0, len(lines)):
            rho = lines[i][0][0]
            theta = lines[i][0][1]
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a * rho
            y0 = b * rho
            pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
            pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
            cv2.line(cdst, pt1, pt2, (0,0,255), 3, cv2.LINE_AA)
    
    linesP = cv2.HoughLinesP(dst, 1, np.pi / 180, 50, None, 50, 1000000) 
    # linesP = restoreArray(checkLines(arrayCreator(linesP), linesP))

    if linesP is not None:
        for i in range(0, len(linesP)):
            l = linesP[i][0]
            cv2.line(cdstP, (l[0], l[1]), (l[2], l[3]), (0,0,255), 3, cv2.LINE_AA)
            print('end')
        ##cv2.imshow("Source", src)
        ##cv2.imshow("Detected Lines (in red) - Standard Hough Line Transform", cdst)
        cv2.imshow("Detected Lines (in red) - Probabilistic Line Transform", cdstP)

    cv2.waitKey()
    cv2.destroyAllWindows()
    return 0
    
if __name__ == "__main__":
    main(sys.argv[1:])
