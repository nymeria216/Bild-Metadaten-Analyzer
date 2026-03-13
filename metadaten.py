import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path

from reader import bild_metadaten_auslesen
from export import als_csv_exportieren, als_json_exportieren

aktuelle_metadaten = None
aktueller_dateipfad = None


# Prüft, ob die ausgewählte Datei ein unterstütztes Bildformat hat
def datei_wird_unterstuetzt(dateipfad):
    dateipfad = dateipfad.lower()

    if dateipfad.endswith(".jpg"):
        return True
    if dateipfad.endswith(".jpeg"):
        return True
    if dateipfad.endswith(".png"):
        return True
    if dateipfad.endswith(".tif"):
        return True
    if dateipfad.endswith(".tiff"):
        return True

    return False


# Formatiert die Metadaten so, dass sie im Textfeld angezeigt werden können
def metadaten_text_formatieren(metadaten):
    text = ""
    text += "Datei: " + str(metadaten["datei"]) + "\n"
    text += "Bildgröße: " + str(metadaten["groesse"]) + "\n"
    text += "\n"

    if metadaten["has_exif"] is False:
        text += "Keine EXIF-Daten vorhanden."
        return text

    text += "EXIF-Daten:\n\n"

    for schluessel in metadaten["exif"]:
        text += str(schluessel) + ": " + str(metadaten["exif"][schluessel]) + "\n"

    return text


# Gibt den Pfad zum Downloads-Ordner zurück
def downloads_ordner_ermitteln():
    return Path.home() / "Downloads"


# Erstellt automatisch den Dateinamen für den Export
def ausgabe_dateipfad_ermitteln(endung):
    global aktueller_dateipfad

    if aktueller_dateipfad is None:
        return None

    original_name = Path(aktueller_dateipfad).stem
    dateiname = original_name + "_Metadata_Auswertung" + endung

    return downloads_ordner_ermitteln() / dateiname


# Öffnet eine Bilddatei und liest die Metadaten aus
def bild_oeffnen(text_feld):
    global aktuelle_metadaten
    global aktueller_dateipfad

    dateipfad = filedialog.askopenfilename(
        title="Bild auswählen",
        filetypes=[
            ("Bilddateien", "*.jpg *.jpeg *.png *.tif *.tiff"),
            ("Alle Dateien", "*.*")
        ]
    )

    if dateipfad == "":
        return

    if not datei_wird_unterstuetzt(dateipfad):
        messagebox.showerror("Fehler", "Dateiformat wird nicht unterstützt.")
        return

    try:
        aktueller_dateipfad = dateipfad
        aktuelle_metadaten = bild_metadaten_auslesen(dateipfad)

        text_feld.delete("1.0", tk.END)
        text_feld.insert(tk.END, metadaten_text_formatieren(aktuelle_metadaten))

        if aktuelle_metadaten["has_exif"] is False:
            messagebox.showinfo("Hinweis", "Keine EXIF-Daten vorhanden.")
    except Exception as fehler:
        messagebox.showerror("Fehler", "Datei konnte nicht gelesen werden.\n" + str(fehler))


# Speichert die Metadaten als CSV-Datei im Downloads-Ordner
def csv_speichern():
    global aktuelle_metadaten

    if aktuelle_metadaten is None:
        messagebox.showwarning("Hinweis", "Bitte zuerst ein Bild auswählen.")
        return

    ausgabe_pfad = ausgabe_dateipfad_ermitteln(".csv")

    try:
        als_csv_exportieren(aktuelle_metadaten, ausgabe_pfad)
        messagebox.showinfo(
            "Erfolg",
            "CSV-Datei wurde gespeichert:\n" + str(ausgabe_pfad)
        )
    except Exception as fehler:
        messagebox.showerror("Fehler", "CSV konnte nicht gespeichert werden.\n" + str(fehler))


# Speichert die Metadaten als JSON-Datei im Downloads-Ordner
def json_speichern():
    global aktuelle_metadaten

    if aktuelle_metadaten is None:
        messagebox.showwarning("Hinweis", "Bitte zuerst ein Bild auswählen.")
        return

    ausgabe_pfad = ausgabe_dateipfad_ermitteln(".json")

    try:
        als_json_exportieren(aktuelle_metadaten, ausgabe_pfad)
        messagebox.showinfo(
            "Erfolg",
            "JSON-Datei wurde gespeichert:\n" + str(ausgabe_pfad)
        )
    except Exception as fehler:
        messagebox.showerror("Fehler", "JSON konnte nicht gespeichert werden.\n" + str(fehler))


# Startet die grafische Oberfläche
def starte_app():
    root = tk.Tk()
    root.title("Analyse Tool von Bild-Metadaten")
    root.geometry("700x500")

    ueberschrift_label = tk.Label(
        root,
        text="Analyse Tool von Bild-Metadaten",
        font=("Arial", 14, "bold")
    )
    ueberschrift_label.pack(pady=10)

    button_frame = tk.Frame(root)
    button_frame.pack(pady=5)

    text_feld = tk.Text(root, wrap="word")
    text_feld.pack(fill="both", expand=True, padx=10, pady=10)

    bild_button = tk.Button(
        button_frame,
        text="Bild auswählen",
        command=lambda: bild_oeffnen(text_feld),
        width=18
    )
    bild_button.grid(row=0, column=0, padx=5)

    csv_button = tk.Button(
        button_frame,
        text="Als CSV speichern",
        command=csv_speichern,
        width=18
    )
    csv_button.grid(row=0, column=1, padx=5)

    json_button = tk.Button(
        button_frame,
        text="Als JSON speichern",
        command=json_speichern,
        width=18
    )
    json_button.grid(row=0, column=2, padx=5)

    root.mainloop()