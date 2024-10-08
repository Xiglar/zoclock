import tkinter as tk
from tkinter.font import Font
from time import strftime

window = tk.Tk()
window.title("Digital Clock")
window.configure(background='black')

window.geometry('1280x832')
#window.attributes('-fullscreen', True)

#font_family = 'Swis721 BlkCn Bt'
custom_font = 'Helvetica Neue Condensed Bold'

def time():
    day, clock = strftime('%a, %d %b'), strftime('%I %M')
    label_clock.config(text = clock)
    label_day.config(text = day.upper())
    label_clock.after(1000, time)

label_clock = tk.Label(window, font=Font(family=custom_font, size = 300), background='black', foreground='#C4C4C4')
label_day = tk.Label(window, font=Font(family=custom_font, size = 35), background='black', foreground='#C4C4C4')
canvas = tk.Canvas(window, width=1200, height=3, bg='black', highlightbackground="black")

label_clock.place(relx=0.5, rely=0.5, anchor='center')
label_day.place(relx=0.3, rely=0.73, anchor='center')
canvas.place(relx=0.5, rely=0.5, anchor='center')




time()

window.mainloop()