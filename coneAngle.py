import sys
import math
import cv2
import numpy as np  

i = 0

def nothing(x):
    pass

def arrayCreator(arr):
    array = [[0 for x in range(6)] for y in range(0, len(arr))]
    for a in range(0, len(arr)):
        b = arr[i][0]
        m = (b[3]-b[1])/(b[2]-b[0])
        l = math.sqrt((b[3]-b[1])**2 + (b[2]-b[0])**2)
        x1 = ((b[2]-b[0])/3) + b[0]
        y1 = ((x1-b[0])*m)+b[1]
        x2 = ((b[2]-b[0])/3)+b[0]+b[0]
        y2 = ((x2-b[0])*m)+b[1]
        array.insert(a, [x1,y1,x2,y2,m,l])
    return array

def checkLines(arr, arrP):
    arr.sort(key=lambda lst:lst[4])
    arrBackup = arr
    for a in range(0, len(arr) - 1):
        if arr[a][4] > arr[a+1][4] - 10 and arr[a][4] < arr[a+1][4] + 10:
            if (arr[a][5] > arr[a+1][5]):
                if(((arr[a][0] - arrP[a][0])*arr[a][4])+arrP[a][1]>arr[a][1]-10 and ((arr[a][0] - arrP[a][0])*arr[a][4])+arrP[a][1] < arr[a][1]+10):
                    arrBackup = np.delete(arrBackup, a, 0)
            else:
                if(((arr[a+1][0] - arrP[a+1][0])*arr[a+1][4])+arrP[a+1][1]>arr[a+1][1]-10 and ((arr[a+1][0] - arrP[a+1][0])*arr[a+1][4])+arrP[a+1][1] < arr[a+1][1]+10):
                    arrBackup = np.delete(arrBackup, a+1, 0)                                                                               
    return arrBackup

def removeQuad(arr):
    for a in range(0, len(arr) - 1):
        if arr[a][4] > arr[a+1][4] - 10 and arr[a][4] < arr[a+1][4] + 10:
            arr = np.delete(arr, a, 0)
            arr = np.delete(arr, a+1, 0)
    return arr    

def main(argv):
    default_file = r'C:\Users\vjoji\OneDrive\Pictures\coneMask.png'
    filename = argv[0] if len(argv) > 0 else default_file
    src = cv2.imread(cv2.samples.findFile(filename), cv2.IMREAD_GRAYSCALE)
    dst = cv2.Canny(src, 50, 200, None, 3)
    cdst = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)
    cdstP = np.copy(cdst)
    lines = cv2.HoughLines(dst, 1, np.pi / 180, 1000000, None, 0, 0)
    
    linesPr = cv2.HoughLinesP(dst, 1, np.pi / 180, 50, None, 50, 1000000) 
    linesP = removeQuad(checkLines(arrayCreator(linesPr), linesPr))

    if linesP is not None:
        for i in range(0, len(linesP)):
            l = linesP[i][0]
            cv2.line(cdstP, (l[0], l[1]), (l[2], l[3]), (0,0,255), 3, cv2.LINE_AA)
            print(l)
    
        ##cv2.imshow("Source", src)
        ##cv2.imshow("Detected Lines (in red) - Standard Hough Line Transform", cdst)
        cv2.imshow("Detected Lines (in red) - Probabilistic Line Transform", cdstP)

    cv2.waitKey()
    cv2.destroyAllWindows()
    return 0
    
if __name__ == "__main__":
    main(sys.argv[1:])
