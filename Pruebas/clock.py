import tkinter as tk
from tkinter.font import Font
from time import strftime

window = tk.Tk()
window.title("Digital Clock")
window.configure(background='black')
window.geometry('1280x832')
#window.attributes('-fullscreen', True)

custom_font = 'Helvetica Neue Condensed Bold'

def time():
    day = strftime('%a, %d %b')
    clock = strftime('%H %M')
    
    # Si la hora empieza con 0, lo eliminamos manualmente
    if clock[0] == '0':
        clock = clock[1:]  # Remover el primer carácter si es un cero

    label_clock.config(text=clock)
    label_day.config(text=day.upper())
    
    # Reposicionamos la fecha debajo de la hora
    window.update_idletasks()  # Asegura que se calculen las dimensiones de los widgets
    clock_width = label_clock.winfo_width()  # Obtiene el ancho del widget de la hora
    clock_height = label_clock.winfo_height()
    clock_x = label_clock.winfo_x()  # Obtiene la posición x de la hora
    clock_y = label_clock.winfo_y()
    print(clock_x, clock_y)
    print(clock_width, clock_height)
    
    # Posiciona la fecha justo debajo de la hora, alineada al comienzo del texto
    label_day.place(x=clock_x, y=clock_y+480)
    
    # Actualiza la hora cada segundo
    label_clock.after(1000, time)

label_clock = tk.Label(window, font=Font(family=custom_font, size = 350), background='black', foreground='#ADADAD')
label_day = tk.Label(window, font=Font(family=custom_font, size = 30), background='black', foreground='#ADADAD')
canvas = tk.Canvas(window, width=1200, height=3, bg='black', highlightbackground="black")

#label_clock.place(relx=0.5, rely=0.5, anchor='center')
#label_day.place(relx=0.3, rely=0.73, anchor='center')
# Posicionar la hora en el centro
label_clock.place(relx=0.5, rely=0.5, anchor='center')
canvas.place(relx=0.5, rely=0.5, anchor='center')



time()

window.mainloop()