# 📱 Générateur de QR Code (Python)

Application graphique simple et efficace permettant de générer des **QR Codes** à partir de texte ou d’URL, développée en **Python** avec **Tkinter**.

## ✨ Fonctionnalités

- 🖥️ Interface graphique intuitive
- 🎯 Fenêtre centrée automatiquement
- 📏 Taille de fenêtre ergonomique
- 💾 Export du QR Code en **PNG**
- 🔒 Environnement Python isolé (venv)
- ⚡ Génération rapide et fiable



## 🛠️ Technologies utilisées

- **Python 3.10+**
- **Tkinter** (interface graphique)
- **qrcode** + **Pillow** (génération d’images)



## 📂 Structure du projet
qr_app/
- app.py # Interface graphique
- qr_generator.py # Logique de génération du  QRCode
- requirements.txt # Dépendances Python
- venv/ # Environnement virtuel (non versionné)


## 🚀 Installation et exécution

### 1️⃣ Cloner le projet
```bash
git clone https://github.com/TON_UTILISATEUR/qr_app.git
cd qr_app
```
---

## Créer un environnement virtuel
python3 -m venv venv

## Activer l’environnement virtuel
source venv/bin/activate

## Installer les dépendances
pip install -r requirements.txt

## Lancer l’application
python app.py
