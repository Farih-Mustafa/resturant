import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import json
import os

ORDER_FILE = "order.json"

# MENU CATEGORIES - All dishes included
MENU_DATA = {
    "Breakfast 🍳": [
        {"name": "Egg Omelet", "price": 8, "img": "egg.jpeg"},
        {"name": "Power Oatmeal", "price": 12, "img": "best-dish.jpeg"}
    ],
    "Lunch 🥗": [
        {"name": "Sushi Rolls", "price": 18, "img": "healthy-food.jpeg"}, # Mapping Sushi
        {"name": "Shrimp Broccoli", "price": 16, "img": "chips-brokli.jpeg"}
    ],
    "Dinner 🍽️": [
        {"name": "Grilled Meat", "price": 25, "img": "fish.jpeg"}, # Using fish.jpeg as placeholder for Meat
        {"name": "Meat Salad", "price": 20, "img": "healthy-food.jpeg"},
        {"name": "Grilled Fish", "price": 22, "img": "fish.jpeg"}
    ],
    "Dessert 🍰": [
        {"name": "Fruit Medley", "price": 7, "img": "ftuit-salad.jpeg"},
        {"name": "Healthy Ice", "price": 6, "img": "healthy-ice.jpeg"}
    ]
}

# --- ALGORITHMS ---

def quick_sort_orders(arr):
    """Sorts orders by price: O(n log n)"""
    if len(arr) <= 1: return arr
    pivot = arr[len(arr) // 2]["price"]
    left = [x for x in arr if x["price"] < pivot]
    middle = [x for x in arr if x["price"] == pivot]
    right = [x for x in arr if x["price"] > pivot]
    return quick_sort_orders(left) + middle + quick_sort_orders(right)

memo = {}
def calculate_total_dp(arr, n):
    """Dynamic Programming to optimize total bill calculation."""
    if n < 0: return 0
    if n in memo: return memo[n]
    memo[n] = arr[n]['price'] + calculate_total_dp(arr, n - 1)
    return memo[n]

# --- CORE LOGIC ---

def save_to_order_file(item):
    """Saves added item to order.json"""
    orders = []
    if os.path.exists(ORDER_FILE):
        with open(ORDER_FILE, "r") as f:
            orders = json.load(f)
    orders.append(item)
    with open(ORDER_FILE, "w") as f:
        json.dump(orders, f, indent=4)

def start_app():
    root = tk.Tk()
    root.title("Menu")
    root.geometry("1100x850")
    root.configure(bg="#F9FBF9")

    # Header
    top = tk.Frame(root, bg="#2E7D32", height=70)
    top.pack(fill="x")
    tk.Label(top, text="FRESH RESTAURANT", fg="white", bg="#2E7D32", font=("Arial", 18, "bold")).pack(side="left", padx=20)
    tk.Button(top, text="🛒 MY CHART", font=("Arial", 10, "bold"), command=show_chart_window).pack(side="right", padx=20)

    # Scrollable Menu
    canvas = tk.Canvas(root, bg="#F9FBF9", highlightthickness=0)
    scroll = tk.Scrollbar(root, command=canvas.yview)
    frame = tk.Frame(canvas, bg="#F9FBF9")

    for cat, dishes in MENU_DATA.items():
        tk.Label(frame, text=cat, font=("Helvetica", 22, "bold"), fg="#1B5E20", bg="#F9FBF9").pack(pady=20, anchor="w", padx=40)
        grid = tk.Frame(frame, bg="#F9FBF9")
        grid.pack(fill="x", padx=40)

        for i, dish in enumerate(dishes):
            card = tk.Frame(grid, bg="white", padx=10, pady=10, highlightthickness=1, highlightbackground="#eee")
            card.grid(row=i//2, column=i%2, padx=10, pady=10)

            try:
                img = Image.open(dish["img"]).resize((200, 140), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                lbl = tk.Label(card, image=photo, bg="white"); lbl.image = photo; lbl.pack()
            except:
                tk.Label(card, text="📸 Image", bg="#f0f0f0", width=25, height=8).pack()

            tk.Label(card, text=dish["name"], font=("Arial", 12, "bold"), bg="white").pack()
            tk.Label(card, text=f"${dish['price']}", bg="white", fg="#2E7D32").pack()
            
            tk.Button(card, text="ADD TO CHART", bg="#E8F5E9", relief="flat",
                      command=lambda x=dish: [save_to_order_file(x), messagebox.showinfo("Chart", f"{x['name']} added!")]).pack(pady=5)

    canvas.create_window((0, 0), window=frame, anchor="nw")
    canvas.configure(yscrollcommand=scroll.set)
    canvas.pack(side="left", fill="both", expand=True)
    scroll.pack(side="right", fill="y")
    frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
    root.mainloop()

def show_chart_window():
    if not os.path.exists(ORDER_FILE) or os.stat(ORDER_FILE).st_size == 0:
        messagebox.showinfo("Empty", "No items in chart.")
        return

    win = tk.Toplevel()
    win.title("My Chart")
    win.geometry("450x600")

    with open(ORDER_FILE, "r") as f:
        data = json.load(f)

    # Apply Quick Sort
    sorted_data = quick_sort_orders(data)
    
    # Apply DP for Total
    memo.clear()
    total = calculate_total_dp(sorted_data, len(sorted_data)-1)

    tk.Label(win, text="Review Your Orders", font=("Arial", 14, "bold")).pack(pady=10)
    lb = tk.Listbox(win, width=50, height=20)
    lb.pack(pady=10)

    for item in sorted_data:
        lb.insert(tk.END, f"  ${item['price']} - {item['name']}")

    tk.Label(win, text=f"TOTAL (DP optimized): ${total}", font=("Arial", 12, "bold"), fg="#2E7D32").pack(pady=10)
    tk.Button(win, text="Clear and Close", command=lambda: [open(ORDER_FILE, 'w').close(), win.destroy()]).pack(pady=10)