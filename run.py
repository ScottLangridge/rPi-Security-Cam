import os
from PIL import Image
from time import sleep
from math import sqrt


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
    # Take a bank of reference images
    img_bank = []
    for i in range(10):
        print('Capturing reference images (%i/%i)' % (i + 1, 10))
        img_bank.append(capture())
        # sleep(LOOP_DELAY)

    # Get the mean colour values for each pix
    sum_pix = []
    for i in range(len(img_bank[0])):
        sum_pix.append([0, 0, 0])
    for pix in range(len(sum_pix)):
        for im in img_bank:
            for i in range(3):
                sum_pix[pix][i] += im[pix][i]

    mean_pix = []
    for pix in sum_pix:
        val = []
        for i in pix:
            val.append(i / 10)
        mean_pix.append(val)

    dev_pix = []
    for pix in range(len(mean_pix)):
        val = []
        for i in range(3):
            sum_devience = 0
            for im in img_bank:
                sum_devience += (im[pix][i] - mean_pix[pix][i]) ** 2
            std_devience = sqrt(sum_devience / len(img_bank))
            val.append(std_devience)
        dev_pix.append(val)
    print(dev_pix)
    input()

    return img_bank


def capture():
    os.system('fswebcam -q ' + FILENAME)
    im = Image.open(FILENAME, 'r')
    return list(im.getdata())


def detect_motion(pixels, img_bank):
    pass
    # TODO Detect if something has moved or not here


def detected():
    pass
    # TODO Code for when detected goes here


main_loop()
