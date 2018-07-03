from tkinter import *
from PIL import Image, ImageTk
import os
script_dir = os.path.dirname(os.path.realpath(__file__))
window = Tk()

brick_image = Image.open(script_dir+"\\resources\\red_brick.png")
brick_red = ImageTk.PhotoImage(brick_image)
brick_image = Image.open(script_dir+"\\resources\\blue_brick.png")
brick_blue = ImageTk.PhotoImage(brick_image)
brick_image = Image.open(script_dir+"\\resources\\yellow_brick.png")
brick_yellow = ImageTk.PhotoImage(brick_image)

print_canvas = Canvas(window, width=500, height=500)
print_canvas.pack()

print_canvas.create_rectangle(0, 0, 500, 500, fill="white")
bricks = []


#Distance between two bricks left/right: 60
#Distance between two bricks up/down: 32
#Odd number start x: 40
#Even number start x: 71
#
for y in range(35, (64*4-51), 64):
    for x in range(40, (60*8+40), 60):
        print_canvas.create_image(x, y, image=brick_red)

#print_canvas.create_image(100, 35, image=brick_red)
for y in range(51, (64*4-51), 64):
    for x in range(71, (60*7+71), 60):
        print_canvas.create_image(x, y, image=brick_blue)

#print_canvas.create_image(40, 67, image=brick_yellow)

#print_canvas.create_image(71, 83, image=brick_yellow)

mainloop()