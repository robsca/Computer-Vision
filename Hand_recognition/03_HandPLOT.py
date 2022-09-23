
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
import random
from PIL import Image, ImageOps
from numpy.lib.function_base import _diff_dispatcher

risoluzione = (1280//5, 720//5)
#####################################################################################
#first image
img = Image.open("/Users/robertoscalas/Desktop/VS/Hands_photoset/white.jpg")
img = img.resize(risoluzione)
img = ImageOps.grayscale(img)
pixels = list(img.getdata())
image_one = []

#second image
img_2 = Image.open("/Users/robertoscalas/Desktop/VS/Hands_photoset/0_statua.jpg")
img_2 = img_2.resize(risoluzione)
img_2 = ImageOps.grayscale(img_2)
pixels_2 = list(img_2.getdata())
image_two = []

#scaling (1.00,0.00)
for i in range(len(pixels)):
    p = pixels[i]/(255*2)
    p2 = pixels_2[i]/(255*2)
    image_one.append(p)
    image_two.append(p2)


##################################################################
#crea grid
X  = []
Y  = []
for i in range(risoluzione[1]):
    for e in range(risoluzione[0]):
        X.append(e)
        Y .append(i)


##################################################################
#crea layer blue
blue_layer =[]
for i in range((risoluzione[0] * risoluzione[1])): 
    pixel_sfondo_bianco = image_one[i]
    pixel_immagine = image_two[i]

    diff_from_pix = pixel_sfondo_bianco - pixel_immagine  

    if diff_from_pix > 0.25:
        diff_from_pix = 0.25  
    elif diff_from_pix < 0.1:
        diff_from_pix = diff_from_pix + 0.01
    blue_layer.append(diff_from_pix)



# red layer
red_layer = []
for i in range(len(blue_layer)):
    pixel_sfondo_bianco = image_one[i]
    pixel_immagine = image_two[i]
    if blue_layer[i] > 0.2:
        y =  (blue_layer[i] - 0.01)
        red_layer.append(y)
    else:
        y = blue_layer[i] + 0.01
        red_layer.append(y)

#green layer 
green_layer = []
for i in range(len(blue_layer)):
    elements = (blue_layer[i]+red_layer[i])/2
    green_layer.append(elements)

############################################################################
#show graphs
fig = plt.figure()
ax = fig.add_subplot(projection='3d')

ax.scatter(X, Y, blue_layer, s = 0.09 , c = 'blue' ,alpha = 0.4)
#ax.scatter(X, Y, green_layer,  s = 0.05 , c = 'green',alpha = 0.4)
ax.scatter(X, Y, red_layer,  s = 0.09 , c = 'red'  ,alpha = 0.4)


plt.show()
