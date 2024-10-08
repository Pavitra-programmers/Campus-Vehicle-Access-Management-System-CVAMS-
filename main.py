import cv2
import os
from datetime import time
from Character_reading import *

thres = 0.45 # Threshold to detect object

#capturing video
cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
cap.set(10,70)

#reading name of classes
classNames= []
classFile = 'coco.names'
with open(classFile,'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

#object configuration and weight structure for dnn model
configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightsPath = 'frozen_inference_graph.pb'

#dnn model
net = cv2.dnn_DetectionModel(weightsPath,configPath)

#default chutiyapa mereko nahi pata kya hai ye
net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

def Plate():
  while True:
    #reading frames
    success,img = cap.read()

    #adding class id, confidence level and border to output
    classIds, confs, bbox = net.detect(img,confThreshold=thres)
    # print(classIds,bbox)
    
    if len(classIds) != 0:
        for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
            
            cv2.rectangle(img,box,color=(0,255,0),thickness=2) #rectangle

            cv2.putText(img,classNames[classId-1].upper(),(box[0]+10,box[1]+30),
                        cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2) #class name
            
            cv2.putText(img,str(round(confidence*100,2)),(box[0]+200,box[1]+30),
                        cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2) #confidence
            
            if (classNames[classId-1]=="car" or classNames[classId-1]=="motorcycle" or classNames[classId-1]=="bus" or classNames[classId-1]=="truck"):
                if ( (confidence*100) >= 75 ):
                    ret, frame = cap.read()
                    # Check if the frame was captured successfully
                    if ret:
                     # Create a folder if it does not exist
                        folder_path = 'database'
                        if not os.path.exists(folder_path):
                           os.makedirs(folder_path)
                           
                        saved_img = classNames[classId-1] + str(int(confidence*100)) + ".jpg"

                    # Generate a filename for the image
                        img_name = os.path.join(folder_path, saved_img)

                    # Save the image
                        cv2.imwrite(img_name, frame)
                        print(f"Image saved successfully: {img_name}")
                        extract_num(path=PATH)
                    else:
                        print("Failed to capture the image!")                                        
                else:
                    print("No vehicle detected!")
                    
    #exit from output
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    #cleaning up
    cv2.imshow("Output",img)
    cv2.waitKey(1)
    
Plate()
cap.release()
cv2.destroyAllWindows()
