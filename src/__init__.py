# Name : cafe_machine
# Autor: akrblt et Pang
# Date:  20.01.2025
# Version : 0.1
# Purpose : creer cafe machine


import tkinter as tk
from tkinter import messagebox


class CoffeeMachine:
    def __init__(self):
        # Initialisation des ressources
        self.water = 1000  # millilitres
        self.coffee_beans = 500  # grammes
        self.milk = 500  # millilitres
        self.sugar = 200  # grammes
        self.maintenance_count = 0
        self.balance = 0.0  # Paiement virtuel (en euros)
        self.menu = {
            "Espresso": {"water": 50, "coffee_beans": 18, "milk": 0, "price": 1.5},
            "Cappuccino": {"water": 150, "coffee_beans": 24, "milk": 100, "price": 2.5},
            "Latte Macchiato": {"water": 200, "coffee_beans": 20, "milk": 150, "price": 3.0},
            "Americano": {"water": 100, "coffee_beans": 15, "milk": 0, "price": 2.0},
        }

    def check_resources(self, drink):
        for resource, amount in self.menu[drink].items():
            if resource in ["water", "coffee_beans", "milk"]:
                if getattr(self, resource) < amount:
                    return False, resource
        return True, None

    def prepare_drink(self, drink):
        check, resource = self.check_resources(drink)
        if not check:
            return f"Ressource insuffisante : {resource}."
        for resource, amount in self.menu[drink].items():
            if resource in ["water", "coffee_beans", "milk"]:
                setattr(self, resource, getattr(self, resource) - amount)
        self.balance += self.menu[drink]["price"]
        self.maintenance_count += 1
        if self.maintenance_count >= 5:
            return "Machine nécessite un nettoyage."
        return f"{drink} préparé avec succès !"

    def add_resources(self, water, coffee_beans, milk, sugar):
        self.water += water
        self.coffee_beans += coffee_beans
        self.milk += milk
        self.sugar += sugar

    def clean_machine(self):
        self.maintenance_count = 0


class CoffeeMachineApp:
    def __init__(self, root):
        self.machine = CoffeeMachine()
        self.root = root
        self.root.title("Machine à Café - Simulation")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Machine à Café", font=("Helvetica", 16, "bold")).pack(pady=10)

        frame_menu = tk.Frame(self.root)
        frame_menu.pack(pady=10)
        tk.Label(frame_menu, text="Menu des Boissons :", font=("Helvetica", 12)).pack()
        for drink in self.machine.menu.keys():
            btn = tk.Button(
                frame_menu,
                text=f"{drink} ({self.machine.menu[drink]['price']}€)",
                command=lambda d=drink: self.prepare_drink(d),
                width=20,
            )
            btn.pack(pady=5)

        frame_actions = tk.Frame(self.root)
        frame_actions.pack(pady=10)
        tk.Button(frame_actions, text="Afficher les Ressources", command=self.show_status, width=20).pack(pady=5)
        tk.Button(frame_actions, text="Ajouter des Ressources", command=self.add_resources_window, width=20).pack(pady=5)
        tk.Button(frame_actions, text="Nettoyer la Machine", command=self.clean_machine, width=20).pack(pady=5)
        tk.Button(frame_actions, text="Quitter", command=self.root.quit, width=20).pack(pady=5)

        # Canvas pour la tasse de café
        self.canvas = tk.Canvas(self.root, width=300, height=300, bg="white")
        self.canvas.pack(pady=10)

    def prepare_drink(self, drink):
        result = self.machine.prepare_drink(drink)
        messagebox.showinfo("Préparation", result)
        if "préparé" in result:
            self.show_coffee_cup()

    def show_status(self):
        status = (
            f"Ressources actuelles :\n"
            f"Eau : {self.machine.water} ml\n"
            f"Grains de café : {self.machine.coffee_beans} g\n"
            f"Lait : {self.machine.milk} ml\n"
            f"Sucre : {self.machine.sugar} g\n"
            f"Solde : {self.machine.balance }€\n"
            f"Nombre de boissons préparées depuis le dernier nettoyage : {self.machine.maintenance_count}"
        )
        messagebox.showinfo("État des Ressources", status)

    def add_resources_window(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Ajouter des Ressources")

        tk.Label(add_window, text="Eau (ml) :").grid(row=0, column=0, padx=5, pady=5)
        water_entry = tk.Entry(add_window)
        water_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(add_window, text="Grains de café (g) :").grid(row=1, column=0, padx=5, pady=5)
        coffee_entry = tk.Entry(add_window)
        coffee_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(add_window, text="Lait (ml) :").grid(row=2, column=0, padx=5, pady=5)
        milk_entry = tk.Entry(add_window)
        milk_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(add_window, text="Sucre (g) :").grid(row=3, column=0, padx=5, pady=5)
        sugar_entry = tk.Entry(add_window)
        sugar_entry.grid(row=3, column=1, padx=5, pady=5)

        def add_resources():
            try:
                water = int(water_entry.get() or 0)
                coffee = int(coffee_entry.get() or 0)
                milk = int(milk_entry.get() or 0)
                sugar = int(sugar_entry.get() or 0)
                self.machine.add_resources(water, coffee, milk, sugar)
                messagebox.showinfo("Succès", "Ressources ajoutées avec succès !")
                add_window.destroy()
            except ValueError:
                messagebox.showerror("Erreur", "Veuillez entrer des valeurs numériques valides.")

        tk.Button(add_window, text="Ajouter", command=add_resources).grid(row=4, column=0, columnspan=2, pady=10)

      #fonction definir pour macjine nettoayer
    def clean_machine(self):
        self.machine.clean_machine()
        messagebox.showinfo("Nettoyage", "La machine a été nettoyée avec succès !")

    def show_coffee_cup(self):
        self.canvas.delete("all")
        # Base de la tasse
        self.canvas.create_oval(100, 200, 200, 250, fill="brown", outline="")
        # Corps de la tasse
        self.canvas.create_rectangle(110, 150, 190, 200, fill="brown", outline="")
        # Anse de la tasse
        self.canvas.create_oval(190, 160, 210, 190, outline="brown", width=4)
        # Vapeur de café
        self.canvas.create_line(130, 130, 130, 100, fill="gray", width=2)
        self.canvas.create_line(150, 130, 150, 100, fill="gray", width=2)
        self.canvas.create_line(170, 130, 170, 100, fill="gray", width=2)
        #
        #
        #




# Lancer l'application
if __name__ == "__main__":
    root = tk.Tk()
    app = CoffeeMachineApp(root)
    root.mainloop()
