import tkinter as tk
from tkinter import filedialog, messagebox
from qr_generator import generate_qr
import os
import re
from urllib.parse import urlparse
import unicodedata


def center_large_window(root, width_ratio=0.6, height_ratio=0.6):
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()

    width = int(screen_w * width_ratio)
    height = int(screen_h * height_ratio)

    x = (screen_w - width) // 2
    y = (screen_h - height) // 2

    root.geometry(f"{width}x{height}+{x}+{y}")


def sanitize_filename(filename, max_length=50):
    """
    Nettoie une chaîne pour en faire un nom de fichier valide.
    Supprime les caractères spéciaux et limite la longueur.
    """
    # Remplacer les caractères spéciaux par des underscores
    filename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore').decode('ASCII')
    filename = re.sub(r'[^\w\s-]', '', filename)
    filename = re.sub(r'[-\s]+', '_', filename)
    
    # Limiter la longueur
    if len(filename) > max_length:
        # Garder le début et la fin du nom
        half = max_length // 2
        filename = filename[:half-3] + "..." + filename[-half+3:]
    
    return filename.strip('_').lower()


def extract_domain(url):
    """Extrait le domaine d'une URL pour le nom de fichier."""
    try:
        parsed = urlparse(url)
        domain = parsed.netloc
        if not domain and parsed.path:
            # Si pas de domaine (URL courte), prendre le chemin
            domain = parsed.path.split('/')[0] if parsed.path else "url"
        
        # Supprimer www. et protocol
        domain = domain.replace('www.', '').replace('http://', '').replace('https://', '')
        
        # Prendre seulement la première partie du domaine (avant le premier point)
        domain_parts = domain.split('.')
        if domain_parts and len(domain_parts[0]) > 0:
            return domain_parts[0]
        else:
            return "qr"
    except:
        return "qr"


def generate_filename_from_url(url, folder, index=None):
    """Génère un nom de fichier unique basé sur l'URL."""
    # Extraire le domaine pour le nom de base
    base_name = extract_domain(url)
    
    # Ajouter un extrait du chemin si disponible
    try:
        parsed = urlparse(url)
        if parsed.path and len(parsed.path) > 1:
            path_parts = [p for p in parsed.path.split('/') if p]
            if path_parts:
                # Prendre le dernier segment significatif du chemin
                last_part = path_parts[-1]
                if len(last_part) > 3 and '.' not in last_part:  # Éviter les extensions
                    base_name += "_" + sanitize_filename(last_part[:20])
    except:
        pass
    
    # Si le nom est trop court ou générique, ajouter un index
    if len(base_name) < 3:
        base_name = "qr"
        if index:
            base_name += f"_{index}"
    
    # Nettoyer le nom
    base_name = sanitize_filename(base_name)
    
    # Vérifier si le fichier existe déjà et ajouter un numéro si nécessaire
    filename = base_name + ".png"
    counter = 1
    filepath = os.path.join(folder, filename)
    
    while os.path.exists(filepath):
        filename = f"{base_name}_{counter}.png"
        filepath = os.path.join(folder, filename)
        counter += 1
    
    return filename


def generate():
    raw_data = text.get("1.0", tk.END).strip()

    if not raw_data:
        messagebox.showerror("Erreur", "Veuillez entrer au moins une URL")
        return

    # Une URL par ligne
    urls = [line.strip() for line in raw_data.splitlines() if line.strip()]
    
    # Récupérer le mode sélectionné
    mode = mode_var.get()
    
    if mode == "single":
        if len(urls) > 1:
            # Demander si l'utilisateur veut concaténer ou prendre seulement la première URL
            response = messagebox.askyesno(
                "Choix du mode",
                "Vous avez saisi plusieurs URLs en mode 'Un seul QR Code'.\n\n"
                "Souhaitez-vous :\n"
                "• Oui : Créer un QR code avec toutes les URLs concaténées\n"
                "• Non : Créer un QR code avec seulement la première URL"
            )
            
            if response:  # Oui = concaténer toutes les URLs
                data = "\n".join(urls)
                # Générer un nom basé sur la première URL
                default_name = extract_domain(urls[0]) + "_combined.png"
            else:  # Non = prendre seulement la première URL
                data = urls[0]
                default_name = generate_filename_from_url(urls[0], "", index=1).replace(".png", "")
        
        else:
            data = urls[0]
            default_name = generate_filename_from_url(urls[0], "", index=1).replace(".png", "")
        
        # Nettoyer le nom de fichier
        default_name = sanitize_filename(default_name)
        
        # Demander où sauvegarder le fichier
        file_path = filedialog.asksaveasfilename(
            title="Enregistrer le QR Code",
            defaultextension=".png",
            initialfile=default_name,
            filetypes=[("Fichiers PNG", "*.png"), ("Tous les fichiers", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            generate_qr(data, file_path)
            messagebox.showinfo("Succès", f"QR Code généré avec succès !\n\nEmplacement : {file_path}")
            # Effacer le champ texte après génération réussie
            text.delete("1.0", tk.END)
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la génération : {str(e)}")
            return  # Ne pas effacer en cas d'erreur
    
    else:  # Mode multiple
        if len(urls) == 1:
            response = messagebox.askyesno(
                "Confirmation",
                "Vous avez saisi une seule URL en mode 'Plusieurs QR Codes'.\n"
                "Voulez-vous quand même continuer ?"
            )
            if not response:
                return
        
        folder = filedialog.askdirectory(title="Choisir le dossier de sauvegarde")
        if not folder:
            return

        success_count = 0
        failed_urls = []
        
        for i, url in enumerate(urls, start=1):
            # Générer un nom de fichier basé sur l'URL
            filename = generate_filename_from_url(url, folder, index=i)
            path = os.path.join(folder, filename)
            
            try:
                generate_qr(url, path)
                success_count += 1
            except Exception as e:
                failed_urls.append(f"URL {i} ({url[:50]}...)\nErreur : {str(e)}")
        
        if success_count > 0:
            message_text = f"{success_count} QR Code(s) généré(s) avec succès !\n\n"
            message_text += f"Dossier : {folder}"
            
            if failed_urls:
                message_text += f"\n\nÉchecs ({len(failed_urls)}) :\n" + "\n---\n".join(failed_urls)
            
            messagebox.showinfo("Succès", message_text)
            # Effacer le champ texte après génération réussie (au moins un QR code généré)
            text.delete("1.0", tk.END)
        else:
            messagebox.showerror("Erreur", "Aucun QR Code n'a pu être généré.")
            # Ne pas effacer le champ texte en cas d'échec complet

    text.focus_set()


# ================= Fenêtre principale =================
root = tk.Tk()
root.title("Générateur de QR Code")
root.configure(bg="#e9edf3")
root.minsize(500, 400)  # Légèrement plus haut pour ajouter les boutons radio

center_large_window(root, 0.65, 0.65)

root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)

# ================= Header =================
header = tk.Frame(root, bg="#4a90e2")
header.grid(row=0, column=0, sticky="nsew")

tk.Label(
    header,
    text="Générateur de QR Code",
    bg="#4a90e2",
    fg="white",
    font=("Segoe UI", 18, "bold")
).pack(pady=20)

# ================= Contenu =================
container = tk.Frame(root, bg="#e9edf3")
container.grid(row=1, column=0, sticky="nsew", padx=40, pady=20)

container.grid_columnconfigure(0, weight=1)
container.grid_rowconfigure(0, weight=1)

card = tk.Frame(
    container,
    bg="white",
    highlightthickness=1,
    highlightbackground="#d0d4da"
)
card.grid(row=0, column=0, sticky="nsew")
card.grid_columnconfigure(0, weight=1)

content = tk.Frame(card, bg="white")
content.grid(row=0, column=0, padx=40, pady=30, sticky="nsew")
content.grid_columnconfigure(0, weight=1)

# ================= Sélection du mode =================
mode_frame = tk.Frame(content, bg="white")
mode_frame.grid(row=0, column=0, sticky="w", pady=(0, 15))

tk.Label(
    mode_frame,
    text="Mode de génération :",
    bg="white",
    fg="#333",
    font=("Segoe UI", 11)
).pack(side=tk.LEFT, padx=(0, 15))

mode_var = tk.StringVar(value="multiple")  # Valeur par défaut

single_radio = tk.Radiobutton(
    mode_frame,
    text="Un seul QR Code",
    variable=mode_var,
    value="single",
    bg="white",
    font=("Segoe UI", 10),
    activebackground="white",
    cursor="hand2"
)
single_radio.pack(side=tk.LEFT, padx=(0, 20))

multiple_radio = tk.Radiobutton(
    mode_frame,
    text="Plusieurs QR Codes",
    variable=mode_var,
    value="multiple",
    bg="white",
    font=("Segoe UI", 10),
    activebackground="white",
    cursor="hand2"
)
multiple_radio.pack(side=tk.LEFT)

# ================= Champ multi-lignes =================
tk.Label(
    content,
    text="Entrez une URL par ligne",
    bg="white",
    fg="#333",
    font=("Segoe UI", 12)
).grid(row=1, column=0, sticky="w", pady=(10, 5))

text = tk.Text(
    content,
    font=("Segoe UI", 14),
    height=6,
    wrap="word",
    relief="flat",
    highlightthickness=1,
    highlightbackground="#ccc",
    highlightcolor="#4a90e2"
)
text.grid(row=2, column=0, sticky="nsew", pady=10)

# ================= Information selon le mode =================
info_label = tk.Label(
    content,
    text="Mode 'Plusieurs QR Codes' : un QR code sera généré pour chaque URL\n"
         "Nom des fichiers : basé sur le domaine de l'URL",
    bg="white",
    fg="#666",
    font=("Segoe UI", 9),
    justify=tk.LEFT,
    wraplength=500
)
info_label.grid(row=3, column=0, sticky="w", pady=(5, 15))

def update_info_label(*args):
    if mode_var.get() == "single":
        info_label.config(
            text="Mode 'Un seul QR Code' : toutes les URLs seront combinées en un seul QR code\n"
                 "Nom du fichier : basé sur le domaine de la première URL\n"
                 "Si plusieurs URLs sont saisies, vous pourrez choisir de toutes les combiner ou de ne prendre que la première."
        )
    else:
        info_label.config(
            text="Mode 'Plusieurs QR Codes' : un QR code sera généré pour chaque URL\n"
                 "Nom des fichiers : basé sur le domaine de chaque URL"
        )

mode_var.trace("w", update_info_label)

# ================= Bouton =================
tk.Button(
    content,
    text="Générer les QR Codes",
    font=("Segoe UI", 12, "bold"),
    bg="#4a90e2",
    fg="white",
    activebackground="#357ABD",
    relief="flat",
    cursor="hand2",
    command=generate
).grid(row=4, column=0, pady=20, ipadx=30, ipady=12)

root.mainloop()