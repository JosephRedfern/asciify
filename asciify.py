from PIL import Image

ASCII_CHARS = ['.',',',':',';','+','*','?','%','S','#','@']
ASCII_CHARS = ASCII_CHARS[::-1]

'''
method resize():
    - takes as parameters the image, and the final width
    - resizes the image into the final width while maintaining aspect ratio
'''
def resize(image, new_width=100):
    (old_width, old_height) = image.size
    aspect_ratio = old_height/old_width
    new_height = int(aspect_ratio * new_width)
    new_dim = (new_width, new_height)
    new_image = image.resize(new_dim)
    return new_image
'''
method grayscalify():
    - takes an image as a parameter
    - returns the grayscale version of image
'''
def grayscalify(image):
    return image.convert('L')

'''
method get_ansi_color():
    - returns ANSI escape code for the given color.
    - requires Truecolor support from terminal
'''
def get_ansi_color(value):
    r, g, b = value
    return '\x1b[38;2;{r};{g};{b}m'.format(r=str(r).zfill(3), g=str(g).zfill(3), b=str(b).zfill(3))

'''
method modify():
    - replaces every pixel with a character whose intensity is similar.
    - takes grayscale image and rgb image, grayscale used to choose intensity,
      rgb image used for pixel colour.
'''
def modify(image_g, image, buckets=25):
    initial_pixels_g = list(image_g.getdata())
    initial_pixels = list(image.getdata())

    new_pixels = [get_ansi_color(initial_pixels[i]) + ASCII_CHARS[pixel_value//buckets] for i, pixel_value in enumerate(initial_pixels_g)]
    return ''.join(new_pixels)

'''
method do():
    - does all the work by calling all the above functions
'''
def do(image, new_width=100):
    image = resize(image)
    image_g = grayscalify(image)

    pixels = modify(image_g, image)

    len_pixels = len(pixels)

    pixel_size = 1 + len(get_ansi_color((255,255,255)))

    # Construct the image from the character list
    new_image = [pixels[index:index+new_width*pixel_size] for index in range(0, len_pixels, new_width*pixel_size)]

    return '\n'.join(new_image)

'''
method runner():
    - takes as parameter the image path and runs the above code
    - handles exceptions as well
    - provides alternative output options
'''
def runner(path):
    image = None
    try:
        image = Image.open(path)
    except Exception:
        print("Unable to find image in",path)
        #print(e)
        return
    image = do(image)

    # To print on console
    print(image)

    # Else, to write into a file
    # Note: This text file will be created by default under
    #       the same directory as this python file,
    #       NOT in the directory from where the image is pulled.
    f = open('img.txt','w')
    f.write(image)
    f.close()

'''
method main():
    - reads input from console
    - profit
'''
if __name__ == '__main__':
    import sys
    path = sys.argv[1]
    runner(path)
