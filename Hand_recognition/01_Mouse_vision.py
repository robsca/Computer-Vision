import pyautogui   # control mouse
import time        # 
import cv2         # camera vision
import mediapipe as mp # modulo di riconoscimento -> check
import pygame
import math

window = pygame.display.set_mode((120,120))
pygame.display.set_caption('TITLE')
window.fill((0,0,0))



def draw():
    if len(coords) >= 5:
        x = coords[-1]
        z = coords[-2]
        pygame.draw.line(window, (255,255,255),x, z,5)
        pygame.display.update()

camera = cv2.VideoCapture(0)  # apri camera al canale 0, il canale dipende a seconda del dispositivo

trova_mani = mp.solutions.hands          # utilizza il modulo Mediapipe per trovare le mani
crea_mani  = trova_mani.Hands(max_num_hands = 1 ,min_detection_confidence=0.5, min_tracking_confidence=0.8)

disegna_mani = mp.solutions.drawing_utils   # trova i punti di flessione della mano e li mostra sullo schermo

run = True
fps = 60
clock = pygame.time.Clock()

coords = []

while run:                                             # LOOP
    clock.tick(fps)

    pygame.time.delay(0)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    success, immagine_mirror = camera.read()          # trova l'immagine a specchio
    immagine = cv2.flip(immagine_mirror,1)                         # ruota l'immagine orizzontalmente
    imgRGB = cv2.cvtColor(immagine, cv2.COLOR_BGR2RGB)       # cambia i valori del colore -> perchè?
    results = crea_mani.process(imgRGB)                     # trova la mano con il modulo di computer vision

    #print(results.multi_hand_landmarks)
    
    if results.multi_hand_landmarks:                   # se la mano viene individuata

        for handLms in results.multi_hand_landmarks:   # per ogni mano che viene individuata
            disegna_mani.draw_landmarks(immagine, handLms, trova_mani.HAND_CONNECTIONS) # unisci i punti di flessione all'interno della mano

            for id, lm in enumerate(handLms.landmark): # per ogni punto di flessioni in quante mani trovi 
                print(immagine)
                h, w, x  = immagine.shape
                h, w, x  = (h*2.8), (w*1), x                  # trova larghezza e altezza dello schermo
                cx, cy = int(lm.x*(w*1)), int(lm.y*(h*2.8))      # coordinata x è uguale al valore assoluto tra 0 e 1 moltiplicato per la risoluzione

                
                if id == 8:                            # id 8 = trova la punta dell'indice -> conta le falangi
                    indice_x, indice_y = int(lm.x*w), int(lm.y*h)      # coordinata x è uguale al valore assoluto tra 0 e 1 moltiplicato per la risoluzione
                    indice = cv2.circle(immagine, (indice_x, indice_y), 10, (255, 0, 255), cv2.FILLED) # disegna un cerchio nel punto alle coordinate cx e cy

                elif id == 12:
                    medio_x, medio_y = int(lm.x*w), int(lm.y*h)      # coordinata x è uguale al valore assoluto tra 0 e 1 moltiplicato per la risoluzione
                    medio = cv2.circle(immagine, (medio_x, medio_y), 10, (255, 255,0), cv2.FILLED) # disegna un cerchio nel punto alle coordinate cx e cy

                #una volta che ha tutti i punti che ti servono -> calcola tutte le distanze che ti servono
                elif id == 16:
                    anulare_x, anulare_y = int(lm.x*w), int(lm.y*h)      
                    anulare = cv2.circle(immagine, (anulare_x, anulare_y), 10, (0, 255,0), cv2.FILLED) 
                    
                    distanza_Anul_Index = math.sqrt((anulare_x - indice_x)**2 + (anulare_y - indice_y)**2)
                    print('Distanza Indice Anulare:')
                    print(distanza_Anul_Index)

                    print('Distanza Indice Medio:')
                    distanza_due_dita = math.sqrt((medio_x - indice_x)**2 + (medio_y- indice_y)**2)
                    print(distanza_due_dita)

                    #activation distance
                    if distanza_Anul_Index <= 78 or distanza_due_dita <= 150:
                        action = True
                        # posizione del mouse -> in mezzo tra le dita
                        coord = []
                        X = indice_x + abs(medio_x)
                        Y = indice_y + abs(medio_y)

                        coord.append([X,Y])

                        if len(coord) > 100:
                            coord.pop(0)    
                        indice_vel = 0
                        distanze = []
                        if len(coord)==100:
                            for e in range(len(coord)):
                                if e%len(coord)!=1:
                                    x , y = coord[e][0], coord[e][1]
                                    x1, y1 = coord[e+1][0], coord[e+1][1]
                                    #calculate distances
                                    distance = math.sqrt((x-x1)**2+(y-y1)**2)
                                    distanze.append(distance)
                                    num_distances = len(distanze)
                                    indice_vel = math.sqrt((sum(distanze)/num_distances)/100)          
                        

                        x = (indice_x + abs(medio_x)/2) + (indice_vel*2)
                        y = (indice_y + abs(medio_y)/2 )+ (indice_vel*2)



                        pyautogui.moveTo(x,y)

                        # action distance
                        if action:
                            if distanza_Anul_Index <= 45:
                                double = True
                            else:
                                double = False
                                

                            
                            if distanza_due_dita <30:
                                click = True
                            else:
                                click = False

                            if double and click:
                                start_pos = pyautogui.position()
                                print('Double')
                                pyautogui.doubleClick()
                                '''
                                import speech_recognition as sr

                                # obtain audio from the microphone
                                r = sr.Recognizer()

                                def analizza_frase(frase):
                                    frase = frase.split()
                                    print(frase)
                                #inizia discussione

                                with sr.Microphone() as source:
                                    r.adjust_for_ambient_noise(source)  # listen for 1 second to calibrate the energy threshold for ambient noise levels
                                    print("Say something!")

                                    counter= 0
                                    run = True
                                    while run == True:
                                        audio = r.listen(source)
                                        counter +=1 

                                        # recognize speech using Google Speech Recognition
                                        try:
                                            print("TIME: ",counter)
                                            # for testing purposes, we're just using the default API key
                                            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
                                            # instead of `r.recognize_google(audio)`
                                            frase = r.recognize_google(audio, language='it-IT').lower()
                                            print("G: " + frase)
                                            analizza_frase(frase)


                                        except sr.UnknownValueError:
                                            print("Non ti sento o non capisco.")
                                        except sr.RequestError as e:
                                            print("TIME: ",counter,"Could not request results from Google Speech Recognition service; {0}".format(e))

                                # funzione di analisi


                                '''
                                counter =+1
                                start_pos = pyautogui.position()
                                draw()

                                pyautogui.doubleClick()
                                pyautogui.mouseDown(start_pos[0],start_pos[1],button = 'left')
                                
                                if counter >=3:
                                    print('DRAG')

                            if click and not double:
                                
                                pyautogui.mouseUp()
                                print('click')
                                pyautogui.click()
                    else:
                        #mouvi il mouse
                        pyautogui.moveTo(indice_x,indice_y)
                            


                        
                    
    #show time on the screen
    cv2.imshow('Image', immagine) #show image on the screen
    cv2.waitKey(1)           #image every millisecond

