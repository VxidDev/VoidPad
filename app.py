import tkinter as tk
import customtkinter as ctk
import json , pathlib
from tkinter import filedialog

# window setup
window = ctk.CTk()
window.geometry("610x450")
window.resizable(width=False , height=False)
window.title("VoidPad")

# Variables

app_path = pathlib.Path(__file__).resolve().parent

file_selected = None
path_to_file = ctk.StringVar()
text_inputted = None

default_config = {
    "current_theme": "darkblue",
    "themes": {
        "darkblue": {
            "bg_window": "#212e47",
            "bg_button": "#212e60",
            "hover_button": "#212e70",
            "text_color": "#41608a"
        },
        "dark": {
            "bg_window": "#394252",
            "bg_button": "#272d38",
            "hover_button": "#303745",
            "text_color": "#48546e",
        }
    }
}

def redo_config():
    with open(f"{app_path}/theme.json" , "w") as file:
        json.dump(default_config , file)

def load_config():
    try:
        with open(f"{app_path}/theme.json" , "r") as file:
            theme_config = json.load(file)
        return theme_config
    except (FileNotFoundError , json.JSONDecodeError):
        redo_config()
        return default_config 

config = load_config()
current_theme = config["current_theme"]
bg_window = config["themes"][current_theme]["bg_window"]
bg_button = config["themes"][current_theme]["bg_button"]
hover_button = config["themes"][current_theme]["hover_button"]
text_color = config["themes"][current_theme]["text_color"]

window.configure(fg_color=bg_window)

text_area_fontsize = 12
text_editor_frame_x = 53

# frames
text_editor_frame = ctk.CTkFrame(window, width=10 ,  height=5)
text_editor_frame.place(x=0 , y=30)

# commands
def fetch_path():
    global file_selected
    file_selected = getting_path.get()
    try:
        with open(file_selected , "r") as file:
            file.read()
        fetch_info_from_file()
    except (FileNotFoundError , IsADirectoryError) as e:
        print(str(e))

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
    try:
        with open(getting_path.get() , "r") as file:
            for line in file.readlines():
                text_area.insert("end" , line)
    except (IsADirectoryError , FileNotFoundError) as e:
        text_area.insert("1.0" , str(e))

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

def change_theme(currentTheme):
    global current_theme , buttons
    current_theme_index = list(config["themes"].keys()).index(currentTheme) + 1
    try:
        theme = config["themes"][list(config["themes"].keys())[current_theme_index]]
    except IndexError:
        current_theme_index = 0
        theme = config["themes"][list(config["themes"].keys())[current_theme_index]]
    
    current_theme = list(config["themes"].keys())[current_theme_index]
    
    with open(f"{app_path}/theme.json" , "w") as file:
        config["current_theme"] = current_theme
        json.dump(config , file)

    for button in buttons:
        button.button.configure(fg_color=theme["bg_button"] , text_color=theme["text_color"] , hover_color=theme["hover_button"])
    window.configure(fg_color=theme["bg_window"])
    text_area.configure(bg=theme["bg_window"])

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

    text_editor_frame.place(x=text_editor_frame_x , y=30)

def refresh():
    # logic
    if file_selected is None and len(text_area.get("1.0" , "end-1c")) == 0:
        file_name.configure(text="No File Selected.")
    elif len(text_area.get("1.0" , "end-1c")) > 0 and file_selected is None:
        file_name.configure(text="New file.")
    else:
        if len(file_selected) > 70:
            overflow = len(file_selected) - 70
            file_name.configure(text=f"{file_selected[:-overflow]}...")
        else:
            file_name.configure(text=file_selected)

    window.after(1 , refresh)

def undo(text_area):
    try:
        text_area.edit_undo()
    except tk.TclError:
        pass

def redo(text_area):
    try:
        text_area.edit_redo()
    except tk.TclError:
        pass

class Button:
    def __init__(self , text , font=("arial" , 16 , "bold") , size=(75 , 60) , pos=(0 , 0) , fg_color=bg_button , hover_color=hover_button , text_color=text_color , corner_radius=20 , command=lambda: None):
        self.button = ctk.CTkButton(window , text=text , font=font , width=size[0] , height=size[1] , corner_radius=corner_radius , fg_color=fg_color , hover_color=hover_color , text_color=text_color , command=lambda: command())
        self.button.place(x=pos[0] , y=pos[1])
# GUI

open_file = Button(text="Open File" , pos=(495 , 375) , command=lambda: file_selection())

file_name = ctk.CTkLabel(window , text=file_selected , font=("arial" , 20 , "bold") , text_color="white")
file_name.place(x=0 , y=0)

text_area = tk.Text(text_editor_frame , width=53, wrap="word", undo=True, font=("arial", text_area_fontsize , "bold"), fg="white", bg=bg_window, borderwidth = 0 , highlightthickness=0 , insertbackground="white")
text_area.pack(fill="both")

save_button = Button(text="Save" , size=(110 , 55) , pos=(500 , 0), command=lambda: save())

undo_button = Button(text="Undo" , size=(110 , 55) , pos=(500 , 60) , command=lambda: undo(text_area))

redo_button = Button(text="Redo" , size=(110 , 55) , pos=(500 , 120) , command=lambda: redo(text_area))

new_button = Button(text="New" , size=(110 , 55) , pos=(500 , 180), command=lambda: text_area.delete("1.0" , "end"))

themes_button = Button(text="Themes" , size=(110 , 55) , pos=(500 , 240) , command=lambda: change_theme(current_theme))

sliderplus_button = Button(text=">" , size=(40 , 65) , pos=(555 , 300) , command=lambda: slider(side="right"))

sliderminus_button = Button(text="<" , size=(40 , 65), pos=(500 , 300) , command=lambda: slider(side="left"))

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

window.update()

refresh()

window.mainloop()
