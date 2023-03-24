import cv2

vid = cv2.VideoCapture(0)
  
while(True):
    ret, frame = vid.read()
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_filtered = cv2.bilateralFilter(gray, 10, 40, 40)
    edges_filtered = cv2.Canny(gray_filtered, 30, 60)
    cv2.imshow('frame', edges_filtered)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
vid.release()
cv2.destroyAllWindows()