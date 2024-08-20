import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import psutil

class MultiAppLauncher(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MultiApp Launcher v.0.1.3")
        self.geometry("600x450")
        self.resizable(False, False)
        self.config(bg="#1a1a1a")

        self.processes = []

        # Adăugare Label pentru a lansa aplicațiile
        self.label = tk.Label(self, text="Launch multiple instances of Multiapp.exe", fg="#c2c2d6", bg="#1a1a1a")
        self.label.pack(pady=10)

        self.launch_button = tk.Button(self, text="Launch Applications", fg="#ccff66", bg="#333333", bd=5, command=self.launch_apps)
        self.launch_button.pack(pady=10)

        self.instances_label = tk.Label(self, text="Number of instances:", fg="#c2c2d6", bg="#1a1a1a")
        self.instances_label.pack(pady=5)

        self.instances_entry = tk.Entry(self, fg="#ccff66", bg="#404040", insertbackground="#ccff66")
        self.instances_entry.pack(pady=5)

        self.stop_button = tk.Button(self, text="Stop Applications", fg="#ff6666", bg="#333333", bd=5, command=self.stop_apps)
        self.stop_button.pack(pady=10)

        # Cadru principal pentru conturi cu scrollbar
        self.accounts_canvas = tk.Canvas(self, bg="#1a1a1a")
        self.accounts_frame = tk.Frame(self.accounts_canvas, bg="#1a1a1a")
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.accounts_canvas.yview)
        self.accounts_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.accounts_canvas.pack(side="left", fill="both", expand=True)
        self.accounts_canvas.create_window((0, 0), window=self.accounts_frame, anchor="nw")

        self.accounts_frame.bind("<Configure>", self.on_frame_configure)

        # Creează cadrele separate pentru conturi
        self.frame_no_key = tk.LabelFrame(self.accounts_frame, text="Accounts without Product Key", fg="#ccff66", bg="#1a1a1a", bd=5, padx=10, pady=10)
        self.frame_with_key = tk.LabelFrame(self.accounts_frame, text="Accounts with Product Key", fg="#ff6666", bg="#1a1a1a", bd=5, padx=10, pady=10)

        self.frame_no_key.pack(pady=10, fill=tk.BOTH, expand=True)
        self.frame_with_key.pack(pady=10, fill=tk.BOTH, expand=True)

        # Citește și afișează conturile
        self.load_accounts()

    def launch_apps(self):
        try:
            num_instances = int(self.instances_entry.get())
            if num_instances <= 0:
                raise ValueError("The number must be positive")

            for _ in range(num_instances):
                process = subprocess.Popen(["Multiapp.exe"], cwd=os.getcwd())
                self.processes.append(process)

            messagebox.showinfo("Success", f"{num_instances} instances have been launched.")
        except ValueError as ve:
            messagebox.showerror("Error", f"Invalid value: {ve}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def stop_apps(self):
        try:
            # Identifică și oprește procesele utilizând psutil
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'] == 'Multiapp.exe':
                    proc.terminate()  # Termină procesul
                    proc.wait()  # Așteaptă ca procesul să fie închis complet

            # Golește lista de procese
            self.processes = []
            messagebox.showinfo("Stopped", "All instances of Multiapp.exe have been stopped.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop processes: {e}")

    def load_accounts(self):
        try:
            with open("Accounts.txt", "r") as file:
                lines = file.readlines()

            # Variabile pentru organizarea layout-ului
            row_no_key = 0
            col_no_key = 0
            row_with_key = 0
            col_with_key = 0

            for line in lines:
                line = line.strip()
                if line and '|' not in line and not line.startswith('---'):  # Sari peste liniile goale, titluri și linii cu '-'
                    user_info = line.split()[0]  # Preia doar numele utilizatorului
                    
                    if "product_key" in line:
                        # Conturile care necesită product_key
                        account_label = tk.Label(self.frame_with_key, text=user_info, fg="#ccff66", bg="#333333", width=20, height=2, bd=5, relief="groove")
                        account_label.grid(row=row_with_key, column=col_with_key, padx=10, pady=10)
                        col_with_key += 1
                        if col_with_key == 3:  # Afișează 3 pe o linie
                            col_with_key = 0
                            row_with_key += 1
                    else:
                        # Conturile care nu necesită product_key
                        account_label = tk.Label(self.frame_no_key, text=user_info, fg="#ccff66", bg="#333333", width=20, height=2, bd=5, relief="groove")
                        account_label.grid(row=row_no_key, column=col_no_key, padx=10, pady=10)
                        col_no_key += 1
                        if col_no_key == 3:  # Afișează 3 pe o linie
                            col_no_key = 0
                            row_no_key += 1

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load accounts: {e}")

    def on_frame_configure(self, event):
        """Reconfigurează scroll-ul pentru canvas."""
        self.accounts_canvas.configure(scrollregion=self.accounts_canvas.bbox("all"))

if __name__ == "__main__":
    app = MultiAppLauncher()
    app.mainloop()
