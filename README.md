# Visual-OneTimePad
## Introduction
`Visual-OneTimePad` lets you generate a pair of encrypted images that doesn't require a computer to decrypt.

Input:

![input](https://raw.githubusercontent.com/Derek-Lun/Visual-OneTimePad/master/example_scaled.png)

Output (animated):

![output](https://raw.githubusercontent.com/Derek-Lun/Visual-OneTimePad/master/example_animated.gif)

## Usage
```
python onetimepad.py -f file_name
```

example: ``` python onetimepad.py -f example.png ```

for more options: ``` python onetimepad.py -h ```

example to generate the animated output above: ``` python onetimepad.py -f example.png -A -scale 2 -speed 0.1 ```

|optional arguments:| |
| :-----------: |:------------:|
|  -h, --help           |show help message|
|  -o                   |generate an overlap image|
|  -x                   |generate a foldable image where folding the image in the middle result in the overlapped image|
|  -a                   |generate an animated image|
|  -A                   |generate all of the above|
|  -scale SCALE         |scale image size up by this factor|
|  -speed SPEED         |length of each frame in seconds|
