from PIL import Image


def main():
    FILENAME = 'images/cap.jpg'

    pixels = conv_to_pix(FILENAME)


def conv_to_pix(filename):
    im = Image.open(filename, 'r')
    return list(im.getdata())


main()
