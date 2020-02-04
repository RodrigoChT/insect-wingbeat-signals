import numpy as np
import cv2

cap = cv2.VideoCapture(-1)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('recordings/videos/test2.avi',fourcc, 30.0, (640,480))

while(cap.isOpened()):
    ret, frame = cap.read()
    out.write(frame)
    cv2.imshow('frame',frame)
    
    if cv2.waitKey(1) & 0xFF == ord('x'):
        break

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()