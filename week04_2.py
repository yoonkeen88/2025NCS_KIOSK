class MenuItem:
    """Represents a single menu item."""
    def __init__(self, name: str, price: int):
        self.name = name
        self.price = price

    def __str__(self):
        return f"{self.name}: {self.price} won"


class Menu:
    """Manages a collection of menu items."""
    def __init__(self):
        self.items = []

    def add_item(self, name: str, price: int):
        """Adds a new menu item."""
        self.items.append(MenuItem(name, price))

    def get_items(self):
        """Returns the list of menu items."""
        return self.items

    def display_menu(self):
        """Returns a formatted string for displaying the menu."""
        return " | ".join([f"({i+1}) {item}" for i, item in enumerate(self.items)]) + \
               f"\n({len(self.items)+1}) Exit\nEnter the menu number: "


class OrderSystem:
    """Handles order processing and discounts."""
    DISCOUNT_THRESHOLD_10 = 10000
    DISCOUNT_THRESHOLD_5 = 5000
    DISCOUNT_RATE_10 = 0.9
    DISCOUNT_RATE_5 = 0.95

    def __init__(self, menu: Menu):
        """
        Initializes the order system with a given menu.
        :param menu: Menu object containing menu items.
        """
        self.menu = menu.get_items()
        self.amount = {item.name: 0 for item in self.menu}  # Track order quantities
        self.total = 0  # Total order price

    def apply_discount(self):
        """Applies a discount based on the total price."""
        if self.total >= self.DISCOUNT_THRESHOLD_10:
            return int(self.total * self.DISCOUNT_RATE_10)
        elif self.total >= self.DISCOUNT_THRESHOLD_5:
            return int(self.total * self.DISCOUNT_RATE_5)
        return self.total

    def process_order(self, item_index: int):
        """Processes an order for the selected menu item."""
        item = self.menu[item_index]
        self.amount[item.name] += 1
        self.total += item.price
        print(f"{item} ordered.")
        print(f"Total: {self.total} won")
        print("-----------------------------------------------")

    def show_summary(self):
        """Displays the final order summary, including discounts."""
        print("\nProduct Name\t|\tAmount\t|\tSubtotal")
        print("-----------------------------------------------")
        for item in self.menu:
            if self.amount[item.name] > 0:
                subtotal = self.amount[item.name] * item.price
                print(f"{item.name}\t|\t{self.amount[item.name]}\t|\t{subtotal} won")

        print(f"Total Price: {self.total} won")

        discounted_total = self.apply_discount()
        if discounted_total == self.total:
            print("No discount applied.")
        else:
            print(f"You received a discount!\nDiscounted Total:\t{discounted_total} won")
            print(f"You saved {self.total - discounted_total} won.")

    def run(self):
        """Runs the order system in a loop, allowing users to place orders."""
        while True:
            try:
                order = int(input(menu.display_menu()))
                if order == len(self.menu) + 1:
                    break
                elif order < 1 or order > len(self.menu):
                    print("Invalid selection. Please choose again.")
                else:
                    self.process_order(order - 1)
            except ValueError:
                print("Invalid input. Please enter a number.")

        self.show_summary()


# 프로그램 실행
if __name__ == "__main__":
    menu = Menu()
    menu.add_item("Ice Americano", 2600)
    menu.add_item("Ice Latte", 3300)
    menu.add_item("Ice Choco", 3600)
    
    order_system = OrderSystem(menu)
    order_system.run()


### 위 코드의 개설할 점 
### 수정 방안 제시해봐라