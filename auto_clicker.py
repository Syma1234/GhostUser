import customtkinter as ctk
import time
import threading
import subprocess
from pynput import keyboard

def faire_clic():
    subprocess.run(["xdotool", "click", "1"])


class AutoClickerWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Ghost User")
        self.geometry("350x560")
        self.resizable(False, False)

        self.en_cours = False
        self.thread_click = None
        self.listener_clavier = None

        ctk.CTkLabel(self, text="Auto Clicker", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=20)

        ctk.CTkLabel(self, text="Appuie sur ESPACE pour stopper l'auto-clicker", font=ctk.CTkFont(size=12), text_color="#f0a500").pack(pady=(0, 10))

        ctk.CTkLabel(self, text="Temps entre les clics (secondes) :",font=ctk.CTkFont(size=12), justify="center").pack(pady=(5, 5))

        self.entree_intervalle = ctk.CTkEntry(self, width=120, placeholder_text="ex: 0.05")
        self.entree_intervalle.insert(0, "0.05")
        self.entree_intervalle.pack()

        ctk.CTkLabel(self, text="Nombre de clics (0 = infini) :", font=ctk.CTkFont(size=12)).pack(pady=(15, 5))

        self.entree_nb_clics = ctk.CTkEntry(self, width=120, placeholder_text="ex: 100")
        self.entree_nb_clics.insert(0, "0")
        self.entree_nb_clics.pack()

        ctk.CTkLabel(self, text="Délai avant démarrage (secondes) :", font=ctk.CTkFont(size=12)).pack(pady=(15, 5))

        self.entree_delai = ctk.CTkEntry(self, width=120, placeholder_text="ex: 3")
        self.entree_delai.insert(0, "3")
        self.entree_delai.pack()

        self.btn_start_stop = ctk.CTkButton(
            self,
            text="Démarrer",
            width=200,
            height=45,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="green",
            hover_color="#1e7e34",
            command=self.toggle_clicker
        )
        self.btn_start_stop.pack(pady=20)

        self.label_statut = ctk.CTkLabel(
            self,
            text="En attente...",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.label_statut.pack()

        self.protocol("WM_DELETE_WINDOW", self.fermer)

    def toggle_clicker(self):
        if not self.en_cours:
            self.demarrer()
        else:
            self.arreter()

    def demarrer(self):
        try:
            intervalle = float(self.entree_intervalle.get())
            nb_clics = int(self.entree_nb_clics.get())
            delai = float(self.entree_delai.get())
        except ValueError:
            self.label_statut.configure(text="Valeurs invalides !", text_color="orange")
            return

        self.en_cours = True
        self.btn_start_stop.configure(text="Arrêter", fg_color="red", hover_color="#b71c1c")
        self.demarrer_listener_clavier()

        self.thread_click = threading.Thread(
            target=self.boucle_clic,
            args=(intervalle, nb_clics, delai),
            daemon=True
        )
        self.thread_click.start()

    def demarrer_listener_clavier(self):
        def on_press(key):
            if key == keyboard.Key.space:
                self.arreter()

        self.listener_clavier = keyboard.Listener(on_press=on_press)
        self.listener_clavier.start()

    def boucle_clic(self, intervalle, nb_clics, delai):
        for i in range(int(delai), 0, -1):
            if not self.en_cours:
                return
            self.label_statut.configure(
                text=f"Démarrage dans {i} secondes...",
                text_color="orange"
            )
            time.sleep(1)

        compteur = 0

        while self.en_cours:
            faire_clic()

            compteur += 1
            self.label_statut.configure(
                text=f"Clics effectués : {compteur}",
                text_color="lightgreen"
            )

            if nb_clics > 0 and compteur >= nb_clics:
                break

            time.sleep(intervalle)

        self.en_cours = False
        self.btn_start_stop.configure(text="Démarrer", fg_color="green", hover_color="#1e7e34")
        self.label_statut.configure(text=f"Terminé ! ({compteur} clics)", text_color="lightgreen")

        if self.listener_clavier:
            self.listener_clavier.stop()

    def arreter(self):
        self.en_cours = False
        self.btn_start_stop.configure(text="Démarrer", fg_color="green", hover_color="#1e7e34")
        self.label_statut.configure(text="Appuie sur ESPACE pour arrêter", text_color="gray")

        if self.listener_clavier:
            self.listener_clavier.stop()

    def fermer(self):
        self.arreter()
        self.destroy()