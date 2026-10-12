import tkinter as tk
from tkinter import messagebox
import turtle
import math
import random

def draw_heart():
    t.penup()
    t.goto(0, -50)
    t.pendown()
    t.begin_fill()
    
    for i in range(630):
        t_val = i / 100
        x = 16 * math.sin(t_val) ** 3
        y = 13 * math.cos(t_val) - 5 * math.cos(2*t_val) - 2 * math.cos(3*t_val) - math.cos(4*t_val)
        t.goto(x * 12, (y * 12) - 20)
        
    t.end_fill()
    t.penup()
    t.goto(0, -180)
    t.color("#d60000")
    t.write("", align="center", font=("Verdana", 18, "bold"))

def move_no_button(event):
    width = root.winfo_width()
    height = root.winfo_height()
    new_x = random.randint(20, width - 80)
    new_y = random.randint(350, height - 50) 
    
    no_btn.place(x=new_x, y=new_y)

def on_yes():
    messagebox.showinfo("YAYYYYYYY!!!", "I LOVE YOU MY DIGITAL DARLING 😋🎀")
    root.destroy()

root = tk.Tk()
root.title("A Question for You...")
root.geometry("600x500")
root.configure(bg="#ffc0cb") 

canvas = tk.Canvas(root, width=600, height=350, bg="#ffc0cb", highlightthickness=0)
canvas.pack()

screen = turtle.TurtleScreen(canvas)
screen.bgcolor("#ffc0cb")

t = turtle.RawTurtle(screen)
t.shape("turtle")
t.speed(0)
t.color("#d60000", "#ff4d4d")

label = tk.Label(root, text="Will you be my Valentine?", 
                 font=("Comic Sans MS", 22, "bold"), bg="#ffc0cb", fg="#d60000")
label.place(x=300, y=360, anchor="center")
yes_btn = tk.Button(root, text="YES! ❤️", font=("Arial", 14, "bold"), 
                    bg="white", fg="green", width=10, command=on_yes)
yes_btn.place(x=180, y=420)
no_btn = tk.Button(root, text="No", font=("Arial", 14), 
                   bg="white", fg="red", width=10)
no_btn.place(x=320, y=420)
no_btn.bind("<Enter>", move_no_button)
draw_heart()
root.mainloop()