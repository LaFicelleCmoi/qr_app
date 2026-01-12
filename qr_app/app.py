import tkinter as tk
from tkinter import filedialog, messagebox
from qr_generator import generate_qr


def center_window(window: tk.Tk, width: int, height: int) -> None:
    """
    Centre la fenêtre à l'écran.
    """
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    window.geometry(f"{width}x{height}+{x}+{y}")


def generate():
    data = entry.get().strip()

    if not data:
        messagebox.showerror("Erreur", "Le champ est vide")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("Image PNG", "*.png")]
    )

    if file_path:
        generate_qr(data, file_path)
        messagebox.showinfo("Succès", "QR Code généré avec succès")


# --- Fenêtre principale ---
root = tk.Tk()
root.title("Générateur de QR Code")
root.resizable(False, False)

# Taille moyenne + centrage
WINDOW_WIDTH = 460
WINDOW_HEIGHT = 220
center_window(root, WINDOW_WIDTH, WINDOW_HEIGHT)

# --- Interface ---
tk.Label(
    root,
    text="Contenu du QR Code :",
    font=("Arial", 11)
).pack(pady=15)

entry = tk.Entry(root, width=50)
entry.pack()

tk.Button(
    root,
    text="Générer le QR Code",
    width=25,
    command=generate
).pack(pady=25)

root.mainloop()
