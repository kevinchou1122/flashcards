from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
to_learn={}
try:
    data = pandas.read_csv("./data/words_to_learn.csv")
    if data.empty:
        raise FileNotFoundError  # Force fallback to original list
except (FileNotFoundError, pandas.errors.EmptyDataError):
    original_data = pandas.read_csv("data/chinese_words.csv")
    data_dict = original_data.to_dict(orient="records")
else:
    data_dict = data.to_dict(orient="records")

current_card={}
flip_timer=None

def check_mark():
    global current_card,flip_timer
    flip_back_to_front()
    current_card=random.choice(data_dict)
    canvas.itemconfig(french_word,text=current_card["Chinese"])
    if flip_timer:
        window.after_cancel(flip_timer)

        # Schedule the reveal function after 3 seconds
    flip_timer = window.after(3000, reveal)


def reveal():
    canvas.itemconfig(card, image=card_back)  # Flip to back
    canvas.itemconfig(french_word, text=current_card["English"])  # Show English translation
    canvas.itemconfig(title, text="English")

def flip_back_to_front():
    # Flip back to the front of the card and show the French word again
    canvas.itemconfig(card, image=card_front)
    canvas.itemconfig(title, text="Chinese")

def is_known():
    data_dict.remove(current_card)
    data_known=pandas.DataFrame(data_dict)
    data_known.to_csv("data/words_to_learn.csv",index=False)
    check_mark()

window = Tk()
window.title("Flash Cards")
window.config(padx=50, pady=50,background=BACKGROUND_COLOR)

canvas = Canvas(width=800,height=526,highlightthickness=0,background=BACKGROUND_COLOR)
card_front = PhotoImage(file="./images/card_front.png")
card_back = PhotoImage(file="./images/card_back.png")
card=canvas.create_image(400,263,image=card_front)
title=canvas.create_text(400,150,text="Chinese",font=("Ariel",40,"italic"),fill="black")
french_word=canvas.create_text(400,263,text="",font=("Ariel",60,"bold"),fill="black")
canvas.grid(row=0, column=0,columnspan=2)

check=PhotoImage(file="./images/right.png")
cross=PhotoImage(file="./images/wrong.png")
know_button=Button(image=check,command=is_known)
know_button.grid(row=1,column=1)
cross_button=Button(image=cross,command=check_mark)
cross_button.grid(column=0,row=1)
know_button.config(highlightthickness=0,borderwidth=0,background=BACKGROUND_COLOR, activebackground=BACKGROUND_COLOR)
cross_button.config(highlightthickness=0,borderwidth=0,background=BACKGROUND_COLOR, activebackground=BACKGROUND_COLOR)

check_mark()

window.mainloop()