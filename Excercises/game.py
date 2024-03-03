#Curl Ups
import sys
import fontTools
import pygame
import cv2
import numpy as np
import math
import win32api
from player import Fighter  # Import your Fighter class from the player module
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


def attack():
    global health
    health -= 10
    if health < 0:
        health = 0

def draw_bg(bg_image, screen):
    scaled_bg = pygame.transform.scale(bg_image, (1000, 600))
    screen.blit(scaled_bg, (0, 0))

def draw_health_bar(health, x, y, screen):
    ratio = health / 200
    pygame.draw.rect(screen, (255, 0, 0), (x, y, 400, 30))
    pygame.draw.rect(screen, (255, 255, 0), (x, y, 400 * ratio, 30))

def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    rad = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(rad * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle




# SCREEN_WIDTH = 1000
# SCREEN_HEIGHT = 600
# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
# font = pygame.font.Font(None, 36)
#
# clock = pygame.time.Clock()
#
# font = pygame.font.Font(None, 36)
# victory_text = font.render("Victory!", True, (0, 0, 255))
# text_rect = victory_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
# #spritesheet = pygame.image.load("lobsterkenney.png")
#
# victory = False
#
# pygame.display.set_caption("Brawler")
# damage_left = 0
# damage_right = 0
# YELLOW = (255, 255, 0)
# RED = (255, 0, 0)
# WHITE = (0, 0, 0)
# bg_image = pygame.image.load("backgroundColorGrass.png").convert_alpha()
#
#
# fighter_1 = Fighter(70, 310)
# fighter_2 = Fighter(700, 310)
#
# fighter_2_health = 200
# damage_left = 10
# damage_right = 10
# paused = False
# victory_text = None
#
# victory_start_time = None
#
#
# victory = False

def game(image, pose, fighter_2_health, count_left, count_right, screen, font, fighter_1, fighter_2, clock, damage_left, damage_right, bg_image, stage_left, stage_right):
    run = True
    # victory = False
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.quit()

        if fighter_2_health <= 0:
            # print("Player completed push-ups challenge. Enemy defeated!")
            message = font.render("Enemy defeated! You are getting stronger!", True, (128, 0, 128))
            screen.blit(message, (250, 100))
        pygame.display.flip()
        clock.tick(30)

        # Recolor Image
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        # Make Detection
        results = pose.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        try:
            landmarks = results.pose_landmarks.landmark
            fighter_1.update_animation()
            fighter_2.update_animation()

            draw_bg(bg_image, screen)
            # draw_health_bar(fighter_1.health, 20, 20)
            draw_health_bar(fighter_2.health, 300, 20, screen)

            # Left arm
            left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                          landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                          landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

            angle_left = calculate_angle(left_shoulder, left_elbow, left_wrist)

            cv2.putText(image, f"Left: {int(angle_left)}", tuple(np.multiply(left_elbow, [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2, cv2.LINE_AA)

            # Counter for left arm
            if angle_left > 160:
                stage_left = "down"
            if angle_left < 100 and stage_left == 'down':
                stage_left = "up"
                count_left += 1
                print(f"Left Count: {count_left}")
                # damage_left = 5
                fighter_2_health -= damage_left
                print(f"Fighter 2 Health: {fighter_2_health}")
                fighter_2.attack(damage_left)

            # Right arm
            right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                           landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                           landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

            angle_right = calculate_angle(right_shoulder, right_elbow, right_wrist)

            cv2.putText(image, f"Right: {int(angle_right)}", tuple(np.multiply(right_elbow, [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2, cv2.LINE_AA)

            # Counter for right arm
            if angle_right > 160:
                stage_right = "down"
            if angle_right < 100 and stage_right == 'down':
                stage_right = "up"
                count_right += 1
                print(f"Right Count: {count_right}")
                # damage_right = 5
                fighter_2_health -= damage_right
                print(f"Fighter 2 Health: {fighter_2_health}")
                fighter_2.attack(damage_right)





        except Exception as e:
            pass

        # draw_bg()
        # draw_health_bar(fighter_1.health, 20, 20)
        # draw_health_bar(fighter_2.health, 580, 20)

        fighter_1.draw(screen)
        fighter_2.draw(screen)

        # if victory_text:
        # screen.blit(victory_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2))

        # pygame.display.update()

        cv2.putText(image, f"Left Hand Count: {count_left}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2,
                    cv2.LINE_AA)
        cv2.putText(image, f"Right Hand Count: {count_right}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2,
                    cv2.LINE_AA)

        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(0, 165, 255), thickness=2, circle_radius=4),
                                  mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                  )

        return image, fighter_2_health, count_left, count_right, stage_left, stage_right
