import os
import shutil
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox

# File type definitions
FILE_TYPES = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
    'Videos': ['.mp4', '.mkv', '.flv', '.avi', '.mov'],
    'Documents': ['.pdf', '.docx', '.doc', '.txt', '.xls', '.xlsx', '.pptx'],
    'Music': ['.mp3', '.wav', '.aac', '.flac'],
    'Archives': ['.zip', '.rar', '.tar', '.gz'],
    'Scripts': ['.py', '.js', '.html', '.css', '.php', '.java'],
    'Others': []
}

LOG_FILE = "log.txt"


def get_category(extension):
    for category, extensions in FILE_TYPES.items():
        if extension.lower() in extensions:
            return category
    return 'Others'


def get_unique_path(path):
    base, ext = os.path.splitext(path)
    counter = 1
    while os.path.exists(path):
        path = f"{base}({counter}){ext}"
        counter += 1
    return path


def organize_folder(folder_path, status_label, summary_label):
    if not os.path.exists(folder_path):
        messagebox.showerror("Error", "Folder does not exist.")
        return

    summary = {}

    with open(LOG_FILE, "w") as log:
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path):
                _, ext = os.path.splitext(file)
                category = get_category(ext)
                summary[category] = summary.get(category, 0) + 1
                category_path = os.path.join(folder_path, category)
                if not os.path.exists(category_path):
                    os.mkdir(category_path)
                new_path = os.path.join(category_path, file)
                new_path = get_unique_path(new_path)
                shutil.move(file_path, new_path)
                log.write(f"{new_path}|{file_path}\n")

    summary_str = "📊 Summary: " + \
        ", ".join([f"{cat}: {count}" for cat, count in summary.items()])
    summary_label.config(text=summary_str, bootstyle=INFO)
    status_label.config(text="✅ Folder organized!", bootstyle=SUCCESS)


def undo_organization(status_label):
    if not os.path.exists(LOG_FILE):
        messagebox.showerror("Error", "No log file found. Cannot undo.")
        return

    with open(LOG_FILE, "r") as log:
        lines = log.readlines()

    for line in reversed(lines):
        new_path, original_path = line.strip().split('|')
        if os.path.exists(new_path):
            restored_path = get_unique_path(original_path)
            shutil.move(new_path, restored_path)

    status_label.config(text="🔄 Undo complete.", bootstyle=WARNING)

# GUI Setup


def launch_gui():
    app = ttk.Window(themename="flatly")
    app.title("📁 File Organizer")
    app.geometry("520x300")
    app.resizable(False, False)

    # ✅ Set custom icon (make sure icon.ico exists in the same directory)
    try:
        app.iconbitmap("icon.ico")
    except Exception as e:
        print(f"Error loading icon: {e}")

    # --- Theme Switch (Top Right Corner) ---
    theme_var = ttk.BooleanVar(value=False)

    def switch_theme():
        app.style.theme_use("darkly" if theme_var.get() else "flatly")

    theme_switch = ttk.Checkbutton(
        app,
        text="Dark Mode",
        variable=theme_var,
        command=switch_theme,
        bootstyle="switch"
    )
    theme_switch.place(x=390, y=10)

    # --- Status & Summary ---
    status_label = ttk.Label(app, text="", font=("Helvetica", 10))
    status_label.pack(pady=(40, 5))

    summary_label = ttk.Label(app, text="", font=("Helvetica", 9))
    summary_label.pack()

    # --- Folder Selection ---
    selected_folder = ttk.StringVar(value="")

    def choose_folder():
        folder = filedialog.askdirectory()
        if folder:
            selected_folder.set(f"📂 Selected: {folder}")
            organize_folder(folder, status_label, summary_label)

    ttk.Button(app, text="🗂 Choose Folder & Organize",
               command=choose_folder, bootstyle=PRIMARY).pack(pady=10)

    folder_label = ttk.Label(
        app, textvariable=selected_folder, font=("Helvetica", 9))
    folder_label.pack()

    # --- Undo Button ---
    ttk.Button(app, text="↩ Undo", width=15, command=lambda: undo_organization(
        status_label), bootstyle=WARNING).pack(pady=50)

    app.mainloop()


if __name__ == "__main__":
    launch_gui()
    