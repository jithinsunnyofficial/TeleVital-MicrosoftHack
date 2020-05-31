import cv2
from keras.models import load_model
from label_detect import classify_face



#face = cv2.CascadeClassifier('/media/preeth/Data/prajna_files/Drowsiness_detection/haar_cascade_files/haarcascade_frontalface_alt.xml')
vs = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_COMPLEX_SMALL
score=0
thicc=2
#faces = face.detectMultiScale(gray,minNeighbors=5,scaleFactor=1.1,minSize=(25,25))
while(True):
    ret, frame = vs.read()
    height,width = frame.shape[:2]
    label = classify_face(frame)
    if(label == 'with_mask'):
        print("No Beep")
    else:
        print("Beep")   
    cv2.putText(frame,str(label),(100,height-20), font, 1,(255,255,255),1,cv2.LINE_AA)
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
vs.release()
cv2.destroyAllWindows()