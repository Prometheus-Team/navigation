# Using Android IP Webcam video .jpg stream (tested) in Python2 OpenCV3

import urllib
import cv2
import numpy as np
import time

# Replace the URL with your own IPwebcam shot.jpg IP:port
# URL='http://192.168.0.102:8080/video'
URL='http://192.168.0.102:8080/shot.jpg'
FPS = 10

def main():
    frames = []
    curFrame = 0
    init = time.time()
    while True:
        # init = time.time()
        # Use urllib to get the image from the IP camera
        imgResp = urllib.urlopen(URL)
        # print(time.time()-init)
        
        # Numpy to convert into a array
        imgNp = np.array(bytearray(imgResp.read()),dtype=np.uint8)

        # Finally decode the array to OpenCV usable format ;) 
        img = cv2.imdecode(imgNp,-1)
        cv2.imshow('IPWebcam',img)
        
        frames.append(img)
        curFrame += 1

        # When we have fetched 30 frames 
        if time.time()-init>1:
            init = time.time()
            # Publish the array of frames to the topic ???????????
            frames = []

        
if __name__ == '__main__':
    main()


'''
# put the image on screen
        cv2.imshow('IPWebcam',img)

        #To give the processor some less stress
        #time.sleep(0.1) 

        # Quit if q is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
'''

