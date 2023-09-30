import cv2
import tkinter as tk
from tkinter import ttk
import random
from PIL import Image, ImageTk
import face_recognition

colors = [cv2.COLOR_BGR2YCrCb, cv2.COLOR_BGR2GRAY, cv2.COLOR_BGR2HLS, cv2.COLOR_BGR2HSV, cv2.COLOR_BGR2LAB,
          cv2.COLOR_BGR2XYZ]


# function to update the video feed
def update_video_feed():
    # read the current frame from live feed camera
    ret, frame = cap.read()
    if ret:
        # get all locations of faces in frame
        face_locations = face_recognition.face_locations(frame)
        # draw a square around each face
        for face_loc in face_locations:
            rec_colors = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            cv2.rectangle(frame, (face_loc[3], face_loc[0]), (face_loc[1], face_loc[2]), color=rec_colors, thickness=2)
        # if suprise is pressed than color will randomly change
        if not show_surprise:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        else:
            frame = cv2.cvtColor(frame, colors[num])

        # used gpt for this, need to convert frame from cv2 format to tkinter format so it can be displayed
        photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
        label.config(image=photo)
        label.image = photo

    # update video feed after 5 miliseconds, call the function on the ttk window object and not in a 'normal' call
    window.after(5, update_video_feed)


# function to change the button text, as well as generate random number to pick a color to display(random color changer)
def toggle_surprise():
    if toggle_button['text'] == "Surprise is Off":
        toggle_button['text'] = "Surprise is On"
    else:
        toggle_button['text'] = "Surprise is Off"
    global show_surprise
    show_surprise = not show_surprise
    global num
    # by changing it here, every press of the button will generate random num, and thus livefeed won't constantly
    # change colors but just once, everytime we press the button
    num = random.randint(0, len(colors) - 1)


# initialize opencv video capture
cap = cv2.VideoCapture(0)

# create the window where everything will be shown
window = tk.Tk()
window.title("Video Feed")

# this label will hold the video feed
label = ttk.Label(window)
label.pack(padx=10, pady=10)

# create the surprise button
toggle_button = ttk.Button(window, text="Surprise is Off", command=toggle_surprise)
toggle_button.pack(pady=10)
global rec_colors

# initialize global variables
show_surprise = False
num = 0
rec_colors = (0, 0, 0)
# updating video feed with rgb colors or random colors according to show_suprise
update_video_feed()

# quit button which will never be used because we close it using the x button
quit_button = ttk.Button(window, text="Quit", command=window.quit)
quit_button.pack(pady=10)

# run the tkinter mainloop after all parameters have been set
window.mainloop()

# gpt helped adding the cap.release() line, appearntly we need to release the camera before closing the window and not after
cap.release()
cv2.destroyAllWindows()
