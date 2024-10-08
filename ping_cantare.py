import tkinter as tk
import subprocess
import threading
import time
import os
import json
from queue import Queue
from tkinter import filedialog, simpledialog, messagebox

class PingWorker(threading.Thread):
    def __init__(self, ip, queue):
        super().__init__()
        self.ip = ip
        self.queue = queue

    def run(self):
        try:
            response = subprocess.run(['ping', '-n', '1', self.ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=2)
            status = "Online" if "TTL=" in response.stdout.decode('utf-8') else "Offline"
        except subprocess.TimeoutExpired:
            status = "Offline"
        except Exception as e:
            status = "Error"
        self.queue.put((self.ip, status))

class PingApp:
    def __init__(self, rootSA):
        self.rootSA = rootSA
        self.rootSA.title("Listener - Device Checking")
        self.rootSA.geometry("1000x600")
        self.rootSA.config(bg="gray40")  # #cccccc
        
        self.search_label = tk.Label(rootSA, font=("Arial", 12, "bold"), text="Search:", fg="#ccff66", bg="gray40")
        self.search_label.pack(pady=5)
        
        self.search_entry = tk.Entry(rootSA, fg="cyan", bg="#333333", bd=4, insertbackground="#ccff66")
        self.search_entry.pack(pady=5)
        
        self.search_button = tk.Button(rootSA, text="Filter", fg="cyan", bg="gray20", bd=6, command=self.update_labels)
        self.search_button.pack(pady=5)
        
        # Canvas pentru scroll
        self.canvas = tk.Canvas(rootSA)
        self.canvas.config(bg="#cccccc")
        self.scroll_y = tk.Scrollbar(rootSA, orient="vertical", command=self.canvas.yview)
        self.scroll_y.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # Frame pentru conținutul scrollabil
        self.frame = tk.Frame(self.canvas)
        self.frame.config(bg="#cccccc")
        self.canvas.create_window((0, 0), window=self.frame, anchor='nw')
        self.frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.configure(yscrollcommand=self.scroll_y.set)
        
        # Bind mousewheel event
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        self.results = {"groups": []}
        self.queue = Queue()
        
        if not os.path.exists("Results_IP"):
            os.makedirs("Results_IP")
        
        self.update_interval = 10
        self.schedule_update()
        
        self.create_menu()
        
        # Load the JSON file if it exists
        #self.load_initial_json()
    
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    '''
    def load_initial_json(self):
        json_file_path = "cantare.json"
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                self.results = {"groups": []}
                for group in data.get("groups", []):
                    group_name = group.get("name")
                    ips = group.get("ips", {})
                    if group_name and ips:
                        self.results["groups"].append({
                            "name": group_name,
                            "ips": {ip: "Unknown" for ip in ips}
                        })
                self.update_labels()
        else:
            print(f"{json_file_path} not found.")
    '''
    
    def create_menu(self):
        menu = tk.Menu(self.rootSA)
        #menu.config(bg="gray40")
        self.rootSA.config(menu=menu)
        
        file_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open JSON", command=self.open_json)
        file_menu.add_command(label="Create JSON", command=self.create_json)
        file_menu.add_command(label="Edit JSON", command=self.open_edit_json)

    def open_json(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                self.results = {"groups": []}
                for group in data.get("groups", []):
                    group_name = group.get("name")
                    ips = group.get("ips", [])
                    if group_name and ips:
                        self.results["groups"].append({
                            "name": group_name,
                            "ips": {ip: "Unknown" for ip in ips}
                        })
                self.update_labels()
    
    def create_json(self):
        num_groups = simpledialog.askinteger("Create JSON", "Enter the number of groups:")
        if num_groups and num_groups > 0:
            groups = []
            for i in range(num_groups):
                group_name = simpledialog.askstring("Create JSON", f"Enter the name of group {i+1}:")
                ips_input = simpledialog.askstring("Create JSON", f"Enter IP addresses for group '{group_name}' separated by commas:")
                if group_name and ips_input:
                    ips = [ip.strip() for ip in ips_input.split(',') if ip.strip()]
                    if ips:
                        groups.append({
                            "name": group_name,
                            "ips": {ip: "Unknown" for ip in ips}  # Convertim lista în dicționar
                        })
            if groups:
                data = {
                    "groups": groups
                }
                file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
                if file_path:
                    with open(file_path, 'w', encoding='utf-8') as file:
                        json.dump(data, file, indent=4)
                self.results = {"groups": groups}
                self.update_labels()

    def open_edit_json(self):
        self.edit_window = tk.Toplevel(self.rootSA)
        self.edit_window.title("Edit JSON")
        self.edit_window.geometry("800x400")
        self.edit_window.config(bg="gray40")
        
        self.json_text = tk.Text(self.edit_window, wrap='word', undo=True, bg="black", fg="cyan", bd=6, insertbackground="#ccff66")
        self.json_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Button to load JSON content
        load_button = tk.Button(self.edit_window, text="Load JSON", command=self.load_json, bg="gray40", fg="#ccff66", bd=4)
        load_button.pack(side='left', padx=10, pady=5)
        
        # Button to save JSON content
        save_button = tk.Button(self.edit_window, text="Save JSON", command=self.save_json, bg="gray40", fg="#ccff66", bd=4)
        save_button.pack(side='left', padx=10, pady=5)
        
        # Button to close the edit window
        close_button = tk.Button(self.edit_window, text="Close", command=self.edit_window.destroy, bg="gray40", fg="red", bd=4)
        close_button.pack(side='right', padx=10, pady=5)
    
    def load_json(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                json_content = file.read()
                self.json_text.delete(1.0, tk.END)
                self.json_text.insert(tk.END, json_content)
    
    def save_json(self):
        try:
            json_content = self.json_text.get(1.0, tk.END)
            data = json.loads(json_content)  # Validate JSON
            file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(json.dumps(data, indent=4))
                messagebox.showinfo("Success", "JSON saved successfully!")
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid JSON format. Please check your JSON content.")

    def schedule_update(self):
        threading.Thread(target=self.update_results, daemon=True).start()
        self.rootSA.after(self.update_interval * 1000, self.schedule_update)
    
    def update_results(self):
        try:
            ips = [ip for group in self.results.get("groups", []) for ip in group.get("ips", {}).keys()]
            
            self.results = {"groups": [{ "name": group["name"], "ips": {ip: "Unknown" for ip in group["ips"].keys()}} for group in self.results.get("groups", [])]}
            
            ips.sort()
            
            threads = []
            for ip in ips:
                worker = PingWorker(ip, self.queue)
                worker.start()
                threads.append(worker)
            
            for thread in threads:
                thread.join()
            
            while not self.queue.empty():
                ip, status = self.queue.get()
                for group in self.results.get("groups", []):
                    if ip in group["ips"]:
                        group["ips"][ip] = status
            
            timestamp = time.strftime('%Y%m%d-%H%M%S')
            result_file = f"Results_IP/Scann_{timestamp}.json"
            
            with open(result_file, 'w', encoding='utf-8') as output_file:
                json.dump({
                    "timestamp": time.strftime('%H:%M:%S'),
                    "results": self.results
                }, output_file, indent=4)
                    
            self.rootSA.after(0, self.update_labels)
            
            if not os.path.exists('Results'):
                os.makedirs('Results')
            
            timestamp = time.strftime('%Y%m%d-%H%M%S')
            result_file = f"Results_IP/Scann_{timestamp}.json"
            
            with open(result_file, 'w', encoding='utf-8') as output_file:
                json.dump({
                    "timestamp": time.strftime('%H:%M:%S'),
                    "results": self.results
                }, output_file, indent=4)
                    
            self.rootSA.after(0, self.update_labels)
        
        except Exception as e:
            print(f"Error: {str(e)}")
    
    def update_labels(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        search_term = self.search_entry.get().strip().lower()

        max_groups_per_column = 30  # Numărul maxim de grupuri per coloană
        row = 0
        col = 0
        groups_displayed = 0  # Numără grupurile afișate în coloană
        column_spacing = 50  # Spațiul între coloane

        # Afișează grupurile și IP-urile aferente
        for group in self.results.get("groups", []):
            group_name = group.get("name")
            ips = group.get("ips", {})

            # Filtrare IP-uri pe baza termenului de căutare
            filtered_ips = {ip: status for ip, status in ips.items() if search_term in ip}

            if filtered_ips:  # Afișează grupul doar dacă are IP-uri care se potrivesc căutării
                if groups_displayed >= max_groups_per_column:
                    groups_displayed = 0
                    row = 0
                    col += 2  # Treci la următoarea pereche de coloane

                tk.Label(self.frame, text=f"Group: {group_name}", font=('Arial', 12, 'bold')).grid(row=row, column=col, columnspan=2, padx=(column_spacing, 20), pady=10, sticky="w")
                row += 1

                for ip, status in filtered_ips.items():
                    color = 'green' if status == "Online" else 'red'

                    ip_label = tk.Label(self.frame, text=ip, bg='white', borderwidth=1, relief="solid", padx=5, pady=2)
                    ip_label.grid(row=row, column=col, padx=(column_spacing, 5), pady=2, sticky="w")

                    status_label = tk.Label(self.frame, text=status, bg=color, fg='white', borderwidth=1, relief="solid", padx=5, pady=2)
                    status_label.grid(row=row, column=col + 1, padx=(5, 20), pady=2, sticky="w")

                    row += 1

                groups_displayed += 1

                # Reinițializare rând la finalul grupului
                if row >= max_groups_per_column:
                    row = 0
                    col += 2
                    groups_displayed = 0


if __name__ == "__main__":
    rootSA = tk.Tk()
    app = PingApp(rootSA)
    rootSA.mainloop()
