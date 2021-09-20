from tkinter import *
import pandas
from random import choice

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
french_dict = {}

try:
    french_words = pandas.read_csv("data/words_to_learn.csv")  # read csv
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    french_dict = original_data.to_dict(orient="records")
else:
    # french_words_dataframe = pandas.DataFrame(french_words)  # making it dataframe
    french_dict = french_words.to_dict(orient="records")  # turning to dict


def random_french_word():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = choice(french_dict)
    canvas.itemconfig(french_text, text='French', fill='black')
    canvas.itemconfig(word_text, text=current_card['French'], fill='black')
    canvas.itemconfig(canvas_image, image=front_card)
    flip_timer = window.after(3000, func=random_english_word)


def random_english_word():
    canvas.itemconfig(french_text, text='English', fill='white')
    canvas.itemconfig(word_text, text=current_card['English'], fill='white')
    canvas.itemconfig(canvas_image, image=back_card)


def is_known():
    french_dict.remove(current_card)
    print(len(french_dict))

    data = pandas.DataFrame(french_dict)
    data.to_csv("data/words_to_learn.csv", index=False)

    random_french_word()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title('Maru 3K Flash')
window.config(pady=50, padx=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=random_english_word)

# Making Canvas
canvas = Canvas(width=800, height=526)
front_card = PhotoImage(file="images/card_front.png")
back_card = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=front_card)

# Text
french_text = canvas.create_text(400, 150, text='', font=("Ariel", 40, 'italic'))
word_text = canvas.create_text(400, 263, text='', font=("Ariel", 60, 'bold'))

# Canvas on grid
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=2)

# Wrong button
wrong_button_img = PhotoImage(file='images/wrong.png')
wrong_button = Button(image=wrong_button_img, highlightthickness=0, command=random_french_word)
wrong_button.grid(row=1, column=0)

# Right button
right_button_img = PhotoImage(file='images/right.png')
right_button = Button(image=right_button_img, highlightthickness=0, command=is_known)
right_button.grid(row=1, column=1)

random_french_word()

window.mainloop()
