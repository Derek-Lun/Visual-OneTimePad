from PIL import Image, ImageMath
from array import *
import os, sys, numpy

def randomBit():
    return (ord(os.urandom(1)) >> 7) * 255

def generaterandom_array(size):
    numOfPix = size[0]*size[1]
    array = numpy.zeros(numOfPix)
    for x in range(0, numOfPix):
        array[x] = randomBit()
    return array

def generaterandom_image(random_array, dimension):
    random_image = numpy.zeros(dimension[0]*dimension[1]*4)
    newDimension = (dimension[1]*2, dimension[0]*2)
    for x in range(0, random_array.size):
        random_image[(x/dimension[0])*dimension[0]*2 + x*2] = random_array[x]
        random_image[(x/dimension[0])*dimension[0]*2 + x*2 + 1] = 0 if random_array[x] == 255 else 255
        random_image[(x/dimension[0])*dimension[0]*2 + dimension[0]*2 + x*2] = 0 if random_array[x] == 255 else 255
        random_image[(x/dimension[0])*dimension[0]*2 + dimension[0]*2 + x*2 + 1] = random_array[x]
    return Image.fromarray(random_image.reshape(newDimension).astype('uint8'))

def generatepad_image(random_array, original):
    pad_image = numpy.zeros(original.size[0]*original.size[1]*4)
    newDimension = (original.size[1]*2, original.size[0]*2)
    originalArray = list(original.getdata())
    for x in range(0, random_array.size):
        pad_image[(x/original.size[0])*original.size[0]*2 + x*2] = 255 if random_array[x] == originalArray[x] else 0
        pad_image[(x/original.size[0])*original.size[0]*2 + x*2 + 1] = 0 if random_array[x] == originalArray[x] else 255
        pad_image[(x/original.size[0])*original.size[0]*2 + original.size[0]*2 + x*2] = 0 if random_array[x] == originalArray[x] else 255
        pad_image[(x/original.size[0])*original.size[0]*2 + original.size[0]*2 + x*2 + 1] = 255 if random_array[x] == originalArray[x] else 0
    return Image.fromarray(pad_image.reshape(newDimension).astype('uint8'))

def main():
    try:
        original = Image.open(sys.argv[1])
    except:
        print "Error when reading image file"
        return

    print "Opening file and converting to black and white"
    original = original.convert('1')

    print "Generating random array"
    random_array = generaterandom_array(original.size)

    file_name = os.path.splitext(sys.argv[1])[0]
    file_ext = os.path.splitext(sys.argv[1])[1]

    print "Generating front image"
    random_image = generaterandom_image(random_array, original.size)
    random_image.save(file_name + "_front" + file_ext)

    print "Generating back image"
    pad_image = generatepad_image(random_array, original)
    pad_image.save(file_name + "_back" + file_ext)

    print "Generating overlap image"
    overlap_image = ImageMath.eval("convert((a & b), 'L')", a=random_image, b=pad_image)
    overlap_image.save(file_name + "_merged" + file_ext)

    print "Generating foldable image"
    foldable_image = Image.new('1', (original.size[0]*4, original.size[1]*2))
    foldable_image.paste(random_image.transpose(Image.FLIP_LEFT_RIGHT), (0,0))
    foldable_image.paste(pad_image, (original.size[0]*2,0))
    foldable_image.save(file_name + "_foldable" + file_ext)
    
if __name__ == "__main__":
    main()