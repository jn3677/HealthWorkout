import cv2
import win32api
from Excercises.curls import curl_ups
from Excercises.push_ups import push_up
from Excercises.squats import sqaut

from Excercises.tap_scroll import tap_scroll
from Excercises.buttons import buttons
from game import game
from player import Fighter  # Import your Fighter class from the player module
import mediapipe as mp
import pygame

pygame.init()

screen_width = win32api.GetSystemMetrics(0)
screen_height = win32api.GetSystemMetrics(1)

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
mp_pose = mp.solutions.pose


cap = cv2.VideoCapture(0)




        # declare the roi_x/y, width, and height
roi_x = 0
roi_y = 0
roi_width = 0
roi_height = 0

frame_count = 0



def main():
    screen_width = win32api.GetSystemMetrics(0)
    screen_height = win32api.GetSystemMetrics(1)
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, screen_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, screen_height)
    with mp_hands.Hands(model_complexity=0,
                        min_detection_confidence=0.5,
                        min_tracking_confidence=0.5) as hands,\
             mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:

        # used for scrolling
        prev_x = None
        prev_y = None
        scroll_value = 0
        scroll_horizontal = 0
        scroll_horizontal_limit = 10
        scroll_threshold = 40
        swipe_value = 0
        swipe_vertical = 0
        init = False
        #curls
        count_left = 0
        count_right = 0
        stage_left = None
        stage_right = None


        count_push_up = 0

        stage_push_up = None

        # sqaut
        count_squats = 0
        stage_court = None

        roi_x = 0
        roi_y = 0
        roi_width = 0
        roi_height = 0

        frame_count = 0
        height = 0
        width = 0

        scroll_value = 0
        scroll_horizontal = 0


        old_num = 0
        num = 0

        locked = False

        func_dict = {
            0: "Curls",
            1: "Lock",
            2: "Push Ups",
            3: "GameMode",
            4: "Squats",
            5: "Quit"
        }
        button_list = []
        timer = 20

        temp = old_num
        SCREEN_WIDTH = 1000
        SCREEN_HEIGHT = 600
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        font = pygame.font.Font(None, 36)

        clock = pygame.time.Clock()

        font = pygame.font.Font(None, 36)
        victory_text = font.render("Victory!", True, (0, 0, 255))
        text_rect = victory_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        # spritesheet = pygame.image.load("lobsterkenney.png")

        victory = False

        pygame.display.set_caption("Brawler")
        damage_left = 0
        damage_right = 0
        YELLOW = (255, 255, 0)
        RED = (255, 0, 0)
        WHITE = (0, 0, 0)
        bg_image = pygame.image.load("backgroundColorGrass.png").convert_alpha()

        fighter_1 = Fighter(70, 310)
        fighter_2 = Fighter(700, 310)

        fighter_2_health = 200
        damage_left = 10
        damage_right = 10
        paused = False
        victory_text = None

        victory_start_time = None

        victory = False
        while cap.isOpened():
            ret, image = cap.read()
            image =  cv2.flip(image, 1)

            if (init is False):
                height, width = image.shape[:2]
                init = True

            #image, locked, timer = pointer(image, hands, locked, timer)



            image, roi_y, prev_y, prev_x, scroll_value, scroll_horizontal, num = tap_scroll(image, hands, prev_y, prev_x, roi_y, button_list, screen_width, screen_height, width, height, frame_count,scroll_value, scroll_horizontal, num, locked)
            image, button_list = buttons(image, width, height, roi_y, func_dict, locked,num=6)



            if(num != old_num):
                roi_y = -450
                temp = old_num
                old_num = num
                #reset everything
                count_left = 0
                count_right = 0
                stage_left = None
                stage_right = None
                stage_push_up = None
                count_push_up = 0
                stage_court = None
                count_squats = 0
                print(num)
            if(num == 5):
                break





            if(num == 0):
                # 0
                image, count_left, count_right, stage_left, stage_right = curl_ups(image, pose, count_left, count_right, stage_left, stage_right)
            elif(num == 2):
                #2
                image, count_left, count_right, count_push_up, stage_left, stage_right, stage_push_up = push_up(image, pose,count_left, count_right,count_push_up,stage_left,stage_right,stage_push_up)
            elif(num == 4):
                image, count_left, count_right, count_squats, stage_left, stage_right, stage_court = sqaut(image, pose, count_left,count_right, count_squats, stage_left,stage_right, stage_court)
            elif(num == -1):
                locked = False
                print("-1")
                num = temp
            elif(num == 1):
                locked = True
                print("1")
                num = temp
            elif( num == 3):
                image, fighter_2_health, count_left, count_right , stage_left, stage_right = game(image, pose, fighter_2_health, count_left, count_right, screen, font,
                                                                        fighter_1, fighter_2,clock, damage_left, damage_right, bg_image, stage_left, stage_right)





            cv2.imshow('Hand and Body Detection', image)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()