from __future__ import print_function
import boto3
import cv2
from torchvision import models
import numpy as np
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import torch
import torchvision.transforms as T
import webcolors as wc
from scipy.spatial import KDTree
import os
import io
import json
if not os.path.isdir('/tmp/torch_home'):
    os.mkdir('/tmp/torch_home')

os.environ['TORCH_MODEL_ZOO'] = '/tmp/torch_home'
os.environ['TORCH_HOME'] = '/tmp/torch_home'

dlab = models.segmentation.deeplabv3_resnet101(pretrained=1).eval()
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
def decode_segmap(image,source, nc=21):
  
  label_colors = np.array([(0, 0, 0),  # 0=background
               # 1=aeroplane, 2=bicycle, 3=bird, 4=boat, 5=bottle
               (128, 0, 0), (0, 128, 0), (128, 128, 0), (0, 0, 128), (128, 0, 128),
               # 6=bus, 7=car, 8=cat, 9=chair, 10=cow
               (0, 128, 128), (128, 128, 128), (64, 0, 0), (192, 0, 0), (64, 128, 0),
               # 11=dining table, 12=dog, 13=horse, 14=motorbike, 15=person
               (192, 128, 0), (64, 0, 128), (192, 0, 128), (64, 128, 128), (192, 128, 128),
               # 16=potted plant, 17=sheep, 18=sofa, 19=train, 20=tv/monitor
               (0, 64, 0), (128, 64, 0), (0, 192, 0), (128, 192, 0), (0, 64, 128)])

  r = np.zeros_like(image).astype(np.uint8)
  g = np.zeros_like(image).astype(np.uint8)
  b = np.zeros_like(image).astype(np.uint8)
  
  for l in range(0, nc):
    idx = image == l
    r[idx] = label_colors[l, 0]
    g[idx] = label_colors[l, 1]
    b[idx] = label_colors[l, 2]
    
  rgb = np.stack([r, g, b], axis=2)
  foreground = cv2.imread(source)

  # Change the color of foreground image to RGB
  # and resize image to match shape of R-band in RGB output map
  foreground = cv2.cvtColor(foreground, cv2.COLOR_BGR2RGB)
  foreground = cv2.resize(foreground,(r.shape[1],r.shape[0]))

  # Create a background array to hold white pixels
  # with the same size as RGB output map
  background = 255 * np.ones_like(rgb).astype(np.uint8)

  # Convert uint8 to float
  foreground = foreground.astype(float)
  background = background.astype(float)

  # Create a binary mask of the RGB output map using the threshold value 0
  th, alpha = cv2.threshold(np.array(rgb),0,255, cv2.THRESH_BINARY)

  # Apply a slight blur to the mask to soften edges
  alpha = cv2.GaussianBlur(alpha, (7,7),0)

  # Normalize the alpha mask to keep intensity between 0 and 1
  alpha = alpha.astype(float)/255

  # Multiply the foreground with the alpha matte
  foreground = cv2.multiply(alpha, foreground)

  # Multiply the background with ( 1 - alpha )
  background = cv2.multiply(1.0 - alpha, background)

  # Add the masked foreground and background
  outImage = cv2.add(foreground, background)

  # Return a normalized output image for display
  return outImage/255

def segment(path, dev='cpu'):
  img = Image.open(path)

  # Comment the Resize and CenterCrop for better inference results
  trf = T.Compose([T.Resize(640), 
                   #T.CenterCrop(224), 
                   T.ToTensor(), 
                   T.Normalize(mean = [0.485, 0.456, 0.406], 
                               std = [0.229, 0.224, 0.225])])
  inp = trf(img).unsqueeze(0).to(dev)
  out = dlab.to(dev)(inp)['out']
  om = torch.argmax(out.squeeze(), dim=0).detach().cpu().numpy()
  rgb = decode_segmap(om,path)
  #plt.imshow(rgb); plt.axis('off'); plt.show()
  return rgb

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
    s3 = boto3.client('s3')
    

    for record in event['Records']:
        print(json.dumps(record,indent=4))
        if record['eventName'] == 'REMOVE' or record['eventName'] == 'MODIFY':
            print("Not an insert record")
            #print(json.dumps(record,indent=4))
            continue
        image_type = 'NewImage' if 'NewImage' in record['dynamodb'] else 'OldImage'
        path = record['dynamodb'][image_type]['img_path']['S']
        print('Downloading image')

        s3.download_file('senior-design-images',path, '/tmp/img.png')
        print("Segmenting background")
        foreground = segment('/tmp/img.png')
        print('saving foreground image')
        plt.axis('off')
        plt.imshow(foreground)
        plt.savefig('/tmp/img_foreground.png', bbox_inches='tight')
        print("Removing background")
        img = Image.open('/tmp/img_foreground.png')
        img = img.convert("RGBA")
        datas = img.getdata()
        newData = []
        for item in datas:
            if item[0] == 255 and item[1] == 255 and item[2] == 255:
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)
        img.putdata(newData)
        img.save('/tmp/img_foreground.png', "PNG")
        print('saving new forground')
        print('getting colors')
        colors = get_colors('/tmp/img_foreground.png',numcolors=10)
        cnames = set([convert_rgb_to_names(color) for color in colors])
        print(cnames)
        print(colors)
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        table = dynamodb.Table('Image_Info')
        response = table.put_item(
            Item={
                'img_path': path,
                'color_names': list(cnames),
                'color_rgbs':list(colors),
                'lat':record['dynamodb'][image_type]['lat']['N'],
                'lon':record['dynamodb'][image_type]['lon']['N'],
                'ts':record['dynamodb'][image_type]['timestamp']['N']
            }
        )
        '''
        table = dynamodb.Table('Input_Packets')
        table.update_item(
            Key={
                'timestamp': record['dynamodb']['Keys']['timestamp']['N'],
            },
            UpdateExpression="set colors=:c",
            ExpressionAttributeValues={
                ':c': list(cnames),
            },
            ReturnValues="UPDATED_NEW"
        )
        '''
        print("UpdateItem succeeded")


    return
