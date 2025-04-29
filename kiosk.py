# kiosk.py
from typing import List
import logging
import sqlite3

logging.basicConfig(level=logging.INFO)

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