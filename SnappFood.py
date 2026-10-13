import json
import os
import tkinter as tk
from tkinter import messagebox

# oop

class MenuItem:
    def __init__(self, name, price, item_type, is_available=True):
        self.name = name
        self.price = price
        self.item_type = item_type
        self.is_available = is_available

    def to_dict(self):
        return {
            "name": self.name, 
            "price": self.price, 
            "item_type": self.item_type, 
            "is_available": self.is_available
        }

class Order:
    def __init__(self, order_id, customer_id, restaurant_id, items=None):
        self.order_id = order_id
        self.customer_id = customer_id
        self.restaurant_id = restaurant_id
        self.items = items if items else []

    def add_item(self, item):
        self.items.append(item)

    def calculate_total(self):
        return sum(item.price for item in self.items)

    def to_dict(self):
        return {
            "order_id": self.order_id, 
            "customer_id": self.customer_id,
            "restaurant_id": self.restaurant_id,
            "items": [item.to_dict() for item in self.items],
            "total_price": self.calculate_total()
        }

class Restaurant:
    def __init__(self, name, manager_id, restaurant_id):
        self.name = name
        self.manager_id = manager_id
        self.restaurant_id = restaurant_id
        self.menu = []

    def add_item_to_menu(self, item):
        self.menu.append(item)

    def to_dict(self):
        return {
            "name": self.name, 
            "manager_id": self.manager_id,
            "restaurant_id": self.restaurant_id,
            "menu": [item.to_dict() for item in self.menu]
        }
    
class User:
    def __init__(self, user_id, name, password, role):
        self.user_id = user_id
        self.name = name
        self.password = password
        self.role = role

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "password": self.password,
            "role": self.role
        }

class Manager(User):
    def __init__(self, user_id, name, password, restaurant_name):
        super().__init__(user_id, name, password, "manager")
        self.restaurant_name = restaurant_name

    def to_dict(self):
        data = super().to_dict()
        data["restaurant_name"] = self.restaurant_name
        return data

class Customer(User):
    def __init__(self, user_id, name, password):
        super().__init__(user_id, name, password, "customer")

    def to_dict(self):
        return super().to_dict()


# backend logic


class Platform:
    def __init__(self):
        self.users = {}        
        self.restaurants = {}
        self.orders = []
        self.data_file = "database.json"
        self.load_data()

    def register_user(self, user_id, name, password, role, restaurant_name=None):
        if role == "manager":
            new_user = Manager(user_id, name, password, restaurant_name)
        else:
            new_user = Customer(user_id, name, password)
        
        self.users[user_id] = new_user.to_dict()
        
        if role == "manager" and restaurant_name:
            res_id = "res_" + str(len(self.restaurants) + 1)
            self.restaurants[res_id] = Restaurant(restaurant_name, user_id, res_id)
            
        self.save_data()

    def login(self, user_id, password):
        if user_id in self.users and self.users[user_id]["password"] == password:
            return self.users[user_id]
        return None

    def save_data(self):
        data = {
            "users": self.users,
            "restaurants": {rid: res.to_dict() for rid, res in self.restaurants.items()},
            "orders": self.orders
        }
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.users = data.get("users", {})
                
                # بازسازی اشیاء رستوران و منو
                res_data = data.get("restaurants", {})
                for rid, r_info in res_data.items():
                    res = Restaurant(r_info["name"], r_info["manager_id"], r_info["restaurant_id"])
                    for m_info in r_info["menu"]:
                        res.add_item_to_menu(MenuItem(m_info["name"], m_info["price"], m_info["item_type"], m_info["is_available"]))
                    self.restaurants[rid] = res
                
                self.orders = data.get("orders", [])

#   GUI

class RestaurantApp:
    def __init__(self, root):
        self.platform = Platform()
        self.root = root
        self.root.title("سیستم مدیریت رستوران")
        self.root.geometry("450x500")
        self.current_user = None
        self.current_restaurant = None
        self.show_login_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_login_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="ورود به سیستم", font=("Arial", 18, "bold")).pack(pady=20)
        
        tk.Label(self.root, text="شناسه کاربر (ID):").pack()
        user_ent = tk.Entry(self.root)
        user_ent.pack(pady=5)

        tk.Label(self.root, text="رمز عبور:").pack()
        pass_ent = tk.Entry(self.root, show="*")
        pass_ent.pack(pady=5)

        def login_action():
            user = self.platform.login(user_ent.get(), pass_ent.get())
            if user:
                self.current_user = user
                self.show_main_menu()
            else:
                messagebox.showerror("خطا", "شناسه یا رمز عبور اشتباه است!")

        tk.Button(self.root, text="ورود", width=15, bg="lightblue", command=login_action).pack(pady=15)
        tk.Button(self.root, text="ثبت نام جدید", width=15, command=self.show_register_screen).pack()

    def show_register_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="صفحه ثبت نام", font=("Arial", 16, "bold")).pack(pady=15)

        tk.Label(self.root, text="نام کامل:").pack()
        name_ent = tk.Entry(self.root); name_ent.pack()

        tk.Label(self.root, text="ایجاد شناسه (ID) یکتا:").pack()
        id_ent = tk.Entry(self.root); id_ent.pack()

        tk.Label(self.root, text="رمز عبور:").pack()
        pass_ent = tk.Entry(self.root, show="*"); pass_ent.pack()

        tk.Label(self.root, text="نقش (manager یا customer):").pack()
        role_ent = tk.Entry(self.root); role_ent.pack()

        tk.Label(self.root, text="نام رستوران (فقط برای مدیر):").pack()
        res_name_ent = tk.Entry(self.root); res_name_ent.pack()

        def register_action():
            role = role_ent.get().lower().strip()
            r_name = res_name_ent.get().strip()
            
            if role not in ["manager", "customer"]:
                messagebox.showerror("خطا", "نقش باید manager یا customer باشد")
                return
            
            if role == "manager" and not r_name:
                messagebox.showerror("خطا", "برای مدیر باید نام رستوران وارد شود")
                return

            self.platform.register_user(id_ent.get(), name_ent.get(), pass_ent.get(), role, r_name)
            messagebox.showinfo("موفقیت", "ثبت نام با موفقیت انجام شد!")
            self.show_login_screen()

        tk.Button(self.root, text="تایید و ثبت نام", command=register_action, bg="lightgreen").pack(pady=20)
        tk.Button(self.root, text="بازگشت به ورود", command=self.show_login_screen).pack()

    def show_main_menu(self):
        self.clear_screen()
        role = self.current_user["role"]
        tk.Label(self.root, text=f"خوش آمدید، {self.current_user['name']}", font=("Arial", 14)).pack(pady=15)
        tk.Label(self.root, text=f"نقش شما: {role}", fg="gray").pack()

        if role == "manager":
            self.show_manager_menu()
        else:
            self.show_customer_menu()

    # manager menu
    def show_manager_menu(self):
        res = next((r for r in self.platform.restaurants.values() if r.manager_id == self.current_user["user_id"]), None)
        self.current_restaurant = res

        if not res:
            messagebox.showerror("خطا", "رستورانی برای شما یافت نشد!")
            self.show_login_screen()
            return

        tk.Label(self.root, text=f"مدیریت رستوران: {res.name}", font=("Arial", 12, "bold"), fg="darkblue").pack(pady=10)

        tk.Button(self.root, text="➕ افزودن آیتم به منو", width=25, command=self.manager_add_item).pack(pady=5)
        tk.Button(self.root, text="📋 مشاهده سفارش‌های دریافتی", width=25, command=self.manager_view_orders).pack(pady=5)
        tk.Button(self.root, text="🚪 خروج", width=25, command=self.show_login_screen).pack(pady=20)

    def manager_add_item(self):
        win = tk.Toplevel(self.root)
        win.title("افزودن آیتم جدید")
        win.geometry("300x300")

        tk.Label(win, text="نام غذا/نوشیدنی:").pack()
        n = tk.Entry(win); n.pack()
        tk.Label(win, text="قیمت (تومان):").pack()
        p = tk.Entry(win); p.pack()
        tk.Label(win, text="نوع (غذا / نوشیدنی):").pack()
        t = tk.Entry(win); t.pack()

        def save():
            try:
                item = MenuItem(n.get(), int(p.get()), t.get())
                self.current_restaurant.add_item_to_menu(item)
                self.platform.save_data()
                messagebox.showinfo("موفقیت", "آیتم با موفقیت به منو اضافه شد!")
                win.destroy()
            except ValueError:
                messagebox.showerror("خطا", "قیمت باید عدد باشد!")

        tk.Button(win, text="ذخیره در منو", command=save, bg="lightgreen").pack(pady=20)

    def manager_view_orders(self):
        win = tk.Toplevel(self.root)
        win.title("سفارش‌های رستوران")
        win.geometry("400x300")
        
        txt = tk.Text(win, height=12, width=45)
        txt.pack(pady=10)

        found = False
        for o in self.platform.orders:
            if o["restaurant_id"] == self.current_restaurant.restaurant_id:
                txt.insert(tk.END, f"🆔 سفارش: {o['order_id']} | 💰 مبلغ: {o['total_price']} تومان\n")
                found = True
        
        if not found:
            txt.insert(tk.END, "هنوز هیچ سفارشی ثبت نشده است.")
            
        tk.Button(win, text="بستن", command=win.destroy).pack()

    # customer menu
    def show_customer_menu(self):
        self.clear_screen()
        tk.Label(self.root, text="انتخاب رستوران مورد نظر", font=("Arial", 14, "bold")).pack(pady=15)

        listbox = tk.Listbox(self.root, width=40, height=10)
        listbox.pack(pady=10)

        for rid, r in self.platform.restaurants.items():
            listbox.insert(tk.END, r.name)

        def enter_restaurant():
            selection = listbox.curselection()
            if selection:
                name = listbox.get(selection[0])
                res = next((r for r in self.platform.restaurants.values() if r.name == name), None)
                if res:
                    self.current_restaurant = res
                    self.show_restaurant_menu()
            else:
                messagebox.showwarning("هشدار", "لطفاً یک رستوران را انتخاب کنید!")

        tk.Button(self.root, text="ورود به رستوران", command=enter_restaurant, bg="lightyellow").pack(pady=5)
        tk.Button(self.root, text="خروج", command=self.show_login_screen).pack(pady=20)

    def show_restaurant_menu(self):
        self.clear_screen()
        tk.Label(self.root, text=f"منوی {self.current_restaurant.name}", font=("Arial", 14, "bold"), fg="green").pack(pady=10)

        listbox = tk.Listbox(self.root, width=50, height=12)
        listbox.pack(pady=5)

        cart = []

        for item in self.current_restaurant.menu:
            status = "✅" if item.is_available else "❌"
            listbox.insert(tk.END, f"{status} {item.name} - {item.price} تومان ({item.item_type})")

        def add_to_cart():
            sel = listbox.curselection()
            if sel:
                idx = sel[0]
                item = self.current_restaurant.menu[idx]
                if item.is_available:
                    cart.append(item)
                    messagebox.showinfo("سبد خرید", f"{item.name} به سبد اضافه شد.")
                else:
                    messagebox.showwarning("خطا", "این آیتم در حال حاضر موجود نیست!")
            else:
                messagebox.showwarning("هشدار", "لطفاً یک آیتم را انتخاب کنید!")

        def finalize_order():
            if not cart:
                messagebox.showwarning("خطا", "سبد خرید شما خالی است!")
                return
            
            # new order
            order_id = len(self.platform.orders) + 1
            new_order = Order(order_id, self.current_user["user_id"], self.current_restaurant.restaurant_id, cart)
            
            # adding order
            self.platform.orders.append(new_order.to_dict())
            self.platform.save_data()
            
            messagebox.showinfo("تایید", f"🎉 سفارش با موفقیت ثبت شد!\nمبلغ قابل پرداخت: {new_order.calculate_total()} تومان")
            self.show_customer_menu()

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="➕ افزودن به سبد", command=add_to_cart).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="💳 ثبت سفارش و پرداخت", command=finalize_order, bg="lightgreen").pack(side=tk.LEFT, padx=5)
        tk.Button(self.root, text="🔙 بازگشت به لیست رستوران‌ها", command=self.show_customer_menu).pack(pady=10)

# operating app

if __name__ == "__main__":
    root = tk.Tk()
    app = RestaurantApp(root)
    root.mainloop()