import tkinter
from tkinter import ttk
from PIL import ImageTk, Image, UnidentifiedImageError
import gridGen
import threading, time

root = tkinter.Tk()
label = tkinter.Label(root)
label.pack()

def imageLoop():
    while True:
        gridGen.runGridGen()

        # Wait until image is ready
        while True:
            try:
                with Image.open("grid.ppm") as img:
                    img.load()
                    resized = img.resize((300, 300))
                break
            except (UnidentifiedImageError, ValueError, FileNotFoundError):
                time.sleep(0.1)

        # Push UI update to main thread
        root.after(0, lambda r=resized: setImage(r))

        # Wait 3 seconds before next update
        time.sleep(3)

def setImage(res):
    tkImg = ImageTk.PhotoImage(res)
    label.config(image=tkImg)
    label.image = tkImg  # prevent GC

# Start the loop in a single background thread
threading.Thread(target=imageLoop, daemon=True).start()


root.mainloop()