import tkinter as tk
import PIL, PIL.ImageTk
import cv2
import numpy as np
import ctypes

def padding(array, xx, yy):
    # Method to add padding to the images so that the output window doesn't resize when images are resized.
    
    dif_height = xx - array.shape[1]
    dif_width = yy - array.shape[0]
    
    array = np.pad(array, ((0, dif_width//2), (0, dif_height//2)), 'constant', constant_values=(0, 0))
    array = np.pad(array, ((dif_width//2, 0), (dif_height//2, 0)), 'constant', constant_values=(0, 0))

    return array

# Getting screen resolution
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
print(f"Screen Resolution (or the maximum resolution supported by the camera): {screensize[0]} x {screensize[1]}")

# Setting capture resolution = screen resolution (is supported)
vid = cv2.VideoCapture(0, cv2.CAP_DSHOW)
vid.set(cv2.CAP_PROP_FRAME_WIDTH, screensize[0])
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, screensize[1])


##########################################################
#Defining variables and designing the Control Panel
##########################################################
window = tk.Tk()

# Method to flip the video along y-axis
flip = True
def flip_video():
    print("Flipping video...")
    global flip
    flip = not flip

button = tk.Button(
    window,
    text="Flip Video",
    command=flip_video
).grid(row=0, column=0)





thresh_1 = 0
def change_thresh_1_val(value):
    global thresh_1
    thresh_1 = int(value)
    
tk.Label(window, text="Upper Threshold").grid(row=1, column=0)
slider = tk.Scale(from_=0, to=100, orient=tk.HORIZONTAL, command=change_thresh_1_val)
slider.set(30)
slider.grid(row=1, column=1)
    
thresh_2 = 0
def change_thresh_2_val(value):
    global thresh_2
    thresh_2 = int(value)

tk.Label(window, text="Lower Threshold").grid(row=2, column=0)
slider2 = tk.Scale(from_=0, to=100, orient=tk.HORIZONTAL, command=change_thresh_2_val)
slider2.set(60)
slider2.grid(row=2, column=1)

scale = 1
def change_scale_val(value):
    global scale
    scale = int(value)

tk.Label(window, text="Scale").grid(row=3, column=0)
slider3 = tk.Scale(from_=1, to=10, orient=tk.HORIZONTAL, command=change_scale_val)
slider3.set(10)
slider3.grid(row=3, column=1)


method_canny = True
def set_method_canny():
    global method_canny
    method_canny = True

def set_method_hed():
    global method_canny
    method_canny = False

tk.Label(window, text="Method").grid(row=5, column=0)
button2 = tk.Button(
    window,
    text="Canny",
    command=set_method_canny
).grid(row=6, column=0)

button3 = tk.Button(
    window,
    text="HED",
    command=set_method_hed
).grid(row=6, column=1)


ret, frame = vid.read()
canvas = tk.Canvas(window, width = screensize[0] // 4, height = screensize[1] // 4)
canvas.grid(row=4, column=0, columnspan=2)



##########################################################

# An empty black frame to display when the video is not being displayed
black_frame = np.zeros((screensize[1], screensize[0]), dtype=np.uint8)

# Load the HED model files from local directory
hed_model = cv2.dnn.readNetFromCaffe("deploy.prototxt", "hed_pretrained_bsds.caffemodel")

n_frames = 0

while 1:
    
    if n_frames == 0:
        cv2.imshow('frame', black_frame)
    
    else:
        ret, frame = vid.read()
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        edges_filtered = None
        if method_canny is True:
            # Extract edges using canngy Edge Detection based on the thresholds set by the user in the Control Panel
            gray_filtered = cv2.bilateralFilter(gray, 10, 40, 40)
            edges_filtered = cv2.Canny(gray_filtered, thresh_1, thresh_2)
        
        elif method_canny is False:
            # Extract edges using Hedonic Edge Detection
            blob = cv2.dnn.blobFromImage(frame, scalefactor=1.0, size=(screensize[0], screensize[1]),swapRB=False, crop=False)
            hed_model.setInput(blob)
            hed = hed_model.forward()
            hed = cv2.resize(hed[0, 0], (screensize[0], screensize[1]))
            edges_filtered = (255 * hed).astype("uint8")
            
        
        # Resizing the model frames to the scale set by the user in the Control Panel
        edges_filtered = cv2.resize(edges_filtered, (int(edges_filtered.shape[1] * (scale/10)), int(edges_filtered.shape[0] * (scale/10))))
        
        # Padding the model frames to the screen resolution
        edges_filtered = padding(edges_filtered, screensize[0], screensize[1])
        
        
        if flip is True:
            # Flipping the model frames along y-axis if user specifies that
            edges_filtered = cv2.flip(edges_filtered, 1)
    
        # Displaying the model frames in the output window as well as control panel
        cv2.imshow('frame', edges_filtered)
        
        preview = cv2.resize(edges_filtered, (screensize[0] // 4, screensize[1] // 4))
        photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(preview))
        canvas.create_image(0, 0, image = photo, anchor = tk.NW)
    
    n_frames = (n_frames + 1) % 10
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    window.update_idletasks()
    window.update()
    
vid.release()
cv2.destroyAllWindows()