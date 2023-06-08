import cv2
import os
import pytesseract

def ReadImage(img):
    file = open("KeyWords.txt", "r")
    read = file.readlines()

    Keywords = []
    for word in read:
        Keywords.append(word[0:-1])

    Filepath = os.path.dirname(os.path.abspath(__file__))

    pytesseract.tesseract_cmd = os.path.join(Filepath, r"Tess\tesseract.exe")
    words_in_image = pytesseract.image_to_string(img)

    file.close()


    for word in Keywords:
        if word.upper() in words_in_image.upper():
            print(word)
            return True

    return False