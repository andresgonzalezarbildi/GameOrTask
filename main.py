import random
import subprocess
import tkinter as tk
from tkinter import messagebox
import psutil
import json

def open_game():
    game_path = r"C:\Riot Games\Riot Client\RiotClientServices.exe"
    args = ["--launch-product=league_of_legends", "--launch-patchline=live"]

    # Cierra el proceso si ya está activo
    if isProgramRunning("RiotClientServices.exe"):
        subprocess.call(["taskkill", "/F", "/IM", "RiotClientServices.exe"])

    # Abre el juego con los argumentos
    subprocess.Popen([game_path] + args)

def isProgramRunning(program_name):
    """Verifica si un programa está en ejecución."""
    for process in psutil.process_iter(['name']):
        if process.info['name'] == program_name:
            return True
    return False

def load_config():
    """Carga la configuración de un archivo JSON."""
    with open('config.json', 'r') as f:
        return json.load(f)

def choose_option(options):
    """Selecciona una opción según las probabilidades definidas."""
    total = sum(options.values())
    random_number = random.randint(1, total)

    cumulative = 0
    for option, probability in options.items():
        cumulative += probability
        if random_number <= cumulative:
            return option

def show_custom_message(message):
    """Muestra un mensaje personalizado en una ventana de tkinter."""
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

def main():
    options = load_config()
    selected_option = choose_option(options)

    if selected_option == "Abrir Lolcito":
        open_game()
    else:
        show_custom_message(f"{selected_option}")

if __name__ == "__main__":
    main()
