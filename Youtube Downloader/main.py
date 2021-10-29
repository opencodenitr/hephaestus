import tkinter as tk
from tkinter import Canvas
from gui import GUI

# Init action for tkinter window and canvas

win = tk.Tk()
win.config(bg='red')
win.title('Youtube Downloader v1.0')
canvas = Canvas(win, width=750, height=500, bg='red')
canvas.pack()
win.resizable(0,0)

gui = GUI(win, canvas)
gui.create_GUI_layout()
