from __future__ import print_function
from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import imutils
import cv2 as cv
import numpy as np
import argparse
import random as rng
import time
import requests
rng.seed(12345)

def midpoint(ptA, ptB):
	return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)

##RETR_TREE
def redesign_image(val,overlay,src_gray,img_src,src,source_window,max_thresh,args,ap,img_src_jpeg,output_img):
    threshold = val
    # Detect edges using Canny
    canny_output = cv.Canny(src_gray, threshold, threshold * 2)
    canny_output = cv.dilate(canny_output, None, iterations=1)
    canny_output = cv.erode(canny_output, None, iterations=1)
    # Find contours
    cnts, hierarchy = cv.findContours(canny_output, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    # Draw contours

    pixelsPerMetric = None
    
    ##drawing = np.zeros((canny_output.shape[0], canny_output.shape[1], 3), dtype=np.uint8)
    
    ##for i in range(len(cnts)):
    ##    color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
    ##    cv.drawContours(drawing, cnts, i, color, 2, cv.LINE_8, hierarchy, 0)
    # Show in a window
    ##cv.imshow('restructured image', drawing)
    print(len(cnts))
    i=0
    index=0
    if(img_src=="shashank"):
     cv.namedWindow('shirt1',cv.WINDOW_NORMAL)
     cv.moveWindow("shirt1", 0,0)
     cv.resizeWindow('shirt1', 600,600)
     
##calculating the first area of the box index 0 
    orig = src.copy()
    box = cv.minAreaRect(cnts[0])
    box = cv.cv.BoxPoints(box) if imutils.is_cv2() else cv.boxPoints(box)
    box = np.array(box, dtype="int")

    cv.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)

    # loop over the original points and draw them
    for (x, y) in box:
     cv.circle(orig, (int(x), int(y)), 5, (0, 0, 255), -1)
    (tl, tr, br, bl) = box
    print(len(tl),len(tr),len(bl),len(br))
    (tltrX, tltrY) = midpoint(tl, tr)
    (blbrX, blbrY) = midpoint(bl, br)
        
    # compute the midpoint between the top-left and top-right points,
    # followed by the midpoint between the top-righ and bottom-right
    (tlblX, tlblY) = midpoint(tl, bl)
    (trbrX, trbrY) = midpoint(tr, br)

    # draw the midpoints on the image
    cv.circle(orig, (int(tltrX), int(tltrY)), 5, (255, 0, 0), -1)
    cv.circle(orig, (int(blbrX), int(blbrY)), 5, (255, 0, 0), -1)
    cv.circle(orig, (int(tlblX), int(tlblY)), 5, (255, 0, 0), -1)
    cv.circle(orig, (int(trbrX), int(trbrY)), 5, (255, 0, 0), -1)

    # draw lines between the midpoints
    cv.line(orig, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)),(255, 0, 255), 2)
    cv.line(orig, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)),(255, 0, 255), 2)

    # compute the Euclidean distance between the midpoints
    dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
    dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))

    # if the pixels per metric has not been initialized, then
    # compute it as the ratio of pixels to supplied metric
    # (in this case, inches)
    if pixelsPerMetric is None:
     pixelsPerMetric = dB / args["width"]

    # compute the size of the object
    dimA = dA / pixelsPerMetric
    dimB = dB / pixelsPerMetric

    maxArea=dimA*dimB

####min area cal func ends#############    
    
    while(i<(len(cnts))):
     # if the contour is not sufficiently large, ignore it
     ##if cv.contourArea(cnts[i]) < 100:
     ## continue
     # compute the rotated bounding box of the contour
     orig = src.copy()
     box = cv.minAreaRect(cnts[i])
     box = cv.cv.BoxPoints(box) if imutils.is_cv2() else cv.boxPoints(box)
     box = np.array(box, dtype="int")
     

     # order the points in the contour such that they appear
     # in top-left, top-right, bottom-right, and bottom-left
     # order, then draw the outline of the rotated bounding
     # box
     ##box = perspective.order_points(box)
     cv.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)

     # loop over the original points and draw them
     for (x, y) in box:
      cv.circle(orig, (int(x), int(y)), 5, (0, 0, 255), -1)

     (tl, tr, br, bl) = box
     (tltrX, tltrY) = midpoint(tl, tr)
     (blbrX, blbrY) = midpoint(bl, br)

     # compute the midpoint between the top-left and top-right points,
     # followed by the midpoint between the top-righ and bottom-right
     (tlblX, tlblY) = midpoint(tl, bl)
     (trbrX, trbrY) = midpoint(tr, br)

     # draw the midpoints on the image
     cv.circle(orig, (int(tltrX), int(tltrY)), 5, (255, 0, 0), -1)
     cv.circle(orig, (int(blbrX), int(blbrY)), 5, (255, 0, 0), -1)
     cv.circle(orig, (int(tlblX), int(tlblY)), 5, (255, 0, 0), -1)
     cv.circle(orig, (int(trbrX), int(trbrY)), 5, (255, 0, 0), -1)

     # draw lines between the midpoints
     cv.line(orig, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)),(255, 0, 255), 2)
     cv.line(orig, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)),(255, 0, 255), 2)

     # compute the Euclidean distance between the midpoints
     dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
     dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))

     # if the pixels per metric has not been initialized, then
     # compute it as the ratio of pixels to supplied metric
     # (in this case, inches)
     if pixelsPerMetric is None:
         pixelsPerMetric = dB / args["width"]
         print(pixelsPerMetric)
     # compute the size of the object
     dimA = dA / pixelsPerMetric
     dimB = dB / pixelsPerMetric

     newMaxArea=dimA*dimB
     if(newMaxArea>maxArea):
      maxArea=newMaxArea
      index = i
      
     
     i=i+1
     print(i)
    print("index for max area : "+str(index))


##calculating the max area of the box index 0 
    orig = src.copy()
    box = cv.minAreaRect(cnts[index])
    box = cv.cv.BoxPoints(box) if imutils.is_cv2() else cv.boxPoints(box)
    box = np.array(box, dtype="int")

    cv.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)

    # loop over the original points and draw them
    for (x, y) in box:
     cv.circle(orig, (int(x), int(y)), 5, (0, 0, 255), -1)
    (tl, tr, br, bl) = box
    
    print("tl : ("+str(int(tl[0]))+" , "+str(int(tl[1]))+") tr : ("+str(int(tr[0]))+" , "+str(int(tr[1]))+") br: ("+str(int(br[0]))+" , "+str(int(br[1]))+") bl : ("+str(int(bl[0]))+" , "+str(int(bl[1]))+")")

####################param for rectangle###############################
    a=int(tr[1])
    b=int(bl[1])
    l=int(tr[0])
    m=int(bl[0])
            
######################end of param####################################

    (tltrX, tltrY) = midpoint(tl, tr)
    (blbrX, blbrY) = midpoint(bl, br)
        
    # compute the midpoint between the top-left and top-right points,
    # followed by the midpoint between the top-righ and bottom-right
    (tlblX, tlblY) = midpoint(tl, bl)
    (trbrX, trbrY) = midpoint(tr, br)

    # draw the midpoints on the image
    cv.circle(orig, (int(tltrX), int(tltrY)), 5, (255, 0, 0), -1)
    cv.circle(orig, (int(blbrX), int(blbrY)), 5, (255, 0, 0), -1)
    cv.circle(orig, (int(tlblX), int(tlblY)), 5, (255, 0, 0), -1)
    cv.circle(orig, (int(trbrX), int(trbrY)), 5, (255, 0, 0), -1)

    # draw lines between the midpoints
    cv.line(orig, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)),(255, 0, 255), 2)
    cv.line(orig, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)),(255, 0, 255), 2)

    # compute the Euclidean distance between the midpoints
    dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
    dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))

    # if the pixels per metric has not been initialized, then
    # compute it as the ratio of pixels to supplied metric
    # (in this case, inches)
    if pixelsPerMetric is None:
     pixelsPerMetric = dB / args["width"]

    # compute the size of the object
    dimA1 = dA / pixelsPerMetric
    dimB1 = dB / pixelsPerMetric
    print(dimA1)
    print(dimB1)

    # draw the object sizes on the image
    cv.putText(orig, "{:.1f}in".format(dimA1),(int(tltrX - 15), int(tltrY - 10)), cv.FONT_HERSHEY_SIMPLEX,0.65, (255, 255, 255), 2)
    cv.putText(orig, "{:.1f}in".format(dimB1),(int(trbrX + 10), int(trbrY)), cv.FONT_HERSHEY_SIMPLEX,0.65, (255, 255, 255), 2)

    im=cv.imread(img_src_jpeg)
    im1 = cv.resize(im, (600,600), interpolation = cv.INTER_AREA)
    im2 = cv.resize(orig, (600,600), interpolation = cv.INTER_AREA)

    if(img_src=="samyak"):
     Croped = im1[41:350, 82:454]
    elif(img_src=="gaurav"): 
     Croped = im1[a:(b+145), l:m]
    else:
     Croped = im1[a:b, l:m]       
    print(Croped.shape[0])
    print(Croped.shape[1])
    blue = cv.imread(overlay)

     
    blue1 = cv.resize(blue, (Croped.shape[1],Croped.shape[0]), interpolation = cv.INTER_AREA)

    ##bg = overlay_transparent(im1, blue1, samyakCroped.shape[0], samyakCroped.shape[1])
    ##added_image = cv2.addWeighted(samyakCroped,1,blue1,1,0)
   
    if(img_src=="samyak"):
     added_image = cv.addWeighted(im1[291:600, 132:504],0.6,blue1,1,0)
     cv.imwrite("output/output11.png",added_image)
    elif(img_src=="gaurav"):
     added_image = cv.addWeighted(im1[a:(b+145), l:m],0.6,blue1,1,0)
     cv.imwrite("output/output11.png",added_image)
    else:
     added_image = cv.addWeighted(im1[a:b, l:m],0.6,blue1,1,0)
     cv.imwrite("output/output11.png",added_image)
    ##im1[291:600, 132:504]=blue1
    #cv.imwrite("output.png",im1)
    #cv.imshow("shirt1",added_image)
    if(img_src=="samyak"):
     cv.moveWindow("shirt1", l32,(600-Croped.shape[0]))
    elif(img_src=="gaurav"):
     cv.moveWindow("shirt1", l,600-Croped.shape[0])
    else:
     cv.moveWindow("shirt1", l,600-Croped.shape[0])
    #cv.imwrite("final.png",im1)
    
    cv.imwrite("output/im_rec.png",im2)
    #cv.moveWindow("im_rec", 700,100)
    

####################################################################3input#############################################333


def mains(filenamess):    
        img_src=filenamess
        img_srcs='image/'+img_src
        overlay="maroon.png"
        ######################################################################input###############################################

        #load image
        img_src_jpeg=img_srcs+".jpeg"
        output_img=img_srcs+".png"

        response = requests.post(
            'https://api.remove.bg/v1.0/removebg',
            files={'image_file': open(img_src_jpeg, 'rb')},
            data={'size': 'auto'},
            headers={'X-Api-Key': 'rmVDXez9AxduDDrbSAwPGwUu'},
        )
        if response.status_code == requests.codes.ok:
            with open(output_img, 'wb') as out:
                out.write(response.content)

        else:
            print("Error:", response.status_code, response.text)
            
        ap = argparse.ArgumentParser()
        ap.add_argument("-i", "--image", help="path to the input image", default=output_img)
        ap.add_argument("-w", "--width", type=float,help="width of the object in the image", default=0.955 )
        args = vars(ap.parse_args())
        src = cv.imread(args["image"])
        if src is None:
            print('Could not open or find the image:', args.input)
            exit(0)
            
        # Convert image to gray and blur it
        src_gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
        src_gray = cv.blur(src_gray, (3,3))
        # Create Window

        source_window = 'Try fit'
        ##cv.namedWindow(source_window)
        ##cv.imshow(source_window, src)
        max_thresh = 255
        thresh = 100 # initial threshold
        ##cv.createTrackbar('depth:', source_window, thresh, max_thresh, redesign_image)
        redesign_image(thresh,overlay,src_gray,img_src,src,source_window,max_thresh,args,ap,img_src_jpeg,output_img)
        cv.waitKey()
