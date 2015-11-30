from PIL import Image, ImageMath
from images2gif import writeGif
import os, sys, numpy, argparse

def generate_images(original_image):
    front_image = Image.new("1", [dimension * 2 for dimension in original_image.size])
    back_image = Image.new("1", [dimension * 2 for dimension in original_image.size])

    for x in range(0, original_image.size[0]):
        for y in range(0, original_image.size[1]):
            if original_image.getpixel((x, y)) == 0:
                if ord(os.urandom(1)) > 127:
                    front_image.putpixel((x * 2 + 0, y * 2 + 0), 255)
                    front_image.putpixel((x * 2 + 0, y * 2 + 1), 0)
                    front_image.putpixel((x * 2 + 1, y * 2 + 0), 0)
                    front_image.putpixel((x * 2 + 1, y * 2 + 1), 255)

                    back_image.putpixel((x * 2 + 0, y * 2 + 0), 0)
                    back_image.putpixel((x * 2 + 0, y * 2 + 1), 255)
                    back_image.putpixel((x * 2 + 1, y * 2 + 0), 255)
                    back_image.putpixel((x * 2 + 1, y * 2 + 1), 0)

                else:
                    front_image.putpixel((x * 2 + 0, y * 2 + 0), 0)
                    front_image.putpixel((x * 2 + 0, y * 2 + 1), 255)
                    front_image.putpixel((x * 2 + 1, y * 2 + 0), 255)
                    front_image.putpixel((x * 2 + 1, y * 2 + 1), 0)

                    back_image.putpixel((x * 2 + 0, y * 2 + 0), 255)
                    back_image.putpixel((x * 2 + 0, y * 2 + 1), 0)
                    back_image.putpixel((x * 2 + 1, y * 2 + 0), 0)
                    back_image.putpixel((x * 2 + 1, y * 2 + 1), 255)
            else:
                if ord(os.urandom(1)) > 127:
                    front_image.putpixel((x * 2 + 0, y * 2 + 0), 255)
                    front_image.putpixel((x * 2 + 0, y * 2 + 1), 0)
                    front_image.putpixel((x * 2 + 1, y * 2 + 0), 0)
                    front_image.putpixel((x * 2 + 1, y * 2 + 1), 255)

                    back_image.putpixel((x * 2 + 0, y * 2 + 0), 255)
                    back_image.putpixel((x * 2 + 0, y * 2 + 1), 0)
                    back_image.putpixel((x * 2 + 1, y * 2 + 0), 0)
                    back_image.putpixel((x * 2 + 1, y * 2 + 1), 255)

                else:
                    front_image.putpixel((x * 2 + 0, y * 2 + 0), 0)
                    front_image.putpixel((x * 2 + 0, y * 2 + 1), 255)
                    front_image.putpixel((x * 2 + 1, y * 2 + 0), 255)
                    front_image.putpixel((x * 2 + 1, y * 2 + 1), 0)

                    back_image.putpixel((x * 2 + 0, y * 2 + 0), 0)
                    back_image.putpixel((x * 2 + 0, y * 2 + 1), 255)
                    back_image.putpixel((x * 2 + 1, y * 2 + 0), 255)
                    back_image.putpixel((x * 2 + 1, y * 2 + 1), 0)
    return front_image, back_image

def generate_animated_images_old(back_image, front_image, scale_factor):
    animated_images = []
    for x in xrange (0, back_image.size[0], scale_factor):
        temp_image = Image.new('1', back_image.size, "white")
        temp_image.paste(back_image.crop((back_image.size[0] - x, 0, back_image.size[0], back_image.size[1])), (0,0))
        animated_image = ImageMath.eval("convert((a & b), 'L')", a=temp_image, b=front_image)
        #animated_image.save(file_name + "_" + str(x) + file_ext)
        animated_images.append(animated_image)

    for x in xrange (0, back_image.size[0] + 1, scale_factor):
        temp_image = Image.new('1', back_image.size, "white")
        temp_image.paste(back_image.crop((0, 0, back_image.size[0] - x, back_image.size[1])), (x,0))
        animated_image = ImageMath.eval("convert((a & b), 'L')", a=temp_image, b=front_image)
        #animated_image.save(file_name + "_" + str(x+back_image.size[0]) + file_ext)
        animated_images.append(animated_image)
    return animated_images

def generate_animated_images(back_image, front_image, scale_factor):
    animated_images = []
    for x in xrange (-scale_factor, back_image.size[0], scale_factor):
        left_image = Image.new('1', (back_image.size[0]*2, back_image.size[1]), "white")
        left_image.paste(back_image, (x, 0))
        right_image = Image.new('1', (back_image.size[0]*2, back_image.size[1]), "white")
        right_image.paste(front_image, (back_image.size[0]-x, 0))
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
        original_image = Image.open(args.file)
    except:
        print "Error when reading image file"
        return

    print "Opening file and converting to black and white"
    original_image = original_image.convert('1')
    original_image_scaled = original_image.resize((original_image.size[0]*2*scale_factor, original_image.size[1]*2*scale_factor), Image.NEAREST)
    original_image_scaled.save(file_name + "_scaled" + file_ext)

    print "Generating front and back image"
    front_image, back_image = generate_images(original_image)

    back_image = back_image.resize((back_image.size[0]*scale_factor, back_image.size[1]*scale_factor), Image.NEAREST)
    back_image.save(file_name + "_front" + file_ext)
    front_image = front_image.resize((back_image.size[0], back_image.size[1]), Image.NEAREST)
    front_image.save(file_name + "_back" + file_ext)

    if args.A or args.o:
        print "Generating overlap image"
        overlap_image = ImageMath.eval("convert((a & b), 'L')", a=back_image, b=front_image)
        overlap_image.save(file_name + "_merged" + file_ext)

    if args.A or args.x:
        print "Generating foldable image"
        foldable_image = Image.new('1', (back_image.size[0]*2, back_image.size[1]))
        foldable_image.paste(back_image.transpose(Image.FLIP_LEFT_RIGHT), (0,0))
        foldable_image.paste(front_image, (back_image.size[0],0))
        foldable_image.save(file_name + "_foldable" + file_ext)

    if args.A or args.a:
        print "Generating animated gif"
        writeGif(file_name + "_animated.gif", generate_animated_images(back_image, front_image, scale_factor), duration=args.speed)

if __name__ == "__main__":
    main()