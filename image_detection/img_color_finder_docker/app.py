from __future__ import print_function
import boto3
from PIL import Image, ImageDraw
import webcolors as wc
from scipy.spatial import KDTree

css3_db = wc.CSS3_HEX_TO_NAMES
names = []
rgb_values = []

for color_hex, color_name in css3_db.items():
    names.append(color_name)
    rgb_values.append(wc.hex_to_rgb(color_hex))
kdt_db = KDTree(rgb_values)
def convert_rgb_to_names(rgb_tuple): 
    # a dictionary of all the hex and their respective names in css3
    distance, index = kdt_db.query(rgb_tuple)
    return names[index]

def get_colors(image_file, numcolors=10, resize=150):
    # Resize image to speed up processing
    img = Image.open(image_file)
    img = img.copy()
    img.thumbnail((resize, resize))

    # Reduce to palette
    paletted = img.convert('P', palette=Image.ADAPTIVE, colors=numcolors)

    # Find dominant colors
    palette = paletted.getpalette()
    color_counts = sorted(paletted.getcolors(), reverse=True)
    colors = list()
    for i in range(numcolors):
        palette_index = color_counts[i][1]
        dominant_color = palette[palette_index*3:palette_index*3+3]
        colors.append(tuple(dominant_color))

    return colors

def save_palette(colors, swatchsize=20, outfile="palette.png" ):
    num_colors = len(colors)
    palette = Image.new('RGB', (swatchsize*num_colors, swatchsize))
    draw = ImageDraw.Draw(palette)

    posx = 0
    for color in colors:
        draw.rectangle([posx, 0, posx+swatchsize, swatchsize], fill=color) 
        posx = posx + swatchsize

    del draw
    palette.save(outfile, "PNG")

def handler(event, context):
    print(event)
    print(context)
    s3 = boto3.client('s3')
    path = event['preprocessed_image_path']
    print('Downloading image')

    s3.download_file('electri_upload_images',path, '/tmp/img.png')
    
    img = Image.open('/tmp/img.png')
    img = img.convert("RGBA")
    datas = img.getdata()
    newData = []
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
    img.putdata(newData)
    img.save('/tmp/img.png', "PNG")
    print('saving new forground')
    print('getting colors')
    colors = get_colors('/tmp/img_foreground.png',numcolors=10)
    cnames = set([convert_rgb_to_names(color) for color in colors])
    print(cnames)
    print(colors)
    ret = {}
    ret['colors'] = colors
    ret['color_names'] = cnames
    return ret
