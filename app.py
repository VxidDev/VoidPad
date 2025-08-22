import tkinter as tk
from tkinter import filedialog

# window setup
window = tk.Tk()
window.geometry("600x400")
window.resizable(width=False , height=False)
window.title("VoidPad")

window.config(bg="#212e47")

# Variables
file_selected = None
path_to_file = tk.StringVar()
text_inputted = None

theme = "darkblue"
bg_window = "#212e47"
bg_button = "#212e60"
activebg_button = "#212e70"
fg_button = "#41608a"
activefg_button = "4c70b5"

# frames
text_editor_frame = tk.Frame(window, width=10 ,  height=5 , border = 0)
text_editor_frame.place(x=0 , y=20)

# commands
def fetch_path():
    global file_selected
    file_selected = getting_path.get()
    try:
        with open(file_selected , "r") as file:
            file.read()
        fetch_info_from_file()
    except FileNotFoundError:
        print("File Not Found!")

def choose_file():
    global file_selected
    file_path = filedialog.askopenfilename(
        initialdir="/",
        title="Select a File",
        filetypes=(("Text files", "*.txt*"), ("All files", "*.*"))
    )
    if file_path:  # only set if user actually selected something
        path_to_file.set(file_path)
        file_selected = path_to_file.get()
        fetch_info_from_file()

def fetch_info_from_file():
    text_area.delete("1.0" , "end")
    with open(getting_path.get() , "r") as file:
        for line in file.readlines():
            text_area.insert("end" , line)

def file_selection():
    global getting_path
    file_selection = tk.Toplevel()
    file_selection.geometry("200x60")
    file_selection.resizable(width=False , height=False)

    getting_path = tk.Entry(master=file_selection , textvariable=path_to_file , width=20 , font=("arial" , 15 , "bold"))
    getting_path.pack()

    submit = tk.Button(master=file_selection , text="Submit" , font=("arial" , 10 , "bold") , command=lambda: fetch_path())
    submit.place(x=15 , y=30)

    choose_from_explorer = tk.Button(master=file_selection , text="Open Explorer" , font=("Arial" , 10 , "bold") , command=lambda: choose_file())
    choose_from_explorer.place(x=80 , y=30)

def save():
    if file_selected != None:
        with open(file_selected , "w") as file:
            file.write(text_area.get("1.0" , "end-1c"))
    else:
        save_path = filedialog.asksaveasfilename(
        initialdir="/",
        title="Save file as",
        filetypes=(("Text files","*.txt"), ("All files","*.*")),
        defaultextension=".txt",
        confirmoverwrite=True          # prompt if file exists
)
        with open(save_path , "w") as file:
            file.write(text_area.get("1.0" , "end-1c"))

def change_theme():
    global theme 
    if theme == "darkblue":
        bg_window = "#394252"
        bg_button = "#272d38"
        activebg_button = "#303745"
        fg_button = "#3b4654"
        activefg_button = "#48546e"
        theme = "dark"
    else:
        bg_window = "#212e47"
        bg_button = "#212e60"
        activebg_button = "#212e70"
        fg_button = "#41608a"
        activefg_button = "#4c70b5"
        theme = "darkblue"

    themes_button.config(bg=bg_button , activebackground=activebg_button , fg=fg_button , activeforeground=activefg_button)
    new_button.config(bg=bg_button , activebackground=activebg_button , fg=fg_button , activeforeground=activefg_button)
    redo_button.config(bg=bg_button , activebackground=activebg_button , fg=fg_button , activeforeground=activefg_button)
    undo_button.config(bg=bg_button , activebackground=activebg_button , fg=fg_button , activeforeground=activefg_button)
    save_button.config(bg=bg_button , activebackground=activebg_button , fg=fg_button , activeforeground=activefg_button)
    open_file.config(bg=bg_button , activebackground=activebg_button , fg=fg_button , activeforeground=activefg_button)
    window.config(bg=bg_window)
    text_area.config(bg=bg_window)
    file_name.config(bg=bg_window)

def refresh():
    # logic
    if file_selected is None and len(text_area.get("1.0" , "end-1c")) == 0:
        file_name.config(text="No File Selected.")
    elif len(text_area.get("1.0" , "end-1c")) > 0 and file_selected is None:
        file_name.config(text="New file.")
    if file_selected != None:
        if len(file_selected) > 70:
            overflow = len(file_selected) - 70
            file_name.config(text=f"{file_selected[:-overflow]}...")
        else:
            file_name.config(text=file_selected)

    window.after(1 , refresh)

# GUI

open_file = tk.Button(text="Open File" , font=("Arial" , 10 , "bold") , width=10 , height=3 , bg="#212e60" , activebackground="#212e70" , fg="#41608a" , activeforeground="#4c70b5", highlightthickness=0 , border=0 , command=lambda: file_selection())
open_file.place(x=500 , y=340)

file_name = tk.Label(text=file_selected , font=("arial" , 10 , "bold") , fg="white" , bg="#212e47")
file_name.place(x=0 , y=0)

text_area = tk.Text(text_editor_frame , width=53, wrap="word", undo=True, font=("arial", 12 , "bold"), fg="white", bg="#212e47" , borderwidth = 0 , highlightthickness=0 , insertbackground="white")
text_area.pack(fill="both")

save_button = tk.Button(text="Save" , font=("arial" , 10 , "bold") , width=10 , height=3 , bg="#212e60" , activebackground="#212e70" , fg="#41608a" , activeforeground="#4c70b5" , highlightthickness=0 , border=0 , command=lambda: save())
save_button.place(x=500 , y=0)

undo_button = tk.Button(text="Undo" , font=("arial" , 10 , "bold") , width=10 , height=3 , bg="#212e60" , activebackground="#212e70" , fg="#41608a" , activeforeground="#4c70b5" , highlightthickness=0 , border=0 , command=lambda: text_area.edit_undo())
undo_button.place(x=500 , y=60)

redo_button = tk.Button(text="Redo" , font=("arial" , 10 , "bold") , width=10 , height=3 , bg="#212e60" , activebackground="#212e70" , fg="#41608a" , activeforeground="#4c70b5" , highlightthickness=0 , border=0 , command=lambda: text_area.edit_redo())
redo_button.place(x=500 , y=120)

new_button = tk.Button(text="New" , font=("arial" , 10 , "bold") , width=10 , height=3 , bg="#212e60" ,activebackground="#212e70" , fg="#41608a" , activeforeground="#4c70b5" , highlightthickness=0 , border=0 , command=lambda: text_area.delete("1.0" , "end"))
new_button.place(x=500 , y=180)

themes_button = tk.Button(text="Themes" , font=("arial" , 10 , "bold") , width=10 , height=3 , bg=bg_button , activebackground="#212e70" , fg="#41608a" , activeforeground="#4c70b5" , highlightthickness=0 , border=0 , command=lambda: change_theme())
themes_button.place(x=500 , y=240)

refresh()

window.mainloop()
