# ------------------ APPLICATION DE GESTION DE TÂCHES ------------------
# ----------------------- DÉBUT DU CODE -------------------------------

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

class TaskManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestionnaire de Tâches")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        # Fichier pour stocker les tâches
        self.tasks_file = "tasks.json"
        self.tasks = self.load_tasks()
        
        # Variables
        self.task_var = tk.StringVar()
        self.description_var = tk.StringVar()
        self.priority_var = tk.StringVar(value="Moyenne")
        self.due_date_var = tk.StringVar()
        self.filter_var = tk.StringVar(value="Toutes")
        self.search_var = tk.StringVar()
        
        # Interface utilisateur
        self.create_widgets()
        
    def create_widgets(self):
        # Cadre pour les entrées
        input_frame = tk.Frame(self.root, bg="#f0f0f0", pady=10)
        input_frame.pack(fill="x", padx=10)
        
        # Zone de titre
        title_frame = tk.Frame(self.root, bg="#4a7abc", pady=15)
        title_frame.pack(fill="x")
        
        app_title = tk.Label(title_frame, text="GESTIONNAIRE DE TÂCHES", font=("Arial", 16, "bold"), 
                            bg="#4a7abc", fg="white")
        app_title.pack()
        
        # Entrées pour les nouvelles tâches
        entry_frame = tk.LabelFrame(self.root, text="Ajouter une nouvelle tâche", 
                                   font=("Arial", 10, "bold"), bg="#f0f0f0", padx=10, pady=10)
        entry_frame.pack(fill="x", padx=10, pady=10)
        
        # Titre de la tâche
        tk.Label(entry_frame, text="Titre:", bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        task_entry = tk.Entry(entry_frame, textvariable=self.task_var, width=30)
        task_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Description
        tk.Label(entry_frame, text="Description:", bg="#f0f0f0").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        desc_entry = tk.Entry(entry_frame, textvariable=self.description_var, width=30)
        desc_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Priorité
        tk.Label(entry_frame, text="Priorité:", bg="#f0f0f0").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        priority_combo = ttk.Combobox(entry_frame, textvariable=self.priority_var, 
                                     values=["Basse", "Moyenne", "Haute"], width=15)
        priority_combo.grid(row=0, column=3, padx=5, pady=5)
        
        # Date d'échéance
        tk.Label(entry_frame, text="Date d'échéance:", bg="#f0f0f0").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        due_entry = tk.Entry(entry_frame, textvariable=self.due_date_var, width=15)
        due_entry.grid(row=1, column=3, padx=5, pady=5)
        due_entry.insert(0, datetime.now().strftime("%d/%m/%Y"))
        
        # Boutons
        button_frame = tk.Frame(entry_frame, bg="#f0f0f0")
        button_frame.grid(row=2, column=0, columnspan=4, pady=10)
        
        add_btn = tk.Button(button_frame, text="Ajouter", command=self.add_task, 
                          bg="#4CAF50", fg="white", width=10)
        add_btn.grid(row=0, column=0, padx=5)
        
        update_btn = tk.Button(button_frame, text="Modifier", command=self.update_task, 
                             bg="#2196F3", fg="white", width=10)
        update_btn.grid(row=0, column=1, padx=5)
        
        delete_btn = tk.Button(button_frame, text="Supprimer", command=self.delete_task, 
                             bg="#F44336", fg="white", width=10)
        delete_btn.grid(row=0, column=2, padx=5)
        
        # Recherche et filtrage
        filter_frame = tk.Frame(self.root, bg="#f0f0f0", padx=10, pady=5)
        filter_frame.pack(fill="x")
        
        tk.Label(filter_frame, text="Rechercher:", bg="#f0f0f0").pack(side="left", padx=5)
        search_entry = tk.Entry(filter_frame, textvariable=self.search_var, width=20)
        search_entry.pack(side="left", padx=5)
        
        tk.Button(filter_frame, text="🔍", command=self.filter_tasks, bg="#ddd").pack(side="left", padx=5)
        
        tk.Label(filter_frame, text="Filtrer par priorité:", bg="#f0f0f0").pack(side="left", padx=5)
        filter_combo = ttk.Combobox(filter_frame, textvariable=self.filter_var, 
                                   values=["Toutes", "Basse", "Moyenne", "Haute"], width=10)
        filter_combo.pack(side="left", padx=5)
        filter_combo.bind("<<ComboboxSelected>>", lambda e: self.filter_tasks())
        
        # Liste des tâches
        list_frame = tk.Frame(self.root, bg="#fff")
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Treeview pour afficher les tâches
        self.task_tree = ttk.Treeview(list_frame, columns=("ID", "Titre", "Description", "Priorité", "Date d'échéance", "Statut"), 
                                     show="headings", selectmode="browse")
        
        # Définir les en-têtes de colonnes
        self.task_tree.heading("ID", text="ID")
        self.task_tree.heading("Titre", text="Titre")
        self.task_tree.heading("Description", text="Description")
        self.task_tree.heading("Priorité", text="Priorité")
        self.task_tree.heading("Date d'échéance", text="Date d'échéance")
        self.task_tree.heading("Statut", text="Statut")
        
        # Définir les largeurs de colonnes
        self.task_tree.column("ID", width=40)
        self.task_tree.column("Titre", width=150)
        self.task_tree.column("Description", width=200)
        self.task_tree.column("Priorité", width=100)
        self.task_tree.column("Date d'échéance", width=120)
        self.task_tree.column("Statut", width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.task_tree.yview)
        self.task_tree.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        self.task_tree.pack(side="left", fill="both", expand=True)
        
        # Événements
        self.task_tree.bind("<ButtonRelease-1>", self.select_task)
        self.task_tree.bind("<Double-1>", self.toggle_status)
        
        # Actualiser la liste des tâches
        self.refresh_task_list()
        
        # Barre d'état
        self.status_var = tk.StringVar()
        status_bar = tk.Label(self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.status_var.set("Prêt")
    
    def load_tasks(self):
        if os.path.exists(self.tasks_file):
            try:
                with open(self.tasks_file, "r") as file:
                    return json.load(file)
            except:
                return []
        return []
    
    def save_tasks(self):
        with open(self.tasks_file, "w") as file:
            json.dump(self.tasks, file, indent=4)
    
    def add_task(self):
        title = self.task_var.get().strip()
        description = self.description_var.get().strip()
        priority = self.priority_var.get()
        due_date = self.due_date_var.get()
        
        if not title:
            messagebox.showwarning("Attention", "Le titre ne peut pas être vide!")
            return
        
        # Générer un ID unique
        task_id = 1
        if self.tasks:
            task_id = max(int(task["id"]) for task in self.tasks) + 1
        
        # Ajouter la nouvelle tâche
        new_task = {
            "id": str(task_id),
            "title": title,
            "description": description,
            "priority": priority,
            "due_date": due_date,
            "status": "À faire"
        }
        
        self.tasks.append(new_task)
        self.save_tasks()
        self.refresh_task_list()
        
        # Vider les champs
        self.task_var.set("")
        self.description_var.set("")
        self.priority_var.set("Moyenne")
        self.due_date_var.set(datetime.now().strftime("%d/%m/%Y"))
        
        self.status_var.set(f"Tâche '{title}' ajoutée avec succès")
    
    def select_task(self, event):
        try:
            selected_item = self.task_tree.selection()[0]
            values = self.task_tree.item(selected_item, "values")
            
            self.task_var.set(values[1])
            self.description_var.set(values[2])
            self.priority_var.set(values[3])
            self.due_date_var.set(values[4])
            
            self.selected_task_id = values[0]
        except IndexError:
            pass
    
    def update_task(self):
        try:
            selected_item = self.task_tree.selection()[0]
            task_id = self.task_tree.item(selected_item, "values")[0]
            
            for task in self.tasks:
                if task["id"] == task_id:
                    task["title"] = self.task_var.get().strip()
                    task["description"] = self.description_var.get().strip()
                    task["priority"] = self.priority_var.get()
                    task["due_date"] = self.due_date_var.get()
                    
                    self.save_tasks()
                    self.refresh_task_list()
                    
                    self.status_var.set(f"Tâche '{task['title']}' mise à jour")
                    return
        except IndexError:
            messagebox.showwarning("Attention", "Veuillez sélectionner une tâche à modifier")
    
    def delete_task(self):
        try:
            selected_item = self.task_tree.selection()[0]
            task_id = self.task_tree.item(selected_item, "values")[0]
            
            for i, task in enumerate(self.tasks):
                if task["id"] == task_id:
                    task_title = task["title"]
                    del self.tasks[i]
                    
                    self.save_tasks()
                    self.refresh_task_list()
                    
                    # Vider les champs
                    self.task_var.set("")
                    self.description_var.set("")
                    self.priority_var.set("Moyenne")
                    self.due_date_var.set(datetime.now().strftime("%d/%m/%Y"))
                    
                    self.status_var.set(f"Tâche '{task_title}' supprimée")
                    return
        except IndexError:
            messagebox.showwarning("Attention", "Veuillez sélectionner une tâche à supprimer")
    
    def toggle_status(self, event):
        try:
            selected_item = self.task_tree.selection()[0]
            task_id = self.task_tree.item(selected_item, "values")[0]
            
            for task in self.tasks:
                if task["id"] == task_id:
                    if task["status"] == "À faire":
                        task["status"] = "Terminée"
                    else:
                        task["status"] = "À faire"
                    
                    self.save_tasks()
                    self.refresh_task_list()
                    self.status_var.set(f"Statut de la tâche '{task['title']}' changé à '{task['status']}'")
                    return
        except IndexError:
            pass
    
    def filter_tasks(self):
        self.refresh_task_list()
    
    def refresh_task_list(self):
        # Vider la liste
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)
        
        # Filtrer les tâches
        filter_priority = self.filter_var.get()
        search_term = self.search_var.get().lower()
        
        filtered_tasks = self.tasks
        
        if filter_priority != "Toutes":
            filtered_tasks = [task for task in filtered_tasks if task["priority"] == filter_priority]
        
        if search_term:
            filtered_tasks = [task for task in filtered_tasks if 
                             search_term in task["title"].lower() or 
                             search_term in task["description"].lower()]
        
        # Remplir avec les tâches filtrées
        for task in filtered_tasks:
            values = (
                task["id"],
                task["title"],
                task["description"],
                task["priority"],
                task["due_date"],
                task["status"]
            )
            
            # Différentes couleurs selon la priorité et le statut
            tag = task["priority"].lower()
            if task["status"] == "Terminée":
                tag = "done"
            
            self.task_tree.insert("", tk.END, values=values, tags=(tag,))
        
        # Configurer les couleurs des tags
        self.task_tree.tag_configure("basse", background="#e8f5e9")
        self.task_tree.tag_configure("moyenne", background="#fff9c4")
        self.task_tree.tag_configure("haute", background="#ffcdd2")
        self.task_tree.tag_configure("done", background="#e0e0e0", foreground="#757575")

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManager(root)
    root.mainloop()
