import cv2
from PIL import Image, ImageOps
import numpy as np


run = True
working_memory = []

# Crea e restituisce una lista 'MEMORIA' di lunghezza('max_photograms)
# ogni 'photograms' in memoria contiene una lista di 921.600 pixels( w * h = 1280 * 720 )
# ogni pixel è rappresentato da un valore di scale di grigi ( 1.00,0.00 -> bianco, nero )   

def eye(max_photograms):
    memoria =[]
    while run:
        camera = cv2.VideoCapture(0)
        result, img = camera.read()
        img_greys = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #cv2.imshow('Title' , img_greys)
        #cv2.waitKey(1)

        #per ogni riga in immagine, per ogni pixel in ogni riga,
        # metti il valore in una lista -> pixels
        pixels = []
        sums = 0
        
        for i in range(len(img_greys)):
            # 0 -> i -> 720
            riga = img_greys[i]

            for e in range(len(riga)):
                # 0 -> i -> 1280
                pixel = riga[e]/255
                pixels.append(pixel)
                sums += pixel

                memoria.append([pixels, sums])

                if len(memoria) >= max_photograms:
                    memoria.pop(0)
        return memoria

def open_image_convert(memoria):
    #first hand
    mano = Image.open("/Users/robertoscalas/Desktop/VS/Hands/Hand_0000002.jpg")
    mano = mano.resize([1280,720])
    mano = ImageOps.grayscale(mano)
    pixels = list(mano.getdata())
    hand_1 = pixels
    #second hand
    mano = Image.open("/Users/robertoscalas/Desktop/VS/Hands/Hand_0000002.jpg")
    mano = mano.resize([1280,720])
    mano = ImageOps.grayscale(mano)
    pixels = list(mano.getdata())
    hand_2 = pixels

    run = True

    while run:
        eye = memoria[0][0]
        
        # calcola differenze                  
        differenze =[]
        for i in range(len(eye)):
            diff = hand_2[i] - hand_1[i]
            differenze.append(diff)

        print(len(differenze))
        print(sum(differenze))

open_image_convert(eye(10))

 

