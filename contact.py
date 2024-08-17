from tkinter import *
import sqlite3
import tkinter.ttk as ttk
import tkinter.messagebox as tkMessageBox

root = Tk()
root.title("Contact List")
width = 700
height = 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0, 0)
root.config(bg="gray40")

#============================VARIABLES===================================
NAME = StringVar()
SURNAME = StringVar()
EMAIL = StringVar()
POSITION = StringVar()
PHONE = StringVar()
DETAILS = StringVar()

#============================METHODS=====================================
def update_database_schema():
    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()
    # Adaugarea coloanelor noi daca nu exista deja
    try:
        cursor.execute("ALTER TABLE `member` ADD COLUMN `surname` TEXT")
    except sqlite3.OperationalError:
        pass  # Coloana exista deja
    
    try:
        cursor.execute("ALTER TABLE `member` ADD COLUMN `email` TEXT")
    except sqlite3.OperationalError:
        pass
    
    try:
        cursor.execute("ALTER TABLE `member` ADD COLUMN `position` TEXT")
    except sqlite3.OperationalError:
        pass

    try:
        cursor.execute("ALTER TABLE `member` ADD COLUMN `phone` TEXT")
    except sqlite3.OperationalError:
        pass

    try:
        cursor.execute("ALTER TABLE `member` ADD COLUMN `details` TEXT")
    except sqlite3.OperationalError:
        pass

    conn.commit()
    cursor.close()
    conn.close()

update_database_schema()

def Database():
    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS `member` (
            mem_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            surname TEXT,
            email TEXT,
            position TEXT,
            phone TEXT,
            details TEXT
        )
    """)
    cursor.execute("SELECT * FROM `member` ORDER BY `surname` ASC")
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data))
    cursor.close()
    conn.close()


def SubmitData():
    if NAME.get() == "" or SURNAME.get() == "" or EMAIL.get() == "" or POSITION.get() == "" or PHONE.get() == "" or DETAILS.get() == "":
        tkMessageBox.showwarning('', 'Please Complete The Required Field', icon="warning")
    else:
        tree.delete(*tree.get_children())
        conn = sqlite3.connect("contacts.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO `member` (name, surname, email, position, phone, details) VALUES(?, ?, ?, ?, ?, ?)", 
                       (str(NAME.get()), str(SURNAME.get()), str(EMAIL.get()), str(POSITION.get()), str(PHONE.get()), str(DETAILS.get())))
        conn.commit()
        cursor.execute("SELECT * FROM `member` ORDER BY `surname` ASC")
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()
        NAME.set("")
        SURNAME.set("")
        EMAIL.set("")
        POSITION.set("")
        PHONE.set("")
        DETAILS.set("")


def UpdateData():
    if EMAIL.get() == "":
       result = tkMessageBox.showwarning('', 'Please Complete The Required Field', icon="warning")
    else:
        tree.delete(*tree.get_children())
        conn = sqlite3.connect("contacts.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE `member` SET `name` = ?, `surname` = ?, `email` =?, `position` = ?,  `phone` = ?, `details` = ? WHERE `mem_id` = ?", (str(NAME.get()), str(SURNAME.get()), str(EMAIL.get()), str(POSITION.get()), str(PHONE.get()), str(DETAILS.get()), int(mem_id)))
        conn.commit()
        cursor.execute("SELECT * FROM `member` ORDER BY `surname` ASC")
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()
        NAME.set("")
        SURNAME.set("")
        EMAIL.set("")
        POSITION.set("")
        PHONE.set("")
        DETAILS.set("")

def OnSelected(event):
    global mem_id, UpdateWindow
    curItem = tree.focus()
    contents =(tree.item(curItem))
    selecteditem = contents['values']
    mem_id = selecteditem[0]
    NAME.set("")
    SURNAME.set("")
    EMAIL.set("")
    POSITION.set("")
    PHONE.set("")
    DETAILS.set("")
    NAME.set(selecteditem[1])
    SURNAME.set(selecteditem[2])
    EMAIL.set(selecteditem[3])
    POSITION.set(selecteditem[4])
    PHONE.set(selecteditem[5])
    DETAILS.set(selecteditem[6])
    UpdateWindow = Toplevel()
    UpdateWindow.title("Contact List")
    width = 400
    height = 300
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = ((screen_width/2) + 450) - (width/2)
    y = ((screen_height/2) + 20) - (height/2)
    UpdateWindow.resizable(0, 0)
    UpdateWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))
    if 'NewWindow' in globals():
        NewWindow.destroy()

    #===================FRAMES==============================
    FormTitle = Frame(UpdateWindow)
    FormTitle.pack(side=TOP)
    ContactForm = Frame(UpdateWindow)
    ContactForm.pack(side=TOP, pady=10)
    
    #===================LABELS==============================
    lbl_title = Label(FormTitle, text="Updating Contacts", font=('arial', 16), bg="orange",  width = 300)
    lbl_title.pack(fill=X)
    lbl_name = Label(ContactForm, text="Name", font=('arial', 14), bd=5)
    lbl_name.grid(row=0, sticky=W)
    lbl_surname = Label(ContactForm, text="Surname", font=('arial', 14), bd=5)
    lbl_surname.grid(row=1, sticky=W)
    lbl_email = Label(ContactForm, text="Email", font=('arial', 14), bd=5)
    lbl_email.grid(row=2, sticky=W)
    lbl_position = Label(ContactForm, text="Position", font=('arial', 14), bd=5)
    lbl_position.grid(row=3, sticky=W)
    lbl_phone = Label(ContactForm, text="Phone", font=('arial', 14), bd=5)
    lbl_phone.grid(row=4, sticky=W)
    lbl_details = Label(ContactForm, text="Other Details", font=('arial', 14), bd=5)
    lbl_details.grid(row=5, sticky=W)

    #===================ENTRY===============================
    name = Entry(ContactForm, textvariable=NAME, font=('arial', 14))
    name.grid(row=0, column=1)
    surname = Entry(ContactForm, textvariable=SURNAME, font=('arial', 14))
    surname.grid(row=1, column=1)
    email = Entry(ContactForm, textvariable=EMAIL, font=('arial', 14))
    email.grid(row=2, column=1)
    position = Entry(ContactForm, textvariable=POSITION, font=('arial', 14))
    position.grid(row=3, column=1)
    phone = Entry(ContactForm, textvariable=PHONE, font=('arial', 14))
    phone.grid(row=4, column=1)
    details = Entry(ContactForm, textvariable=DETAILS, font=('arial', 14))
    details.grid(row=5, column=1)
    
    #==================BUTTONS==============================
    btn_updatecon = Button(ContactForm, text="Update", width=50, command=UpdateData)
    btn_updatecon.grid(row=6, columnspan=2, pady=10)

def DeleteData():
    if not tree.selection():
       result = tkMessageBox.showwarning('', 'Please Select Something First!', icon="warning")
    else:
        result = tkMessageBox.askquestion('', 'Are you sure you want to delete this record?', icon="warning")
        if result == 'yes':
            curItem = tree.focus()
            contents =(tree.item(curItem))
            selecteditem = contents['values']
            tree.delete(curItem)
            conn = sqlite3.connect("contacts.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM `member` WHERE `mem_id` = %d" % selecteditem[0])
            conn.commit()
            cursor.close()
            conn.close()

def AddNewWindow():
    global NewWindow
    NAME.set("")
    SURNAME.set("")
    EMAIL.set("")
    POSITION.set("")
    PHONE.set("")
    DETAILS.set("")
    NewWindow = Toplevel()
    NewWindow.title("Contact List")
    width = 400
    height = 300
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = ((screen_width/2) - 455) - (width/2)
    y = ((screen_height/2) + 20) - (height/2)
    NewWindow.resizable(0, 0)
    NewWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))
    if 'UpdateWindow' in globals():
        UpdateWindow.destroy()
    
    #===================FRAMES==============================
    FormTitle = Frame(NewWindow)
    FormTitle.pack(side=TOP)
    ContactForm = Frame(NewWindow)
    ContactForm.pack(side=TOP, pady=10)
    
    #===================LABELS==============================
    lbl_title = Label(FormTitle, text="Adding New Contacts", font=('arial', 16), bg="orange",  width = 300)
    lbl_title.pack(fill=X)
    lbl_name = Label(ContactForm, text="Name", font=('arial', 14), bd=5)
    lbl_name.grid(row=0, sticky=W)
    lbl_surname = Label(ContactForm, text="Surname", font=('arial', 14), bd=5)
    lbl_surname.grid(row=1, sticky=W)
    lbl_email = Label(ContactForm, text="Email", font=('arial', 14), bd=5)
    lbl_email.grid(row=2, sticky=W)
    lbl_position = Label(ContactForm, text="Position", font=('arial', 14), bd=5)
    lbl_position.grid(row=3, sticky=W)
    lbl_phone = Label(ContactForm, text="Phone", font=('arial', 14), bd=5)
    lbl_phone.grid(row=4, sticky=W)
    lbl_details = Label(ContactForm, text="Details", font=('arial', 14), bd=5)
    lbl_details.grid(row=5, sticky=W)

    #===================ENTRY===============================
    name = Entry(ContactForm, textvariable=NAME, font=('arial', 14))
    name.grid(row=0, column=1)
    surname = Entry(ContactForm, textvariable=SURNAME, font=('arial', 14))
    surname.grid(row=1, column=1)
    email = Entry(ContactForm, textvariable=EMAIL, font=('arial', 14))
    email.grid(row=2, column=1)
    position = Entry(ContactForm, textvariable=POSITION, font=('arial', 14))
    position.grid(row=3, column=1)
    phone = Entry(ContactForm, textvariable=PHONE, font=('arial', 14))
    phone.grid(row=4, column=1)
    details = Entry(ContactForm, textvariable=DETAILS, font=('arial', 14))
    details.grid(row=5, column=1)

    #==================BUTTONS==============================
    btn_addcon = Button(ContactForm, text="Save", width=50, command=SubmitData)
    btn_addcon.grid(row=6, columnspan=2, pady=10)

#============================FRAMES======================================

Top = Frame(root, width=500, bd=1, relief=SOLID)
Top.pack(side=TOP)
Mid = Frame(root, width=500, bg="gray40")
Mid.pack(side=TOP)
MidLeft = Frame(Mid, width=100)
MidLeft.pack(side=LEFT, pady=10)
MidLeftPadding = Frame(Mid, width=370, bg="gray40")
MidLeftPadding.pack(side=LEFT)
MidRight = Frame(Mid, width=100)
MidRight.pack(side=RIGHT, pady=10)
TableMargin = Frame(root, width=500)
TableMargin.pack(side=TOP)

#============================LABELS======================================
lbl_title = Label(Top, text="Contact Management System", font=('arial', 16), bg="gray",  width=500)
lbl_title.pack(fill=X)

#============================BUTTONS=====================================
btn_add = Button(MidLeft, text="+ ADD NEW", bg="lightgreen", command=AddNewWindow)
btn_add.pack()
btn_delete = Button(MidRight, text="DELETE", bg="red", command=DeleteData)
btn_delete.pack(side=RIGHT)

#============================TABLE=======================================
scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
tree = ttk.Treeview(TableMargin, columns=("MemberID", "Name", "Surname", "Email", "Position", "Phone", "Details"), height=400, selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
scrollbary.config(command=tree.yview)
scrollbary.pack(side=RIGHT, fill=Y)
scrollbarx.config(command=tree.xview)
scrollbarx.pack(side=BOTTOM, fill=X)
tree.heading('MemberID', text="MemberID", anchor=W)
tree.heading('Name', text="Name", anchor=W)
tree.heading('Surname', text="Surname", anchor=W)
tree.heading('Email', text="Email", anchor=W)
tree.heading('Position', text="Position", anchor=W)
tree.heading('Phone', text="Phone", anchor=W)
tree.heading('Details', text="Details", anchor=W)
tree.column('#0', stretch=NO, minwidth=0, width=0)
tree.column('#1', stretch=NO, minwidth=0, width=0)
tree.column('#2', stretch=NO, minwidth=80, width=100)
tree.column('#3', stretch=NO, minwidth=0, width=80)
tree.column('#4', stretch=NO, minwidth=0, width=100)
tree.column('#5', stretch=NO, minwidth=0, width=80)
tree.column('#6', stretch=NO, minwidth=0, width=80)
tree.column('#7', stretch=NO, minwidth=0, width=120)
tree.pack()
tree.bind('<Double-Button-1>', OnSelected)

#============================INITIALIZATION==============================
if __name__ == '__main__':
    Database()
    root.mainloop()
