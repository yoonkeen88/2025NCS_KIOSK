import tkinter as tk
from tkinter import messagebox
from kiosk import Menu, DiscountPolicy, OrderSystem

class KioskApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cafe Kiosk")
        self.root.geometry("480x700")
        self.root.configure(bg="#f7f2e8")  # 따뜻한 베이지톤 배경

        self.menu = Menu()
        self.discount_policy = DiscountPolicy()
        self.order_system = OrderSystem(self.menu, self.discount_policy)

        # 메뉴 등록
        self.menu.add_item("Americano", 3000)
        self.menu.add_item("Latte", 3500)
        self.menu.add_item("Vanilla Latte", 4000)
        self.menu.add_item("Cold Brew", 4500)
        self.menu.add_item("Mocha", 4200)
        self.menu.add_item("Cappuccino", 3700)

        self.create_widgets()

    def create_widgets(self):
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

        # 하단 버튼들
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
            text="🛒 Show Cart",
            font=("Helvetica", 12),
            bg="#d9cfc1",
            fg="black",
            width=30,
            command=self.show_cart
        ).pack(pady=5)

        tk.Button(
            self.root,
            text="🧼 Reset Order",
            font=("Helvetica", 12),
            bg="#e0b4a3",
            fg="black",
            width=30,
            command=self.reset_order
        ).pack(pady=5)

    def add_to_order(self, idx):
        self.order_system.process_order(idx)
        item = self.menu.get_items()[idx]
        messagebox.showinfo("Order Added", f"{item.name} has been added to your order.")

    def complete_order(self):
        summary = self.order_system.get_summary()
        q_num = self.order_system.get_queue_number()
        messagebox.showinfo(
            "Order Complete",
            f"{summary}\n\n📌 Your Queue Number is: {q_num}\n☕ Thank you for your order!"
        )
        self.root.quit()

    def show_cart(self):
        summary = self.order_system.get_summary()
        messagebox.showinfo("🛒 Your Cart", summary)

    def reset_order(self):
        self.order_system.amount = {item.name: 0 for item in self.menu.get_items()}
        self.order_system.total = 0
        messagebox.showinfo("Reset Complete", "Your order has been cleared.")

if __name__ == '__main__':
    root = tk.Tk()
    app = KioskApp(root)
    root.mainloop()

