# programm.py

import tkinter as tk
import gui

def main():
    fenster = tk.Tk()
    fenster.title("Mein EXIF Tool")

    label = tk.Label(fenster, text="Noch kein Bild ausgewählt")
    label.pack(pady=10)

    canvas = tk.Canvas(fenster, width=320, height=300)
    canvas.pack()

    scroll = tk.Scrollbar(fenster, orient="vertical", command=canvas.yview)
    scroll.pack(side="right", fill="y")

    frame = tk.Frame(canvas)
    canvas.create_window((0,0), window=frame, anchor="nw")
    canvas.configure(yscrollcommand=scroll.set)

    def resize(e):
        canvas.configure(scrollregion=canvas.bbox("all"))

    frame.bind("<Configure>", resize)

    btn1 = tk.Button(fenster, text="Ein Bild öffnen", 
                     command=lambda: gui.lade_ein_bild(label, frame))
    btn1.pack(pady=5)

    btn2 = tk.Button(fenster, text="Ordner öffnen",
                     command=lambda: gui.lade_ordner(label, frame))
    btn2.pack(pady=5)

    btn3 = tk.Button(fenster, text="Auswahl als CSV speichern",
                     command=gui.csv_export)
    btn3.pack(pady=10)

    fenster.mainloop()


if __name__ == "__main__":
    main()
