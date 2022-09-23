import time, mediapipe as mp, cv2

class detector():
    def __init__(self, mode = False, maxHands = 1, detectionCon = 0.5, trackCon = 0.5):
        #proprierties
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        #tracker
        self.module = mp.solutions.hands
        self.hand = self.module.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)
        self.structure = mp.solutions.drawing_utils

    def find_hands(self,img):
        #convert image
        imgrgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        #analise image
        results = self.hand.process(imgrgb)

        if results:
            


def main():
    run = True
    #open camera
    camera = cv2.VideoCapture(0)
    #create detector
    d = detector()

    while run:
        #read image
        success, img = camera.read()
        #function of detector
        d.find_hands(img)

        cv2.imshow('Camera', img)       
        cv2.waitKey(1) 

if __name__=='__main__':
    main()