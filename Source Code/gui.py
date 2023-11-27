import sys
import os
from tkinter import *
import recorder
import time
from PIL import Image,ImageTk

def start():
    global running, start_time

    if running is not None:
        print('Recording already in progress')
    else:
        start_time = time.time()  # Record the start time
        running = rec.open('AudioFile/audio.wav', 'wb')
        running.start_recording()
        update_timer()  # Start updating the timer

def stop():
    global running, start_time

    if running is not None:
        running.stop_recording()
        running.close()
        running = None
        window.after_cancel(timer_id)  # Stop updating the timer
        elapsed_time = time.time() - start_time
        print(f'Recording stopped. Elapsed time: {elapsed_time:.2f} seconds')
    else:
        print('No recording in progress')

def update_timer():
    elapsed_time = time.time() - start_time
    timer_label.config(text=f'Time: {elapsed_time:.2f} seconds')
    global timer_id
    timer_id = window.after(100, update_timer)  # Update the timer every 100 milliseconds

def run():
    os.system('python "Source Code/summarization.py"')

rec = recorder.Recorder(channels=1)
running = None
start_time = 0
timer_id = None

window = Tk()
window.title("Running Python Script")
window.geometry('550x200')

# Styling
font_style = ("Helvetica", 12)

background_image = Image.open('images/background.jpeg')

background_image = background_image.resize((550,200),Image.LANCZOS)



background_image= ImageTk.PhotoImage(background_image, master= window)

label = Label(window, image=background_image)
label.place(x = 0,y = 0)


button_rec = Button(window, text='Start Recording', command=start ,font=font_style)
button_rec.pack(pady=10)


button_stop = Button(window, text='Stop Recording', command=stop,font=font_style)
button_stop.pack(pady=10)

btn = Button(window, text="Summarize", command=run ,font=font_style)
btn.pack(pady=10)

timer_label = Label(window, text='Time: 0.00 seconds', font=font_style)
timer_label.pack(pady=10)

window.mainloop()