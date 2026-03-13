import customtkinter as ctk
from auto_clicker import AutoClickerWindow
from keyboardRecorder import MacroClavierWindow

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

#mettre les fenetres en premier plan pour bien voir

#auto-clicker | Utiliser Ubuntu sur Xorg pour que ca marche !!!
#bot pour jeu
#record une sequence de touches 
#pareil avec la souris ou déplacement aléatoire
#Ajouter un bouton home sur chaque fonctionnalités
#Feature ou on peut enregistrer plusieurs sequences avec le recorder et cliquer pour en lancer une particulière ?


class Hub(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Ghost User")
        self.geometry("400x500")
        self.resizable(True, True)

        self.label_titre = ctk.CTkLabel(
            self,
            text="Ghost User Hub",
            font=ctk.CTkFont(size=26, weight="bold")
        )
        self.label_titre.pack(pady=30)

        self.label_sous_titre = ctk.CTkLabel(
            self,
            text="Choisissez une fonctionnalité",
            font=ctk.CTkFont(size=14),
        )
        self.label_sous_titre.pack(pady=(0, 30))

        self.btn_auto_clicker = ctk.CTkButton(
            self,
            text="Auto Clicker",
            width=250,
            height=50,
            font=ctk.CTkFont(size=15),
            command=self.ouvrir_auto_clicker
        )
        self.btn_auto_clicker.pack(pady=10)

        self.btn_macro_clavier = ctk.CTkButton(
            self,
            text="Keyboard Recorder",
            width=250,
            height=50,
            font=ctk.CTkFont(size=15),
            command=self.ouvrir_macro_clavier
        )
        self.btn_macro_clavier.pack(pady=10)

        self.btn_future3 = ctk.CTkButton(
            self,
            text="Déplacement Souris (Soon)",
            width=250,
            height=50,
            font=ctk.CTkFont(size=15),
            state="disabled"
        )
        self.btn_future3.pack(pady=10)

        self.label_footer = ctk.CTkLabel(
            self,
            text="pyautogui + customtkinter project",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        self.label_footer.pack(side="bottom", pady=15)

    def ouvrir_auto_clicker(self):
        fenetre = AutoClickerWindow(self)

    def ouvrir_macro_clavier(self):
        fenetre = MacroClavierWindow(self)


if __name__ == "__main__":
    app = Hub()
    app.mainloop()