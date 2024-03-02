import cv2
import mediapipe as mp
import numpy as np
import win32api

# Get the size of the primary display monitor
screen_width = win32api.GetSystemMetrics(0)
screen_height = win32api.GetSystemMetrics(1)

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, screen_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, screen_height)


#defin scroll vertical
# if vertical distance is
SCROLL = 280 # vertical
TAP = 1 #second


scroll_horizontal_limit = 10
scroll_threshold = 20

def distance(x1,x2,y1,y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

def scroll(current_x, current_y,  prev_y, prev_x, scroll_value, scroll_horizontal):
    # measure how much your finger moved
    value = 0
    if (prev_y is not None):
        change_in_y = current_y - prev_y
        scroll_value += change_in_y

        # check the x axis as well
        change_in_x = current_x - prev_x
        scroll_horizontal += change_in_x


        #
        if abs(scroll_horizontal) > scroll_horizontal_limit:
            scroll_value = 0
            scroll_horizontal = 0
        if abs(scroll_value) > scroll_threshold:
            if scroll_value > 0:
                value = -1
                print("Scroll down")
            else:
                value = 1
                print("scroll up")
            scroll_value = 0
            scroll_horizontal = 0

    return scroll_value,scroll_horizontal, value
def cal_pinch_ratio(indexX, indexY, thumbX, thumbY, wristX,wristY):
 #   thumb_index_distance = ((thumb_tip.x - index_tip.x) ** 2 + (thumb_tip.y - index_tip.y) ** 2) ** 0.5
    thumb_index_distance = ((thumbX - indexX) ** 2 + (thumbY - indexY) ** 2) ** 0.5
    # Calculate the distance between index finger tip and wrist
    index_middle_distance = ((indexX - wristX) ** 2 + (indexY - wristY) ** 2) ** 0.5

    # Calculate the pinch ratio
    pinch_ratio = thumb_index_distance / index_middle_distance

    return pinch_ratio

def cal_roi_y(value: int, roi_y: int):
    if (value != 0):
        roi_y += 50 * value * (-1)
        print(roi_y)
        if (roi_y > 750):
            print("reached")
            roi_y = 750
        if roi_y < -50:
            roi_y = -50
            print("reached")
    return roi_y



def tap(frame_count, roi_x, roi_y, roi_width, roi_height, index_tip,middle_tip, wrist_tip):
    # index_tip = [
    #     round(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * screen_width),
    #     round(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y* screen_height)]
    # middle_tip = [
    #     round(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x * screen_width),
    #     round(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y * screen_height)]
    # wrist_tip = [round(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x * screen_width),
    #              round(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y * screen_height)]

    index_middle_distance = distance(index_tip[0], middle_tip[0], index_tip[1], middle_tip[1])

    middle_to_wrist = distance(index_tip[0], wrist_tip[0], index_tip[1], wrist_tip[1])
    #print(index_tip[0], index_tip[1])
    ratio = 0
    if middle_to_wrist != 0:
        ratio = index_middle_distance / middle_to_wrist


    print(ratio)
    #circle mesurements

    between_x = (roi_x < index_tip[0]) and (index_tip[0] < (roi_x+roi_width))
    between_y = (roi_y < index_tip[1]) and (index_tip[1] < (roi_y+ roi_height))
    if between_x and between_y and (ratio < .15):
        print(True)
    # if finger tip is between the x roi_y, roi_height,   and y roi_x, roi_width
        frame_count += 1
        if frame_count >= 2:
            #considered a tap:
            frame_count = 0
            print("tapped")
    return ratio ,(index_tip[0]), (index_tip[1]), int(index_middle_distance/2)




pass


def main():
    with mp_hands.Hands(model_complexity=0,
                        min_detection_confidence=0.5,
                        min_tracking_confidence=0.5) as hands:
        # used for scrolling.
        prev_x = None
        prev_y = None
        scroll_value = 0
        scroll_horizontal = 0

        init = False

        # declare the roi_x/y, width, and height
        roi_x = 0
        roi_y = 0
        roi_width = 0
        roi_height = 0

        frame_count = 0
        while cap.isOpened():
            # capture a frame from the camera
            ret, image = cap.read()
            if(init is False):
                height, width = image.shape[:2]
                roi_x = width // 8 + width // 16
                roi_y = height // 8 + height // 16
                roi_width = width // 8
                roi_height = height // 8
                init = True
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(image)

            # draw the hands
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # draw region of interest
            # plan is to that when a finger is in that region of interest for a certian duration
            # this is identified as a tap.

            # extracted
     #       roi = image[roi_y:roi_y + roi_height, roi_x:roi_x + roi_width]
            value = 0

            # draw rectangle
            cv2.rectangle(image, (roi_x, roi_y), (roi_x + roi_width, roi_y + roi_height), (0, 255, 0), 2)

            if results.multi_hand_landmarks:

                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        image,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style()
                    )
                    # cv2.line(image, (0, roi_y), (image.shape[0],roi_y), (0, 255, 0), 2)
                    # cv2.line(image, (roi_width + roi_x, 0), (roi_width + roi_x, image.shape[0]), (0, 0, 0), 2)

                    index_tip = [
                        round(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * screen_width),
                        round(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * screen_height)]
                    middle_tip = [
                        round(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x * screen_width),
                        round(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y * screen_height)]
                    wrist_tip = [round(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x * screen_width),
                                 round(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y * screen_height)]
                    thumb_tip = [round(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x * screen_width),
                                 round(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y * screen_height)]
                    # pinch start
                    ratio = cal_pinch_ratio(index_tip[0], index_tip[1], thumb_tip[0], thumb_tip[1], wrist_tip[0],
                                            wrist_tip[1])

                    if (ratio < .3):
                        scroll_value, scroll_horizontal, value = scroll(index_tip[0], index_tip[1], prev_y, prev_x,
                                                                        scroll_value, scroll_horizontal)

                    prev_x = index_tip[0]
                    prev_y = index_tip[1]
                    roi_y = cal_roi_y(value, roi_y)
                    ## pinch end



                    #tap
                    index_tip = [
                        round(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * width),
                        round(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * height)]
                    middle_tip = [
                        round(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x * width),
                        round(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y * height)]
                    wrist_tip = [round(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x * width),
                                 round(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y * height)]
                    ratio, center_x ,center_y, dist = tap(frame_count, roi_x, roi_y, roi_width, roi_height, index_tip, middle_tip, wrist_tip)


                    if(ratio <.15):
                         image = cv2.circle(image, (center_x, center_y), dist,(255, 255, 255), -1)


                    #tap end
# end crap
          #  cv2.imshow("Webcam", image)

            cv2.imshow('Web Cam', cv2.flip(image, 1))

            if cv2.waitKey(10) & 0xFF == ord('q') or \
                    cv2.getWindowProperty('Distance Detection', cv2.WND_PROP_VISIBLE):
                break
        cap.release()
        cv2.destroyAllWindows()






if __name__ == '__main__':
    main()