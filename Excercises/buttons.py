

import cv2


def buttons(image, width, height, roi_y, func_dict, locked,num=6 ):
    button_positions = []
    start = (width // 14)
    start_y = (height // 4) + roi_y
    if locked:
        height, width = image.shape[:2]
        print("reached")
        button_x = width - ( width//8 + width // 8)
        button_y = (height // 16)
        button_positions.append((-1, button_x, button_y, button_x + (width // 4), button_y + (height // 8)))
        cv2.rectangle(image, (button_x, button_y), (button_x + (width // 4), button_y + (height // 8)), (255, 255, 255),-1)
        text_size = cv2.getTextSize("UNLOCK",cv2.FONT_HERSHEY_SIMPLEX, 1, 1)[0]
        text_x = button_x + ((width // 4) - text_size[0]) // 2  # Center the text horizontally
        text_y = button_y + ((height // 8) + text_size[1]) // 2  # Center the text vertically
        cv2.putText(image, "UNLOCK", (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)
        return image, button_positions

#    total_width = ((width // 8) +(height // 16)) * num - (height // 16)
    start = (width // 14)
    start_y = (height // 4) + roi_y
    x = 0

    for i in range(3):
        for row in range(2):
            button_x = start + i * ((width // 4) + (height // 8))
            button_y = start_y + row * ((height // 8) + (height // 8))
            button_positions.append((x,button_x, button_y, button_x + (width // 4),button_y + (height // 8) ))
            x +=1

            cv2.rectangle(image, (button_x, button_y), (button_x + (width // 4), button_y + (height // 8)), (255, 255, 255), -1)
            text = func_dict[x-1]
            font = cv2.FONT_HERSHEY_SIMPLEX
            text_size = cv2.getTextSize(text, font, 1, 1)[0]
            text_x = button_x + ((width // 4) - text_size[0]) // 2  # Center the text horizontally
            text_y = button_y + ((height // 8) + text_size[1]) // 2  # Center the text vertically
            cv2.putText(image, text, (text_x, text_y), font, 1,(0, 0, 0), 1)

    return image, button_positions

