#!/usr/bin/python3

import time
import threading

class Horloge:
    def __init__(self, heures, minutes, secondes, mode_affichage=24):
        self.heures = heures
        self.minutes = minutes
        self.secondes = secondes
        self.mode_affichage = mode_affichage
        self.alarme = None
        self.pause = False
        self.heure_pause = (0, 0, 0)
        self.temps_pause = 0
        self.thread = threading.Thread(target=self.actualiser_heure_thread, daemon=True)

    def afficher_heure(self, heure=None):
        if heure is None:
            heure = (self.heures, self.minutes, self.secondes)

        format_heure = (
            f"{heure[0]:02d}:{heure[1]:02d}:{heure[2]:02d}" if self.mode_affichage == 24 else
            f"{heure[0] % 12 if heure[0] != 12 else 12:02d}:{heure[1]:02d}:{heure[2]:02d} {'AM' if heure[0] < 12 else 'PM'}"
        )

        return f"\rHeure de l'horloge : {format_heure}{'P' if self.pause else ''} 'P' pour pause, 'R' pour reprendre, ou 'Q' pour quitter : "

    def changer_mode_affichage(self, mode):
        if mode in [12, 24]:
            self.mode_affichage = mode
            print(self.afficher_heure())
        else:
            print("Mode d'affichage invalide. Choisissez entre 12 et 24 heures.")

    def regler_alarme(self, heure):
        self.alarme = heure

    def afficher_message_alarme(self):
        if self.alarme and (self.heures, self.minutes, self.secondes) == self.alarme:
            print("\nAlarme! L'heure de l'alarme est atteinte.")

    def mettre_en_pause(self):
        if not self.pause:
            self.pause = True
            self.heure_pause = (self.heures, self.minutes, self.secondes)
            self.temps_pause = time.time()
            print(self.afficher_heure())
            print("L'horloge est en pause.")
        else:
            print("L'horloge est déjà en pause.")

    def reprendre(self):
        if self.pause:
            self.pause = False
            duree_pause = time.time() - self.temps_pause
            self.heures, self.minutes, self.secondes = self.heure_pause
            self.incrementer_temps(int(duree_pause))
            self.thread = threading.Thread(target=self.actualiser_heure_thread, daemon=True)
            self.thread.start()
            print(self.afficher_heure())
        else:
            print("L'horloge n'est pas en pause.")

    def actualiser_heure_thread(self):
        while True:
            if not self.pause:
                time.sleep(1)
                self.incrementer_temps()
                print(self.afficher_heure(), end='', flush=True)
                self.afficher_message_alarme()

    def incrementer_temps(self, seconds=1):
        self.secondes += seconds
        while self.secondes >= 60:
            self.secondes -= 60
            self.minutes += 1
            while self.minutes >= 60:
                self.minutes -= 60
                self.heures += 1
                while self.heures >= 24:
                    self.heures -= 24

    def demarrer_horloge(self):
        self.thread.start()

if __name__ == "__main__":
    horloge = Horloge(16, 30, 0, mode_affichage=24)
    horloge.demarrer_horloge()
    horloge.regler_alarme((16, 30, 30))

    try:
        while True:
            action = input(horloge.afficher_heure()).lower()
            if action == 'p':
                horloge.mettre_en_pause()
            elif action == 'r':
                horloge.reprendre()
            elif action == 'q':
                break
            else:
                print("Action non reconnue. Veuillez entrer 'P', 'R', ou 'Q'.")
    except KeyboardInterrupt:
        print("\nArrêt de l'horloge.")
