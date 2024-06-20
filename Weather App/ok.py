from configparser import ConfigParser
import requests
from tkinter import *
from tkinter import messagebox

# Function to get weather details
def get_weather(city):
    try:
        result = requests.get(url.format(city, api_key))
        result.raise_for_status()  # Raise an exception for any HTTP error
        json_data = result.json()
        
        city_name = json_data['name']
        country = json_data['sys']['country']
        temp_kelvin = json_data['main']['temp']
        temp_celsius = temp_kelvin - 273.15
        weather_description = json_data['weather'][0]['description']
        
        return city_name, country, temp_celsius, weather_description
    except requests.exceptions.RequestException as e:
        messagebox.showerror('Error', f"Failed to fetch data: {e}")
        return None

# Function to handle search button click
def search():
    city = city_text.get()
    if city:
        weather_info = get_weather(city)
        if weather_info:
            location_lbl.config(text=f'{weather_info[0]}, {weather_info[1]}')
            temperature_label.config(text=f'{weather_info[2]:.2f} °C')
            weather_l.config(text=weather_info[3])
    else:
        messagebox.showwarning('Warning', "Please enter a city name.")

# Load API key from config file
config_file = "config.ini"
config = ConfigParser()
try:
    config.read(config_file)
    api_key = config.get('myapp', 'api')
except (ConfigParser.Error, FileNotFoundError) as e:
    messagebox.showerror('Error', f"Failed to read configuration: {e}")
    exit()

# Define API URL
url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'

# Create GUI
app = Tk()
app.title("Weather App")
app.geometry("300x150")

# Labels and Entry
city_label = Label(app, text="City:")
city_label.grid(row=0, column=0, padx=5, pady=5)

city_text = StringVar()
city_entry = Entry(app, textvariable=city_text)
city_entry.grid(row=0, column=1, padx=5, pady=5)

# Search Button
search_btn = Button(app, text="Search Weather", width=15, command=search)
search_btn.grid(row=1, column=0, columnspan=2, pady=5)

# Weather Information Labels
location_lbl = Label(app, text="Location")
location_lbl.grid(row=2, column=0, columnspan=2)

temperature_label = Label(app, text="")
temperature_label.grid(row=3, column=0, columnspan=2)

weather_l = Label(app, text="")
weather_l.grid(row=4, column=0, columnspan=2)

# Run the GUI application
app.mainloop()