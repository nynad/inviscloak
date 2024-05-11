import cv2 
import time 
import numpy as np 

video=cv2.VideoCapture('inviscloak.mp4') 
# anything that is a class always has capital letter. functions do not.  
# once loading the video, it is brought into our primary memory from out secondary memory for faster and easier access
time.sleep(1)

bg=0
# we will store the plain background here that we will use to replace the colour of the cloak later

count=0 
# the number of frames we will get 

for i in range(60):
    # reading individual frames: what we get V
    # status: whether the reading failed or succeeded in capturing a frame. represented in boolean (true=success/false=fail)
    # frame data: 
    status, bg = video.read() 
    if status==False: 
        continue
    # will simply skips whatever triggered the if condition and continue the loop

bg=np.flip(bg,axis=1)
# specify what we are flipping and over what axis 1=x, 0=y

while video.isOpened(): 
    returnval, image = video.read()
    # now 
    if not returnval: 
        break 
    count=count+1 
    print(count)
    image=np.flip(image,axis=1) 

    hsvimg=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    lowerred=np.array([100,40,40])
    upperred=np.array([100,255,255])
    mask1=cv2.inRange(hsvimg,lowerred,upperred)

    lowerred=np.array([155,40,40])
    upperred=np.array([180,255,255])
    mask2=cv2.inRange(hsvimg,lowerred,upperred)

    mask=mask1+mask2

    # we will refine the raw image and the background image into an HSV format

    mask=cv2.morphologyEx(mask,cv2.MORPH_OPEN,np.ones((3,3),np.uint8),iterations=2)

    # applying morphology on our combines masks. first, we must be able to open the mask and convert it into binary in 8-bit

    mask=cv2.dilate(mask,np.ones((3,3),np.uint8),iterations=1)

    masktwo=cv2.bitwise_not(mask)

    resultone=cv2.bitwise_and(bg,bg,mask=mask)

    # the first mask is the property used, second mask is the variable of our two different masks.

    resulttwo=cv2.bitwise_and(image,image,mask=masktwo)

    finalimage=cv2.addWeighted(resultone,1,resulttwo,1,0)
    # here, we are adding the two "puzzle pieces" of the bg and the place becoming "invisble." the 
    # numbered paramaters can vary from 0-1. it used to transition from 1 image to another image. 
    # its a type of visual weight as to how much are you using and how much you're excluding.
    # 1 means the entre image/visual weight is being used, 0 means not enough at all.

    # now, we are displaying the output of the final image 

    cv2.imshow("Invisibility Cloak",finalimage)
    if cv2.waitKey(10)==27:
        break 













