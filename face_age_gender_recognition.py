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
            face_top, face_right, face_bottom, face_left=face_loc
            random_color_scheme = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            cv2.rectangle(frame, (face_left, face_top), (face_right, face_bottom), color=random_color_scheme, thickness=2)
            face = frame[max(0, face_top):min(face_bottom + 15, frame.shape[0] - 1),
                   max(0, face_left - 15):min(face_right + 15,frame.shape[1] - 1)]
            blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
            gen.setInput(blob)
            age.setInput(blob)
            genderPreds = gen.forward()
            agePreds=age.forward()
            gender = list_of_genders[genderPreds[0].argmax()]
            age_of_face=list_of_ages[agePreds[0].argmax()]
            cv2.putText(frame,f"This is a {gender}, {round(genderPreds[0][genderPreds[0].argmax()]*100,2)}% ",
                        (face_left,face_top-20),cv2.FONT_HERSHEY_PLAIN,1,random_color_scheme,1)
            cv2.putText(frame,f"user seems to be aged {age_of_face}, {round(agePreds[0][agePreds[0].argmax()]*100,2)}%",
                          (face_left, face_top - 10), cv2.FONT_HERSHEY_PLAIN, 1, random_color_scheme, 1)
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
# Importing Models and set mean values
age1 = "age_deploy.prototxt"
age2 = "age_net.caffemodel"
gen1 = "gender_deploy.prototxt"
gen2 = "gender_net.caffemodel"
MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
# Using models
# age
age = cv2.dnn.readNet(age2, age1)
# gender
gen = cv2.dnn.readNet(gen2, gen1)
# Categories of distribution
list_of_ages = ['(0-2)', '(4-6)', '(8-12)', '(15-20)',
      '(25-32)', '(38-43)', '(48-53)', '(60-100)']
list_of_genders = ['Male', 'Female']

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

# initialize global variables
show_surprise = False
num = 0
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
