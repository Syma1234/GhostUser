import customtkinter as ctk
import time
import threading
import subprocess
from pynput import keyboard
from pynput.keyboard import Controller, Listener, Key


clavier = Controller()


class MacroClavierWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Ghost User")
        self.geometry("350x560")
        self.resizable(False, False)

        self.enregistrement_en_cours = False
        self.replay_en_cours = False
        self.touches_enregistrees = []   
        self.temps_debut = None
        self.listener_enregistrement = None
        self.listener_stop = None
        self.thread_replay = None

        ctk.CTkLabel(self, text="Keyboard Recorder", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=20)

        ctk.CTkLabel(self, text="F7 = stop enregistrement  |  F6 = stop replay",font=ctk.CTkFont(size=12),text_color="#f0a500"
        ).pack(pady=(0, 15))

        ctk.CTkLabel(self, text="Nombre de répétitions du replay (0 = infini) :", font=ctk.CTkFont(size=13)).pack(pady=(5, 5))

        self.entree_repetitions = ctk.CTkEntry(self, width=120, placeholder_text="ex: 3")
        self.entree_repetitions.insert(0, "1")
        self.entree_repetitions.pack()

        ctk.CTkLabel(self, text="Délai avant démarrage du replay (secondes) :", font=ctk.CTkFont(size=13)).pack(pady=(15, 5))

        self.entree_delai = ctk.CTkEntry(self, width=120, placeholder_text="ex: 3")
        self.entree_delai.insert(0, "3")
        self.entree_delai.pack()

        self.btn_enregistrer = ctk.CTkButton(
            self,
            text="Enregistrer",
            width=250,
            height=45,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#c0392b",
            hover_color="#922b21",
            command=self.toggle_enregistrement
        )
        self.btn_enregistrer.pack(pady=(25, 8))

        self.btn_rejouer = ctk.CTkButton(
            self,
            text="Rejouer",
            width=250,
            height=45,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="green",
            hover_color="#1e7e34",
            state="disabled", 
            command=self.toggle_replay
        )
        self.btn_rejouer.pack(pady=8)

        self.btn_effacer = ctk.CTkButton(
            self,
            text="Effacer l'enregistrement",
            width=250,
            height=35,
            font=ctk.CTkFont(size=13),
            fg_color="gray30",
            hover_color="gray20",
            state="disabled",
            command=self.effacer
        )
        self.btn_effacer.pack(pady=8)

        self.label_statut = ctk.CTkLabel(
            self,
            text="En attente...",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.label_statut.pack(pady=(15, 0))

        self.label_touches = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        self.label_touches.pack()

        self.protocol("WM_DELETE_WINDOW", self.fermer)

    def toggle_enregistrement(self):
        if not self.enregistrement_en_cours:
            self.demarrer_enregistrement()
        else:
            self.stopper_enregistrement()

    def demarrer_enregistrement(self):
        self.touches_enregistrees = []
        self.temps_debut = time.time()
        self.enregistrement_en_cours = True

        self.btn_enregistrer.configure(text="Stop enregistrement")
        self.btn_rejouer.configure(state="disabled")
        self.btn_effacer.configure(state="disabled")
        self.label_statut.configure(text="Enregistrement en cours...", text_color="#e74c3c")
        self.label_touches.configure(text="0 touche enregistrée")

        def on_press(key):
            if key == Key.f7:
                self.stopper_enregistrement()
                return
            if self.enregistrement_en_cours:
                t = time.time() - self.temps_debut
                self.touches_enregistrees.append(("press", key, t))
                self.label_touches.configure(
                    text=f"{len(self.touches_enregistrees)} touches enregistrées !"
                )

        def on_release(key):
            if key == Key.f7:
                return
            if self.enregistrement_en_cours:
                t = time.time() - self.temps_debut
                self.touches_enregistrees.append(("release", key, t))

        self.listener_enregistrement = Listener(on_press=on_press, on_release=on_release)
        self.listener_enregistrement.start()

    def stopper_enregistrement(self):
        self.enregistrement_en_cours = False

        if self.listener_enregistrement:
            self.listener_enregistrement.stop()

        nb = len([e for e in self.touches_enregistrees if e[0] == "press"])
        self.btn_enregistrer.configure(text="Enregistrer à nouveau")
        self.label_statut.configure(
            text=f"Enregistrement terminé !",
            text_color="lightgreen"
        )
        self.label_touches.configure(text=f"{nb} touches enregistrées")

        if self.touches_enregistrees:
            self.btn_rejouer.configure(state="normal")
            self.btn_effacer.configure(state="normal")

    def toggle_replay(self):
        if not self.replay_en_cours:
            self.demarrer_replay()
        else:
            self.arreter_replay()

    def demarrer_replay(self):
        try:
            repetitions = int(self.entree_repetitions.get())
            delai = float(self.entree_delai.get())
        except ValueError:
            self.label_statut.configure(text="Valeurs invalides !", text_color="orange")
            return

        self.replay_en_cours = True
        self.btn_rejouer.configure(text="Arrêter le replay", fg_color="red", hover_color="#b71c1c")
        self.btn_enregistrer.configure(state="disabled")

        def on_press_stop(key):
            if key == Key.f6:
                self.arreter_replay()

        self.listener_stop = Listener(on_press=on_press_stop)
        self.listener_stop.start()

        self.thread_replay = threading.Thread(
            target=self.boucle_replay,
            args=(repetitions, delai),
            daemon=True
        )
        self.thread_replay.start()

    def boucle_replay(self, repetitions, delai):
        for i in range(int(delai), 0, -1):
            if not self.replay_en_cours:
                return
            self.label_statut.configure(
                text=f"Replay dans {i} secondes...",
                text_color="orange"
            )
            time.sleep(1)

        compteur = 0

        while self.replay_en_cours:
            self.label_statut.configure(
                text=f"Replay en cours...",
                text_color="lightgreen"
            )

            temps_precedent = 0
            for (action, key, t) in self.touches_enregistrees:
                if not self.replay_en_cours:
                    return
                # Pour bien avoir les meme timings ca
                time.sleep(t - temps_precedent)
                temps_precedent = t

                if action == "press":
                    clavier.press(key)
                elif action == "release":
                    clavier.release(key)

            compteur += 1

            if repetitions > 0 and compteur >= repetitions:
                break

        self.replay_en_cours = False
        self.btn_rejouer.configure(text="Rejouer", fg_color="green", hover_color="#1e7e34")
        self.btn_enregistrer.configure(state="normal")
        self.label_statut.configure(
            text=f"Replay terminé !",
            text_color="lightgreen"
        )

        if self.listener_stop:
            self.listener_stop.stop()

    def arreter_replay(self):
        self.replay_en_cours = False
        self.btn_rejouer.configure(text="Rejouer", fg_color="green", hover_color="#1e7e34")
        self.btn_enregistrer.configure(state="normal")
        self.label_statut.configure(text="Replay arrêté avec F6", text_color="gray")

        if self.listener_stop:
            self.listener_stop.stop()

    def effacer(self):
        self.touches_enregistrees = []
        self.btn_rejouer.configure(state="disabled")
        self.btn_effacer.configure(state="disabled")
        self.btn_enregistrer.configure(text="Enregistrer")
        self.label_statut.configure(text="Enregistrement effacé", text_color="gray")
        self.label_touches.configure(text="")

    def fermer(self):
        self.enregistrement_en_cours = False
        self.replay_en_cours = False
        if self.listener_enregistrement:
            self.listener_enregistrement.stop()
        if self.listener_stop:
            self.listener_stop.stop()
        self.destroy()