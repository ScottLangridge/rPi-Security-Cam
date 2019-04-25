import os
from PIL import Image
from time import sleep


FILENAME = 'images/cap.jpg'
LOOP_DELAY = 1


def main_loop():
    img_bank = setup()
    oldest = 0

    while True:
        pixels = capture()

        if detect_motion(pixels, img_bank):
            detected()

        img_bank[oldest] = pixels
        oldest = (oldest + 1) % 10
        sleep(LOOP_DELAY)


def setup():
    img_bank = []
    for i in range(10):
        img_bank.append(capture())
        sleep(LOOP_DELAY)
    return img_bank


def capture():
    os.system('fswebcam -q '  + FILENAME)
    im = Image.open(FILENAME, 'r')
    return list(im.getdata())


def detect_motion(pixels, img_bank):
    pass
    #Detect if something has moved or not here


def detected():
    pass
    #TODO Code for when detected goes here

main()
