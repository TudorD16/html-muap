import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import numpy as np
import os
import aspose.words as aw
import subprocess

def main2():
    class FileCopyApp:
        def __init__(self, root):
            self.root = root
            self.root.title("Office Reader 1.0")
            self.root.geometry("400x400")
            self.root.config(bg="gray20")  # Set background color to dark gray

            # Destination directory
            self.current_user = os.getenv('USERNAME')

    def open_excel_and_display_table():
        file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx"), ("All Files", "*.*")])
        if file_path:
            try:
                wb = pd.ExcelFile(file_path)
                sheet_names = wb.sheet_names

                # Creating a new window for selecting the worksheet
                selection_window = tk.Toplevel(bg="gray20")
                selection_window.geometry("300x300")
                selection_window.title("Select Worksheet")
                selection_window.resizable(False, False)

                # Check if the custom style already exists
                style = ttk.Style()
                if 'custom_style' not in style.theme_names():
                    style.theme_create('custom_style',
                       parent='alt',
                       settings={'TCombobox':
                                 {'configure':
                                  {'selectforeground': 'white',
                                   'selectbackground': '#1a2228',
                                   'fieldforeground': 'white',
                                   'fieldbackground': '#1a2228',
                                   'background': '#1a2228'
                                   }
                                  }
                                 }
                       )
                style.theme_use('custom_style')

                style.configure('TCombobox', fieldbackground='#222222', background='#222222', foreground='#00ee00', arrowcolor='#00ee00', activeBackground="#222222")

                selection_window.option_add('*TCombobox*Listbox*Background', '#222222')
                selection_window.option_add('*TCombobox*Listbox*Foreground', '#00ee00')
                sheet_option = ttk.Combobox(selection_window, values=sheet_names)
                sheet_option.pack(pady=10)

                display_button = tk.Button(selection_window, text="Show Table", command=lambda: display_table(wb, sheet_option.get()), bg="gray40", fg="white", bd=1)
                display_button.pack(pady=5)

            except Exception as e:
                print("Error opening file:", e)

    def display_table(wb, sheet_name):
        df = wb.parse(sheet_name)
        df.replace(np.nan, '', inplace=True)

        table_window = tk.Toplevel()
        table_window.title("Excel Table")
        table_window.configure(bg="gray20")

        canvas = tk.Canvas(table_window)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        frame = tk.Frame(canvas)
        frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(table_window, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.configure(yscrollcommand=scrollbar.set)

        frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=frame, anchor="nw")

        for i in range(df.shape[0] + 1):  # Rows
            for j in range(df.shape[1] + 1):  # Columns
                if i == 0:
                    if j == 0:
                        label = tk.Label(frame, text="", width=10, height=2, borderwidth=1, relief="solid", bg="lightgray")
                    else:
                        label = tk.Label(frame, text=df.columns[j - 1], width=20, height=2, borderwidth=1, relief="solid", font=("Helvetica", 10, "bold"), bg="lightgray")
                else:
                    if j == 0:
                        label = tk.Label(frame, text=df.index[i - 1], width=10, height=2, borderwidth=1, relief="solid", font=("Helvetica", 10, "bold"))
                    else:
                        cell_text = str(df.iloc[i - 1, j - 1])
                        label_width = max(20, len(cell_text) + 2)
                        entry = tk.Entry(frame, width=label_width, borderwidth=1, relief="solid")
                        entry.insert(0, cell_text)
                        entry.config(state="readonly")
                        entry.bind("<FocusIn>", lambda event, entry=entry: entry.config(state="normal"))
                        entry.bind("<FocusOut>", lambda event, entry=entry: entry.config(state="readonly"))
                        entry.grid(row=i, column=j, sticky="nsew")
                label.grid(row=i, column=j, sticky="nsew")

        for i in range(df.shape[0] + 1):
            frame.grid_rowconfigure(i, weight=1)
        for j in range(df.shape[1] + 1):
            frame.grid_columnconfigure(j, weight=1)

        nav_frame = tk.Frame(table_window)
        nav_frame.config(bg="gray20")
        nav_frame.pack(side=tk.BOTTOM, pady=10)

        def navigate_left():
            canvas.xview_scroll(-1, "units")

        def navigate_right():
            canvas.xview_scroll(1, "units")

        left_button = tk.Button(nav_frame, text="← Left", bg="gray40", fg="white", command=navigate_left)
        left_button.pack(side=tk.LEFT, padx=5)

        right_button = tk.Button(nav_frame, text="Right →", bg="gray40", fg="white", command=navigate_right)
        right_button.pack(side=tk.LEFT, padx=5)

    def open_word_file_with_aspose():
        file_path = filedialog.askopenfilename(filetypes=[("Word Files", "*.docx"), ("All Files", "*.*")])
        if file_path:
            try:
                # Citește fișierul Word folosind Aspose
                doc = aw.Document(file_path)

                # Extrage fiecare paragraf separat
                paragraphs = [para.get_text() for para in doc.get_child_nodes(aw.NodeType.PARAGRAPH, True)]
                
                # Afișează conținutul într-o fereastră Tkinter
                display_word_content(paragraphs)
            except Exception as e:
                print(f"Error opening Word file: {e}")

    def display_word_content(paragraphs):
        text_window = tk.Toplevel()
        text_window.title("Word Document Content")
        text_window.geometry("600x400")

        # Crează un frame pentru text box și scrollbars
        frame = tk.Frame(text_window)
        frame.pack(fill=tk.BOTH, expand=True)

        # Crează scrollbars
        v_scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        h_scrollbar = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        # Crează text box
        text_box = tk.Text(frame, wrap=tk.NONE, bg="white", fg="black", yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        text_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Configurează scrollbars
        v_scrollbar.config(command=text_box.yview)
        h_scrollbar.config(command=text_box.xview)

        # Inserează textul paragrafelor, delimitând cu o linie goală între ele
        for para in paragraphs:
            text_box.insert(tk.END, para + "\n\n")

        text_box.config(state=tk.DISABLED)

    def open_word_file_with_wordpad():
        file_path = filedialog.askopenfilename(filetypes=[("Word Files", "*.docx"), ("All Files", "*.*")])
        if file_path:
            try:
                # Specifică calea completă a executabilului WordPad
                wordpad_path = r"C:\Program Files\Windows NT\Accessories\wordpad.exe"
                subprocess.run([wordpad_path, file_path], check=True)
            except Exception as e:
                print(f"Error opening file with WordPad: {e}")

    root = tk.Tk()
    root.title("Office Reader 1.0")
    root.geometry("300x300")
    root.config(bg="gray20")
    root.resizable(False, False)

    main_frame = tk.Frame(root, bg="gray20")
    main_frame.pack(padx=20, pady=20)

    open_excel_button = tk.Button(main_frame, text="Open Excel File", command=open_excel_and_display_table, bg="gray40", fg="white", bd=1)
    open_excel_button.pack(pady=5)

    open_word_button = tk.Button(main_frame, text="Open Word File", command=open_word_file_with_aspose, bg="gray40", fg="white", bd=1)
    open_word_button.pack(pady=5)

    open_wordpad_button = tk.Button(main_frame, text="Open Word File with WordPad", command=open_word_file_with_wordpad, bg="gray40", fg="white", bd=1)
    open_wordpad_button.pack(pady=5)

    info_label = tk.Label(main_frame, text="Note: Opening with WordPad", bg="gray20", fg="white")
    info_label.pack(pady=10)

    info_label1 = tk.Label(main_frame, text="Is only for documents containing images.", bg="gray20", fg="white")
    info_label1.pack(pady=10)

    info_labe2 = tk.Label(main_frame, text="This option is not currently available.", bg="gray20", fg="white")
    info_labe2.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main2()
