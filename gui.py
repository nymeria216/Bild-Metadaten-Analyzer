import tkinter as tk
from tkinter import filedialog
from main import read_exif_data


def open_image():
    file_path = filedialog.askopenfilename(
        filetypes=[("Images", "*.jpg *.jpeg *.png *.tiff")]
    )

    if not file_path:
        return

    exif_data = read_exif_data(file_path)

    output.delete("1.0", tk.END)

    for key, value in exif_data.items():
        output.insert(tk.END, f"{key}: {value}\n")


window = tk.Tk()

output = tk.Text(window, width=80, height=25)
output.pack()

button = tk.Button(
    window,
    text="Open image",
    command=open_image
)
button.pack()

window.mainloop()
