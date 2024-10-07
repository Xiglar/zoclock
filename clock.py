import tkinter as tk
from time import strftime

window = tk.Tk()
window.title("Digital Clock")
window.configure(background='black')

def time():
    day, clock = strftime('%a, %d %b'), strftime('%I %M')
    label_day.config(text = day)
    label_clock.config(text = clock)
    label_clock.after(1000, time)

label_day = tk.Label(window, font=('impact', 10, 'bold'), background='black', foreground='white')
label_clock = tk.Label(window, font=('impact', 50, 'bold'), background='black', foreground='white')

label_clock.pack(anchor='center')
label_day.pack(side='left', fill='both')

time()

window.mainloop()