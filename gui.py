import tkinter as tk
import time
import cv2
import ctypes

# Getting screen resolution
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
print(f"Screen Resolution: {screensize[0]} x {screensize[1]}")

# Setting capture resolution = screen resolution (is supported)
vid = cv2.VideoCapture(0, cv2.CAP_DSHOW)
vid.set(cv2.CAP_PROP_FRAME_WIDTH, screensize[0])
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, screensize[1])

flip = True
def flip_video():
    print("Flipping video...")
    global flip
    flip = not flip

thresh_1 = 0
def change_thresh_1_val(value):
    global thresh_1
    thresh_1 = int(value)
    
thresh_2 = 0
def change_thresh_2_val(value):
    global thresh_2
    thresh_2 = int(value)

window = tk.Tk()

button = tk.Button(
    window,
    text="Flip Video",
    padx=100,
    command=flip_video
)
button.pack()

slider = tk.Scale(from_=0, to=100, orient=tk.HORIZONTAL, command=change_thresh_1_val)
slider.set(30)
slider.pack()
slider2 = tk.Scale(from_=0, to=100, orient=tk.HORIZONTAL, command=change_thresh_2_val)
slider2.set(60)
slider2.pack()
#window.mainloop()

while 1:
    ret, frame = vid.read()
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_filtered = cv2.bilateralFilter(gray, 10, 40, 40)
    edges_filtered = cv2.Canny(gray_filtered, thresh_1, thresh_2)
    
    if flip is True:
        edges_filtered = cv2.flip(edges_filtered, 1)
    
    cv2.imshow('frame', edges_filtered)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    
    window.update_idletasks()
    window.update()
    time.sleep(0.01)
    
vid.release()
cv2.destroyAllWindows()