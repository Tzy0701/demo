import cv2

for i in range(5):
    cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
    ret, frame = cap.read()
    cap.release()
    
    print(f"Camera index {i}: {'OK' if ret else 'FAIL'}")
