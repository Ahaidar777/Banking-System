import json     
import os
import customtkinter as ctk
from tkinter import messagebox

# File to store user data
DATA_FILE = "bank_data.json"

# Set appearance mode and color theme
ctk.set_appearance_mode("System")  # Can be "System", "Dark", or "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"

class BankAccount:
    def __init__(self, name, balance=0):     
        self.name = name
        self.balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return f"Deposited ${amount}. New balance: ${self.balance}"
        else:
            return "Invalid deposit amount."

    def withdraw(self, amount):
        if 0 < amount <= self.balance:           
            self.balance -= amount
            return f"Withdrew ${amount}. New balance: ${self.balance}"
        else:
            return "Insufficient funds or invalid amount."

    def check_balance(self):
        return f"Account balance for {self.name}: ${self.balance}"

    def to_dict(self):
        return {"name": self.name, "balance": self.balance}


class BankingApp:
    def __init__(self):
        self.accounts = self.load_data()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as file:
                data = json.load(file)
                return {name: BankAccount(name, account["balance"]) for name, account in data.items()}
        return {}

    def save_data(self):
        data = {name: account.to_dict() for name, account in self.accounts.items()}
        with open(DATA_FILE, "w") as file:
            json.dump(data, file, indent=4)

    def register_user(self, name):
        if name in self.accounts:
            return "User already exists."
        else:
            self.accounts[name] = BankAccount(name)
            self.save_data()
            return f"User {name} registered successfully."

    def get_account(self, name):
        if name in self.accounts:
            return self.accounts[name]
        else:
            return None

    def deposit_money(self, name, amount):
        account = self.get_account(name)
        if account:
            result = account.deposit(amount)
            self.save_data()
            return result
        else:
            return "User not found."

    def withdraw_money(self, name, amount):
        account = self.get_account(name)
        if account:
            result = account.withdraw(amount)
            self.save_data()
            return result
        else:
            return "User not found."

    def check_balance(self, name):
        account = self.get_account(name)
        if account:
            return account.check_balance()
        else:
            return "User not found."

    def delete_user(self, name):
        if name in self.accounts:
            del self.accounts[name]
            self.save_data()
            return f"User {name} deleted successfully."
        else:
            return "User not found."

    def list_users(self):
        if self.accounts:
            return "\n".join([f"- {name}" for name in self.accounts])
        else:
            return "No users registered."


class BankingAppGUI:
    def __init__(self, root):
        self.banking_app = BankingApp()
        self.root = root
        self.root.title("Modern Banking App")
        self.root.geometry("500x400")

        # Create GUI elements
        self.label = ctk.CTkLabel(root, text="Welcome to Haidar Banking App", font=("Arial", 20))
        self.label.pack(pady=20)

        self.name_label = ctk.CTkLabel(root, text="Name:")
        self.name_label.pack()
        self.name_entry = ctk.CTkEntry(root, width=300)
        self.name_entry.pack()

        self.amount_label = ctk.CTkLabel(root, text="Amount:")
        self.amount_label.pack()
        self.amount_entry = ctk.CTkEntry(root, width=300)
        self.amount_entry.pack()

        self.register_button = ctk.CTkButton(root, text="Register User", command=self.register_user)
        self.register_button.pack(pady=10)

        self.deposit_button = ctk.CTkButton(root, text="Deposit Money", command=self.deposit_money)
        self.deposit_button.pack(pady=10)

        self.withdraw_button = ctk.CTkButton(root, text="Withdraw Money", command=self.withdraw_money)
        self.withdraw_button.pack(pady=10)

        self.balance_button = ctk.CTkButton(root, text="Check Balance", command=self.check_balance)
        self.balance_button.pack(pady=10)

        self.delete_button = ctk.CTkButton(root, text="Delete User", command=self.delete_user)
        self.delete_button.pack(pady=10)

        self.list_button = ctk.CTkButton(root, text="List Users", command=self.list_users)
        self.list_button.pack(pady=10)

        self.exit_button = ctk.CTkButton(root, text="Exit", command=root.quit)
        self.exit_button.pack(pady=10)

    def register_user(self):
        name = self.name_entry.get()
        if name:
            result = self.banking_app.register_user(name)
            messagebox.showinfo("Result", result)
        else:
            messagebox.showwarning("Input Error", "Please enter a name.")

    def deposit_money(self):
        name = self.name_entry.get()
        amount = self.amount_entry.get()
        if name and amount:
            try:
                amount = float(amount)
                result = self.banking_app.deposit_money(name, amount)
                messagebox.showinfo("Result", result)
            except ValueError:
                messagebox.showwarning("Input Error", "Invalid amount.")
        else:
            messagebox.showwarning("Input Error", "Please enter name and amount.")

    def withdraw_money(self):
        name = self.name_entry.get()
        amount = self.amount_entry.get()
        if name and amount:
            try:
                amount = float(amount)
                result = self.banking_app.withdraw_money(name, amount)
                messagebox.showinfo("Result", result)
            except ValueError:
                messagebox.showwarning("Input Error", "Invalid amount.")
        else:
            messagebox.showwarning("Input Error", "Please enter name and amount.")

    def check_balance(self):
        name = self.name_entry.get()
        if name:
            result = self.banking_app.check_balance(name)
            messagebox.showinfo("Result", result)
        else:
            messagebox.showwarning("Input Error", "Please enter a name.")

    def delete_user(self):
        name = self.name_entry.get()
        if name:
            result = self.banking_app.delete_user(name)
            messagebox.showinfo("Result", result)
        else:
            messagebox.showwarning("Input Error", "Please enter a name.")

    def list_users(self):
        result = self.banking_app.list_users()
        messagebox.showinfo("Registered Users", result)


# Run the GUI
if __name__ == "__main__":
    root = ctk.CTk()
    app = BankingAppGUI(root)
    root.mainloop()    
    