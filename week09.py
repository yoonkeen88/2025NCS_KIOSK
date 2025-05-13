# app.py
import tkinter as tk
from tkinter import messagebox
from typing import Any
from kiosk import Menu, DiscountPolicy, OrderSystem
from datetime import datetime
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

        self.create_widgets()

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

        self.cart_text = tk.Text(self.root, height=15, width=55, font=("Helvetica", 10))
        self.cart_text.pack(pady=10)
        self.update_cart()

        tk.Button(
            self.root,
            text="✅ Complete Order",
            font=("Helvetica", 14, "bold"),
            bg="#6b4226",
            fg="white",
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
        self.update_cart()  # ✅ 팝업 제거하고 장바구니만 갱신

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

if __name__ == '__main__':
    root = tk.Tk()
    app = KioskApp(root)
    root.mainloop()