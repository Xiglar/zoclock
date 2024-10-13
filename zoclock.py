'''
                ### Bienvenida Zoe Xaubet, feliz cumpleaños!!! ###

    Este proyecto surge de la imposibilidad de descargar el reloj digital de tipo flip en tu versión de MacOS
y tu gusto por los relojes minimalistas de este tipo.
No conseguí lograr la animación de "flip" debido a que tkinter no es bueno para eso (desde ya te lo advierto
por si elegís importarlo en otros proyectos) y chatgpt, quien colaboró como desarrollador ayudante, recomendó
esta librería pero sin ese aviso previo :)
Espero que te guste y lo uses en tus 2 pcs a pesar de que en la de windows si puedas descargar el profesional.
Si te es necesario modificar alguna configuración o querés personalizarlo con otros colores, otra fuente u
otros tamaños, luego de las lineas de importación de librerías, hay un apartado para que lo personalices a tu gusto.
Gracias por ser la mejor novia del mundo, y que lo disfrutes, felices 21!!!
'''

import tkinter as tk # pip install tkinter
from tkinter.font import Font
from time import strftime
import requests # pip install requests
from PIL import Image, ImageTk # pip install pillow
import io


### Personalización ###

custom_font = 'Helvetica Neue Condensed Bold' # Default: 'Helvetica Neue Condensed Bold'
time_size = 350 # Default: 350 (280-420)
date_size = 30 # Default: 30
weather_size = 25 # Default: 25

bg_color = 'black' # Default: 'black'
fg_time_color = '#AAAAAA' # Default: '#AAAAAA'
fg_date_color = '#A2A2A2' # Default: '#A2A2A2'
fg_weather_color = '#A2A2A2' # Default: '#A2A2A2'

### /////////////// ###



# Configuración de la ventana
window = tk.Tk()
window.title("Digital Clock")
window.configure(background=bg_color)
window.attributes('-fullscreen', True)


#Clave API de OpenWeatherMap
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
    '''Obtiene la hora, la fecha y el clima, crea sus respectivos widgets y los actualiza
    por cada minuto que pasa.'''

    day, hour, minute = strftime('%a, %d %b'), strftime('%H'), strftime('%M')
    
    # Si la hora empieza con 0, lo eliminamos manualmente
    if hour[0] == '0':
        hour = hour[1:]  # Remover el primer carácter si es un cero

    label_hour.config(text=hour)
    label_minute.config(text=minute)
    label_day.config(text=day.upper())
    
    # Reposicionamos la fecha debajo de la hora
    window.update_idletasks()  # Asegura que se calculen las dimensiones de los widgets
    shade_x = label_shade.winfo_x()  # Obtiene la posición x de la hora
    shade_y = label_shade.winfo_y()  # Obtiene la posición y de la hora

    # Posiciona la fecha justo debajo de la hora, alineada al comienzo del texto
    label_day.place(x=shade_x, y=shade_y+370+time_size-350)

    # Actualizar clima
    temperature, description, icon_photo = get_weather_data()

    if temperature is not None:
        label_temperature.config(text=f"{temperature:.1f}°C,")
        label_description.config(text=description)
        label_icon.config(image=icon_photo)
        label_icon.image = icon_photo  # Mantener referencia de la imagen

    # Posiciona el clima justo por encima de la hora, alineada al comienzo del texto
    label_icon.place(x=shade_x, y=shade_y-46)
    label_temperature.place(x=shade_x+50, y=shade_y-46)
    label_description.place(x=shade_x+158, y=shade_y-46)
    
    # Actualiza la hora cada segundo
    label_hour.after(1000, update_time_and_weather)


# Estructurar widgets
label_shade = tk.Canvas(window, width=time_size+100, height=time_size, bg=bg_color, highlightbackground=bg_color)

# Etiquetas para el reloj y la fecha
label_hour = tk.Label(window, font=Font(family=custom_font, size = time_size), background=bg_color, foreground=fg_time_color)
label_minute = tk.Label(window, font=Font(family=custom_font, size = time_size), background=bg_color, foreground=fg_time_color)
label_day = tk.Label(window, font=Font(family=custom_font, size = date_size), background=bg_color, foreground=fg_date_color)
line = tk.Canvas(window, width=1200, height=3, bg=bg_color, highlightbackground=bg_color)

# Etiquetas para el clima
label_icon = tk.Label(window, background=bg_color)  # Acá va el ícono del clima
label_temperature = tk.Label(window, font=Font(family=custom_font, size = weather_size), background=bg_color, foreground=fg_weather_color)
label_description = tk.Label(window, font=Font(family=custom_font, size = weather_size), background=bg_color, foreground=fg_weather_color)


# Posicionar la hora en el centro
label_shade.place(relx=0.30, rely=0.5, anchor='center')
label_hour.place(relx=0.30, rely=0.5, anchor='center')
label_minute.place(relx=0.70, rely=0.5, anchor='center')
line.place(relx=0.5, rely=0.5, anchor='center')


update_time_and_weather()
window.mainloop()