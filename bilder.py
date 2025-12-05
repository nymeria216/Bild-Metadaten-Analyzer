# bilder.py
import os
from tkinter import filedialog, messagebox

def bild_auswaehlen():
    pfad = filedialog.askopenfilename(
        title="Bild wählen",
        filetypes=[("JPG Bilder", "*.jpg *.jpeg")]
    )

    if pfad == "":
        return None

    return pfad


def ordner_auswaehlen():
    ordner = filedialog.askdirectory(title="Ordner wählen")

    if ordner == "":
        return []

    bilder = []
    for d in os.listdir(ordner):
        if d.lower().endswith(".jpg") or d.lower().endswith(".jpeg"):
            bilder.append(os.path.join(ordner, d))

    if len(bilder) == 0:
        messagebox.showinfo("Hinweis", "Keine JPG-Bilder gefunden.")

    return bilder
