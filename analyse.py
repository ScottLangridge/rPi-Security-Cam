from PIL import Image


def main():
    with open('test.txt', 'w+') as f:
        f.write(str(conv_to_pix('images/cap.jpg')))


def conv_to_pix(filename):
    im = Image.open(filename, 'r')
    return list(im.getdata())


main()
