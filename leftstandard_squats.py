import cv2
import mediapipe as mp
import math

mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils

pose = mp_pose.Pose()

cam = cv2.VideoCapture(0)

print('Stand UPRIGHT with the left side of your body facing the camera \n')

direction = 0 #for downward movement
count = 0
shallow = []
good = []
deep = []
depth = []
counts = []
clr = (0,0,0)

while True:
    _,frame = cam.read()
    RGB_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    results = pose.process(RGB_frame)

    h,w,c = frame.shape
    if results.pose_landmarks:
        if (results.pose_landmarks.landmark[11] and results.pose_landmarks.landmark[23] and results.pose_landmarks.landmark[25] 
            and results.pose_landmarks.landmark[29] and results.pose_landmarks.landmark[31]):

            cv2.rectangle(frame, (1150,50), (1250,150), clr, cv2.FILLED)

            left_shoulder_x , left_shoulder_y = int(results.pose_landmarks.landmark[11].x * w), int(results.pose_landmarks.landmark[11].y * h)
            left_waist_x, left_waist_y = int(results.pose_landmarks.landmark[23].x * w), int(results.pose_landmarks.landmark[23].y * h)
            left_knee_x, left_knee_y = int(results.pose_landmarks.landmark[25].x * w), int(results.pose_landmarks.landmark[25].y * h)
            left_heel_x, left_heel_y = int(results.pose_landmarks.landmark[29].x * w), int(results.pose_landmarks.landmark[29].y * h)
            left_toes_x, left_toes_y = int(results.pose_landmarks.landmark[31].x * w), int(results.pose_landmarks.landmark[31].y * h)
             
             #connect landmarks with lines
            cv2.line(frame, (left_shoulder_x , left_shoulder_y), (left_waist_x, left_waist_y), (255,0,0), 5)
            cv2.line(frame, (left_waist_x, left_waist_y), (left_knee_x, left_knee_y), (255,0,0), 5)
            cv2.line(frame, (left_knee_x, left_knee_y), (left_heel_x, left_heel_y), (255,0,0), 5)
            cv2.line(frame, (left_heel_x, left_heel_y), (left_toes_x, left_toes_y), (255,0,0), 5)
            
            #draw circles on landmarks
            cv2.circle(frame, (left_shoulder_x , left_shoulder_y), 7, (0,255,0), cv2.FILLED)
            cv2.circle(frame, (left_shoulder_x , left_shoulder_y), 10, (0,255,0), 2)
            cv2.circle(frame, (left_waist_x, left_waist_y), 7, (0,255,0), cv2.FILLED)
            cv2.circle(frame, (left_waist_x, left_waist_y), 10, (0,255,0), 2)
            cv2.circle(frame, (left_knee_x, left_knee_y), 7, (0,255,0), cv2.FILLED)
            cv2.circle(frame, (left_knee_x, left_knee_y), 10, (0,255,0), 2)
            cv2.circle(frame, (left_heel_x, left_heel_y), 7, (0,255,0), cv2.FILLED)
            cv2.circle(frame, (left_heel_x, left_heel_y), 10, (0,255,0), 2)
            cv2.circle(frame, (left_toes_x, left_toes_y), 7, (0,255,0), cv2.FILLED)
            cv2.circle(frame, (left_toes_x, left_toes_y), 10, (0,255,0), 2)

            #calculate the knee angle
            knee_angle = 180 - math.degrees(math.atan2(abs(left_waist_y - left_knee_y), abs(left_waist_x - left_knee_x))
                                            + math.atan2(abs(left_heel_y - left_knee_y), abs(left_heel_x - left_knee_x)))
            
            #check angle for shallow squat
            if knee_angle > 59 and knee_angle < 80:
                shallow.append(knee_angle)

            #check angle for a good standard squat
            if knee_angle > 79 and knee_angle < 101:
                good.append(knee_angle)

            #check angle for a deep squat
            if knee_angle > 100:
                deep.append(knee_angle)  
            
            if len(shallow) > 1 and len(good) == 0 and len(deep) == 0:
                depth.append('shallow')

            elif len(shallow) > 1 and len(good) > 1 and len(deep) == 0:
                depth.append('good')
                shallow.clear()
                good.clear()
                
            elif len(shallow) > 1 and len(good) > 1 and len(deep) > 1:
                depth.append('deep')
                shallow.clear()
                good.clear()
                deep.clear()
            
            #count the number of squats done
            if knee_angle > 46 and knee_angle < 115: 
                if direction == 0: #check for downward movement
                    count += 0.5
                    direction = 1
                counts.append(int(count))     
                    
            if knee_angle > 4 and knee_angle < 40:
                if direction == 1: #check for upward movement
                    count += 0.5
                    direction = 0
                counts.append(int(count))
            
            #check for depth of squat and display a corresponding color  
            # Yellow is for shallow, green is for good standard squat, and red color is for a deep squat. 
            if len(depth) != 0 and depth[-1] == 'shallow' :
                if counts[-1] == counts[-2]:
                    ...
                else:
                    clr = (0, 255, 255)

            elif len(depth)!= 0 and depth[-1] == 'good':
                if counts[-1] == counts[-2]:
                    ...
                else:
                    clr = (0, 255, 0)

            elif len(depth)!= 0 and depth[-1] == 'deep':
                if counts[-1] == counts[-2]:
                    ...
                else:
                    clr = (0, 0, 255)

    
    cv2.imshow('squatFrame',frame)
    
    if cv2.waitKey(1) == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
