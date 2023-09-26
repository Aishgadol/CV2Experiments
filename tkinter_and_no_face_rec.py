import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# Create a function to update the video feed
def update_video_feed():
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
        label.config(image=photo)
        label.image = photo
    window.after(10, update_video_feed)  # Update every 10 milliseconds

# Initialize OpenCV video capture
cap = cv2.VideoCapture(0)

# Create a Tkinter window
window = tk.Tk()
window.title("Video Feed")

# Create a label to display the video feed
label = ttk.Label(window)
label.pack(padx=5, pady=5)

# Start updating the video feed
update_video_feed()

# Create a quit button to exit the application
quit_button = ttk.Button(window, text="Quit", command=window.quit)
quit_button.pack(pady=15)

# Run the Tkinter main loop
window.mainloop()

# Release the camera when the application is closed
cap.release()
cv2.destroyAllWindows()
