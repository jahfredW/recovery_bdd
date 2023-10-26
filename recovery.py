import os
import subprocess
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox, ttk, filedialog




# fonction de sauvegarde des bdds 
def dump_database(backup_path):
    host = "localhost"
    user = "root"
    password = ""  # À noter: c'est dangereux de laisser un mot de passe vide ou hardcodé
    
    # chemin vers les databases
    
    # Spécifiez le chemin du dossier que vous souhaitez parcourir
    

    # Utilisez la fonction os.listdir pour obtenir la liste des fichiers dans le dossier
    fichiers = os.listdir(backup_path)


    for index, fichier in enumerate(fichiers):
        # La commande pour créer la base de données

        # recherche de substring et index 
        substring = "backup"
        position = fichier.find(substring)

        # dump_file = os.path.join(backup_path, fichier)
        # print(dump_file)
      

        if position!= -1:

            index_underscore = fichier.find("_")
            index_point = fichier.find(".")
            db_name = fichier[index_underscore + 1:index_point] 
           

            command = ["mysql", "-h", host, "-u", user, "-e", f"DROP DATABASE IF EXISTS {db_name};"]
            result = subprocess.run(command, shell=True)

            command = ["mysql", "-h", host, "-u", user, "-e", f"CREATE DATABASE {db_name};"]
            result = subprocess.run(command, shell=True)

            dump_file = os.path.join(backup_path, fichier)
         
           
            command = ["mysql", "-h", host, "-u", user, db_name]
            with open(dump_file, 'rb') as f:
                result = subprocess.run(command, stdin=f, shell=True)

            # Créez la commande pour supprimer la base de données si elle existe
            # drop_command = f"mysqladmin -h {host} -u {user} -p drop {db}"


            # Mettre à jour la barre de progression
            progress_percentage = (index + 1) / len(fichiers) * 100
            progress_bar['value'] = progress_percentage
            root.update()

            if result.returncode == 0:
                print(f"Sauvegarde de {db_name} réussie.")
            else:
                print(f"Erreur pendant la sauvegarde de {db_name}.")
                messagebox.showinfo("Incident", "Toutes les bases de données n'ont pas pu être sauvegardées!")

     # Afficher un message une fois que tous les dumps sont terminés
    messagebox.showinfo("Sauvegarde terminée", "Toutes les bases de données ont été sauvegardées avec succès!")
    
    # Quitter l'application
    root.quit()

# fonction de sélection du dossier de sauvegarde
def select_directory():
    backup_path.set(filedialog.askdirectory())

# fonction de cconfirmation : instancie la progress bar et appelle backup_database
def confirm_backup():
    global progress_bar


    status_label = tk.Label(root, text="Dump en cours")
    status_label.pack(pady=10)

    # Créez la barre de progression
    progress_bar = ttk.Progressbar(root, orient='horizontal', length=200, mode='determinate')
    progress_bar.pack(pady=20)

    root.update()

    dump_database(backup_path.get())

# Interface utilisateur avec tkinter
root = tk.Tk()
root.title("Sauvegarde des bases de données")
root.minsize(width=300, height=300)  # Largeur minimale de 300 pixels et hauteur minimale de 300 pixels


# Création du label pour le statut






backup_path = tk.StringVar()  # Cette variable stockera le chemin du dossier choisi

# Bouton pour choisir le dossier de sauvegarde
btn_select = tk.Button(root, text="Choisir le dossier de sauvegarde", command=select_directory)
btn_select.pack(padx=20, pady=20)

# Label pour afficher le chemin du dossier choisi
path_label = tk.Label(root, textvariable=backup_path)
path_label.pack(padx=20, pady=20)

# Bouton de confirmation pour démarrer le dump
btn_confirm = tk.Button(root, text="Confirmer", command=confirm_backup)
btn_confirm.pack(padx=10, pady=10)

root.mainloop()


