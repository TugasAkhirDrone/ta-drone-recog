from ultralytics import YOLO
import cv2
import math
from flask_mysqldb import MySQL
import os
from db_config import app,mysql
import datetime


def video_detection(path_x):
    model = YOLO('best_8s.pt')

    # Open the video file
    
    cap = cv2.VideoCapture(path_x)
    unique_id=set()
    classnames = ['Bird', 'Cat', 'Cow', 'Deer', 'Dog', 'Elephant', 'Giraffle', 'Pig', 'Sheep']
    count = [0,0,0,0,0,0,0,0,0]
    while cap.isOpened():
        # Read a frame from the video
        success, frame = cap.read()
        
        
        if success:
            # Run YOLOv8 inference on the frame
            results = model.track(frame,conf=0.25,iou=0.5,device=0,classes=[2,3,8],tracker="botsort.yaml",persist=True) 
            img = results[0].plot()
            height, width, _ = img.shape
            # print(results)
            if  results[0].boxes.id !=  None:
                boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)
                classes = results[0].boxes.cls.cpu().numpy().astype(int)
             
                # x1,y1,x2,y2=results[0].boxes.xyxy[0]
                # x1,y1,x2,y2=int(x1), int(y1), int(x2), int(y2)
                # print(x1,y1,x2,y2)
                # cv2.rectangle(img, (x1,y1), (x2,y2), (255,0,255),3)

                ids = results[0].boxes.id.cpu().numpy().astype(int)
                for box, id,cls in zip(boxes, ids,classes):
                    # Check if the id is unique
                    int_id =int(id)
                    if  int_id  not  in  unique_id:
                        count[cls] = count[cls] + 1
                        unique_id.add(int_id)               
                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        break
                cv2.putText(img, f'Number of Cows: {count[2]}', (width - 500, 70), 0, 1, [225, 255, 255], thickness=2, lineType=cv2.LINE_AA)
                cv2.putText(img, f'Number of Deer: {count[3]}', (width - 500, 105), 0, 1, [225, 255, 255], thickness=2, lineType=cv2.LINE_AA)
                cv2.putText(img, f'Number of Sheep: {count[8]}', (width - 500, 140), 0, 1, [225, 255, 255], thickness=2, lineType=cv2.LINE_AA)
                cv2.line(img, (width - 500,25), (width,25), [85,45,255], 40)
                cv2.putText(img, f'Number of Animals: {len(unique_id)}', (width - 500, 35), 0, 1, [225, 255, 255], thickness=2, lineType=cv2.LINE_AA)
                # resized_img = ResizeWithAspectRatio(img, height=720)
                # cv2.imshow('Detected Frame', resized_img)
                print(len(unique_id))
            yield img
            cv2.destroyAllWindows()

            
                        # Break the loop if 'q' is pressed
            
        else:
            # Break the loop if the end of the video is reached
            break
        

    # Release the video capture object and close the display window
    print("work2")
    cap.release()
    current_time = datetime.datetime.now()
    with app.app_context():
        
        cur = mysql.connection.cursor()
        insert = cur.execute("INSERT INTO detection(filename,timestamp, sheep_count, cow_count, deer_count, total_count) VALUES (%s,%s,%s,%s,%s,%s)", (path_x, current_time,count[8],count[2],count[3],count[2]+count[3]+count[8]))
        mysql.connection.commit()
        if insert:
            print("work")
        cur.close()





# Load the YOLOv8 model




# def video_detection(path_x):
#     video_capture = path_x
#     #Create a Webcam Object
#     cap=cv2.VideoCapture(video_capture)
#     frame_width=int(cap.get(3))
#     frame_height=int(cap.get(4))
#     #out=cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc('M', 'J', 'P','G'), 10, (frame_width, frame_height))

#     model=YOLO("../YOLO-Weights/best.pt")
#     classNames = ["Cow","Deer","Sheep","Deer"]
#     t_cow = 0
#     t_deer = 0
#     t_sheep = 0
#     while True:
#         success, img = cap.read()
#         results=model.track(img,stream=True)
#         print(results)
#         for r in results:
#             boxes=r.boxes
#             for box in boxes:
#                 x1,y1,x2,y2=box.xyxy[0]
#                 x1,y1,x2,y2=int(x1), int(y1), int(x2), int(y2)
#                 print(x1,y1,x2,y2)
#                 cv2.rectangle(img, (x1,y1), (x2,y2), (255,0,255),3)
#                 conf=math.ceil((box.conf[0]*100))/100
#                 cls=int(box.cls[0])
#                 class_name=classNames[cls]
#                 if class_name == "Cow":
#                     t_cow += 1
#                 elif class_name == "Deer":
#                     t_deer += 1
#                 elif class_name == "Sheep":
#                     t_sheep += 1
                
#                 label=f'{class_name}{conf}'
#                 t_size = cv2.getTextSize(label, 0, fontScale=1, thickness=2)[0]
#                 print(t_size)
#                 c2 = x1 + t_size[0], y1 - t_size[1] - 3
#                 cv2.rectangle(img, (x1,y1), c2, [255,0,255], -1, cv2.LINE_AA)  # filled
#                 cv2.putText(img, label, (x1,y1-2),0, 1,[255,255,255], thickness=1,lineType=cv2.LINE_AA)
#                 cv2.putText(img,f"Total Cows = {t_cow}",(0,50),2,1,[255,0,0])
#                 cv2.putText(img,f"Total Deers = {t_deer}",(0,100),2,1,[255,0,0])
#                 cv2.putText(img,f"Total Sheeps = {t_sheep}",(0,150),2,1,[255,0,0])
#                 cv2.putText(img,f"Total Animals = {t_cow+t_deer+t_sheep}",(0,200),2,1,[255,0,0])



#         yield img
#         cv2.destroyAllWindows()
        #out.write(img)
        #cv2.imshow("image", img)
        #if cv2.waitKey(1) & 0xFF==ord('1'):
            #break
    #out.release()
