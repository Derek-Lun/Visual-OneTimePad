from PIL import Image, ImageMath
from images2gif import writeGif
import os, sys, numpy, argparse

def generate_random_array(size):
    numOfPix = size[0]*size[1]
    array = numpy.zeros(numOfPix)
    for x in range(0, numOfPix):
        array[x] = (ord(os.urandom(1)) >> 7) * 255
    return array

def generate_random_image(random_array, dimension):
    random_image = numpy.zeros(dimension[0]*dimension[1]*4)
    newDimension = (dimension[1]*2, dimension[0]*2)
    for x in range(0, random_array.size):
        random_image[(x/dimension[0])*dimension[0]*2 + x*2] = random_array[x]
        random_image[(x/dimension[0])*dimension[0]*2 + x*2 + 1] = 0 if random_array[x] == 255 else 255
        random_image[(x/dimension[0])*dimension[0]*2 + dimension[0]*2 + x*2] = 0 if random_array[x] == 255 else 255
        random_image[(x/dimension[0])*dimension[0]*2 + dimension[0]*2 + x*2 + 1] = random_array[x]
    return Image.fromarray(random_image.reshape(newDimension).astype('uint8')).convert('1')

def generate_pad_image(random_array, original):
    pad_image = numpy.zeros(original.size[0]*original.size[1]*4)
    newDimension = (original.size[1]*2, original.size[0]*2)
    originalArray = list(original.getdata())
    for x in range(0, random_array.size):
        pad_image[(x/original.size[0])*original.size[0]*2 + x*2] = 255 if random_array[x] == originalArray[x] else 0
        pad_image[(x/original.size[0])*original.size[0]*2 + x*2 + 1] = 0 if random_array[x] == originalArray[x] else 255
        pad_image[(x/original.size[0])*original.size[0]*2 + original.size[0]*2 + x*2] = 0 if random_array[x] == originalArray[x] else 255
        pad_image[(x/original.size[0])*original.size[0]*2 + original.size[0]*2 + x*2 + 1] = 255 if random_array[x] == originalArray[x] else 0
    return Image.fromarray(pad_image.reshape(newDimension).astype('uint8')).convert('1')

def generate_animated_images_old(random_image, pad_image, scale_factor):
    animated_images = []
    for x in xrange (0, random_image.size[0], scale_factor):
        temp_image = Image.new('1', random_image.size, "white")
        temp_image.paste(random_image.crop((random_image.size[0] - x, 0, random_image.size[0], random_image.size[1])), (0,0))
        animated_image = ImageMath.eval("convert((a & b), 'L')", a=temp_image, b=pad_image)
        #animated_image.save(file_name + "_" + str(x) + file_ext)
        animated_images.append(animated_image)
    for x in xrange (0, random_image.size[0] + 1, scale_factor):
        temp_image = Image.new('1', random_image.size, "white")
        temp_image.paste(random_image.crop((0, 0, random_image.size[0] - x, random_image.size[1])), (x,0))
        animated_image = ImageMath.eval("convert((a & b), 'L')", a=temp_image, b=pad_image)
        #animated_image.save(file_name + "_" + str(x+random_image.size[0]) + file_ext)
        animated_images.append(animated_image)
    return animated_images

def generate_animated_images(random_image, pad_image, scale_factor):
    animated_images = []
    for x in xrange (-scale_factor, random_image.size[0], scale_factor):
        left_image = Image.new('1', (random_image.size[0]*2, random_image.size[1]), "white")
        left_image.paste(random_image, (x, 0))
        right_image = Image.new('1', (random_image.size[0]*2, random_image.size[1]), "white")
        right_image.paste(pad_image, (random_image.size[0]-x, 0))
        animated_image = ImageMath.eval("convert((a & b), 'L')", a=left_image, b=right_image)
        #animated_image.save(str(x) + ".png")
        animated_images.append(animated_image)
    return animated_images

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-file', '-f', required=True, help='input file name')
    parser.add_argument('-o', action='store_true', default=False, help='generate an overlap image')
    parser.add_argument('-x', action='store_true', default=False, help='generate a foldable image where folding the image in the middle result in the overlapped image')
    parser.add_argument('-a', action='store_true', default=False, help='generate an animated image')
    parser.add_argument('-A', action='store_true', default=False, help='generate all of the above')
    parser.add_argument('-scale', type=int, default=1, help='scale image size up by this factor')
    parser.add_argument('-speed', type=float, default=0.05, help='length of each frame in seconds')
    args = parser.parse_args()

    scale_factor = args.scale
    file_name = os.path.splitext(args.file)[0]
    file_ext = os.path.splitext(args.file)[1]

    try:
        original = Image.open(args.file)
    except:
        print "Error when reading image file"
        return

    print "Opening file and converting to black and white"
    original = original.convert('1')
    #original_scaled = original.resize((original.size[0]*2*scale_factor, original.size[1]*2*scale_factor), Image.NEAREST)
    #original_scaled.save(file_name + "_scaled" + file_ext)

    print "Generating random array"
    random_array = generate_random_array(original.size)

    print "Generating front and back image"
    random_image = generate_random_image(random_array, original.size)
    pad_image = generate_pad_image(random_array, original)

    random_image = random_image.resize((random_image.size[0]*scale_factor, random_image.size[1]*scale_factor), Image.NEAREST)
    random_image.save(file_name + "_front" + file_ext)
    pad_image = pad_image.resize((random_image.size[0], random_image.size[1]), Image.NEAREST)
    pad_image.save(file_name + "_back" + file_ext)

    if args.A or args.o:
        print "Generating overlap image"
        overlap_image = ImageMath.eval("convert((a & b), 'L')", a=random_image, b=pad_image)
        overlap_image.save(file_name + "_merged" + file_ext)

    if args.A or args.x:
        print "Generating foldable image"
        foldable_image = Image.new('1', (random_image.size[0]*2, random_image.size[1]))
        foldable_image.paste(random_image.transpose(Image.FLIP_LEFT_RIGHT), (0,0))
        foldable_image.paste(pad_image, (random_image.size[0],0))
        foldable_image.save(file_name + "_foldable" + file_ext)

    if args.A or args.a:
        print "Generating animated gif"
        writeGif(file_name + "_animated.gif", generate_animated_images(random_image, pad_image, scale_factor), duration=args.speed)

if __name__ == "__main__":
    main()