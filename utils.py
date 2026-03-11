import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path

from reader import read_image_metadata
from export import export_to_csv, export_to_json


current_metadata = None
current_file_path = None


def is_supported_file(file_path):
    file_path = file_path.lower()

    if file_path.endswith(".jpg"):
        return True
    if file_path.endswith(".jpeg"):
        return True
    if file_path.endswith(".png"):
        return True
    if file_path.endswith(".tif"):
        return True
    if file_path.endswith(".tiff"):
        return True

    return False


def format_metadata_text(metadata):
    text = ""
    text += "Datei: " + str(metadata["datei"]) + "\n"
    text += "Format: " + str(metadata["format"]) + "\n"
    text += "Bildgröße: " + str(metadata["groesse"]) + "\n"
    text += "\n"

    if metadata["has_exif"] is False:
        text += "Keine EXIF-Daten vorhanden."
        return text

    text += "EXIF-Daten:\n\n"

    for key in metadata["exif"]:
        text += str(key) + ": " + str(metadata["exif"][key]) + "\n"

    return text


def get_downloads_path():
    return Path.home() / "Downloads"


def get_output_file_path(extension):
    global current_file_path

    if current_file_path is None:
        return None

    original_name = Path(current_file_path).stem
    file_name = original_name + "_Metadata_Auswertung" + extension

    return get_downloads_path() / file_name


def open_file(text_box):
    global current_metadata
    global current_file_path

    file_path = filedialog.askopenfilename(
        title="Bild auswählen",
        filetypes=[
            ("Bilddateien", "*.jpg *.jpeg *.png *.tif *.tiff"),
            ("Alle Dateien", "*.*")
        ]
    )

    if file_path == "":
        return

    if not is_supported_file(file_path):
        messagebox.showerror("Fehler", "Dateiformat wird nicht unterstützt.")
        return

    try:
        current_file_path = file_path
        current_metadata = read_image_metadata(file_path)

        text_box.delete("1.0", tk.END)
        text_box.insert(tk.END, format_metadata_text(current_metadata))

        if current_metadata["has_exif"] is False:
            messagebox.showinfo("Hinweis", "Keine EXIF-Daten vorhanden.")
    except Exception as e:
        messagebox.showerror("Fehler", "Datei konnte nicht gelesen werden.\n" + str(e))


def save_csv():
    global current_metadata

    if current_metadata is None:
        messagebox.showwarning("Hinweis", "Bitte zuerst ein Bild auswählen.")
        return

    output_path = get_output_file_path(".csv")

    try:
        export_to_csv(current_metadata, output_path)
        messagebox.showinfo(
            "Erfolg",
            "CSV-Datei wurde gespeichert:\n" + str(output_path)
        )
    except Exception as e:
        messagebox.showerror("Fehler", "CSV konnte nicht gespeichert werden.\n" + str(e))


def save_json():
    global current_metadata

    if current_metadata is None:
        messagebox.showwarning("Hinweis", "Bitte zuerst ein Bild auswählen.")
        return

    output_path = get_output_file_path(".json")

    try:
        export_to_json(current_metadata, output_path)
        messagebox.showinfo(
            "Erfolg",
            "JSON-Datei wurde gespeichert:\n" + str(output_path)
        )
    except Exception as e:
        messagebox.showerror("Fehler", "JSON konnte nicht gespeichert werden.\n" + str(e))


def start_app():
    root = tk.Tk()
    root.title("Analyse Tool von Bild-Metadaten")
    root.geometry("700x500")

    title_label = tk.Label(
        root,
        text="Analyse Tool von Bild-Metadaten",
        font=("Arial", 14, "bold")
    )
    title_label.pack(pady=10)

    button_frame = tk.Frame(root)
    button_frame.pack(pady=5)

    text_box = tk.Text(root, wrap="word")
    text_box.pack(fill="both", expand=True, padx=10, pady=10)

    open_button = tk.Button(
        button_frame,
        text="Bild auswählen",
        command=lambda: open_file(text_box),
        width=18
    )
    open_button.grid(row=0, column=0, padx=5)

    csv_button = tk.Button(
        button_frame,
        text="Als CSV speichern",
        command=save_csv,
        width=18
    )
    csv_button.grid(row=0, column=1, padx=5)

    json_button = tk.Button(
        button_frame,
        text="Als JSON speichern",
        command=save_json,
        width=18
    )
    json_button.grid(row=0, column=2, padx=5)

    root.mainloop()