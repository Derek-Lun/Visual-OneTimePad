from PIL import Image, ImageMath
from array import *
import os, sys, numpy

def randomBit():
    return (ord(os.urandom(1)) >> 7) * 255

def generateRandomArray(size):
    numOfPix = size[0]*size[1]
    array = numpy.zeros(numOfPix)
    for x in range(0, numOfPix):
        array[x] = randomBit()
    return array

def generateRandomImage(randomArray, dimension):
    randomImage = numpy.zeros(dimension[0]*dimension[1]*4)
    newDimension = (dimension[1]*2, dimension[0]*2)
    for x in range(0, randomArray.size):
        randomImage[(x/dimension[0])*dimension[0]*2 + x*2] = randomArray[x]
        randomImage[(x/dimension[0])*dimension[0]*2 + x*2 + 1] = 0 if randomArray[x] == 255 else 255
        randomImage[(x/dimension[0])*dimension[0]*2 + dimension[0]*2 + x*2] = 0 if randomArray[x] == 255 else 255
        randomImage[(x/dimension[0])*dimension[0]*2 + dimension[0]*2 + x*2 + 1] = randomArray[x]
    return Image.fromarray(randomImage.reshape(newDimension).astype('uint8'))

def generatePadImage(randomArray, original):
    padImage = numpy.zeros(original.size[0]*original.size[1]*4)
    newDimension = (original.size[1]*2, original.size[0]*2)
    originalArray = list(original.getdata())
    for x in range(0, randomArray.size):
        padImage[(x/original.size[0])*original.size[0]*2 + x*2] = 255 if randomArray[x] == originalArray[x] else 0
        padImage[(x/original.size[0])*original.size[0]*2 + x*2 + 1] = 0 if randomArray[x] == originalArray[x] else 255
        padImage[(x/original.size[0])*original.size[0]*2 + original.size[0]*2 + x*2] = 0 if randomArray[x] == originalArray[x] else 255
        padImage[(x/original.size[0])*original.size[0]*2 + original.size[0]*2 + x*2 + 1] = 255 if randomArray[x] == originalArray[x] else 0
    return Image.fromarray(padImage.reshape(newDimension).astype('uint8'))

def main():
    try:
        original = Image.open(sys.argv[1])
    except:
        print "Error when reading image file"
        return

    print "Opening file and converting to black and white"
    original = original.convert('1')

    print "Generating random array"
    randomArray = generateRandomArray(original.size)

    file_name = os.path.splitext(sys.argv[1])[0]
    file_ext = os.path.splitext(sys.argv[1])[1]

    print "Generating front image"
    randomImage = generateRandomImage(randomArray, original.size)
    randomImage.save(file_name + "_front" + file_ext)

    print "Generating back image"
    padImage = generatePadImage(randomArray, original)
    padImage.save(file_name + "_back" + file_ext)

    print "Generating merged image"
    mergedImage = ImageMath.eval("convert((a & b), 'L')", a=randomImage, b=padImage)
    mergedImage.save(file_name + "_merged" + file_ext)

if __name__ == "__main__":
    main()