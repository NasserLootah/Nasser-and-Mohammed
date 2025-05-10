import tkinter as tk
from tkinter import messagebox
import pickle
import os

# -------------------------
# Models
# -------------------------

class User:
    def __init__(self, username, password, name, email):
        self.username = username
        self.password = password
        self.name = name
        self.email = email
        self.orders = []  # Placeholder for future order support

# -------------------------
# File Handling
# -------------------------

def load_file(filename):
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)
    return {}

def save_file(data, filename):
    with open(filename, 'wb') as f:
        pickle.dump(data, f)

users = load_file('users.pkl')

# -------------------------
# GUI App
# -------------------------

class TicketApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Grand Prix Booking - Part 1")
        self.root.geometry("600x400")
        self.current_user = None
        self.main_menu()

    def main_menu(self):
        self.clear()
        tk.Label(self.root, text="Welcome to Grand Prix Booking", font=("Arial", 18)).pack(pady=20)
        tk.Button(self.root, text="Login", width=30, command=self.login_screen).pack(pady=10)
        tk.Button(self.root, text="Sign Up", width=30, command=self.signup_screen).pack(pady=10)

    def signup_screen(self):
        self.clear()
        tk.Label(self.root, text="Create New Account", font=("Arial", 14)).pack(pady=10)
        entries = {}
        for field in ["Username", "Password", "Name", "Email"]:
            tk.Label(self.root, text=field).pack()
            entry = tk.Entry(self.root, show="*" if field == "Password" else "")
            entry.pack()
            entries[field.lower()] = entry

        def create_user():
            u = entries['username'].get()
            if u in users:
                messagebox.showerror("Error", "Username already exists")
                return
            users[u] = User(
                u,
                entries['password'].get(),
                entries['name'].get(),
                entries['email'].get()
            )
            save_file(users, 'users.pkl')
            messagebox.showinfo("Success", "Account created")
            self.main_menu()

        tk.Button(self.root, text="Create Account", command=create_user).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.main_menu).pack()

    def login_screen(self):
        self.clear()
        tk.Label(self.root, text="Login", font=("Arial", 14)).pack(pady=10)
        tk.Label(self.root, text="Username").pack()
        username_entry = tk.Entry(self.root)
        username_entry.pack()
        tk.Label(self.root, text="Password").pack()
        password_entry = tk.Entry(self.root, show="*")
        password_entry.pack()

        def login():
            u = username_entry.get()
            p = password_entry.get()
            if u in users and users[u].password == p:
                self.current_user = users[u]
                self.user_dashboard()
            else:
                messagebox.showerror("Error", "Invalid login")

        tk.Button(self.root, text="Login", command=login).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.main_menu).pack()

    def user_dashboard(self):
        self.clear()
        tk.Label(self.root, text=f"Welcome {self.current_user.name}", font=("Arial", 16)).pack(pady=20)
        tk.Button(self.root, text="Logout", width=30, command=self.main_menu).pack(pady=10)

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# -------------------------
# Start App
# -------------------------

root = tk.Tk()
app = TicketApp(root)
root.mainloop()
