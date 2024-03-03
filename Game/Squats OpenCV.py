#Squats Actually works

import mediapipe as mp
import cv2
import numpy as np
import math

import win32api

screen_width = win32api.GetSystemMetrics(0)
screen_height = win32api.GetSystemMetrics(1)


mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

cap = cv2.VideoCapture(0)

count_left = 0
count_right = 0
count_squats = 0
stage_left = None
stage_right = None
stage_court = None

sprite_sheet = cv2.imread('DinoSprites - doux.png')  # Replace with the correct path to your sprite sheet
sprite_height, sprite_width, _ = sprite_sheet.shape


current_frame_index = 0

frame_width = sprite_width // 6  # Assuming 6 frames in a row
frame_height = sprite_height // 1  # Assuming 1 row

def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    rad = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(rad * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:

    while cap.isOpened():
        ret, image = cap.read()
        # Recolor Image
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        # Make Detection
        results = pose.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        try:
            landmarks = results.pose_landmarks.landmark

            # Left leg
            left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

            angle_left = calculate_angle(left_hip, left_knee, left_ankle)

            #cv2.putText(image, f"Left: {int(angle_left)}", tuple(np.multiply(left_elbow, [640, 480]).astype(int)),
                        #cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2, cv2.LINE_AA)

            # Counter for left arm
            if angle_left > 160:
                stage_left = "down"
            if angle_left < 100 and stage_left == 'down':
                stage_left = "up"
                count_left += 1
                #print(f"Left Count: {count_left}")

            # Right Leg
            right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
            right_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]


            angle_right = calculate_angle(right_hip, right_knee, right_ankle)

            #cv2.putText(image, f"Right: {int(angle_right)}", tuple(np.multiply(right_elbow, [640, 480]).astype(int)),
                        #cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2, cv2.LINE_AA)
            #cv2.putText(image, f"Left Shoulder: {left_shoulder}", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

            # Counter for right arm
            if angle_right > 160:
                stage_right = "down"
            if angle_right < 100 and stage_right == 'down':
                stage_right = "up"
                count_right += 1
                #print(f"Right Count: {count_right}")


            #Check if that shit is a Squats
            if stage_left == 'up' and stage_right == 'up':
                stage_push_up = "up"
            if stage_left == 'down' and stage_right == 'down' and stage_push_up == 'up':
                stage_push_up = "counted"
                count_squats +=1
                print(f"Squats Count: {count_squats}")
                start_x = current_frame_index * frame_width
                end_x = start_x + frame_width
                start_y = 0
                end_y = frame_height

                image[0:frame_height, 0:frame_width] = sprite_sheet[start_y:end_y, start_x:end_x]
        except Exception as e:
            pass

        
        #cv2.putText(image, f"Left Hand Count: {count_left}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)
        #cv2.putText(image, f"Right Hand Count: {count_right}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(image, f"Squats Count: {count_squats}", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)

        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(0, 165, 255), thickness=2, circle_radius=4),
                                  mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                  )
        cv2.imshow('Web Cam', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
