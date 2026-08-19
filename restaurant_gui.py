import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import json
import os

ORDER_FILE = "order.json"
MENU_FILE = "menu.json"

# Algos
def quick_sort_orders(arr):
    if len(arr) <= 1: return arr
    pivot = arr[len(arr) // 2]["price"]
    left = [x for x in arr if x["price"] < pivot]
    middle = [x for x in arr if x["price"] == pivot]
    right = [x for x in arr if x["price"] > pivot]
    return quick_sort_orders(left) + middle + quick_sort_orders(right)

memo = {}
def calculate_total_dp(arr, n):
    if n < 0: return 0
    if n in memo: return memo[n]
    memo[n] = arr[n]['price'] + calculate_total_dp(arr, n - 1)
    return memo[n]

#  USER-SPECIFIC CART LOGIC
current_user = "Guest"

def add_to_order_json(item):
    all_carts = {}
    if os.path.exists(ORDER_FILE) and os.path.getsize(ORDER_FILE) > 0:
        with open(ORDER_FILE, "r", encoding="utf-8") as f:
            try:
                content = json.load(f)
                all_carts = content if isinstance(content, dict) else {}
            except: all_carts = {}

    if current_user not in all_carts:
        all_carts[current_user] = []
    
    # We save the full item so calories/protein/ingredients are stored in the order history
    all_carts[current_user].append(item)
    with open(ORDER_FILE, "w", encoding="utf-8") as f:
        json.dump(all_carts, f, indent=4, ensure_ascii=False)

def remove_item(index, win):
    try:
        with open(ORDER_FILE, "r", encoding="utf-8") as f:
            all_carts = json.load(f)
        
        if current_user in all_carts:
            all_carts[current_user].pop(index)
            with open(ORDER_FILE, "w", encoding="utf-8") as f:
                json.dump(all_carts, f, indent=4, ensure_ascii=False)
            
            win.destroy() 
            show_chart_window() 
    except Exception as e:
        messagebox.showerror("Error", "Could not remove item.")

def logout(root):
    root.destroy()
    import healthy_restaurant 
    new_root = tk.Tk()
    healthy_restaurant.HealthyRestaurantApp(new_root)
    new_root.mainloop()

# SMOOTH SCROLL LOGIC 
def _on_mousewheel(event, canvas):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

#  MAIN MENU WINDOW
def start_app(username="Guest"):
    global current_user
    current_user = username
    
    try:
        with open(MENU_FILE, "r", encoding="utf-8") as f:
            menu_data = json.load(f)
    except:
        messagebox.showerror("Error", "Check menu.json formatting!")
        return

    root = tk.Tk()
    root.title(f"Healthy Restaurant - Welcome {current_user}")
    root.geometry("1300x950")
    root.configure(bg="#F4F7F4")

    # Header
    header = tk.Frame(root, bg="#1B5E20", height=80)
    header.pack(fill="x")
    tk.Label(header, text="🌿 FRESH EATS", fg="white", bg="#1B5E20", font=("Segoe UI", 22, "bold")).pack(side="left", padx=30)
    tk.Button(header, text="🚪 LOGOUT", font=("Segoe UI", 10, "bold"), bg="#d32f2f", fg="white", padx=15, relief="flat", command=lambda: logout(root)).pack(side="right", padx=10)
    tk.Button(header, text="🛒 MY CART", font=("Segoe UI", 12, "bold"), bg="#4CAF50", fg="white", padx=20, relief="flat", command=show_chart_window).pack(side="right", padx=10)

    container = tk.Frame(root, bg="#F4F7F4")
    container.pack(fill="both", expand=True)

    canvas = tk.Canvas(container, bg="#F4F7F4", highlightthickness=0)
    v_scroll = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    frame = tk.Frame(canvas, bg="#F4F7F4")

    canvas.bind_all("<MouseWheel>", lambda e: _on_mousewheel(e, canvas))

    for cat, dishes in menu_data.items():
        tk.Label(frame, text=cat, font=("Segoe UI", 26, "bold"), fg="#2E7D32", bg="#F4F7F4").pack(pady=(40, 10), anchor="w", padx=80)
        grid = tk.Frame(frame, bg="#F4F7F4")
        grid.pack(fill="x", padx=80)

        for i, dish in enumerate(dishes):
            card = tk.Frame(grid, bg="white", padx=20, pady=20, highlightthickness=1, highlightbackground="#E0E0E0")
            card.grid(row=i//2, column=i%2, padx=20, pady=20, sticky="nsew")

            # Image Display
            try:
                img = Image.open(dish["img"]).resize((320, 200), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                lbl = tk.Label(card, image=photo, bg="white"); lbl.image = photo; lbl.pack(pady=5)
            except:
                tk.Label(card, text="📸 Image Missing", bg="#f0f0f0", width=40, height=10).pack()

            # Text Labels
            tk.Label(card, text=dish["name"], font=("Segoe UI", 18, "bold"), bg="white").pack()
            tk.Label(card, text=f"${dish['price']}", font=("Segoe UI", 14), bg="white", fg="#2E7D32").pack()
            
            # Nutritional Info Display
            stats = f"🔥 {dish.get('calories', 0)} kcal  |  💪 {dish.get('protein', 0)}g Protein"
            tk.Label(card, text=stats, font=("Segoe UI", 10, "italic"), bg="#F1F8E9", fg="#388E3C", pady=5).pack(fill="x", pady=5)

            # Ingredients Display
            ings = ", ".join(dish.get('ingredients', []))
            tk.Label(card, text=ings, font=("Segoe UI", 9), bg="white", fg="#777", wraplength=300).pack(pady=5)

            tk.Button(card, text="ADD TO CART", bg="#2E7D32", fg="white", font=("Segoe UI", 11, "bold"), 
                      padx=25, pady=8, relief="flat", 
                      command=lambda x=dish: [add_to_order_json(x), messagebox.showinfo("Success", f"{x['name']} added!")]).pack(pady=15)

    canvas.create_window((0, 0), window=frame, anchor="nw")
    canvas.configure(yscrollcommand=v_scroll.set)
    canvas.pack(side="left", fill="both", expand=True)
    v_scroll.pack(side="right", fill="y")
    frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
    root.mainloop()

# CHART WINDOW 
def show_chart_window():
    if not os.path.exists(ORDER_FILE) or os.stat(ORDER_FILE).st_size == 0:
        messagebox.showinfo("Empty", "No items in your chart!")
        return

    with open(ORDER_FILE, "r", encoding="utf-8") as f:
        all_carts = json.load(f)
    
    data = all_carts.get(current_user, [])
    if not data:
        messagebox.showinfo("Empty", "Your chart is empty!")
        return

    win = tk.Toplevel()
    win.title(f"{current_user}'s Chart")
    win.geometry("700x750")
    win.configure(bg="white")

    memo.clear()
    total = calculate_total_dp(data, len(data)-1)

    canvas = tk.Canvas(win, bg="white", highlightthickness=0)
    v_scroll = tk.Scrollbar(win, command=canvas.yview)
    content = tk.Frame(canvas, bg="white")
    canvas.bind_all("<MouseWheel>", lambda e: _on_mousewheel(e, canvas))

    for i, item in enumerate(data):
        row = tk.Frame(content, bg="#FAFAFA", pady=15, highlightthickness=1, highlightbackground="#EEE")
        row.pack(fill="x", padx=20, pady=8)

        # image in chart
        try:
            c_img = Image.open(item["img"]).resize((100, 60), Image.Resampling.LANCZOS)
            c_photo = ImageTk.PhotoImage(c_img)
            img_lbl = tk.Label(row, image=c_photo, bg="#FAFAFA")
            img_lbl.image = c_photo 
            img_lbl.pack(side="left", padx=10)
        except:
            tk.Label(row, text="🍱", font=("Segoe UI", 16), bg="#FAFAFA").pack(side="left", padx=20)

        tk.Label(row, text=f"{item['name']} - ${item['price']}", font=("Segoe UI", 12, "bold"), bg="#FAFAFA").pack(side="left", padx=20)
        
        tk.Button(row, text="❌ Remove", bg="#FFEBEE", fg="#C62828", font=("Segoe UI", 9, "bold"),
                  padx=10, relief="flat", command=lambda idx=i: remove_item(idx, win)).pack(side="right", padx=20)

    canvas.create_window((0, 0), window=content, anchor="nw", width=680)
    canvas.configure(yscrollcommand=v_scroll.set)
    canvas.pack(side="top", fill="both", expand=True)
    v_scroll.pack(side="right", fill="y")
    content.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    footer = tk.Frame(win, bg="#1B5E20", pady=25)
    footer.pack(fill="x", side="bottom")
    tk.Label(footer, text=f"TOTAL: ${total}", fg="white", bg="#1B5E20", font=("Segoe UI", 18, "bold")).pack()