import os
from PIL import Image
from time import sleep
from math import sqrt
import statistics as stat
import datetime


FILENAME = 'images/cap.jpg'
LOOP_DELAY = 2


def main_loop():
    calibration = calibrate()
    mean = calibration[1]
    deviation = calibration[2]
    recently_changed = calibration[3]

    print('Running...')
    while True:
        pixels = capture()

        detect_result = detect_motion(pixels, mean, deviation,
                                      recently_changed)
        recently_changed = detect_result[1]
        if detect_result[0]:
            detected()

        sleep(LOOP_DELAY)


def calibrate():
    # Take a bank of reference images
    print('Calibrating')
    img_bank = []
    for i in range(10):
        print('Capturing calibration images (%i/%i)' % (i + 1, 10))
        img_bank.append(capture())
        sleep(LOOP_DELAY)

    # Get stats for stability of pixels
    print('Processing')
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

    # Get stats for stability of images
    recently_changed = detect_motion(capture(), mean_pix, dev_pix, [0,
                                                                    2500])[1]
    for i in range(4):
        recently_changed = detect_motion(capture(), mean_pix, dev_pix,
                                         recently_changed)[1]
    print('Calibration complete')

    return img_bank, mean_pix, dev_pix, recently_changed


def capture():
    os.system('fswebcam -q ' + FILENAME)
    im = Image.open(FILENAME, 'r')
    return list(im.getdata())


def detect_motion(image, mean, pix_devs, changed_recently):
    # Count changed pixels
    changed_pixels = 0
    for pix in range(len(image)):
        for i in range(3):
            if abs(image[pix][i] - mean[pix][i]) > pix_devs[pix][i] * 2:
                changed_pixels += 1

    # Determine if significant
    mean = sum(changed_recently) / len(changed_recently)
    deviation = abs(changed_pixels - mean)
    if deviation > stat.stdev(changed_recently) * 2:
        movement = True
    else:
        movement = False

    # Update changed_recently
    if len(changed_recently) >= 10:
        changed_recently = changed_recently[1:]
    changed_recently.append(changed_pixels)

    # Return result
    return movement, changed_recently


def detected():
    now = str(datetime.datetime.now()).replace(' ', '_')
    print('DETECTED - ' + now)
    os.system('cp images/cap.jpg captures/originals/' + now + '.jpg')
    for i in range(10):
        now = str(datetime.datetime.now()).replace(' ', '_')
        os.system('fswebcam -q captures/' + now + '.jpg')


main_loop()
