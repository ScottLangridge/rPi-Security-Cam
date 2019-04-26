import os
from PIL import Image
from time import sleep
from math import sqrt
import statistics as stat

FILENAME = 'images/cap.jpg'
LOOP_DELAY = 2
CALIBRATION_FRAMES = 10
PIXEL_CHANGE_SENSITIVITY = 2
IMAGE_CHANGE_SENSITIVITY = 2


# Run motion detection
def main_loop():
    calibration = calibrate()
    mean = calibration[0]
    deviation = calibration[1]
    recently_changed = calibration[2]

    print('Running...')
    while True:
        pixels = capture()

        detect_result = detect(pixels, mean, deviation, recently_changed)
        recently_changed = detect_result[1]
        if detect_result[0]:
            detected()

        sleep(LOOP_DELAY)


# Take a frame of reference to compare images against
def calibrate():
    # Take a bank of reference images
    print('Calibrating')
    img_bank = []
    for i in range(CALIBRATION_FRAMES):
        print('Capturing calibration images (%i/%i)' % (i + 1, CALIBRATION_FRAMES))
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
            val.append(i / CALIBRATION_FRAMES)
        mean_pix.append(val)

    dev_pix = []
    for pix in range(len(mean_pix)):
        val = []
        for i in range(3):
            sum_deviance = 0
            for im in img_bank:
                sum_deviance += (im[pix][i] - mean_pix[pix][i]) ** 2
            std_deviance = sqrt(sum_deviance / len(img_bank))
            val.append(std_deviance)
        dev_pix.append(val)

    # Get stats for stability of images
    recently_changed = detect(capture(), mean_pix,
                              dev_pix, [0, 5000])[1]
    for i in range(4):
        recently_changed = detect(capture(), mean_pix, dev_pix,
                                  recently_changed)[1]
    print('Calibration complete')

    return mean_pix, dev_pix, recently_changed


# Captures an image
def capture():
    os.system('fswebcam -q ' + FILENAME)
    im = Image.open(FILENAME, 'r')
    return list(im.getdata())


# Detects whether or not movement has occurred and tells updates recent activity to help filter out small changes
def detect(image, mean, pix_devs, changed_recently):
    # Count changed pixels
    changed_pixels = 0
    for pix in range(len(image)):
        for i in range(3):
            if abs(image[pix][i] - mean[pix][i]) > pix_devs[pix][i] * PIXEL_CHANGE_SENSITIVITY:
                changed_pixels += 1

    # Determine if significant
    mean = sum(changed_recently) / len(changed_recently)
    deviation = abs(changed_pixels - mean)
    if deviation > stat.stdev(changed_recently) * IMAGE_CHANGE_SENSITIVITY:
        movement = True
    else:
        movement = False

    # Update changed_recently
    if len(changed_recently) >= CALIBRATION_FRAMES:
        changed_recently = changed_recently[1:]
    changed_recently.append(changed_pixels)

    # Return result
    return movement, changed_recently


# Runs if movement is detected
def detected():
    print('MOTION DETECTED')


main_loop()
