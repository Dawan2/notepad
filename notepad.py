import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog
from tkinter import Menu

def save_note():
    note_content = text.get("1.0", tk.END)
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])

    if file_path:
        try:
            with open(file_path, "w") as file:
                file.write(note_content)
            messagebox.showinfo("Success", "Note saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving note: {e}")

def open_note():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])

    if file_path:
        try:
            with open(file_path, "r") as file:
                note_content = file.read()
                text.delete("1.0", tk.END)
                text.insert(tk.END, note_content)
            update_status_bar(f"Opened: {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Error opening note: {e}")

def create_new_note():
    text.delete("1.0", tk.END)
    update_status_bar("New Note")

def update_word_count():
    content = text.get("1.0", tk.END)
    words = content.split()
    word_count_label.config(text=f"Words: {len(words)}")

def update_status_bar(message):
    status_bar.config(text=message)

def on_close():
    unsaved_changes = len(text.get("1.0", tk.END)) > 1
    if unsaved_changes:
        confirm = messagebox.askyesnocancel("Unsaved Changes", "Do you want to save your changes before exiting?")
        if confirm is None:
            return
        elif confirm:
            save_note()

    root.destroy()

root = tk.Tk()
root.title("Note Pad")

menu = Menu(root)
root.config(menu=menu)

file_menu = Menu(menu, tearoff=0)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=create_new_note, accelerator="Ctrl+N")
file_menu.add_command(label="Open", command=open_note, accelerator="Ctrl+O")
file_menu.add_command(label="Save", command=save_note, accelerator="Ctrl+S")
file_menu.add_separator()
file_menu.add_command(label="Exit", command=on_close, accelerator="Ctrl+Q")

edit_menu = Menu(menu, tearoff=0)
menu.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Word Count", command=update_word_count)

root.bind('<Control-n>', lambda event: create_new_note())
root.bind('<Control-o>', lambda event: open_note())
root.bind('<Control-s>', lambda event: save_note())
root.bind('<Control-q>', lambda event: on_close())

toolbar = tk.Frame(root, bd=1, relief=tk.RAISED)
toolbar.pack(side=tk.TOP, fill=tk.X)

new_button = tk.Button(toolbar, text="New", command=create_new_note)
new_button.pack(side=tk.LEFT, padx=2, pady=2)

open_button = tk.Button(toolbar, text="Open", command=open_note)
open_button.pack(side=tk.LEFT, padx=2, pady=2)

save_button = tk.Button(toolbar, text="Save", command=save_note)
save_button.pack(side=tk.LEFT, padx=2, pady=2)

status_bar = tk.Label(root, text="Welcome to Note Pad", bd=1, relief=tk.SUNKEN, anchor=tk.W)
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

word_count_label = tk.Label(root, text="Words: 0", bd=1, relief=tk.SUNKEN, anchor=tk.W)
word_count_label.pack(side=tk.BOTTOM, fill=tk.X)

text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=10)
text.pack(expand=True, fill='both')

text.bind("<KeyRelease>", lambda event: update_word_count())

root.protocol("WM_DELETE_WINDOW", on_close)

root.mainloop()
