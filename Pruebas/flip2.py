'''
Intenté hacer la animación de flip, pero era algo muy rebuscado y complicado que
no quedaría bien puesto que tkinter no tiene la capacidad para hacer animaciones
como esa, y entonces el rebote de la ficha del digito no se lograría o quedaría
poco realista, entonces opte porque no tenga animación antes de que sea fea.
'''

import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFont
from time import strftime
import time

# Crear la ventana de Tkinter
window = tk.Tk()
window.title("Flip Clock Animation")
window.configure(bg='black')

# Crear canvas para la animación
canvas = tk.Canvas(window, width=400, height=300, bg='black', highlightthickness=0)
canvas.pack()

# Fuente personalizada para Pillow
font = ImageFont.truetype("arial.ttf", 100)  # Cambia el archivo de fuente si es necesario

# Inicializar números
current_minute = strftime('%M')

# Crear imagen inicial de número con Pillow
def create_number_image(number):
    img = Image.new('RGB', (200, 150), color='black')
    draw = ImageDraw.Draw(img)
    draw.text((50, 20), str(number).zfill(2), font=font, fill='white')
    return img

# Mostrar imagen en el canvas de Tkinter
def show_image(image):
    img = ImageTk.PhotoImage(image)
    canvas.create_image(200, 150, image=img)
    canvas.image = img  # Mantener referencia para evitar que la imagen se borre

# Función para animación tipo flip
def flip_animation(old_number, new_number, step=0):
    if step < 10:
        # Reducir el número viejo en altura (simulando el "flip")
        scale = 1 - step * 0.1
        old_img = create_number_image(old_number)
        old_img = old_img.resize((200, int(150 * scale)))
        show_image(old_img)
        window.after(50, flip_animation, old_number, new_number, step + 1)
    elif step == 10:
        # Iniciar el nuevo número y agrandarlo
        new_img = create_number_image(new_number)
        show_image(new_img)
    elif step < 20:
        # Agrandar el nuevo número en altura
        scale = (step - 10) * 0.1
        new_img = create_number_image(new_number)
        new_img = new_img.resize((200, int(150 * scale)))
        show_image(new_img)
        window.after(50, flip_animation, old_number, new_number, step + 1)

# Función para actualizar el tiempo
def update_time():
    global current_minute
    new_minute = strftime('%M')

    if new_minute != current_minute:
        flip_animation(current_minute, new_minute)  # Iniciar animación
        current_minute = new_minute

    # Actualizar cada segundo
    window.after(1000, update_time)

# Iniciar la actualización de tiempo
update_time()

# Ejecutar la ventana de Tkinter
window.mainloop()
