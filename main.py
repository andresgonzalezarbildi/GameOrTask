import random
import subprocess
import tkinter as tk
from tkinter import messagebox
import psutil
import json
import time
import os

# Ruta para el archivo que guarda el resultado temporalmente
RESULT_FILE = 'result_cache.json'

# Función para abrir el juego
def open_game():
    game_path = r"C:\Riot Games\Riot Client\RiotClientServices.exe"
    args = ["--launch-product=league_of_legends", "--launch-patchline=live"]

    # Cierra el proceso si ya está activo
    if isProgramRunning("RiotClientServices.exe"):
        subprocess.call(["taskkill", "/F", "/IM", "RiotClientServices.exe"])

    # Abre el juego con los argumentos
    subprocess.Popen([game_path] + args)

# Verifica si un programa está en ejecución
def isProgramRunning(program_name):
    for process in psutil.process_iter(['name']):
        if process.info['name'] == program_name:
            return True
    return False

# Carga la configuración de un archivo JSON
def load_config():
    with open('config.json', 'r') as f:
        return json.load(f)

# Selecciona una opción según las probabilidades definidas
def choose_option(options):
    total = sum(options.values())
    random_number = random.randint(1, total)

    cumulative = 0
    for option, probability in options.items():
        cumulative += probability
        if random_number <= cumulative:
            return option

# Muestra un mensaje personalizado en una ventana de tkinter
def show_custom_message(message):
    root = tk.Tk()
    root.title("Opción Seleccionada")
    root.geometry("300x150")  # Tamaño de la ventana
    root.configure(bg="#f0f0f0")  # Color de fondo

    # Usar un marco para el contenido
    frame = tk.Frame(root, bg="#ffffff", bd=5, relief="groove")
    frame.pack(expand=True, fill="both", padx=10, pady=10)

    # Texto del mensaje
    label = tk.Label(frame, text=message, padx=20, pady=20, bg="#ffffff", font=("Helvetica", 12))
    label.pack()

    # Botón de aceptación con un estilo mejorado
    button = tk.Button(frame, text="Aceptar", command=root.destroy, padx=10, pady=5, bg="#4CAF50", fg="white", font=("Helvetica", 10))
    button.pack(pady=(0, 20))

    root.mainloop()

# Guarda el resultado temporalmente en un archivo JSON
def save_result(result):
    with open(RESULT_FILE, 'w') as f:
        json.dump({"result": result, "timestamp": time.time()}, f)

# Carga el resultado del archivo si no ha expirado
def load_cached_result():
    if os.path.exists(RESULT_FILE):
        with open(RESULT_FILE, 'r') as f:
            data = json.load(f)
            if time.time() - data['timestamp'] < 300:  # 5 minutos = 300 segundos
                return data['result']
    return None

def main():
    # Intenta cargar el resultado guardado
    cached_result = load_cached_result()

    if cached_result:
        # Si hay un resultado guardado válido, lo muestra
        show_custom_message(f"Ya te dije, {cached_result}")
    else:
        # Cargar las opciones del archivo JSON
        options = load_config()
        selected_option = choose_option(options)

        if selected_option == "Abrir Lolcito":
            selected_option = "Salió esa grieta"
            open_game()

        # Muestra el resultado y lo guarda por 5 minutos
        show_custom_message(f"{selected_option}")
        save_result(selected_option)

if __name__ == "__main__":
    main()
