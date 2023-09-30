import cv2
import tkinter as tk
from tkinter import ttk
import random
from PIL import Image, ImageTk


colors=[cv2.COLOR_BGR2YCrCb, cv2.COLOR_BGR2GRAY,cv2.COLOR_BGR2HLS,cv2.COLOR_BGR2HSV,cv2.COLOR_BGR2LAB,cv2.COLOR_BGR2XYZ]
# Create a function to update the video feed
def update_video_feed():
    # Read a frame from the camera

    ret, frame = cap.read()
    if ret:
        #if suprise is pressed than color will change
        if not show_surprise:
            frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        else:
            frame=cv2.cvtColor(frame,colors[num])

        # Convert the frame to a format that Tkinter can display
        photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
        label.config(image=photo)
        label.image = photo

    # Schedule the function to run again after 10 milliseconds
    window.after(10, update_video_feed)

# Function to toggle the "surprise" text
def toggle_surprise():
    if toggle_button['text']=="Surprise is Off":
        toggle_button['text']="Surprise is On"
    else:
        toggle_button['text'] = "Surprise is Off"
    global show_surprise
    show_surprise = not show_surprise
    global num
    num = random.randint(0, len(colors)-1)

# Initialize OpenCV video capture
cap = cv2.VideoCapture(0)

# Create a Tkinter window
window = tk.Tk()
window.title("Video Feed")

# Create a label to display the video feed
label = ttk.Label(window)
label.pack(padx=10, pady=10)

# Create a button to toggle the "surprise" text
toggle_button = ttk.Button(window, text="Surprise is Off", command=toggle_surprise)
toggle_button.pack(pady=10)

# Initialize the "show_surprise" variable
show_surprise = False
num = 0
# Start updating the video feed
update_video_feed()

# Create a quit button to exit the application
quit_button = ttk.Button(window, text="Quit", command=window.quit)
quit_button.pack(pady=10)

# Run the Tkinter main loop
window.mainloop()

# Release the camera when the application is closed
cap.release()
cv2.destroyAllWindows()
