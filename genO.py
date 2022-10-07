import cairo, PIL, argparse, math, random
from PIL import Image, ImageDraw

#list of color 
list_of_colors = [(145, 185, 141), (229, 192, 121), (210, 191, 88), (140, 190, 178), (255, 183, 10), (189, 190, 220),
 (221, 79, 91), (16, 182, 98), (227, 146, 80), (241, 133, 123), (110, 197, 233), (235, 205, 188), (197, 239, 247), (190, 144, 212),
 (41, 241, 195), (101, 198, 187), (255, 246, 143), (243, 156, 18), (189, 195, 199), (243, 241, 239)]

float_gen = lambda a, b: random.uniform(a, b)

#draw the orbit of the planets
def draw_orbit(cr, line, x, y, radius, r, g, b):
    cr.set_line_width(line)
    cr.arc(x, y, radius, 0, 2*math.pi)
    cr.stroke()

# Function to draw a planet included the sun
def draw_circle_fill(cr, x, y, radius, r, g, b):
    cr.set_source_rgb(r, g, b)
    cr.arc(x, y, radius, 0, 2*math.pi)
    cr.fill()

def draw_cool_planet(cr, x, y, radius):
    pattern = cairo.LinearGradient(x, x-radius, y, y+radius)
    pattern.add_color_stop_rgb(0, 1, 0.5, 0.5)
    pattern.add_color_stop_rgb(1, 0.5, 0.5, 1)
    cr.set_source(pattern)
    

    cr.arc(x, y, radius, 0, math.pi*2)
    cr.fill()
    
    

def draw_satellite_orbit(cr, x, y, radius, r, g, b):
    cr.set_source_rgb(r, g, b)
    cr.arc(x, y, radius, 0, 2*math.pi)
    cr.set_dash([14.0, 20.0])
    cr.stroke()

#draw the border of the image
def draw_border(cr, size, r, g, b, width, height):
    cr.set_source_rgb(r, g, b)
    cr.rectangle(0, 0, size, height)
    cr.rectangle(0, 0, width, size)
    cr.rectangle(0, height-size, width, size)
    cr.rectangle(width-size, 0, size, height)
    cr.fill()

# draws the background
def draw_background(cr, r, g, b, width, height):
    cr.set_source_rgb(r, g, b)
    cr.rectangle(0, 0, width, height)
    cr.fill()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--width", help="Specify Width", default=3000, type=int)
    parser.add_argument("--height", help="Specify Height", default=2000, type=int)
    parser.add_argument("-o", "--orbit", help="Actual Orbits", default="true", action="store_true")
    parser.add_argument("-s", "--sunsize", help=".", default=random.randint(200, 400), type=int)
    parser.add_argument("-bs", "--bordersize", help=".", default=50, type=int)
    parser.add_argument("-n", "--noise", help="Texture", default=.4, type=float)
    args = parser.parse_args()

# Gets the width, height , bordersize and sun size from the users and set them in variables
    width, height = args.width, args.height
    border_size = args.bordersize
    sun_size = args.sunsize

#sun center is in the middle of the rectangle but above the bordersize
    sun_center_y = height - border_size

    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    cr = cairo.Context(ims)

# Draws background rectangle
    #draw_background(cr, .3, .3, .3, width, height)
    draw_background(cr, 23/255, 44/255, 56/255, width, height)

# Random color from the list for the sun
    sun_color = random.choice(list_of_colors)
    sun_r, sun_g, sun_b = sun_color[0]/255.0, sun_color[1]/255.0, sun_color[2]/255.0

# Draws the sun in the center of the rectangle
    draw_circle_fill(cr, width/2, sun_center_y, sun_size, sun_r, sun_g, sun_b)

    distance_between_planets = 20
    last_center = sun_center_y
    last_size = sun_size
    last_color = sun_color

    min_size = 6
    max_size = 70

    for x in range(1, 20):
        next_size = random.randint(min_size, max_size)
        next_center = last_center - last_size - (next_size * 2) - distance_between_planets

# If the next planet does not overlaps with the border then procedes
        if not(next_center - next_size < border_size):
            if(args.orbit):
                draw_orbit(cr, 4, width/2, sun_center_y, height - next_center - border_size, .6, .6, .6)
            elif(args.line):
                cr.move_to(border_size * 2, next_center)
                cr.line_to(width-(border_size*2), next_center)
                cr.stroke()

# Hides the orbit lines so they don't touch the planets (we put a hidden planet behind of the size of 1.3 bigger)
# Draw the orbit of the satellite 
            if (x == 8):
                a = math.pi / 6
                # space for the orbit of the planet
                #draw_circle_fill(cr, width/2, next_center, next_size*1.5, .3, .3, .3)
                draw_circle_fill(cr, width/2, next_center, next_size*1.5, 23/255, 44/255, 56/255)
                # Draws the satellite
                draw_satellite_orbit(cr, width/2, next_center, next_size*1.3, .3, .6, .6)
                cr.set_dash([1, 1])
                # draw the little satellite
                draw_circle_fill(cr, width/2 + next_size*math.cos(a), next_center + next_size*1.95*math.sin(a), next_size/6, 1, 1, 1)
            else:
                # space for the orbit of the planet
                #draw_circle_fill(cr, width/2, next_center, next_size*1.3, .3, .3, .3)  
                draw_circle_fill(cr, width/2, next_center, next_size*1.3, 23/255, 44/255, 56/255)  

            rand_color = random.choice(list_of_colors)
            while (rand_color is last_color):
                rand_color = random.choice(list_of_colors)

            last_color = rand_color

            r, g, b = rand_color[0]/255.0, rand_color[1]/255.0, rand_color[2]/255.0

            if (x == 8):
                draw_cool_planet(cr, width/2, next_center, next_size)
            else:
                draw_circle_fill(cr, width/2, next_center, next_size, r, g, b)

            last_center = next_center
            last_size = next_size

            min_size += 5
            max_size += 5 * x

    draw_border(cr, border_size, sun_r, sun_g, sun_b, width, height)

    ims.write_to_png('Examples/Generative-Space-Flat-' + str(width) + 'w-' + str(height) + 'h.png')

    pil_image = Image.open('Examples/Generative-Space-Flat-' + str(width) + 'w-' + str(height) + 'h.png')
    pixels = pil_image.load()
    ''' 
    for i in range(pil_image.size[0]):
        for j in range(pil_image.size[1]):
            r, g, b = pixels[i, j]
            noise = float_gen(1.0 - args.noise, 1.0 + args.noise)
            pixels[i, j] = (int(r*noise), int(g*noise), int(b*noise))
    pil_image.save('Examples/Generative-Space-Texture-' + str(width) + 'w-' + str(height) + 'h.png')
    '''
if __name__ == "__main__":
    main()
