import numpy as np
import cv2

def rotateImage(image, angle):
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
  return result


############ Reading and adjusting image #########
image = cv2.imread("CSE365_test_cases_project_1/test_sample9.jpg",0)
width = int(image.shape[1])
height = int(image.shape[0])
ratio = height/width
image = cv2.resize(image, (500,int(500*ratio))) # resizing the image
############################################################################


####### Rotate the image #####
_,thresh = cv2.threshold(image,150,255,1)
lines = cv2.HoughLinesP(thresh,1,np.pi/180,200,maxLineGap=30)
line = lines[0]
x1, y1, x2, y2 = line[0]
angle = int(np.arctan((y2-y1)/(x2-x1))*90) # getting the angle of the page
image = rotateImage(image,angle)
#############################################


#### getting an image with the marked answers and removing any noise ####
_,thresh = cv2.threshold(image,10,255,1)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
enhanced = cv2.erode(thresh,kernel)
###########################################################


################# getting the contours of the image ############
contours, _ = cv2.findContours(enhanced,mode = cv2.RETR_EXTERNAL, method = cv2.CHAIN_APPROX_SIMPLE)
boundingbox = []
result=[]
contours.reverse() # reverse the list, so the marks are from the top to the bottom
enhanced = cv2.cvtColor(enhanced,cv2.COLOR_GRAY2RGB)
################################################################

########### determine the answers ##########
f= open("results.txt","w+")
counter = 0
for i in contours:
    ######### remove the contours that are not marks #######
    if(cv2.contourArea(i)>25):
        continue

    box = cv2.boundingRect(i) #gets the bounding box of the contour
    counter+=1
    ######### gets the answer of the gender question #########
    if(counter == 1):
        if(box[0]<390):
            cv2.putText(enhanced,"M", (box[0],box[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
            f.write("Gender: Male\n")
        if(395<box[0] and box[0]<460):
            cv2.putText(enhanced, "F", (box[0],box[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
            f.write("Gender: Female\n")
        continue

    ######### gets the answer of the semester question #########
    if(counter == 2):
        if(box[0]< 200):
            cv2.putText(enhanced,"Fall", (box[0],box[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
            f.write("Semester: Fall\n")
        elif(box[0]<280):
            cv2.putText(enhanced,"Spring", (box[0],box[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
            f.write("Semester: Spring\n")
        else:
            cv2.putText(enhanced,"Summer", (box[0],box[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
            f.write("Semester: Summer\n")
        continue

    ####### gets the answer of the program question #########
    if(counter == 3):
        if(box[1]< 140):
            if(box[0]<170):
                cv2.putText(enhanced,"MCTA", (box[0],box[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
                f.write("Program: MCTA\n")
            elif(box[0]<195):
                cv2.putText(enhanced,"ENVER", (box[0],box[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
                f.write("Program: ENVER\n")
            elif(box[0]<240):
                cv2.putText(enhanced,"BLDG", (box[0],box[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
                f.write("Program: BLDG\n")
            elif(box[0]<270):
                cv2.putText(enhanced,"CESS", (box[0],box[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
                f.write("Program: CESS\n")
            elif(box[0]<310):
                cv2.putText(enhanced,"ERGY", (box[0],box[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
                f.write("Program: ERGY\n")
            elif(box[0]<355):
                cv2.putText(enhanced,"COMM", (box[0],box[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
                f.write("Program: COMM\n")
            elif(box[0]<400):
                cv2.putText(enhanced,"MANF", (box[0],box[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
                f.write("Program: MANF\n")
        elif(box[1]<152):
            if(box[0]<170):
                cv2.putText(enhanced,"LAAR", (box[0],box[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
                f.write("Program: LAAR\n")
            elif(box[0]<190):
                cv2.putText(enhanced,"MATL", (box[0],box[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
                f.write("Program: MATL\n")
            elif(box[0]<230):
                cv2.putText(enhanced,"CISE", (box[0],box[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
                f.write("Program: CISE\n")
            elif(box[0]<270):
                cv2.putText(enhanced,"HAUD", (box[0],box[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
                f.write("Program: HAUD\n")
        continue
    
    ########### gets the answers of the rest of the questions ######
    if(330 < box[0] and box[0] < 355):
        cv2.putText(enhanced, "SA", (box[0],box[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
        f.write(str(counter-3)+"- Strongly Agree\n")
    elif(360 < box[0] and box[0] < 385):
        cv2.putText(enhanced, "A", (box[0],box[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
        f.write(str(counter-3)+"- Agree\n")
    elif(390 < box[0] and box[0] < 415):
        cv2.putText(enhanced, "N", (box[0],box[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
        f.write(str(counter-3)+"- Neutral\n")
    elif(420 < box[0] and box[0] < 445):
        cv2.putText(enhanced, "D", (box[0],box[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
        f.write(str(counter-3)+"- Disagree\n")
    elif(450 < box[0] and box[0] < 475):
        cv2.putText(enhanced, "SD", (box[0],box[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
        f.write(str(counter-3)+"- Strongly Disgree\n")


cv2.imshow("enhanced",enhanced)
cv2.waitKey(0)
