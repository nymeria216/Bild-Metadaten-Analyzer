# gui.py

import tkinter as tk
from tkinter import messagebox, filedialog

import bilder
import lesen
import speichern

ausgewaehlte_bilder = []
checkboxen = {}

def lade_ein_bild(label, frame):
    global ausgewaehlte_bilder

    pfad = bilder.bild_auswaehlen()
    if pfad is None:
        return

    ausgewaehlte_bilder = [pfad]
    label.config(text=pfad)

    zeige_exif(pfad, frame)


def lade_ordner(label, frame):
    global ausgewaehlte_bilder

    liste = bilder.ordner_auswaehlen()
    if len(liste) == 0:
        return

    ausgewaehlte_bilder = liste
    label.config(text=f"{len(liste)} Bilder ausgewählt")

    # EXIF vom ersten Bild für Checkboxen
    zeige_exif(liste[0], frame)


def zeige_exif(beispiel_bild, frame):
    global checkboxen

    for w in frame.winfo_children():
        w.destroy()

    checkboxen = {}

    daten = lesen.hole_exif(beispiel_bild)

    for tag in daten:
        var = tk.BooleanVar()
        cb = tk.Checkbutton(frame, text=tag, variable=var)
        cb.pack(anchor="w")
        checkboxen[tag] = var


def csv_export():
    global ausgewaehlte_bilder

    auswahl = []

    for tag, var in checkboxen.items():
        if var.get():
            auswahl.append(tag)

    if len(auswahl) == 0:
        messagebox.showwarning("Fehler", "Keine EXIF-Felder gewählt.")
        return

    pfad = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV Datei", "*.csv")]
    )

    if pfad == "":
        return

    speichern.speichere_csv(ausgewaehlte_bilder, auswahl, pfad)

    messagebox.showinfo("OK", "CSV gespeichert!")
