import tkinter as tk
from PIL import Image, ImageTk

def create_splash_screen():
    splash = tk.Tk()
    splash.title("Splash Screen")
    
    # Ascunde bara de titlu
    splash.overrideredirect(True)
    
    # Încărcați imaginea folosind PIL pentru a obține dimensiunile
    image_path = "splash_image.png"
    original_image = Image.open(image_path)
    splash_width, splash_height = original_image.size
    
    # Dimensiunile ecranului
    screen_width = splash.winfo_screenwidth()
    screen_height = splash.winfo_screenheight()
    
    # Calculează poziția ferestrei pentru a fi centrata
    x = (screen_width - splash_width) // 2
    y = (screen_height - splash_height) // 2
    
    # Setează dimensiunile și poziția ferestrei
    splash.geometry(f"{splash_width}x{splash_height}+{x}+{y}")
    
    # Convertiți imaginea într-un format Tkinter compatibil
    splash_image = ImageTk.PhotoImage(original_image)
    
    # Adăugarea imaginii
    label = tk.Label(splash, image=splash_image)
    label.pack(fill=tk.BOTH, expand=True)
    
    # Afișarea splash screen-ului timp de 3 secunde
    splash.after(3000, splash.destroy)  # distruge splash screen-ul după 3000 milisecunde (3 secunde)
    
    splash.mainloop()

# Exemplu de utilizare
create_splash_screen()

# Codul aplicației tale principale ar urma aici
print("Aplicația principală începe acum...")
