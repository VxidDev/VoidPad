import tkinter as tk
from tkinter import filedialog

# window setup
window = tk.Tk()
window.geometry("600x450")
window.resizable(width=False , height=False)
window.title("VoidPad")

# Variables
file_selected = None
path_to_file = tk.StringVar()
text_inputted = None


theme_config = []
with open("theme.conf" , "r") as file:
    for line in file.readlines():
        theme_config.append(line.split()[0])
    print("Done.")    

theme = theme_config[0]
bg_window = theme_config[1]
bg_button = theme_config[2]
activebg_button = theme_config[3]
fg_button = theme_config[4]
activefg_button = theme_config[5]

window.config(bg=bg_window)

text_area_fontsize = 12
text_editor_frame_x = 53

# frames
text_editor_frame = tk.Frame(window, width=10 ,  height=5 , border = 0)
text_editor_frame.place(x=0 , y=30)

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
    with open("theme.conf" , "w") as file:
        file.write(f"{theme} # theme\n{bg_window} # bg_window\n{bg_button} # bg_button\n{activebg_button} # activebg_button\n{fg_button} # fg_button\n{activefg_button} # activefg_button")
    for button in buttons:
        button.config(bg=bg_button , activebackground=activebg_button , fg=fg_button , activeforeground=activefg_button)
    window.config(bg=bg_window)
    text_area.config(bg=bg_window)
    file_name.config(bg=bg_window)

def font_change(event=None , action=None):
    global text_area_fontsize
    if action == "plus":
        if text_area_fontsize < 25:
            text_area_fontsize += 1
    else:
        if text_area_fontsize > 12:
            text_area_fontsize -= 1

    text_area.config(font=("arial" , text_area_fontsize , "bold"))

def slider(event=None , side=None):
    global text_editor_frame_x
    if side == "right":
        if text_editor_frame_x > -525:
            text_editor_frame_x -= 25
    else:
        if text_editor_frame_x < 0:
            text_editor_frame_x += 25

    text_editor_frame.place(x=text_editor_frame_x , y=80)

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

open_file = tk.Button(text="Open File" , font=("Arial" , 10 , "bold") , width=10 , height=3 , bg=bg_button , activebackground=activebg_button , fg=fg_button , activeforeground=activefg_button, highlightthickness=0 , border=0 , command=lambda: file_selection())
open_file.place(x=500 , y=385)

file_name = tk.Label(text=file_selected , font=("arial" , 10 , "bold") , fg="white" , bg=bg_window)
file_name.place(x=0 , y=0)

text_area = tk.Text(text_editor_frame , width=53, wrap="word", undo=True, font=("arial", text_area_fontsize , "bold"), fg="white", bg=bg_window, borderwidth = 0 , highlightthickness=0 , insertbackground="white")
text_area.pack(fill="both")

save_button = tk.Button(text="Save" , font=("arial" , 10 , "bold") , width=10 , height=3 , bg=bg_button , activebackground=activebg_button , fg=fg_button , activeforeground=activefg_button , highlightthickness=0 , border=0 , command=lambda: save())
save_button.place(x=500 , y=0)

undo_button = tk.Button(text="Undo" , font=("arial" , 10 , "bold") , width=10 , height=3 , bg=bg_button , activebackground=activebg_button , fg=fg_button , activeforeground=activefg_button , highlightthickness=0 , border=0 , command=lambda: text_area.edit_undo())
undo_button.place(x=500 , y=60)

redo_button = tk.Button(text="Redo" , font=("arial" , 10 , "bold") , width=10 , height=3 , bg=bg_button , activebackground=activebg_button , fg=fg_button , activeforeground=activefg_button , highlightthickness=0 , border=0 , command=lambda: text_area.edit_redo())
redo_button.place(x=500 , y=120)

new_button = tk.Button(text="New" , font=("arial" , 10 , "bold") , width=10 , height=3 , bg=bg_button ,activebackground=activebg_button , fg=fg_button , activeforeground=activefg_button , highlightthickness=0 , border=0 , command=lambda: text_area.delete("1.0" , "end"))
new_button.place(x=500 , y=180)

themes_button = tk.Button(text="Themes" , font=("arial" , 10 , "bold") , width=10 , height=4 , bg=bg_button , activebackground=activebg_button , fg=fg_button , activeforeground=activefg_button , highlightthickness=0 , border=0 , command=lambda: change_theme())
themes_button.place(x=500 , y=240)

sliderplus_button = tk.Button(text="->" , font=("arial" , 10 , "bold") , width=3 , height=3 , bg=bg_button , activebackground=activebg_button , fg=fg_button , activeforeground=activefg_button , highlightthickness=0 , border=0 , command=lambda: slider(side="right"))
sliderplus_button.place(x=550 , y=320)

sliderminus_button = tk.Button(text="<-" , font=("arial" , 10 , "bold") , width=3 , height=3 , bg=bg_button , activebackground=activebg_button , fg=fg_button , activeforeground=activefg_button , highlightthickness=0 , border=0 , command=lambda: slider(side="left"))
sliderminus_button.place(x=500 , y=320)

# shortcuts
text_area.bind("<Control-plus>", lambda e: font_change(e, action="plus"))
text_area.bind("<Control-minus>", lambda e: font_change(e , action="minus"))

text_area.bind("<Control-Right>", lambda e: slider(e , side="right"))
text_area.bind("<Control-Left>" , lambda e: slider(e , side="left"))

# button list
buttons = [
    open_file,
    save_button,
    undo_button,
    redo_button,
    new_button,
    themes_button,
    sliderplus_button,
    sliderminus_button
]

refresh()

window.mainloop()
