import tkinter as tk
from tkinter import messagebox


class CoffeeMachine:
    def __init__(self):
        # Initial resources for the coffee machine
        self.water = 1000  # milliliters
        self.coffee_beans = 500  # grams
        self.milk = 500  # milliliters
        self.sugar = 200  # grams
        self.maintenance_count = 0  # Counter for maintenance
        self.balance = 0.0  # virtual payment balance (in euros)

        # Menu for different drinks with their ingredients and price
        #Sprint 1
        self.menu = {
            "Espresso": {"water": 50, "coffee_beans": 18, "milk": 0, "price": 1.5, "color": "brown"},
            "Ristretto": {"water": 30, "coffee_beans": 18, "milk": 0, "price": 1.7, "color": "darkred"},
            "Double espresso": {"water": 100, "coffee_beans": 36, "milk": 0, "price": 2.0, "color": "darkbrown"},
            "Café": {"water": 150, "coffee_beans": 20, "milk": 0, "price": 2.0, "color": "beige"},
            "Americano": {"water": 200, "coffee_beans": 15, "milk": 0, "price": 2.2, "color": "lightbrown"},
            "Cappuccino": {"water": 150, "coffee_beans": 24, "milk": 100, "price": 2.5, "color": "tan"},
            "Latte Macchiato": {"water": 200, "coffee_beans": 20, "milk": 150, "price": 3.0, "color": "lightyellow"},
            "Café au lait": {"water": 150, "coffee_beans": 18, "milk": 150, "price": 2.5, "color": "lightpink"},
            "Lait chaud": {"water": 0, "coffee_beans": 0, "milk": 200, "price": 2.0, "color": "lightblue"},
            "Thé": {"water": 200, "coffee_beans": 0, "milk": 0, "price": 1.5, "color": "green"},
        }

    def check_resources(self, drink, size):
        # Check if there are enough resources to prepare the selected drink
        drink_data = self.menu[drink]
        water_required = drink_data["water"] * size
        coffee_beans_required = drink_data["coffee_beans"] * size
        milk_required = drink_data["milk"] * size

        # Check for sufficient water, coffee beans, and milk
        if self.water < water_required:
            return False, "water"
        if self.coffee_beans < coffee_beans_required:
            return False, "coffee_beans"
        if self.milk < milk_required:
            return False, "milk"
        return True, None

    def prepare_drink(self, drink, size):
        # sprint 2
        # Prepare the selected drink if there are enough resources
        drink_data = self.menu[drink]
        water_required = drink_data["water"] * size
        coffee_beans_required = drink_data["coffee_beans"] * size
        milk_required = drink_data["milk"] * size

        check, resource = self.check_resources(drink, size)
        if not check:
            return f"Insufficient resource: {resource}."

        # Deduct resources after preparation
        self.water -= water_required
        self.coffee_beans -= coffee_beans_required
        self.milk -= milk_required
        self.balance += drink_data["price"]
        self.maintenance_count += 1

        # Check if the machine needs cleaning
        if self.maintenance_count >= 5:
            return "Machine requires cleaning."

        return f"{drink} ({size} dl) prepared successfully!"

    def add_resources(self, water, coffee_beans, milk, sugar):
        # sprint 2
        # Add resources to the machine
        self.water += water
        self.coffee_beans += coffee_beans
        self.milk += milk
        self.sugar += sugar

    def clean_machine(self):
        # sprint 1
        # Clean the machine by resetting the maintenance counter
        self.maintenance_count = 0


class CoffeeMachineApp:
    def __init__(self, root):
        self.machine = CoffeeMachine()  # Create an instance of the CoffeeMachine
        self.root = root
        self.root.title("Coffee Machine Simulation")  # Set window title
        self.create_widgets()  # Create the user interface widgets

    def create_widgets(self):
        # sprint1
        # Create widgets for the main window
        tk.Label(self.root, text="Coffee Machine", font=("Helvetica", 16, "bold")).pack(pady=10)

        frame_menu = tk.Frame(self.root)
        frame_menu.pack(pady=10)
        tk.Label(frame_menu, text="Drink Menu:", font=("Helvetica", 12)).pack()

        # Create buttons for each drink in the menu
        for drink in self.machine.menu.keys():
            btn = tk.Button(
                frame_menu,
                text=f"{drink} ({self.machine.menu[drink]['price']}€)",
                command=lambda d=drink: self.show_size_and_payment_window(d),
                width=25,
            )
            btn.pack(pady=5)

        # Create action buttons
        frame_actions = tk.Frame(self.root)
        frame_actions.pack(pady=10)
        tk.Button(frame_actions, text="Show Resources", command=self.show_status, width=20).pack(pady=5)
        tk.Button(frame_actions, text="Add Resources", command=self.add_resources_window, width=20).pack(pady=5)
        tk.Button(frame_actions, text="Clean Machine", command=self.clean_machine, width=20).pack(pady=5)
        tk.Button(frame_actions, text="Quit", command=self.root.quit, width=20).pack(pady=5)

        # Canvas for coffee cup animation
        self.canvas = tk.Canvas(self.root, width=300, height=300, bg="white")
        self.canvas.pack(pady=10)

    def show_size_and_payment_window(self, drink):
        # sprint 2
        # Show a window for selecting the size of the drink
        size_window = tk.Toplevel(self.root)
        size_window.title(f"Select Size for {drink}")

        tk.Label(size_window, text="Select Size:", font=("Helvetica", 12)).pack(pady=10)

        # Options for drink sizes (S, M, L)
        sizes = [("S", 1), ("M", 2), ("L", 3)]
        for size_name, size_value in sizes:
            btn = tk.Button(size_window, text=f"{size_name} - {size_value} dl",
                            command=lambda s=size_value, d=drink: self.show_payment_window(s, d, size_window))
            btn.pack(pady=5)

    def show_payment_window(self, size, drink, size_window):
        # Show a window for selecting the payment method
        size_window.destroy()  # Close size selection window
        payment_window = tk.Toplevel(self.root)
        payment_window.title("Select Payment Method")

        tk.Label(payment_window, text="Select Payment Method:", font=("Helvetica", 12)).pack(pady=10)

        # Available payment methods
        payment_methods = ["Twint", "Cash", "Card"]
        for method in payment_methods:
            btn = tk.Button(payment_window, text=method,
                            command=lambda m=method, s=size, d=drink: self.process_payment(m, s, d, payment_window))
            btn.pack(pady=5)

    def process_payment(self, method, size, drink, payment_window):
        # sprint 2
        # Calculate the price based on the selected drink and size
        price = self.machine.menu[drink]["price"]

        # Adjust price based on size
        if size == 2:  # Medium (M)
            price += 0.50
        elif size == 3:  # Large (L)
            price += 1.00

        payment_window.destroy()  # Close payment window

        # Ask user for payment confirmation
        result = messagebox.askyesno("Payment", f"Do you want to pay {price}€ via {method}?")

        if result:
            # Payment successful
            messagebox.showinfo("Payment Successful", f"Payment of {price}€ via {method} successful.")

            # Start preparing the drink
            preparation_result = self.prepare_drink(drink, size)

            # Show the result of the drink preparation
            messagebox.showinfo("Preparation", preparation_result)

        else:
            # Payment failed
            messagebox.showerror("Payment Failed", "Payment was not completed.")

    def prepare_drink(self, drink, size):
        # sprint 2
        # Prepare the selected drink and show the result
        result = self.machine.prepare_drink(drink, size)
        messagebox.showinfo("Preparation", result)
        if "prepared" in result:
            self.show_coffee_cup(drink, size)  # Show coffee cup animation if prepared

    def show_status(self):
        # Show the current resource status (water, coffee beans, milk, etc.)
        status = (
            f"Current Resources:\n"
            f"Water: {self.machine.water} ml\n"
            f"Coffee Beans: {self.machine.coffee_beans} g\n"
            f"Milk: {self.machine.milk} ml\n"
            f"Sugar: {self.machine.sugar} g\n"
            f"Balance: {self.machine.balance}€\n"
            f"Drinks prepared since last cleaning: {self.machine.maintenance_count}"
        )
        messagebox.showinfo("Resource Status", status)

    def add_resources_window(self):
        # Show a window for adding more resources to the machine
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Resources")

        tk.Label(add_window, text="Water (ml):").grid(row=0, column=0, padx=5, pady=5)
        water_entry = tk.Entry(add_window)
        water_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(add_window, text="Coffee Beans (g):").grid(row=1, column=0, padx=5, pady=5)
        coffee_entry = tk.Entry(add_window)
        coffee_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(add_window, text="Milk (ml):").grid(row=2, column=0, padx=5, pady=5)
        milk_entry = tk.Entry(add_window)
        milk_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(add_window, text="Sugar (g):").grid(row=3, column=0, padx=5, pady=5)
        sugar_entry = tk.Entry(add_window)
        sugar_entry.grid(row=3, column=1, padx=5, pady=5)

        def add_resources():
            # sprint 2
            # Add resources to the machine after valid input
            try:
                water = int(water_entry.get() or 0)
                coffee = int(coffee_entry.get() or 0)
                milk = int(milk_entry.get() or 0)
                sugar = int(sugar_entry.get() or 0)
                self.machine.add_resources(water, coffee, milk, sugar)
                add_window.destroy()
                messagebox.showinfo("Resources Added", "Resources added successfully!")
            except ValueError:
                messagebox.showerror("Error", "Please enter valid values for resources.")

        add_button = tk.Button(add_window, text="Add", command=add_resources)
        add_button.grid(row=4, columnspan=2, pady=10)

    def clean_machine(self):
        #sprint 1
        # Clean the machine and reset maintenance counter
        self.machine.clean_machine()
        messagebox.showinfo("Machine Cleaned", "The machine has been successfully cleaned!")

    def show_coffee_cup(self, drink, size):
        # sprint 1
        # Show an animated coffee cup being filled
        self.canvas.delete("all")  # Clear the canvas
        size_mapping = {1: 50, 2: 100, 3: 150}  # Size to height mapping
        target_height = size_mapping[size]
        color = self.machine.menu[drink]["color"]  # Get the color for the drink

        # Draw a coffee cup with the specific color
        cup_width = 120
        cup_height = 200
        cup_top_left_x = 90
        cup_top_left_y = 300 - cup_height

        self.canvas.create_rectangle(
            cup_top_left_x, cup_top_left_y, cup_top_left_x + cup_width, cup_top_left_y + cup_height,
            fill=color, outline="black")

        # Animate filling the coffee cup
        self.animate_coffee_fill(target_height)

    def animate_coffee_fill(self, target_height):
        # Animate the coffee filling into the cup
        current_height = 0
        increment = 5  # Filling speed

        def fill_coffee():
            nonlocal current_height
            if current_height < target_height:
                current_height += increment
                self.canvas.create_rectangle(90, 300 - current_height, 210, 300, fill="black", outline="black")
                self.root.after(50, fill_coffee)  # Call the fill function repeatedly

        fill_coffee()


# Create the Tkinter window
root = tk.Tk()
app = CoffeeMachineApp(root)  # Create the CoffeeMachineApp instance
root.mainloop()  # Start the Tkinter main loop
