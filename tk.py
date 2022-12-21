import tkinter as tk
from cam import Cam


root = tk.Tk()
root.title("Cam sim")
root.geometry("2000x2000")

canvas = tk.Canvas(root, width=1000, height=1000, bg='black')
canvas.pack()

canvas.create_line(200, 100, 100, 200, fill='red')

cam = Cam()
cam.draw_on(canvas)

root.mainloop()
