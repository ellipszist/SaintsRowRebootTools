import os

from tkinter import ttk, messagebox
from tkinter import StringVar, IntVar, Label
from tkinter import Tk, END, RIDGE
from tkinter import filedialog as fd

from app import main


root = Tk()
root.title("SR Reboot Tool")
root.resizable(False, False)
tab_control = ttk.Notebook(root)

extract_tab = ttk.Frame(tab_control)
patch_tab = ttk.Frame(tab_control)

tab_control.add(extract_tab, text='Extract')
tab_control.add(patch_tab, text='Patch')

tab_control.pack(expand=1, fill="both")

content = ttk.Frame(extract_tab)
content2 = ttk.Frame(patch_tab)

root_dir = os.path.abspath(os.sep)

input_box_value = StringVar()
input_box_patch_value = StringVar()
output_box_value = StringVar()
recursive_enabled = IntVar()
label_value = StringVar()


def apply_patch():
    gamepath = input_box_patch_value.get()
    if not main.validate_gamepath(gamepath):
        messagebox.showerror("Error", "Invalid game path")
        return

    if not main.mod_data_exists(gamepath):
        messagebox.showerror("Error", "No files in mod_data folder to patch")
        return

    if main.is_patched(gamepath):
        if messagebox.askyesno(
            "Apply Patch?",
            "Your game data is already patched. Would you like to \
            overwrite your existing patches with files in mod_data?",
        ):
            main.patch(input_box_patch_value.get())
            update_patched_label()
        return
    else:
        if messagebox.askyesno(
            "Apply Patch?",
            "Patch game files with file in mod_data directory?",
        ):
            main.patch(input_box_patch_value.get())
            update_patched_label()
        return


def remove_patch():
    gamepath = input_box_patch_value.get()
    if not main.validate_gamepath(gamepath):
        messagebox.showerror("Error", "Invalid game path")
        return

    if not main.is_patched(gamepath):
        messagebox.showerror("Error", "No patch is applied")
        return

    if messagebox.askyesno(
            "Remove All Patches?",
            "This returns the game to it's original state"):
        main.unpatch(gamepath)
        update_patched_label()


def open_mod_folder():
    gamepath = input_box_patch_value.get()
    if not main.validate_gamepath(gamepath):
        messagebox.showerror("Error", "Invalid game path")
        return

    main.open_mod_folder(input_box_patch_value.get())


def regen_parent_file():
    gamepath = input_box_patch_value.get()
    if not main.validate_gamepath(gamepath):
        messagebox.showerror("Error", "Invalid game path")
        return

    if messagebox.askyesno(
            "Regenerate parent data",
            "This will reanalyze the file structure of the game (You probably don't need to run this and it takes a long time). Are you sure you want to continue?"):
        main.get_parent_data(gamepath)


def update_patched_label():
    gamepath = input_box_patch_value.get()
    patched = main.is_patched(gamepath)

    if patched:
        label_value.set("Patched: Yes")

    if patched is None:
        label_value.set("Patched: ?")

    if patched is False:
        label_value.set("Patched: No")


def extract_all():
    input_directory = input_box_value.get()
    output_directory = output_box_value.get()
    if messagebox.askyesno(
        "Extract Files?",
        "Are you sure you would like to extract all files from the selected directory? (This may take a while)",
    ):
        main.extract(input_directory, output_directory, recursive_enabled.get())


def select_input_dir_patch():
    initial_dir = root_dir
    if input_box_patch_value.get() != "":
        initial_dir = os.path.normpath(os.path.join(input_box_value.get(), "../"))
    directory = fd.askdirectory(title="Select input directory", initialdir=initial_dir)

    if directory != "":
        # update input box with selected location
        directory = os.path.normpath(directory)
        input_box_patch.delete(0, END)
        input_box_patch.insert(0, directory)
        update_patched_label()


def select_input_dir():
    initial_dir = root_dir
    if input_box_value.get() != "":
        initial_dir = os.path.normpath(os.path.join(input_box_value.get(), "../"))
    directory = fd.askdirectory(title="Select input directory", initialdir=initial_dir)

    if directory != "":
        # update input box with selected location
        directory = os.path.normpath(directory)
        input_box.delete(0, END)
        input_box.insert(0, directory)

        directory = os.path.normpath(os.path.join(directory, "../", "extracted_data"))
        output_box.delete(0, END)
        output_box.insert(0, directory)


def select_output_dir():
    initial_dir = root_dir
    if output_box_value.get() != "":
        initial_dir = os.path.normpath(os.path.join(output_box_value.get(), "../"))
    directory = fd.askdirectory(title="Select output directory", initialdir=initial_dir)
    if directory != "":
        directory = os.path.normpath(directory)
        output_box.delete(0, END)
        output_box.insert(0, directory)


#
# GUI for Extract
#
content.grid(column=0, row=0)


# Buttons
input_button = ttk.Button(content, text="Select Input Directory", command=select_input_dir)
input_button.config(width=22)
input_button.grid(column=3, row=1, padx=(0, 20), pady=(20, 0))

output_button = ttk.Button(content, text="Select Output Directory", command=select_output_dir)
output_button.config(width=22)
output_button.grid(column=3, row=2, padx=(0, 20), pady=(20, 20))

extract_button = ttk.Button(content, text="Extract All", command=extract_all)
extract_button.grid(column=1, columnspan=2, row=3, padx=(0, 20), pady=(20, 20))

# Boxes
input_box = ttk.Entry(content, textvariable=input_box_value)
input_box.config(width=60)
input_box.grid(column=0, row=1, columnspan=3, padx=(20, 20), pady=(20, 0))

output_box = ttk.Entry(content, textvariable=output_box_value)
output_box.config(width=60)
output_box.grid(column=0, row=2, columnspan=3, padx=(20, 20), pady=(20, 20))

# Recursive Checkbox
recursive_box = ttk.Checkbutton(
    content,
    text="Enable Recursive",
    variable=recursive_enabled,
    onvalue=1,
    offvalue=0,
)
recursive_box.state(["!alternate"])
recursive_box.state(["!selected"])
recursive_box.grid(column=0, row=3, padx=(0, 0))

# Set default extraction path
path = os.path.join(root_dir, "Program Files\\Epic Games\\SaintsRow\\sr5\\data")
if os.path.exists(path):
    input_box.delete(0, END)
    input_box.insert(0, path)

    output_path = os.path.normpath(os.path.join(path, "../", "extracted_data"))
    output_box.delete(0, END)
    output_box.insert(0, output_path)


#
# GUI for Patch
#
content2.grid(column=0, row=0)

# Buttons
input_button_patch = ttk.Button(content2, text="Select Game Directory", command=select_input_dir_patch)
input_button_patch.config(width=22)
input_button_patch.grid(column=3, row=1, padx=(0, 20), pady=(20, 0))

mod_folder_button = ttk.Button(content2, text="Open Mod Folder", command=open_mod_folder)
mod_folder_button.grid(column=1, row=3, columnspan=2, ipadx=2, ipady=2, padx=(0, 20), pady=(20, 20))

patch_button = ttk.Button(content2, text="Patch", command=apply_patch)
patch_button.grid(column=0, row=3, columnspan=2, ipadx=2, ipady=2, padx=(0, 0), pady=(20, 20))

unpatch_button = ttk.Button(content2, text="Unpatch", command=remove_patch)
unpatch_button.grid(column=2, row=3, columnspan=2, ipadx=2, ipady=2, padx=(20, 20), pady=(20, 20))

regen_parent_button = ttk.Button(content2, text="Regenerate Parent Data", command=regen_parent_file)
regen_parent_button.grid(column=3, row=2, columnspan=2, ipadx=1, ipady=1, padx=(0, 20), pady=(20, 20))

# Input directory box
input_box_patch = ttk.Entry(content2, textvariable=input_box_patch_value)
input_box_patch.config(width=60)
input_box_patch.grid(column=0, row=1, columnspan=3, padx=(20, 20), pady=(20, 0))

# Patched Yes/No
patched_label = Label(content2, textvariable=label_value, font=('Arial', 14), anchor='w')
patched_label.grid(column=0, row=2, padx=(0, 0), pady=(20, 0))

# Set default directory
path = os.path.join(root_dir, "Program Files\\Epic Games\\SaintsRow\\sr5")
if os.path.exists(path):
    input_box_patch.delete(0, END)
    input_box_patch.insert(0, path)
    update_patched_label()

# run the application
root.mainloop()
