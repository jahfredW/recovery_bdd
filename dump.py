import os
import subprocess
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox, ttk, filedialog


# fonction de sauvegarde des bdds 
def backup_databases(backup_path):
    host = "localhost"
    user = "root"
    password = ""  # À noter: c'est dangereux de laisser un mot de passe vide ou hardcodé
    
    # Récupérer la liste des bases de données
    command = ["mysql", "-h", host, "-u", user, "-e", "SHOW DATABASES;"]

    # Permet de cacher le terminal - A debug - 
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    result = subprocess.run(command, capture_output=True, text=True, startupinfo=startupinfo)

    # récupératon des bdd en splitant la sortie standard
    databases = result.stdout.split()

    # Exclure certaines bases de données
    exclude_databases = ['information_schema', 'performance_schema', 'mysql', 'Database', 'sys']

    #compréhension de liste 
    databases = [db for db in databases if db not in exclude_databases]

    # Créer le dossier s'il n'existe pas
    if not os.path.exists(backup_path):
        os.makedirs(backup_path)

    

    # Dump de chaque base de données
    total_databases = len(databases)


    for index, db in enumerate(databases):
        dump_file = os.path.join(backup_path, f"backup_{db}.sql")
        command = ["mysqldump", "-h", host, "-u", user, db, ">", dump_file]
        result = subprocess.run(" ".join(command), shell=True)

        # Mettre à jour la barre de progression
        progress_percentage = (index + 1) / total_databases * 100
        progress_bar['value'] = progress_percentage
        root.update()

        if result.returncode == 0:
            print(f"Sauvegarde de {db} réussie.")
        else:
            print(f"Erreur pendant la sauvegarde de {db}.")
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

    backup_databases(backup_path.get())

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
