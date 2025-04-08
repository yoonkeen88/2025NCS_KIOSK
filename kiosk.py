from typing import List
import logging

logging.basicConfig(level=logging.INFO)


class MenuItem:
    """Represents a single menu item."""

    def __init__(self, name: str, price: int) -> None:
        self.name = name
        self.price = price

    def __str__(self) -> str:
        return f"{self.name}: {self.price} won"


class Menu:
    """Manages a collection of menu items."""

    def __init__(self) -> None:
        self.items: List[MenuItem] = []

    def add_item(self, name: str, price: int) -> None:
        """Adds a new menu item."""
        self.items.append(MenuItem(name, price))

    def get_items(self) -> List[MenuItem]:
        """Returns the list of menu items."""
        return self.items

    def display_menu(self) -> str:
        """Returns a formatted string for displaying the menu."""
        menu_str = "\n".join([f"({i + 1}) {item}" for i, item in enumerate(self.items)])
        return f"{menu_str}\n({len(self.items) + 1}) Exit\nEnter the menu number: "


class DiscountPolicy:
    """Handles discount logic as a separate component."""

    DISCOUNT_THRESHOLD_10 = 10000
    DISCOUNT_THRESHOLD_5 = 5000
    DISCOUNT_RATE_10 = 0.9
    DISCOUNT_RATE_5 = 0.95

    def apply(self, total: int) -> int:
        """
        Applies discount based on the total price.

        :param total: original total price
        :return: discounted price
        """
        if total >= self.DISCOUNT_THRESHOLD_10:
            logging.info("10% discount applied")
            return round(total * self.DISCOUNT_RATE_10)
        elif total >= self.DISCOUNT_THRESHOLD_5:
            logging.info("5% discount applied")
            return round(total * self.DISCOUNT_RATE_5)
        return total


class OrderSystem:
    """Handles order processing and uses a discount policy."""

    def __init__(self, menu: Menu, discount_policy: DiscountPolicy) -> None:
        self.menu_obj = menu  # Aggregation
        self.menu = menu.get_items()
        self.discount_policy = discount_policy  # Uses-a 관계
        self.amount = {item.name: 0 for item in self.menu}
        self.total = 0

    def process_order(self, item_index: int) -> None:
        """Processes an order for the selected menu item."""
        item = self.menu[item_index]
        self.amount[item.name] += 1
        self.total += item.price
        logging.info(f"{item} ordered. Total so far: {self.total} won")
        print(f"{item} ordered.")
        print(f"Total: {self.total} won\n{'-' * 50}")

    def show_summary(self) -> None:
        """Displays the final order summary, including discounts."""
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
        """Main loop for ordering system."""
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

