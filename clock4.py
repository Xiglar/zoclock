import tkinter as tk
from tkinter.font import Font
from time import strftime
import requests
from PIL import Image, ImageTk
import io

window = tk.Tk()
window.title("Digital Clock")
window.configure(background='black')
window.geometry('1280x832')
#window.attributes('-fullscreen', True)

custom_font = 'Helvetica Neue Condensed Bold'

# Clave API de OpenWeatherMap (cámbiala por tu clave)
API_KEY = '3cdcc7df8e583545b9990d8d4d4ab456'
CITY = 'Buenos Aires'  # Cambia la ciudad a la que desees consultar
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
            icon_image = icon_image.resize((50, 50))  # Ajustar tamaño del ícono
            icon_photo = ImageTk.PhotoImage(icon_image)
            
            return temperature, description.capitalize(), icon_photo
        else:
            return None, "Error obteniendo clima", None
    except Exception as e:
        return None, str(e), None

def update_time_and_weather():
    day, clock = strftime('%a, %d %b'), strftime('%H %M')
    
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
    
    # Posiciona la fecha justo debajo de la hora, alineada al comienzo del texto
    label_day.place(x=clock_x, y=clock_y+480)

    # Actualizar clima
    temperature, description, icon_photo = get_weather_data()

    if temperature is not None:
        label_temperature.config(text=f"{temperature:.1f}°C")
        label_description.config(text=description.upper())
        label_icon.config(image=icon_photo)
        label_icon.image = icon_photo  # Mantener referencia de la imagen

    # Posicionar las etiquetas
    label_icon.place(x=clock_x, y=clock_y+40)
    label_temperature.place(x=clock_x+50, y=clock_y+40)
    label_description.place(x=clock_x+175, y=clock_y+40)
    
    # Actualiza la hora cada segundo
    label_clock.after(1000, update_time_and_weather)


# Etiquetas para el reloj y la fecha
label_clock = tk.Label(window, font=Font(family=custom_font, size = 350), background='black', foreground='#AAAAAA')
label_day = tk.Label(window, font=Font(family=custom_font, size = 30), background='black', foreground='#AAAAAA')
canvas = tk.Canvas(window, width=1200, height=3, bg='black', highlightbackground="black")

# Etiquetas para el clima
label_icon = tk.Label(window, background='black')  # Aquí va el ícono del clima
label_temperature = tk.Label(window, font=Font(family=custom_font, size=30), background='black', foreground='#AAAAAA')
label_description = tk.Label(window, font=Font(family=custom_font, size=30), background='black', foreground='#AAAAAA')

# Posicionar la hora en el centro
label_clock.place(relx=0.5, rely=0.5, anchor='center')
canvas.place(relx=0.5, rely=0.5, anchor='center')


update_time_and_weather()
window.mainloop()