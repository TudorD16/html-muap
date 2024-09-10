import tkinter as tk
from tkinter import font, simpledialog, messagebox, ttk
import urllib.request
import time
import json
import os
import getpass

# URL-ul fișierului de pe GitHub
file_url = "https://raw.githubusercontent.com/TudorD16/html-muap/main/mail.txt"
settings_file = "mail_settings.json"

# Cache pentru stocarea conținutului și timestamp-ului
cache = {'content': [], 'timestamp': 0}
cache_duration = 30  # Durata cache-ului în secunde

# Lista de mesaje și conținut precedent
messages = []
previous_content = []
filtered_messages = []  # Mesajele filtrate în urma căutării

# Variabilă pentru a urmări dacă este activă o căutare
search_active = False

# Funcția pentru a verifica conexiunea la internet
def check_internet_connection():
    try:
        urllib.request.urlopen("http://www.google.com", timeout=5)
        return True
    except Exception as e:
        return False

# Funcția pentru a încărca setările din fișierul JSON
def load_settings():
    if os.path.exists(settings_file):
        with open(settings_file, 'r') as f:
            settings = json.load(f)
    else:
        settings = {"font": "Arial", "size": 12}
        save_settings(settings)
    return settings

# Funcția pentru a salva setările într-un fișier JSON
def save_settings(settings):
    with open(settings_file, 'w') as f:
        json.dump(settings, f)

# Setări implicite pentru font
settings = load_settings()
current_font = (settings.get("font", "Arial"), settings.get("size", 12))

# Funcția pentru a citi conținutul fișierului cu cache
def read_mail_file():
    current_time = time.time()
    if current_time - cache['timestamp'] > cache_duration:
        try:
            with urllib.request.urlopen(file_url) as response:
                content = response.read().decode('utf-8').strip()
                cache['content'] = [mail.strip() for mail in content.split('..') if mail.strip()]
                cache['timestamp'] = current_time
        except Exception as e:
            print(f"Error reading the mail file: {e}")
    return cache['content']

# Funcția pentru a afișa conținutul mesajului selectat (după "::")
def show_message(event):
    selected_index = inbox_listbox.curselection()
    if selected_index:
        selected_message = filtered_messages[selected_index[0]]
        message_text.delete(1.0, tk.END)
        # Afișăm doar partea după "::"
        message_body = extract_message_body(selected_message)
        if not message_body.endswith('.'):
            message_body += '.'
        message_text.insert(tk.END, message_body)

# Funcția pentru a actualiza inbox-ul doar cu mesajele noi
def update_messages_from_file():
    global previous_content, messages
    new_content = read_mail_file()
    if new_content != previous_content:
        new_messages = [msg for msg in new_content if msg not in previous_content]
        if new_messages:
            messages.extend(new_messages)
            previous_content = new_content
            update_inbox()
    root.after(5000, update_messages_from_file)

# Funcția de actualizare a listei de inbox pentru a afișa subiectele
def update_inbox():
    global filtered_messages
    filtered_messages = messages.copy()  # Începem cu toate mesajele afișate
    inbox_listbox.delete(0, tk.END)
    for msg in filtered_messages:
        subject = extract_subject(msg)
        inbox_listbox.insert(tk.END, subject)

# Funcția pentru a extrage subiectul din mesaj
def extract_subject(message):
    if "::" in message:
        return message.split("::")[0].strip()  # Extragem textul până la "::"
    return message[:30]  # Dacă nu există "::", afișăm primele 30 de caractere ca fallback

# Funcția pentru a extrage corpul mesajului după "::"
def extract_message_body(message):
    if "::" in message:
        return message.split("::", 1)[1].strip()  # Extragem textul de după "::"
    return message  # Dacă nu există "::", afișăm tot mesajul

# Funcția pentru a actualiza inbox-ul manual la apăsarea butonului de refresh
def refresh_inbox():
    global previous_content, messages
    previous_content = []
    messages = []
    update_messages_from_file()

# Funcția pentru a căuta mesaje pe baza unui cuvânt cheie
def search_mail():
    global filtered_messages, search_active
    keyword = simpledialog.askstring("Search Mail", "Enter keyword:")
    if keyword:
        filtered_messages = [msg for msg in messages if keyword.lower() in msg.lower()]
        inbox_listbox.delete(0, tk.END)
        if filtered_messages:
            for msg in filtered_messages:
                subject = extract_subject(msg)
                inbox_listbox.insert(tk.END, subject)
        else:
            inbox_listbox.insert(tk.END, "No matches found.")
        search_active = True
        update_clear_search_button()

# Funcția pentru a șterge filtrul de căutare și a afișa toate mesajele
def clear_search():
    global search_active
    search_active = False
    update_inbox()
    update_clear_search_button()

# Funcția pentru a activa/dezactiva butonul de "Clear Search"
def update_clear_search_button():
    search_menu.entryconfig("Clear Search", state=tk.NORMAL if search_active else tk.DISABLED)

# Funcția pentru a selecta un font dintr-o listă predefinită
def choose_font():
    font_choice = tk.Toplevel(root)
    font_choice.title("Choose Font")
    fonts = list(font.families())
    font_listbox = tk.Listbox(font_choice)
    font_listbox.pack(fill=tk.BOTH, expand=True)
    for fnt in fonts:
        font_listbox.insert(tk.END, fnt)

    def set_font():
        global current_font
        selected_font = font_listbox.get(tk.ACTIVE)
        current_font = (selected_font, current_font[1])
        apply_font()
        settings["font"] = selected_font
        save_settings(settings)
        font_choice.destroy()

    select_button = tk.Button(font_choice, text="Select Font", command=set_font)
    select_button.pack()

# Funcția pentru a schimba dimensiunea fontului
def change_font_size():
    global current_font
    new_size = simpledialog.askinteger("Change Font Size", "Enter font size:")
    if new_size:
        current_font = (current_font[0], new_size)
        apply_font()
        settings["size"] = new_size
        save_settings(settings)

# Funcția pentru a aplica fontul selectat
def apply_font():
    inbox_listbox.config(font=current_font)
    message_text.config(font=current_font)

# Funcția pentru a deschide opțiunea de căutare
def open_search(event=None):
    search_mail()

# Verificăm conexiunea la internet înainte de a porni aplicația
if not check_internet_connection():
    messagebox.showerror("No Internet Connection", "Please check your internet connection and try again.")
    exit()

# Crearea interfeței
root = tk.Tk()
current_user = getpass.getuser()  # Obține numele utilizatorului curent
root.title(f"Muap Mail - {current_user}.muap.ro")  # Setează titlul ferestrei

# Stilizare
root.geometry("840x600")
root.configure(bg="#2e2e2e")

# Crearea unei bare de meniu
menubar = tk.Menu(root)
root.config(menu=menubar)

# Meniu "Settings" pentru a schimba fontul și dimensiunea textului
settings_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Settings", menu=settings_menu)
settings_menu.add_command(label="Change Font", command=choose_font)
settings_menu.add_command(label="Change Font Size", command=change_font_size)

# Meniu "Search" pentru a căuta un cuvânt cheie
search_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Search", menu=search_menu)
search_menu.add_command(label="Search Mail", command=open_search)
search_menu.add_command(label="Clear Search", command=clear_search)

# Cadru pentru inbox
inbox_frame = tk.Frame(root, bg="#3c3c3c", padx=10, pady=10)
inbox_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Lista de inbox
inbox_listbox = tk.Listbox(inbox_frame, height=20, width=30, bg="#1e1e1e", fg="#ffffff", font=current_font)
inbox_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
inbox_listbox.bind('<<ListboxSelect>>', show_message)

# Cadru pentru vizualizarea mesajului
message_frame = tk.Frame(root, bg="#3c3c3c", padx=10, pady=10)
message_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Textarea pentru vizualizarea mesajului
message_text = tk.Text(message_frame, bg="#1e1e1e", fg="#ffffff", font=current_font)
message_text.pack(fill=tk.BOTH, expand=True)

# Buton de refresh
refresh_button = tk.Button(root, text="Refresh", command=refresh_inbox, bg="#4CAF50", fg="#ffffff", font=("Arial", 12))
refresh_button.pack(side=tk.BOTTOM, pady=10)

# Aplicăm fontul inițial
apply_font()

# Începem actualizarea mesajelor
update_messages_from_file()

# Bind Ctrl+F pentru a deschide opțiunea de căutare
root.bind('<Control-f>', open_search)

# Start the GUI event loop
root.mainloop()
