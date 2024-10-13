'''
Quice hacerle un efecto de sombreado gradual al reloj para que no tenga un color liso
pero no estuve ni cerca debido a que tkinter no acepta imagenes con transparencias,
entonces no podía poner algo como eso por encima, y por sí solo no es capaz de hacer
colores con gradientes.
'''

import tkinter as tk
from tkinter.font import Font
from time import strftime
import requests
from PIL import Image, ImageTk
import io

window = tk.Tk()
window.title("Digital Clock")
window.configure(background='black')
window.attributes('-fullscreen', True)

custom_font = 'Helvetica Neue Condensed Bold'

# Clave API de OpenWeatherMap (cámbiala por tu clave)
API_KEY = '3cdcc7df8e583545b9990d8d4d4ab456'
CITY = 'Buenos Aires'
WEATHER_URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"


# Función para obtener los datos del clima
def get_weather_data():
    try:
        response = requests.get(WEATHER_URL)
        data = response.json()
        
        if data["cod"] == 200:
            temperature = data['main']['temp']
            description = data['weather'][0]['description']
            icon_code = data['weather'][0]['icon']
            
            # Obtener el ícono del clima
            icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
            icon_response = requests.get(icon_url)
            icon_image = Image.open(io.BytesIO(icon_response.content))
            icon_image = icon_image.resize((50, 50))
            icon_photo = ImageTk.PhotoImage(icon_image)
            
            return temperature, description.capitalize(), icon_photo
        else:
            return None, "Error obteniendo clima", None
    except Exception as e:
        return None, str(e), None

# Función para crear el efecto de gradiente en la fecha
def create_color_gradient(start_color, end_color, steps):
    def interpolate_color(start, end, factor):
        return int(start + (end - start) * factor)
    
    colors = []
    for i in range(steps):
        factor = i / float(steps - 1)
        r = interpolate_color(start_color[0], end_color[0], factor)
        g = interpolate_color(start_color[1], end_color[1], factor)
        b = interpolate_color(start_color[2], end_color[2], factor)
        colors.append(f'#{r:02x}{g:02x}{b:02x}')
    return colors

def apply_gradient_to_date():
    # Crear un gradiente de color de negro a gris claro
    gradient_colors = create_color_gradient((0, 0, 0), (173, 173, 173), len(date_labels))

    current_date = strftime('%a, %d %b').upper()

    # Aplicar gradiente de color a las etiquetas de la fecha
    for i, char in enumerate(current_date):
        if i < len(date_labels):
            date_labels[i].config(text=char, fg=gradient_colors[i])

    window.after(1000, apply_gradient_to_date)

def update_time_and_weather():
    current_time = strftime('%H %M')

    # Si la hora empieza con 0, lo eliminamos manualmente
    if current_time[0] == '0':
        current_time = current_time[1:]

    label_clock.config(text=current_time)

    temperature, description, icon_photo = get_weather_data()

    if temperature is not None:
        label_temperature.config(text=f"{temperature:.1f}°C")
        label_description.config(text=description.upper())
        label_icon.config(image=icon_photo)
        label_icon.image = icon_photo

    label_icon.place(x=label_clock.winfo_x(), y=label_clock.winfo_y() + 40)
    label_temperature.place(x=label_clock.winfo_x() + 50, y=label_clock.winfo_y() + 40)
    label_description.place(x=label_clock.winfo_x() + 175, y=label_clock.winfo_y() + 40)

    window.after(1000, update_time_and_weather)

# Etiquetas para el reloj y la fecha
label_clock = tk.Label(window, font=Font(family=custom_font, size=350), background='black', foreground='#ADADAD')
label_clock.place(relx=0.5, rely=0.5, anchor='center')

# Etiquetas para el clima
label_icon = tk.Label(window, background='black')
label_temperature = tk.Label(window, font=Font(family=custom_font, size=30), background='black', foreground='#C4C4C4')
label_description = tk.Label(window, font=Font(family=custom_font, size=30), background='black', foreground='#C4C4C4')

# Crear etiquetas individuales para cada carácter de la fecha (para aplicar gradiente)
date_labels = []
for i in range(20):  # Suponemos que la fecha tiene un máximo de 20 caracteres
    label = tk.Label(window, font=Font(family=custom_font, size=30), background='black')
    label.place(x=100 + (i * 20), y=100)  # Posición inicial de las etiquetas
    date_labels.append(label)

# Ejecutar la función de tiempo y clima
update_time_and_weather()
apply_gradient_to_date()

window.mainloop()
