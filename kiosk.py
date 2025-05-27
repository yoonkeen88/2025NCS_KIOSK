# kiosk.py
from typing import List
import logging
import sqlite3
import requests

from datetime import datetime
logging.basicConfig(level=logging.INFO)
import threading
import time
import tkinter as tk
from tkinter import messagebox
from typing import Any
from typing import Callable

class MenuItem:
    def __init__(self, name: str, price: int) -> None:
        self.name = name
        self.price = price

    def __str__(self) -> str:
        return f"{self.name}: {self.price} won"

class Menu:
    def __init__(self) -> None:
        self.items: List[MenuItem] = []

    def add_item(self, name: str, price: int) -> None:
        self.items.append(MenuItem(name, price))

    def get_items(self) -> List[MenuItem]:
        return self.items

class DiscountPolicy:
    DISCOUNT_THRESHOLD_10 = 10000
    DISCOUNT_THRESHOLD_5 = 5000
    DISCOUNT_RATE_10 = 0.9
    DISCOUNT_RATE_5 = 0.95

    def apply(self, total: int) -> int:
        if total >= self.DISCOUNT_THRESHOLD_10:
            logging.info("10% discount applied")
            return round(total * self.DISCOUNT_RATE_10)
        elif total >= self.DISCOUNT_THRESHOLD_5:
            logging.info("5% discount applied")
            return round(total * self.DISCOUNT_RATE_5)
        return total

class OrderSystem:
    
    def __init__(self, menu: Menu, discount_policy: DiscountPolicy) -> None:
        self.menu_obj = menu
        self.discount_policy = discount_policy
        self.conn = sqlite3.connect("queue_number.db")
        self.cur = self.conn.cursor()

        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS queue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                number INTEGER NOT NULL
            )
        ''')
        self.conn.commit()

        self.reset_order()


    def reset_order(self) -> None:
        self.menu = self.menu_obj.get_items()
        self.amount = {item.name: 0 for item in self.menu}
        self.total = 0


    def process_order(self, item_index: int) -> None:
        self.menu = self.menu_obj.get_items()
        item = self.menu[item_index]
        if item.name not in self.amount:
            self.amount[item.name] = 0
        self.amount[item.name] += 1
        self.total += item.price
        logging.info(f"{item} ordered. Total so far: {self.total} won")


    def get_summary(self) -> str:
        lines = []
        lines.append("{:<20} | {:^6} | {:>10}".format("Product Name", "Amount", "Subtotal"))
        lines.append("-" * 50)

        for item in self.menu:
            amount = self.amount.get(item.name, 0)
            if amount > 0:
                subtotal = amount * item.price
                lines.append("{:<20} | {:^6} | {:>10} won".format(item.name, amount, subtotal))

        lines.append("-" * 50)
        lines.append(f"{'Total Price':<29}: {self.total:>10} won")
        discounted_total = self.discount_policy.apply(self.total)

        if discounted_total != self.total:
            lines.append("You received a discount!")
            lines.append(f"{'Discounted Total':<29}: {discounted_total:>10} won")
            lines.append(f"{'You saved':<29}: {self.total - discounted_total:>10} won")
            lines.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        else:
            lines.append("No discount applied.")

        return "\n".join(lines)


    def save_receipt(self, filename: str, queue_number: int) -> None:  # [수정] 파일로 저장
        summary = self.get_summary()
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"☕ Cozy Cafe Receipt ☕\n")
            f.write(f"Queue Number: {queue_number}\n")
            f.write("="*50 + "\n")
            f.write(summary + "\n")
            f.write("="*50 + "\n")
            f.write("Thank you for visiting Cozy Cafe!\n")


    def get_queue_number(self) -> int:
        self.cur.execute("SELECT number FROM queue ORDER BY id DESC LIMIT 1")
        result = self.cur.fetchone()

        if result is None:
            number = 1
        else:
            number = result[0] + 1

        self.cur.execute("INSERT INTO queue (number) VALUES (?)", (number,))
        self.conn.commit()
        return number


    def __del__(self):
        self.conn.close()

import threading
import time
import requests
import logging
from typing import Callable
import tkinter as tk
from tkinter import messagebox

logging.basicConfig(level=logging.INFO)

class WeatherManager:
    def __init__(self, update_callback: Callable[[str], None] = None) -> None:
        self.weather_info = "Loading weather..."
        self.update_callback = update_callback
        self.stop_flag = False
        self.update_interval = 300
        self.last_fetched_info = ""
        self.thread = threading.Thread(target=self._auto_update_loop, daemon=True)

    def start_auto_update(self) -> None:
        if not self.thread.is_alive():
            self.thread.start()

    def stop_auto_update(self) -> None:
        self.stop_flag = True

    def _auto_update_loop(self) -> None:
        while not self.stop_flag:
            self.update_weather()
            time.sleep(self.update_interval)

    def update_weather(self) -> str:
        try:
            url = "https://wttr.in/Incheon?format=3"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                new_info = response.text.strip()
                if new_info != self.last_fetched_info:
                    self.weather_info = new_info
                    self.last_fetched_info = new_info
                    logging.info(f"Weather info updated: {self.weather_info}")
                    self._safe_ui_update(self.weather_info)
            else:
                logging.warning("Failed to get weather info: Status code not 200")
                self._safe_ui_update("Weather info not available")
        except requests.RequestException as e:
            logging.error(f"Exception while fetching weather: {e}")
            self._safe_ui_update("Failed to load weather")
        return self.weather_info

    def _safe_ui_update(self, text: str) -> None:
        try:
            if self.update_callback:
                self.update_callback(text)
        except Exception as e:
            logging.error(f"Error updating UI: {e}")

class KioskApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Cafe Kiosk")
        self.root.geometry("500x1000")
        self.root.configure(bg="#f7f2e8")

        self.menu = Menu()
        self.discount_policy = DiscountPolicy()
        self.order_system = OrderSystem(self.menu, self.discount_policy)

        self.menu.add_item("Americano", 3000)
        self.menu.add_item("Latte", 3500)
        self.menu.add_item("Vanilla Latte", 4000)
        self.menu.add_item("Cold Brew", 4500)
        self.menu.add_item("Mocha", 4200)
        self.menu.add_item("Cappuccino", 3700)

        self.weather_manager = WeatherManager(update_callback=self.set_weather_text)
        self.weather_manager.start_auto_update()

        self.create_widgets()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def set_weather_text(self, new_weather: str) -> None:
        if hasattr(self, 'weather_label'):
            self.weather_label.config(text=new_weather)

    def update_weather_once(self) -> None:
        self.weather_manager.update_weather()

    def on_close(self) -> None:
        self.weather_manager.stop_auto_update()
        self.root.destroy()

    def create_widgets(self) -> None:
        tk.Label(
            self.root,
            text="☕ Welcome to Cozy Cafe ☕",
            font=("Helvetica", 20, "bold"),
            bg="#f7f2e8",
            fg="#4b3832"
        ).pack(pady=20)

        self.buttons_frame = tk.Frame(self.root, bg="#f7f2e8")
        self.buttons_frame.pack(pady=10)

        items = self.menu.get_items()
        for idx, item in enumerate(items):
            row = idx // 2
            col = idx % 2
            btn = tk.Button(
                self.buttons_frame,
                text=f"{item.name}\n₩{item.price}",
                font=("Helvetica", 12, "bold"),
                width=18,
                height=4,
                bg="#fffaf0",
                fg="#3e3e3e",
                relief="raised",
                bd=2,
                command=lambda i=idx: self.add_to_order(i)
            )
            btn.grid(row=row, column=col, padx=10, pady=10)

        self.weather_label = tk.Label(
            self.buttons_frame,
            text="🌡️ Loading Weather Information...",
            font=("Helvetica", 14),
            bg="#f7f2e8",
            fg="#4b3832",
            width=40,
            height=2
        )
        self.weather_label.grid(row=(len(items)+1)//2, column=0, columnspan=2, pady=(20, 5))

        self.weather_button = tk.Button(
            self.buttons_frame,
            text="🔄 Update Weather",
            font=("Helvetica", 12),
            bg="#6b4226",
            fg="#87CEEB",
            width=20,
            command=self.update_weather_once
        )
        self.weather_button.grid(row=((len(items)+1)//2)+1, column=0, columnspan=2, pady=(0, 20))

        self.cart_text = tk.Text(self.root, height=15, width=55, font=("Helvetica", 10))
        self.cart_text.pack(pady=10)
        self.update_cart()

        tk.Button(
            self.root,
            text="✅ Complete Order",
            font=("Helvetica", 14, "bold"),
            bg="#6b4226",
            fg="#87CEEB",
            width=30,
            height=2,
            command=self.complete_order
        ).pack(pady=10)

        tk.Button(
            self.root,
            text="🧼 Reset Order",
            font=("Helvetica", 12),
            bg="#e0b4a3",
            fg="black",
            width=30,
            command=self.reset_order
        ).pack(pady=5)

    def add_to_order(self, idx: int) -> None:
        self.order_system.process_order(idx)
        self.update_cart()
        self.update_weather_once()

    def complete_order(self) -> None:
        queue_num = self.order_system.get_queue_number()
        receipt_filename = f"receipt_{queue_num}.txt"
        self.order_system.save_receipt(receipt_filename, queue_num)
        receipt_content = self.order_system.get_summary()
        self.show_receipt_window(receipt_content, queue_num)

    def show_receipt_window(self, content: str, queue_num: int) -> None:
        receipt_win = tk.Toplevel(self.root)
        receipt_win.title(f"Receipt - Queue #{queue_num}")
        receipt_win.geometry("600x600")
        receipt_win.configure(bg="#fffaf0")

        tk.Label(
            receipt_win,
            text=f"🧾 Cozy Cafe Receipt 🧾\nQueue Number: {queue_num}",
            font=("Helvetica", 16, "bold"),
            bg="#fffaf0",
            fg="#4b3832"
        ).pack(pady=10)

        text_widget = tk.Text(receipt_win, wrap=tk.WORD, font=("Courier", 11), bg="white", fg="black")
        text_widget.insert(tk.END, content)
        text_widget.config(state=tk.DISABLED)
        text_widget.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        tk.Button(
            receipt_win,
            text="✅ Close and Exit",
            font=("Helvetica", 12),
            bg="#6b4226",
            fg="white",
            width=25,
            command=self.root.quit
        ).pack(pady=10)

    def update_cart(self) -> None:
        summary = self.order_system.get_summary()
        self.cart_text.delete(1.0, tk.END)
        self.cart_text.insert(tk.END, summary)

    def reset_order(self) -> None:
        self.order_system.reset_order()
        self.update_cart()
        messagebox.showinfo("Reset Complete", "Your order has been cleared.")