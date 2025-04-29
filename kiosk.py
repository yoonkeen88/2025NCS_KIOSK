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

    def display_menu(self) -> str:
        menu_str = "\n".join([f"({i + 1}) {item}" for i, item in enumerate(self.items)])
        return f"{menu_str}\n({len(self.items) + 1}) Exit\nEnter the menu number: "


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
        self.menu = menu.get_items()
        self.discount_policy = discount_policy
        self.amount = {item.name: 0 for item in self.menu}
        self.total = 0

        # SQLite 연결 및 테이블 생성
        self.conn = sqlite3.connect("queue_number.db")
        self.cur = self.conn.cursor()
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS queue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                number INTEGER NOT NULL
            )
        ''')
        self.conn.commit()

    def process_order(self, item_index: int) -> None:
        item = self.menu[item_index]
        self.amount[item.name] += 1
        self.total += item.price
        logging.info(f"{item} ordered. Total so far: {self.total} won")
        print(f"{item} ordered.")
        print(f"Total: {self.total} won\n{'-' * 50}")

    def get_queue_number(self) -> int:
        self.cur.execute("SELECT number FROM queue ORDER BY id DESC LIMIT 1")
        result = self.cur.fetchone()

        if result is None:
            number = 1
            self.cur.execute("INSERT INTO queue (number) VALUES (?)", (number,))
        else:
            number = result[0] + 1
            self.cur.execute("INSERT INTO queue (number) VALUES (?)", (number,))

        self.conn.commit()
        print(f"\n✨ Your Queue Number is: {number} ✨\nPlease wait while we prepare your order.")
        return number

    def show_summary(self) -> None:
        print("\n{:<20} | {:^6} | {:>10}".format("Product Name", "Amount", "Subtotal"))
        print("-" * 50)

        for item in self.menu:
            amount = self.amount[item.name]
            if amount > 0:
                subtotal = amount * item.price
                print("{:<20} | {:^6} | {:>10} won".format(item.name, amount, subtotal))

        print("-" * 50)
        print(f"{'Total Price':<29}: {self.total:>10} won")
        discounted_total = self.discount_policy.apply(self.total)

        if discounted_total == self.total:
            print("No discount applied.")
        else:
            print(f"You received a discount!")
            print(f"{'Discounted Total':<29}: {discounted_total:>10} won")
            print(f"{'You saved':<29}: {self.total - discounted_total:>10} won")

    def run(self) -> None:
        while True:
            try:
                order_input = input(self.menu_obj.display_menu()).strip()
                if order_input.lower() in ['exit', 'e', 'q', str(len(self.menu) + 1)]:
                    break
                order = int(order_input)
                if 1 <= order <= len(self.menu):
                    self.process_order(order - 1)
                else:
                    print("Invalid selection. Please choose again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        self.show_summary()
        self.get_queue_number()

    def __del__(self):
        self.conn.close()
