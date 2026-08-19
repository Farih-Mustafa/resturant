import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import json
import os
import restaurant_gui 

USERS_FILE = "users.json"

if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)

class HealthyRestaurantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Healthy Restaurant 🥗")
        self.root.geometry("900x600")
        self.root.resizable(False, False)
        self.show_welcome()

    def set_bg(self):
        try:
            img = Image.open("backround.jpeg").resize((900, 600), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(img)
            bg_label = tk.Label(self.root, image=self.bg_photo)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            self.root.configure(bg="#E8F5E9")

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_welcome(self):
        self.clear()
        self.set_bg()
        overlay = tk.Frame(self.root, bg="white", padx=40, pady=40, highlightbackground="#2E7D32", highlightthickness=2)
        overlay.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(overlay, text="🥗 Healthy Life", font=("Helvetica", 36, "bold"), fg="#2E7D32", bg="white").pack()
        tk.Label(overlay, text="Fresh food for a better mood", font=("Helvetica", 14), fg="gray", bg="white").pack(pady=10)
        tk.Button(overlay, text="🔑 Enter (Login)", width=22, height=2, bg="#2E7D32", fg="white", font=("Helvetica", 12, "bold"), relief="flat", command=self.show_login).pack(pady=10)
        tk.Button(overlay, text=" New Registration", width=22, height=2, bg="white", fg="#2E7D32", font=("Helvetica", 12, "bold"), borderwidth=2, relief="groove", command=self.show_register).pack()

    def show_login(self):
        self.clear()
        self.set_bg()
        frame = tk.Frame(self.root, bg="white", padx=50, pady=50)
        frame.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(frame, text="Welcome Back! 👋", font=("Helvetica", 24, "bold"), fg="#2E7D32", bg="#F1F8E9").pack(pady=15)
        tk.Label(frame, text="Username", bg="white").pack(anchor="w")
        user_entry = tk.Entry(frame, width=30, font=("Helvetica", 12), bg="#F1F8E9")
        user_entry.pack(pady=5)
        tk.Label(frame, text="Password", bg="white").pack(anchor="w")
        pass_entry = tk.Entry(frame, width=30, show="*", font=("Helvetica", 12), bg="#F1F8E9")
        pass_entry.pack(pady=5)

        def login():
            u_name = user_entry.get().strip()
            u_pass = pass_entry.get().strip()
            try:
                with open(USERS_FILE, "r", encoding="utf-8") as f:
                    users = json.load(f)
            except: users = []
            for u in users:
                if u["username"] == u_name and u["password"] == u_pass:
                    self.root.destroy()
                    restaurant_gui.start_app(u_name)
                    return
            messagebox.showerror("Error", "Wrong username or password ❌")

        tk.Button(frame, text="🔓 Login", bg="#2E7D32", fg="white", width=20, font=("Helvetica", 12, "bold"), command=login).pack(pady=25)
        tk.Button(frame, text="⬅ Back", command=self.show_welcome).pack()

    def show_register(self):
        self.clear()
        self.set_bg()
        frame = tk.Frame(self.root, bg="white", padx=50, pady=50)
        frame.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(frame, text="Username", bg="white").pack(anchor="w")
        user = tk.Entry(frame, width=30, font=("Helvetica", 12)); user.pack(pady=5)
        tk.Label(frame, text="Password", bg="white").pack(anchor="w")
        password = tk.Entry(frame, width=30, show="*", font=("Helvetica", 12)); password.pack(pady=5)

        def register():
            reg_user = user.get().strip()
            reg_pass = password.get().strip()
            if not reg_user or not reg_pass:
                messagebox.showerror("Error", "Fill all fields! ⚠️")
                return
            with open(USERS_FILE, "r", encoding="utf-8") as f: users = json.load(f)
            users.append({"username": reg_user, "password": reg_pass})
            with open(USERS_FILE, "w", encoding="utf-8") as f: json.dump(users, f, indent=4, ensure_ascii=False)
            messagebox.showinfo("Success", "Registered! 🎉")
            self.show_login()

        tk.Button(frame, text="✅ Register Now", bg="#2E7D32", fg="white", command=register).pack(pady=25)
        tk.Button(frame, text="⬅ Back", command=self.show_welcome).pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = HealthyRestaurantApp(root)
    root.mainloop()